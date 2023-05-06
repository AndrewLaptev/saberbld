from typing import Annotated

from typer import Typer, Option, Argument

from saberbld.core import Core
from saberbld.view import View
from saberbld.models import CommandsAliasesPlural, CommandsAliases


app = Typer(
    help="CLI application for comfort view information about builds ant tasks"
)


@app.command()
def list(
    object: Annotated[
        CommandsAliasesPlural, Argument(help="List objects type")
    ],
    builds_file: Annotated[
        str, Option(help="Filepath to builds.yaml file")
    ] = "builds.yaml",
    tasks_file: Annotated[
        str, Option(help="Filepath to tasks.yaml file")
    ] = "tasks.yaml",
):
    """
    List all tasks or builds
    """
    core = Core(builds_file, tasks_file)
    view = View(f"List of available {object.value}:")

    items = [f"* {name}" for name in core.maps[object.value]]

    view.print_list(items)


@app.command()
def get(
    object: Annotated[CommandsAliases, Argument(help="Getting object type")],
    name: Annotated[str, Argument(help="Name of build or task")],
    graph: Annotated[
        bool, Option(help="View dependencies tree as graph")
    ] = False,
    builds_file: Annotated[
        str, Option(help="Filepath to builds.yaml file")
    ] = "builds.yaml",
    tasks_file: Annotated[
        str, Option(help="Filepath to tasks.yaml file")
    ] = "tasks.yaml",
):
    """
    Getting info about task or build
    """
    core = Core(builds_file, tasks_file)
    view = View(f"{object.value} info:".capitalize())

    if object is CommandsAliases.BUILD:
        deps_graph = core.build_tasks_graph(name)
    else:
        deps_graph = core.task_deps_graph(name)

    if graph:
        view.print_graph(name, deps_graph)
    else:
        view.print_list_graph(name, deps_graph)


if __name__ == "__main__":
    app()
