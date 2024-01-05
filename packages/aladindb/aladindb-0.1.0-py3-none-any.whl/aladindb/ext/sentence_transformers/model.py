import dataclasses as dc
import typing as t

import sentence_transformers

from aladindb.base.artifact import Artifact
from aladindb.components.model import Model


@dc.dataclass(kw_only=True)
class SentenceTransformer(Model):
    object: t.Union[Artifact, t.Callable, None] = None

    def __post_init__(self):
        super().__post_init__()
        if self.object is None:
            self.object = Artifact(
                artifact=sentence_transformers.SentenceTransformer(
                    self.identifier, device=self.device
                )
            )
        self.object.artifact = self.object.artifact.to(self.device)
        self.model_to_device_method = '_to'

    def _to(self, device):
        self.object.artifact = self.object.artifact.to(device)
        self.object.artifact._target_device = device
