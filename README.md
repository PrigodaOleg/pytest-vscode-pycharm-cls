# pytest-vscode-pycharm-cls
## Installation
    pip install pytest-vscode-pycharm-cls
## Usage
### Integration to Visual Studio Code
First, generate launch.json file in VSCode. Use Python -> Remote Attach option

At start tests:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.VSCode --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --trace

At tests failed:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.VSCode --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --pdb

### Integration to PyCharm
Attention: debug server is not integrated in community PyCharm version. Sad.
First, create Debug Server configuration.

At start tests:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.PyCharm --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --trace

At tests failed:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.PyCharm --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --pdb