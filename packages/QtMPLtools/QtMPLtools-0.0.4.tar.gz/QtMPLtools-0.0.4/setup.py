import subprocess as sp
import os
import sys
from setuptools import setup, find_packages, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

##### ------ Sets environment variable ------ #####
###################################################
if os.name == 'posix':
    exp = 'export PYQTDESIGNERPATH='+os.path.dirname(os.path.realpath(sys.argv[0]))
elif os.name == 'nt':
    exp = 'setx PYQTDESIGNERPATH '+os.path.dirname(os.path.realpath(sys.argv[0]))

sp.Popen(exp, shell=True).wait()
###################################################

setup(
    name='QtMPLtools',
    version='0.0.4',
    description='Matplotlib plugins for Qt designer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dresis/QtMPLtools',
    author='Andy Velasco',
    author_email='',
    license='MIT',
    install_requires=['matplotlib', 'PyQt6', 'pyqt6-tools'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    # scripts=['scripts/MadQt-rcc'],
    entry_points={
        'console_scripts': [
            'designer=QtMPLtools.scripts.designer:main',
        ],
    },
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11",
    keywords=['python', 'qt', 'matplotlib', 'plugins', 'plots']
)
