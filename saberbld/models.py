from enum import Enum

from pydantic import BaseModel


class CommandsAliases(str, Enum):
    BUILD = "build"
    TASK = "task"


class CommandsAliasesPlural(str, Enum):
    BUILDS = CommandsAliases.BUILD.value + "s"
    TASKS = CommandsAliases.TASK.value + "s"


class TaskModel(BaseModel):
    name: str
    dependencies: list[str]


class BuildModel(BaseModel):
    name: str
    tasks: list[str]


class TasksModel(BaseModel):
    tasks: list[TaskModel]


class BuildsModel(BaseModel):
    builds: list[BuildModel]
