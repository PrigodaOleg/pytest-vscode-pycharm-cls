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
                     default=os.getenv('PYTEST_DEBUG_PORT', 5678),
                     action="store", help="Port to start listen for incoming connections from VSCode "
                                          "or to connect to PyCharm debug server. Default: 5678")
    parser.addoption("--debug-wait-timeout",
                     default=os.getenv('PYTEST_DEBUG_WAIT_TIMEOUT', 300),
                     action="store", help="Timeout in seconds for waiting incoming connections from VSCode "
                                          "or to connect to PyCharm debug server. Default: 300")


def pytest_configure(config):
    os.environ['PYTEST_DEBUG_HOST'] = str(config.getoption('debug_host'))
    os.environ['PYTEST_DEBUG_PORT'] = str(config.getoption('debug_port'))
    os.environ['PYTEST_DEBUG_WAIT_TIMEOUT'] = str(config.getoption('debug_wait_timeout'))


class Pdb:
    is_started = False

    def __init__(self, *args, **kwargs):
        if not Pdb.is_started:
            Pdb.is_started = True
            host = os.environ.get('PYTEST_DEBUG_HOST')
            port = int(os.environ.get('PYTEST_DEBUG_PORT'))
            Pdb.timeout = int(os.environ.get('PYTEST_DEBUG_WAIT_TIMEOUT'))

            # VSCode server
            import debugpy
            debugpy.listen((host, port))

            # PyCharm client

            import pydevd_pycharm
            while Pdb.timeout > 0:
                # Check if VSCode IDE has connected
                if debugpy.is_client_connected():
                    break

                # Trying to connect to PyCharm debugging server
                try:
                    pydevd_pycharm.settrace(host,
                                            port=port,
                                            stdoutToServer=True,
                                            stderrToServer=True
                                            )
                    break
                except:
                    time.sleep(1)
                    Pdb.timeout -= 1

    def runcall(self, func):
        breakpoint()
        func(*func.args, **func.keywords)
