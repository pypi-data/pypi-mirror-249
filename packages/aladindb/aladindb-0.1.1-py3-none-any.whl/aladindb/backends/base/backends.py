from ibis.backends.base import BaseBackend
from pymongo import MongoClient

from aladindb.backends.ibis.data_backend import IbisDataBackend
from aladindb.backends.local.artifacts import FileSystemArtifactStore
from aladindb.backends.mongodb.artifacts import MongoArtifactStore
from aladindb.backends.mongodb.data_backend import MongoDataBackend
from aladindb.backends.mongodb.metadata import MongoMetaDataStore
from aladindb.backends.sqlalchemy.metadata import SQLAlchemyMetadata
from aladindb.vector_search.atlas import MongoAtlasVectorSearcher
from aladindb.vector_search.in_memory import InMemoryVectorSearcher
from aladindb.vector_search.lance import LanceVectorSearcher

data_backends = {
    'mongodb': MongoDataBackend,
    'ibis': IbisDataBackend,
}

artifact_stores = {
    'mongodb': MongoArtifactStore,
    'filesystem': FileSystemArtifactStore,
}

metadata_stores = {
    'mongodb': MongoMetaDataStore,
    'sqlalchemy': SQLAlchemyMetadata,
}

vector_searcher_implementations = {
    'lance': LanceVectorSearcher,
    'in_memory': InMemoryVectorSearcher,
    'mongodb+srv': MongoAtlasVectorSearcher,
}

CONNECTIONS = {
    'pymongo': MongoClient,
    'ibis': BaseBackend,
}
