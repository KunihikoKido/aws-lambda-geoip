import os
print os.getcwd()
import zipfile

from fabric.api import *

BASE_PATH = os.getcwd()

LIB_PATH = os.path.join(BASE_PATH, 'lib')
TEMP_DIR = os.path.join(BASE_PATH, 'tmp')

ZIP_FILE = os.path.join(BASE_PATH, 'lambda_function.zip')
ZIP_EXCLUDE_FILE = os.path.join(BASE_PATH, 'exclude.lst')

LAMBDA_HANDLER = 'lambda_handler'
LAMBDA_FILE = 'lambda_function.py'
LAMBDA_EVENT = 'event.json'

INSTALL_PREFIX = os.path.join(BASE_PATH, 'local')

def install_python_modules():
    local('pip install --upgrade -r requirements.txt -t {}'.format(LIB_PATH))

def install_geolite2_database():
    local('wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz')
    local('gzip -d GeoLite2-City.mmdb.gz')

@task
def setup():
    install_python_modules()
    install_geolite2_database()


@task
def clean():
    local('rm -f lambda_function.zip')
    local('rm -rf {}'.format(LIB_PATH))
    local('rm -rf {}'.format(INSTALL_PREFIX))
    local('rm -rf {}'.format(TEMP_DIR))

@task
def invoke(eventfile=LAMBDA_EVENT):
    with shell_env(PYTHONPATH=LIB_PATH):
        local('python-lambda-local -l {} -f {} {} {}'.format(
            LIB_PATH, LAMBDA_HANDLER, LAMBDA_FILE, eventfile
        ))

@task
def makezip():
    with lcd(BASE_PATH):
        local('rm -f {}'.format(ZIP_FILE))
        local('zip -r9 {} * -x @{}'.format(ZIP_FILE, ZIP_EXCLUDE_FILE))

    with lcd(LIB_PATH):
        local('zip -r9 {} * -x @{}'.format(ZIP_FILE, ZIP_EXCLUDE_FILE))
