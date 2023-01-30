from setuptools import setup

setup(
    name="pytest-vscode-pycharm-cls",
    packages=["pytest_vscode_pycharm_cls"],
    version="0.1",
    description="A PyTest helper to enable start remote debugger on test start or failure "
                "or when pytest.set_trace is used.",
    long_description="A PyTest helper to enable start remote debugger on test start or failure "
                     "or when pytest.set_trace is used. Works with Visual Studio Code and PyCharm.",
    author="Prigoda Oleg",
    author_email="prigodaoleg@gmail.com",
    url="https://github.com/PrigodaOleg/pytest-vscode-pycharm-cls",
    classifiers=[
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Testing",
    ],
    entry_points={"pytest11": ["ide_remote_debugging = pytest_vscode_pycharm_cls.pytest_integration"]},
    install_requires=[
        'pytest',
        'debugpy',
        'pydevd_pycharm'
    ],
)
