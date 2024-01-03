import yaml
from instruction import instructions


class Context:
    def __init__(self, path, job_class):
        self.data = yaml.full_load(open(path))

        self.context_data = {}

        self.job_class = job_class

        self.initialize()

    def initialize(self):
        # load register
        pass

    def run(self):
        task_name = self.data["name"]
        result = self.data["output"]

        for name, job in self.data["jobs"].items():
            self.context_data[name] = self.execute_job(job)

        return self.context_data[result]

    def execute_job(self, job_data):
        steps = job_data["steps"]

        result = None
        for step in steps:
            result = instructions[step["type"]]().execute(result, self, **step["run"])

        return result
