import inspect

from utils import camel_to_underline


class Instruction:

    __args__ = ()
    __opts__ = ()

    def execute(self, instance, context, **kwargs):

        self.before_execute(**kwargs)

        self._check_params(**kwargs)
        result = self.inner_execute(instance, context, **kwargs)

        self.after_execute()

        return result

    def before_execute(self, **kwargs):
        print("=" * 100)
        print(f"Executing {self.__class__.__name__}, params: {kwargs}")

    def after_execute(self, **kwargs):
        pass

    def inner_execute(self, instance, context, **kwargs):
        raise NotImplementedError

    def _check_params(self, **kwargs):
        if self.__args__:
            for arg in self.__args__:
                if arg not in kwargs:
                    raise KeyError(f"{self.__class__.__name__} Parameter {arg} need.")


class Job:
    def __init__(self, context, **kwargs):
        self.context = context
        self.params = kwargs

    @classmethod
    def build(cls, context, **kwargs):
        return Job(context, **kwargs)

    def load(self, name, **kwargs):
        raise NotImplementedError

    def filter(self, items):
        raise NotImplementedError

    def group_by(self, group_fields, aggs):
        raise NotImplementedError

    def left_join(self, right, merge_columns):
        raise NotImplementedError

    def right_join(self, right, merge_columns):
        raise NotImplementedError

    def outer_join(self, right, merge_columns):
        raise NotImplementedError

    def rename(self, from_fields, to_fields):
        raise NotImplementedError

    def map(self, new_field, field, function):
        raise NotImplementedError


class Load(Instruction):

    __args__ = ("name",)

    def inner_execute(self, job, context, **kwargs):
        assert context.job_class is not None, 'job_class is required.'

        if job is None:
            job = context.job_class.build(context, **kwargs)

        return job.load(context, **kwargs)


class Filter(Instruction):

    __args__ = ("items", )
    __opts__ = ("input", )

    def inner_execute(self, job, context, **kwargs):
        return job.filter(**kwargs)


class GroupBy(Instruction):
    __args__ = ("aggs", "group_fields")

    def inner_execute(self, job, context, **kwargs):
        return job.group_by(**kwargs)


class LeftJoin(Instruction):
    __args__ = ("right", "merge_columns")

    def inner_execute(self, job, context, **kwargs):
        context_data = context.context_data
        if "left" in kwargs:
            left = context_data[kwargs.pop("left")]
        else:
            left = job
        right = context_data[kwargs.pop("right")]

        merge_columns = kwargs.pop("merge_columns")

        return left.left_join(right, merge_columns)


class Rename(Instruction):
    __args__ = ("fields",)

    def inner_execute(self, instance, context, **kwargs):
        fields = kwargs.pop("fields")
        from_fields, to_fields = zip(*[(f["from"], f["to"]) for f in fields])
        return instance.rename(from_fields, to_fields)


class Map(Instruction):
    __args__ = ("items",)

    def inner_execute(self, instance, context, **kwargs):

        items = kwargs.pop("items")

        for item in items:
            field = item.pop("field")
            new_field = item.pop("new_field")
            function = item.pop("function")

            instance.map(new_field, field, eval(function))

        return instance


instructions = {camel_to_underline(k): v for k, v in globals().items()
                if inspect.isclass(v) and issubclass(v, Instruction) and v is not Instruction}
