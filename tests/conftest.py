import pytest


def pytest_addoption(parser):
    parser.addoption("--environment",
                     action="store",
                     choices=("local", "actions"),
                     default="actions")


@pytest.fixture(scope="session")
def get_environment(pytestconfig):
    return pytestconfig.getoption("environment")
