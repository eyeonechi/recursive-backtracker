from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read();

def license():
    with open('LICENSE') as f:
        return f.read();

setup(
    name='recursive-backtracker',
    version='0.0.1',
    description='Maze solution and shortest paths generation using the Recursive Backtracker algorithm',
    long_description=readme(),
    url='https://github.com/eyeonechi/recursive-backtracker',
    author='Ivan Ken Weng Chee',
    author_email='ichee@student.unimelb.edu.au',
    license=license(),
    keywords=[
        'COMP10001'
    ],
    scripts=[
        'src/recursive_backtracker'
    ],
    packages=[],
    zip_safe=False,
    include_package_data=True
)
