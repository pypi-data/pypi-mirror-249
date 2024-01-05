import base64
import os
import typing as t

import numpy as np

if t.TYPE_CHECKING:
    from aladindb.components.encoder import Encoder


def str_shape(shape: t.Sequence[int]) -> str:
    if not shape:
        raise ValueError('Shape was empty')
    return 'x'.join(str(x) for x in shape)


def get_key(key_name: str) -> str:
    try:
        return os.environ[key_name]
    except KeyError:
        raise KeyError(f'Environment variable {key_name} is not set') from None


def format_prompt(X: str, prompt: str, context: t.Optional[t.List[str]] = None) -> str:
    format_params = {}
    if '{input}' in prompt:
        format_params['input'] = X
    else:
        prompt += X

    if '{context}' in prompt:
        if context:
            format_params['context'] = '\n'.join(context)
        else:
            raise ValueError(f'A context is required for prompt {prompt}')

    return prompt.format(**format_params)


def aladinencode(object):
    if isinstance(object, np.ndarray):
        from aladindb.ext.numpy import array

        encoded = array(dtype=object.dtype, shape=object.shape).encode(object)
        encoded['shape'] = object.shape
        encoded['dtype'] = str(object.dtype)
        return encoded
    return object


def aladindecode(r: t.Any, encoders: t.List['Encoder']):
    if isinstance(r, dict):
        encoder = encoders[r['_content']['encoder']]
        b = base64.b64decode(r['_content']['bytes'])
        return encoder.decode(b).x
    return r
