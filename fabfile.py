import os
print os.getcwd()
import zipfile

from fabric.api import *

BASE_PATH = os.getcwd()

LIB_PATH = os.path.join(BASE_PATH, 'lib')

ZIP_FILE = os.path.join(BASE_PATH, 'lambda_function.zip')
ZIP_EXCLUDE_FILE = os.path.join(BASE_PATH, 'exclude.lst')

def install_python_modules():
    local('pip install --upgrade -r requirements.txt -t {lib_path}'.format(lib_path=LIB_PATH))

def download_geolite2_database():
    local('wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz')
    local('gzip -d GeoLite2-City.mmdb.gz')

@task
def setup():
    install_python_modules()
    download_geolite2_database()

@task
def run():
    local("""
    python-lambda-local \
        -l {lib_path} \
        -f lambda_handler \
        lambda_function.py \
        event.json
    """.format(lib_path=LIB_PATH))

@task
def bundle():
    with lcd(BASE_PATH):
        local('rm -f {}'.format(ZIP_FILE))
        local('zip -r9 {} * -x @{}'.format(ZIP_FILE, ZIP_EXCLUDE_FILE))

    with lcd(LIB_PATH):
        local('zip -r9 {} * -x @{}'.format(ZIP_FILE, ZIP_EXCLUDE_FILE))
