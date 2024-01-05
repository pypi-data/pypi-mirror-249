import re
import sys
import typing as t

import ibis
import mongomock
import pandas
import pymongo

import aladindb as s
from aladindb import logging
from aladindb.backends.base.backends import data_backends, metadata_stores
from aladindb.backends.local.artifacts import FileSystemArtifactStore
from aladindb.backends.local.compute import LocalComputeBackend
from aladindb.backends.mongodb.artifacts import MongoArtifactStore
from aladindb.backends.ray.compute import RayComputeBackend
from aladindb.base.datalayer import Datalayer


def build_metadata(metadata_store=None):
    if metadata_store is None:
        metadata_store = s.CFG.metadata_store
    return build(metadata_store, metadata_stores, type='metadata')


def build_databackend(databackend: t.Optional[str] = None):
    if databackend is None:
        databackend = s.CFG.data_backend
    return build(databackend, data_backends)


def build_artifact_store(artifact_store: str):
    if artifact_store.startswith('mongodb://'):
        import pymongo

        conn: pymongo.MongoClient = pymongo.MongoClient(
            '/'.join(artifact_store.split('/')[:-1])
        )
        name = artifact_store.split('/')[-1]
        return MongoArtifactStore(conn, name)
    elif artifact_store.startswith('filesystem://'):
        directory = artifact_store.split('://')[1]
        return FileSystemArtifactStore(directory)
    else:
        raise ValueError(f'Unknown artifact store: {artifact_store}')


# Helper function to build a data backend based on the URI.
def build(uri, mapping, type: str = 'data_backend'):
    logging.debug(f"Parsing data connection URI:{uri}")

    if re.match('^mongodb:\/\/', uri) is not None:
        name = uri.split('/')[-1]
        conn: pymongo.MongoClient = pymongo.MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
        )
        return mapping['mongodb'](conn, name)

    elif re.match('^mongodb\+srv:\/\/', uri):
        name = uri.split('/')[-1]
        conn = pymongo.MongoClient(
            '/'.join(uri.split('/')[:-1]),
            serverSelectionTimeoutMS=5000,
        )
        return mapping['mongodb'](conn, name)

    elif uri.startswith('mongomock://'):
        name = uri.split('/')[-1]
        conn = mongomock.MongoClient()
        return mapping['mongodb'](conn, name)

    elif uri.endswith('.csv'):
        if type == 'metadata':
            raise ValueError('Cannot build metadata from a CSV file.')

        import glob

        csv_files = glob.glob(uri)
        tables = {}
        for csv_file in csv_files:
            pattern = re.match('^.*/(.*)\.csv$', csv_file)
            assert pattern is not None
            tables[pattern.groups()[0]] = pandas.read_csv(csv_file)
        ibis_conn = ibis.pandas.connect(tables)
        return mapping['ibis'](ibis_conn, uri.split('/')[0])
    else:
        name = uri.split('//')[0]
        if type == 'data_backend':
            ibis_conn = ibis.connect(uri)
            return mapping['ibis'](ibis_conn, name)
        else:
            assert type == 'metadata'
            from sqlalchemy import create_engine

            sql_conn = create_engine(uri)
            return mapping['sqlalchemy'](sql_conn, name)


def build_compute(compute):
    if compute == 'local' or compute is None:
        return LocalComputeBackend()

    if compute == 'dask+thread':
        from aladindb.backends.dask.compute import DaskComputeBackend

        return DaskComputeBackend('', local=True)

    if compute.split('://')[0] == 'dask+tcp':
        from aladindb.backends.dask.compute import DaskComputeBackend

        uri = compute.split('+')[-1]
        return DaskComputeBackend(uri)

    if compute.split('://')[0] == 'ray':
        return RayComputeBackend(compute)

    return LocalComputeBackend()


def build_datalayer(cfg=None, databackend=None, **kwargs) -> Datalayer:
    """
    Build a Datalayer object as per ``db = aladin(db)`` from configuration.

    :param cfg: Configuration to use. If None, use ``aladindb.CFG``.
    :param databackend: Databacked to use.
                        If None, use ``aladindb.CFG.data_backend``.
    """

    # Configuration
    # ------------------------------
    # Use the provided configuration or fall back to the default configuration.
    cfg = cfg or s.CFG

    # Update configuration with keyword arguments.
    for k, v in kwargs.items():
        cfg.force_set(k, v)

    # Connect to data backend.
    # ------------------------------
    try:
        if not databackend:
            databackend = build(cfg.data_backend, data_backends)
        logging.info("Data Client is ready.", databackend.conn)
    except Exception as e:
        # Exit quickly if a connection fails.
        logging.error("Error initializing to DataBackend Client:", str(e))
        sys.exit(1)

    # Connect to metadata store.
    # ------------------------------
    # 1. try to connect to the metadata store specified in the configuration.
    # 2. if that fails, try to connect to the data backend engine.
    # 3. if that fails, try to connect to the data backend uri.
    if cfg.metadata_store is not None:
        # try to connect to the metadata store specified in the configuration.
        logging.info("Connecting to Metadata Client:", cfg.metadata_store)
        metadata = build(cfg.metadata_store, metadata_stores, type='metadata')
    else:
        try:
            # try to connect to the data backend engine.
            logging.info(
                "Connecting to Metadata Client with engine: ", databackend.conn
            )
            metadata = databackend.build_metadata()
        except Exception as e:
            logging.warn("Error building metadata from DataBackend:", str(e))
            metadata = None

    if metadata is None:
        try:
            # try to connect to the data backend uri.
            logging.info("Connecting to Metadata Client with URI: ", cfg.data_backend)
            metadata = build(cfg.data_backend, metadata_stores, type='metadata')
        except Exception as e:
            # Exit quickly if a connection fails.
            logging.error("Error initializing to Metadata Client:", str(e))
            sys.exit(1)

    # Build DataLayer
    # ------------------------------
    db = Datalayer(
        databackend=databackend,
        metadata=metadata,
        artifact_store=(
            build_artifact_store(cfg.artifact_store)
            if cfg.artifact_store is not None
            else databackend.build_artifact_store()
        ),
        compute=build_compute(cfg.cluster.compute),
    )

    return db
