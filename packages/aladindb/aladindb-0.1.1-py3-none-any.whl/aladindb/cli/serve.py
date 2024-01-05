import subprocess

from . import command


@command(help='Start local dask scheduler')
def dask_scheduler():
    subprocess.Popen(["dask", "scheduler"])


@command(help='Start local dask worker')
def dask_worker():
    subprocess.Popen(["dask", "worker", "tcp://localhost:8786"])


@command(help='Start local cluster: server, dask and change data capture')
def local_cluster():
    from aladindb.base.build import build_datalayer
    from aladindb.server.cluster import cluster

    db = build_datalayer()
    cluster(db)


@command(help='Start vector search server')
def vector_search():
    from aladindb.vector_search.server.app import app

    app.start()


@command(help='Start standalone change data capture')
def cdc():
    from aladindb.cdc.app import app

    app.start()
