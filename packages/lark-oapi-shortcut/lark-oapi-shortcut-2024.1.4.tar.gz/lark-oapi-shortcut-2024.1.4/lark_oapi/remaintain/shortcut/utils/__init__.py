from typing import Optional

import attr


def convert_model_to_dict(o) -> Optional[dict]:
    if attr.has(o):
        return attr.asdict(o)
    elif hasattr(o, '_types'):
        return convert_remaintain_extra_model_to_dict(o)
    else:
        return None


def convert_remaintain_extra_model_to_dict(o) -> Optional[dict]:
    if not hasattr(o, '_types'):
        return None
    kv = {}
    for k in o._types.keys():
        v = getattr(o, k, None)
        if hasattr(v, '_types'):
            kv[k] = convert_remaintain_extra_model_to_dict(v)
        else:
            kv[k] = v
    return kv


def print_model(o):
    kv = convert_model_to_dict(o)
    if not isinstance(kv, dict):
        print(o)
    else:
        print(o.__class__.__name__, end="(\n")
        for k, v in kv.items():
            print(f'\t{k}={v},')
        print(")")
