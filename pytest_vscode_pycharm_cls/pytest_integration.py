import os
import time


def pytest_addoption(parser):
    """
    Add option to get connection options.

    :param parser: parser object
    :return: None
    """
    parser.addoption("--debug-host",
                     default=os.getenv('PYTEST_DEBUG_HOST', 'localhost'),
                     action="store", help="Host to start listen for incoming connections from VSCode "
                                          "or to connect to PyCharm debug server. Default: localhost")
    parser.addoption("--debug-port",
                     default=os.getenv('PYTEST_DEBUG_PORT', 7777),
                     action="store", help="Port to start listen for incoming connections from VSCode "
                                          "or to connect to PyCharm debug server. Default: 7777")
    parser.addoption("--debug-wait-timeout",
                     default=os.getenv('PYTEST_DEBUG_WAIT_TIMEOUT', 300),
                     action="store", help="Timeout in seconds for waiting incoming connections from VSCode "
                                          "or to connect to PyCharm debug server. Default: 300")


def pytest_configure(config):
    os.environ['PYTEST_DEBUG_HOST'] = str(config.getoption('debug_host'))
    os.environ['PYTEST_DEBUG_PORT'] = str(config.getoption('debug_port'))
    os.environ['PYTEST_DEBUG_WAIT_TIMEOUT'] = str(config.getoption('debug_wait_timeout'))


class VSCode:
    is_started = False

    def __init__(self, *args, **kwargs):
        if not VSCode.is_started:
            VSCode.is_started = True
            host = os.environ.get('PYTEST_DEBUG_HOST')
            port = int(os.environ.get('PYTEST_DEBUG_PORT'))
            import debugpy
            debugpy.listen((host, port))
            timeout = int(os.environ.get('PYTEST_DEBUG_WAIT_TIMEOUT'))
            while timeout and not debugpy.is_client_connected():
                time.sleep(1)
                timeout -= 1

    def runcall(self, func):
        func(*func.args, **func.keywords)


class PyCharm:
    is_started = False
    timeout = 0

    def __init__(self, *args, **kwargs):
        if not PyCharm.is_started:
            PyCharm.timeout = int(os.environ.get('PYTEST_DEBUG_WAIT_TIMEOUT'))
            PyCharm.is_started = True

    def runcall(self, func):
        host = os.environ.get('PYTEST_DEBUG_HOST')
        port = int(os.environ.get('PYTEST_DEBUG_PORT'))
        import pydevd_pycharm
        while PyCharm.timeout:
            try:
                pydevd_pycharm.settrace(host,
                                        port=port,
                                        stdoutToServer=True,
                                        stderrToServer=True
                                        )
                break
            except:
                time.sleep(1)
                PyCharm.timeout -= 1
        func(*func.args, **func.keywords)

