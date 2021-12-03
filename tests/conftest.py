import pytest

def pytest_sessionstart(session):
    session.results = dict()
    
def pytest_addoption(parser):
    parser.addoption("--secret")

@pytest.fixture(scope='session')
def secret(request):
    return request.config.getoption("--secret")