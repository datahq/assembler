import os
import tempfile
import requests
import functools
import shutil
import hashlib

from datapackage_pipelines.wrapper import process
from datapackage_pipelines.utilities.resources import PROP_STREAMED_FROM, is_a_url


def modify_datapackage(dp, parameters, stats):
    for resource in dp['resources']:
        if resource['name'] == parameters['name']:
            url = resource.get(PROP_STREAMED_FROM, resource.get('path'))
            if url is None:
                resource.update(parameters['update'])
                continue

            _, file_format = os.path.splitext(url)

            base_path = parameters['update'].pop('base-path', 'archive')
            file_path = os.path.join(base_path, resource['name'] + file_format)

            delete = False
            if is_a_url(url):
                tmp = tempfile.NamedTemporaryFile(delete=False)
                stream = requests.get(url, stream=True).raw
                stream.read = functools.partial(stream.read, decode_content=True)
                shutil.copyfileobj(stream, tmp)
                filesize = tmp.tell()
                hasher = hash_handler(tmp)
                tmp.close()
                url = tmp.name
                delete = True
            else:
                hasher = hash_handler(open(url, 'rb'))
                filesize = os.stat(url).st_size
            if delete:
                os.unlink(url)

            file_hash = hasher.hexdigest()
            resource.update(parameters['update'])
            resource.update(
                hash=file_hash,
                bytes=filesize,
                path=file_path,
                format=file_format.replace('.', '')
            )
    return dp


def hash_handler(tfile):
    tfile.seek(0)
    hasher = hashlib.md5()
    data = 'x'
    while len(data) > 0:
        data = tfile.read(1024)
        if isinstance(data, str):
            hasher.update(data.encode('utf8'))
        elif isinstance(data, bytes):
            hasher.update(data)
    return hasher


process(modify_datapackage=modify_datapackage)
