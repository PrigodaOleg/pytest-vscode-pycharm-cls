# pytest-vscode-pycharm-cls
## Installation
    todo
## Usage
### Integration to Visual Studio Code
First, generate launch.json file in VSCode. Use Python -> Remote Attach option
Second, install debudpy to remote (or local) machine where you planned to run pytest.
    
    pip3 install debugpy

At start tests:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.VSCode --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --trace

At tests failed:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.VSCode --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --pdb

### Integration to PyCharm
Attention: debug server is not integrated in community PyCharm version. Sad.
First, create Debug Server configuration.
Second, install pydevd_pycharm to remote (or local) machine where you planned to run pytest. Be careful to choose version, it must be equal to your PyCharm version.

    pip3 install pydevd-pycharm~=212.5457.59

At start tests:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.PyCharm --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --trace

At tests failed:

    pytest /path/to/your/tests --pdbcls=pytest_vscode_pycharm_cls.PyCharm --debug-host=localhost --debug-port=5678 --debug-wait-timeout=5000 --pdb