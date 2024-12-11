import json
import types


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, types.MappingProxyType):
            return dict(obj)
        elif hasattr(obj, '__json__') and callable(obj.__json__):
            return obj.__json__()
        elif hasattr(obj, '__dict__'):
            filtered_dict = {k: v for k, v in obj.__dict__.items() if not callable(v)}
            return filtered_dict
        else:
            return super().default(obj)