import os
import time
import subprocess


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
    parser.addoption("--debug-port-vscode",
                     default=os.getenv('PYTEST_DEBUG_PORT_VSCODE', 5678),
                     action="store", help="Port to start listen for incoming connections from VSCode. Default: 5678")
    parser.addoption("--debug-port-pycharm",
                     default=os.getenv('PYTEST_DEBUG_PORT_PYCHARM', 7777),
                     action="store", help="Port to connect to PyCharm debug server. Default: 7777")
    parser.addoption("--debug-wait-timeout",
                     default=os.getenv('PYTEST_DEBUG_WAIT_TIMEOUT', 300),
                     action="store", help="Timeout in seconds for waiting incoming connections from VSCode "
                                          "or to connect to PyCharm debug server. Default: 300")


def pytest_configure(config):
    os.environ['PYTEST_DEBUG_HOST'] = str(config.getoption('debug_host'))
    os.environ['PYTEST_DEBUG_PORT_VSCODE'] = str(config.getoption('debug_port_vscode'))
    os.environ['PYTEST_DEBUG_PORT_PYCHARM'] = str(config.getoption('debug_port_pycharm'))
    os.environ['PYTEST_DEBUG_WAIT_TIMEOUT'] = str(config.getoption('debug_wait_timeout'))


class Pdb:
    timeout = 0
    debugger = None
    is_started = False

    def __init__(self, *args, **kwargs):
        if not Pdb.is_started:
            Pdb.host = os.environ.get('PYTEST_DEBUG_HOST')
            Pdb.vscode_port = int(os.environ.get('PYTEST_DEBUG_PORT_VSCODE'))
            Pdb.pycharm_port = int(os.environ.get('PYTEST_DEBUG_PORT_PYCHARM'))
            Pdb.timeout = int(os.environ.get('PYTEST_DEBUG_WAIT_TIMEOUT'))
            Pdb.is_started = True
        if not Pdb.debugger:
            print('Waiting for debugger...')
            listener = subprocess.Popen(f'echo "hello" | nc -l -N {Pdb.vscode_port}', shell=True)
            while Pdb.timeout > 0:
                if listener.poll() == 0:
                    print('VSCode connection detected')
                    listener.terminate()
                    import debugpy
                    debugpy.listen((Pdb.host, Pdb.vscode_port))
                    Pdb.debugger = 'vscode'
                    break
                if os.system(f'ss -tulpn | grep {Pdb.pycharm_port} > /dev/null') == 0:
                    print('PyCharm is on line')
                    Pdb.debugger = 'pycharm'
                    break
                time.sleep(1)
                Pdb.timeout -= 1
            else:
                listener.terminate()

    def runcall(self, func):
        print('runcall start')

        if Pdb.debugger == 'vscode':
            import debugpy
            while Pdb.timeout > 0:
                # Check if VSCode IDE has connected
                if debugpy.is_client_connected():
                    debugpy.breakpoint()
                    break
                time.sleep(1)
                Pdb.timeout -= 1
        elif Pdb.debugger == 'pycharm':
            import pydevd_pycharm
            while Pdb.timeout > 0:
                # Trying to connect to PyCharm debugging server
                try:
                    pydevd_pycharm.settrace(Pdb.host, port=Pdb.pycharm_port, stdoutToServer=True, stderrToServer=True)
                    break
                except:
                    time.sleep(1)
                    Pdb.timeout -= 1

        func(*func.args, **func.keywords)

