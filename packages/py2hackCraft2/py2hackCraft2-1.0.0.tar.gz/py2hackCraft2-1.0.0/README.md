setup:
    <command>
    pip install setuptools wheel twine

build:
    <command>
    python3 setup.py sdist bdist_wheel

deploy:
    <command>
    twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u "__token__"
