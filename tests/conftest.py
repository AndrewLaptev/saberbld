import os
import yaml
from random import randint

from pytest import FixtureRequest, fixture
from typer.testing import CliRunner

from saberbld.main import app


BUILDS_TEST_FILE = "tests/data/builds_test.yaml"
TASKS_TEST_FILE = "tests/data/tasks_test.yaml"

with open(BUILDS_TEST_FILE, "r") as file:
    BUILDS_LIST = [build["name"] for build in yaml.safe_load(file)["builds"]]

with open(TASKS_TEST_FILE, "r") as file:
    TASKS_LIST = [task["name"] for task in yaml.safe_load(file)["tasks"]]

FILES_ARGS = [
    "--builds-file",
    BUILDS_TEST_FILE,
    "--tasks-file",
    TASKS_TEST_FILE,
]


def _defect_diller(
    defect: tuple[str, str],
    builds_filename: str | None = None,
    tasks_filename: str | None = None,
):
    file_args_defect = list(FILES_ARGS)

    if builds_filename:
        with open(BUILDS_TEST_FILE, "r") as file:
            builds_test_file = file.read()

        BUILDS_TEST_DEFECT_FILE = (
            os.path.dirname(BUILDS_TEST_FILE) + f"/{builds_filename}"
        )

        with open(BUILDS_TEST_DEFECT_FILE, "w") as file:
            file.write(builds_test_file.replace(*defect))

        file_args_defect[1] = BUILDS_TEST_DEFECT_FILE

    if tasks_filename:
        with open(TASKS_TEST_FILE, "r") as file:
            tasks_test_file = file.read()

        TASKS_TEST_DEFECT_FILE = (
            os.path.dirname(TASKS_TEST_FILE) + f"/{tasks_filename}"
        )

        with open(TASKS_TEST_DEFECT_FILE, "w") as file:
            file.write(tasks_test_file.replace(*defect))

        file_args_defect[3] = TASKS_TEST_DEFECT_FILE

    return file_args_defect


@fixture()
def res(request: FixtureRequest):
    return CliRunner().invoke(app, request.param.split() + FILES_ARGS)


@fixture()
def res_fileless(request: FixtureRequest):
    return CliRunner().invoke(app, request.param.split())


@fixture()
def res_file_yaml_defect(request: FixtureRequest):
    BUILDS_FILE_DEFECT_NAME = "builds_test_yaml_defect.yaml"
    TASKS_FILE_DEFECT_NAME = "tasks_test_yaml_defect.yaml"

    FILES_ARGS_DEFECT = _defect_diller(
        ("\n", " " * randint(1, 3)),
        BUILDS_FILE_DEFECT_NAME,
        TASKS_FILE_DEFECT_NAME,
    )

    yield CliRunner().invoke(app, request.param.split() + FILES_ARGS_DEFECT)

    os.remove(os.path.dirname(BUILDS_TEST_FILE) + f"/{BUILDS_FILE_DEFECT_NAME}")
    os.remove(os.path.dirname(TASKS_TEST_FILE) + f"/{TASKS_FILE_DEFECT_NAME}")


@fixture()
def res_file_valid_defect(request: FixtureRequest):
    BUILDS_FILE_DEFECT_NAME = "builds_test_valid_defect.yaml"
    TASKS_FILE_DEFECT_NAME = "tasks_test_valid_defect.yaml"

    FILES_ARGS_DEFECT = _defect_diller(
        ("name", "n@me"), BUILDS_FILE_DEFECT_NAME, TASKS_FILE_DEFECT_NAME
    )

    yield CliRunner().invoke(app, request.param.split() + FILES_ARGS_DEFECT)

    os.remove(os.path.dirname(BUILDS_TEST_FILE) + f"/{BUILDS_FILE_DEFECT_NAME}")
    os.remove(os.path.dirname(TASKS_TEST_FILE) + f"/{TASKS_FILE_DEFECT_NAME}")


@fixture()
def res_file_loop_defect(request: FixtureRequest):
    TASKS_FILE_DEFECT_NAME = "tasks_test_loop_defect.yaml"

    FILES_ARGS_DEFECT = _defect_diller(
        ("create_white_cyclops", "design_olive_cyclops"),
        tasks_filename=TASKS_FILE_DEFECT_NAME,
    )

    yield CliRunner().invoke(app, request.param.split() + FILES_ARGS_DEFECT)

    os.remove(os.path.dirname(TASKS_TEST_FILE) + f"/{TASKS_FILE_DEFECT_NAME}")
