
import re
import os
import copy
from kraken_boilerplate.helpers import json
import pkg_resources
from kraken_boilerplate.helpers.dot_notation import to_dot, from_dot
import zipfile
from functools import lru_cache
from io import BytesIO
#from zipfile import ZipFile
from urllib.request import urlopen
import shutil


"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('kraken_boilerplate', old_path)

"""


def get(document_type, record, language='EN-US'):
    """
    """
    content = _get_document(document_type, language)

    # Convert fields to lowercase
    fields = get_fields(document_type, language)
    for i in fields:
        content = content.replace('{{' + i + '}}', '{{' + i.lower() + '}}')
    
    # Replace variables
    items = to_dot(record, [record.get('@type', None)])
    for i in items:
        k = i.get('key', None)
        v = i.get('value', None)

        k = '{{' + k + '}}'
        k = k.lower()
        
        content = content.replace(k, v)

    return content
    

def get_fields(document_type, language='EN-US'):
    """Returns all fields in a given document
    """
    
    content = _get_document(document_type, language)

    pat = '{{(.*?)}}'
    values = re.findall(pat, content)

    return values

def get_record(document_type, language='EN-US'):
    """Returns record to be provided
    """
    fields = get_fields(document_type, language)
    record = {}
    for i in fields:
        record[i] = 'temp'

    record = from_dot(record)
    return record
    

def get_files():
    """
    """
    filepath = pkg_resources.resource_filename('kraken_boilerplate', 'data/')
    files = os.listdir(filepath)
    return files


def refresh():
    """Retrieves new templates from github
    """
    url = 'https://github.com/tactik8/boilerplates/archive/main.zip'

    # Retrieve zip file from github
    resp = urlopen(url)
    f = BytesIO(resp.read())


    # Configure destination path
    destpath = pkg_resources.resource_filename('kraken_boilerplate', 'data/')
    os.makedirs(os.path.dirname(destpath), exist_ok=True)

    # Extract files
    with zipfile.ZipFile(f, mode="r") as archive:
        for file in archive.namelist():

            if file.startswith('boilerplates-main/templates/'):
                filename = os.path.basename(file)
                if not filename:
                    continue
                
                source = archive.open(file)
                target = open(os.path.join(destpath, filename), "wb")

                with source, target:
                    shutil.copyfileobj(source, target)
            
    print('Files extracted from github')

@lru_cache(maxsize=128)
def _get_document(document_type, language):
    """Retrieve docs
    """
    
    filename = f'{document_type.lower()}_{language.lower()}.html'

    filepath = pkg_resources.resource_filename('kraken_boilerplate', 'data/' + filename)

    with open(filepath, 'r') as f:
        content = f.read()
    return content

