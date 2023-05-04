import yaml

from app.models import (
    BuildModel,
    TaskModel,
    BuildsModel,
    TasksModel,
    CommandsAliasesPlural,
)

BUILDS = CommandsAliasesPlural.BUILDS.value
TASKS = CommandsAliasesPlural.TASKS.value


class Core:
    def __init__(
        self,
        builds_file_path: str,
        tasks_file_path: str,
    ) -> None:
        with open(builds_file_path, "r") as file:
            self.builds_data = BuildsModel(**yaml.safe_load(file))

        with open(tasks_file_path, "r") as file:
            self.tasks_data = TasksModel(**yaml.safe_load(file))

        self.maps: dict[str, dict[str, BuildModel | TaskModel]] = {
            BUILDS: {build.name: build for build in self.builds_data.builds},
            TASKS: {task.name: task for task in self.tasks_data.tasks},
        }
        self._uniq_graph_nodes: set[str] = set()

    def task_deps_graph(self, name: str) -> dict | None:
        if name in self._uniq_graph_nodes:
            raise Exception("LOOP")
        
        self._uniq_graph_nodes.add(name)

        task_deps = {}

        if len(self.maps[TASKS][name].dependencies) == 0:
            return None
        else:
            for dep in self.maps[TASKS][name].dependencies:
                task_deps[dep] = self.task_deps_graph(dep)

        return task_deps

    def build_tasks_graph(self, name: str) -> dict:
        build = {}

        for task in self.maps[BUILDS][name].tasks:
            build[task] = self.task_deps_graph(task)

        return build
