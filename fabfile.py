from fabric.api import local

def docs():
    local("./bin/docs")
    local("./bin/python setup.py upload_sphinx --upload-dir=docs/html")

def release():
    local("./bin/python setup.py sdist --formats=gztar,zip upload")
