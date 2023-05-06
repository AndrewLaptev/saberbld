from pytest import mark
from typer.testing import Result

from tests.conftest import BUILDS_LIST, TASKS_LIST


@mark.parametrize("res", ["list builds"], indirect=True)
def test_list_builds(res: Result):
    assert res.exit_code == 0


@mark.parametrize("res", ["list tasks"], indirect=True)
def test_list_tasks(res: Result):
    assert res.exit_code == 0


@mark.parametrize(
    "res", [f"get build {build}" for build in BUILDS_LIST], indirect=True
)
def test_get_build(res: Result):
    assert res.exit_code == 0


@mark.parametrize(
    "res", [f"get task {task}" for task in TASKS_LIST], indirect=True
)
def test_get_task(res: Result):
    assert res.exit_code == 0


@mark.parametrize("res", ["get task @#*%$#*#$"], indirect=True)
def test_get_incorrect_task(res: Result):
    assert res.exit_code == 1


@mark.parametrize("res", ["get build @#*%$#*#$"], indirect=True)
def test_get_incorrect_build(res: Result):
    assert res.exit_code == 1


@mark.parametrize("res", ["get task"], indirect=True)
def test_get_empty_task(res: Result):
    assert res.exit_code == 2


@mark.parametrize("res", ["get build"], indirect=True)
def test_get_empty_build(res: Result):
    assert res.exit_code == 2


@mark.parametrize(
    "res_fileless", ["list builds --builds-file /#!$/$#$"], indirect=True
)
def test_incorrect_builds_filepath(res_fileless: Result):
    assert res_fileless.exit_code == 1


@mark.parametrize(
    "res_fileless", ["list tasks --tasks-file /#!$/$#$"], indirect=True
)
def test_incorrect_tasks_filepath(res_fileless: Result):
    assert res_fileless.exit_code == 1


@mark.parametrize(
    "res_file_yaml_defect", ["list builds", "list tasks"], indirect=True
)
def test_yaml_file_defect(res_file_yaml_defect: Result):
    assert res_file_yaml_defect.exit_code == 1


@mark.parametrize(
    "res_file_valid_defect", ["list builds", "list tasks"], indirect=True
)
def test_valid_file_defect(res_file_valid_defect: Result):
    assert res_file_valid_defect.exit_code == 1


@mark.parametrize(
    "res_file_loop_defect", ["get build time_alone"], indirect=True
)
def test_loop_file_defect(res_file_loop_defect: Result):
    assert res_file_loop_defect.exit_code == 1
