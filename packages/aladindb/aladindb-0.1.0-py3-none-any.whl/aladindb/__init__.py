# ruff: noqa: E402
from .base import config, configs, jsonable, logger
from .base.aladin import aladin

ICON = '🔮'
CFG = configs.CFG
JSONable = jsonable.JSONable
ROOT = configs.ROOT

logging = logger.Logging

__version__ = '0.1.0'

from aladindb.backends import ibis, mongodb

from .base.document import Document
from .components.dataset import Dataset
from .components.encoder import Encoder
from .components.listener import Listener
from .components.metric import Metric
from .components.model import Model
from .components.schema import Schema
from .components.serializer import Serializer
from .components.vector_index import VectorIndex, vector

__all__ = (
    'CFG',
    'ICON',
    'JSONable',
    'ROOT',
    'config',
    'logging',
    'aladin',
    'Encoder',
    'Document',
    'Model',
    'Listener',
    'VectorIndex',
    'vector',
    'Dataset',
    'Metric',
    'Schema',
    'Serializer',
    'mongodb',
    'ibis',
)
