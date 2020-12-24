import json
import os

def get_bool_env(env_var, default=False):
    assert default is False or default is True
    val = os.getenv(env_var, None)
    if val is None:
        return default
    try:
        if val == "True":
            return True

        if val == "False":
            return False

        p = json.loads(val)
        assert p is False or p is True
        return p
    except ValueError:
        raise Exception("Invalid boolean config: {}".format(val))
