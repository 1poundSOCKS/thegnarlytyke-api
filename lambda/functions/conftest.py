from pytest import fixture

def pytest_addoption(parser):
    parser.addoption(
        "--alias",
        action="store"
    )
    parser.addoption(
        "--userdataBucket",
        action="store"
    )
    parser.addoption(
        "--dataBucket",
        action="store"
    )
    parser.addoption(
        "--email",
        action="store"
    )
    parser.addoption(
        "--password",
        action="store"
    )

@fixture()
def alias(request):
    return request.config.getoption("--alias")

@fixture()
def userdataBucket(request):
    return request.config.getoption("--userdataBucket")

@fixture()
def dataBucket(request):
    return request.config.getoption("--dataBucket")

@fixture()
def email(request):
    return request.config.getoption("--email")

@fixture()
def password(request):
    return request.config.getoption("--password")
