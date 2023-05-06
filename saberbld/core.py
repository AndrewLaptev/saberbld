import yaml

from yaml.parser import ParserError
from pydantic import ValidationError

from saberbld.models import (
    BuildModel,
    TaskModel,
    BuildsModel,
    TasksModel,
    CommandsAliasesPlural,
)


BUILDS = CommandsAliasesPlural.BUILDS.value
TASKS = CommandsAliasesPlural.TASKS.value


class Core:
    """
    Main logic for generate dependencies graph
    """

    def __init__(
        self,
        builds_file_path: str,
        tasks_file_path: str,
    ) -> None:
        try:
            with open(builds_file_path, "r") as file:
                self.builds_data = BuildsModel(**yaml.safe_load(file))
            with open(tasks_file_path, "r") as file:
                self.tasks_data = TasksModel(**yaml.safe_load(file))
        except FileNotFoundError as e:
            raise SystemExit(
                f"YAML file not found error: {e.strerror.lower()} {e.filename}"
            )
        except ParserError as e:
            raise SystemExit(f"YAML parsing error: {e}")
        except ValidationError as e:
            raise SystemExit(f"YAML validation error: {e}")

        self.maps: dict[str, dict[str, BuildModel | TaskModel]] = {
            BUILDS: {build.name: build for build in self.builds_data.builds},
            TASKS: {task.name: task for task in self.tasks_data.tasks},
        }
        self._uniq_graph_nodes: set[str] = set()

    def task_deps_graph(self, name: str) -> dict | None:
        """
        Generate task dependencies graph
        """
        if name in self._uniq_graph_nodes:
            raise SystemExit(f"Task dependencies has a loop in task: {name}!")

        self._uniq_graph_nodes.add(name)

        deps_graph = {}

        try:
            if len(self.maps[TASKS][name].dependencies) == 0:
                return None
            else:
                for dep in self.maps[TASKS][name].dependencies:
                    deps_graph[dep] = self.task_deps_graph(dep)
        except KeyError as e:
            raise SystemExit(f"Name '{e.args[-1]}' is not exist in tasks!")

        return deps_graph

    def build_tasks_graph(self, name: str) -> dict:
        """
        Generate build tasks graph
        """
        tasks_graph = {}

        try:
            for task in self.maps[BUILDS][name].tasks:
                tasks_graph[task] = self.task_deps_graph(task)
        except KeyError as e:
            raise SystemExit(f"Name '{e.args[-1]}' is not exist in builds!")

        return tasks_graph
