import inspect


class Register:
    namespace_map = {}

    @classmethod
    def add(cls, key, value):
        cls.namespace_map[key] = value

    @classmethod
    def get(cls, key):
        value = cls.namespace_map.get(key)
        if value is None:
            raise KeyError("No such key '%s'" % key)
        return value


class FunctionRegister(Register):
    namespace_map = {}

    @classmethod
    def import_all(cls):
        stack = inspect.stack()
        caller_frame = stack[1][0]
        caller_locals = caller_frame.f_locals

        for k, v in FunctionRegister.namespace_map.items():
            caller_locals[k] = v

