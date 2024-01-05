# xleb - web-based remote file manager
# Copyright (C) 2024  bitrate16
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import re
import os
import shutil
import pathlib
import logging

import aiohttp
import aiohttp.web
import aiohttp.web_exceptions

from xleb.state import state
from xleb.config import config



# Plain API definition
# --------------------

@state.routes.get('/css/{tail:.*}')
async def root__css(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Getter for `/css/` directory"""

    css_dir = os.path.join(state.moddir, 'static/css')
    file_path = os.path.join(css_dir, request.match_info['tail'])

    # Check for traversal
    if file_path.startswith(css_dir + os.sep):
        return aiohttp.web.FileResponse(file_path)

    raise aiohttp.web_exceptions.HTTPNotFound()


@state.routes.get('/media/{tail:.*}')
async def root__css(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Getter for `/media/` directory"""

    media_dir = os.path.join(state.moddir, 'static/media')
    file_path = os.path.join(media_dir, request.match_info['tail'])

    # Check for traversal
    if file_path.startswith(media_dir + os.sep):
        return aiohttp.web.FileResponse(file_path)

    raise aiohttp.web_exceptions.HTTPNotFound()


# Advanced API definition
# -----------------------

def wrap_auto(method: str='GET'):
    """
    Automatically generate api path based on function name.

    Name is split by `'__'` and joined with leading `'/'`.
    """

    def actual_decorator(handler):
        if handler.__name__ == 'root':
            path = '/'
        else:
            path = '/' + '/'.join(handler.__name__.split('__'))

        logging.debug(f'registering "{ handler.__name__ }" as "{ path }"')

        return state.routes.route(method, path)(handler)

    return actual_decorator


@wrap_auto('GET')
async def root(request: aiohttp.web.Request) -> aiohttp.web.Response:
    if not request['authorized']:
        return aiohttp.web.FileResponse(os.path.join(state.moddir, 'static/auth.html'))
    return aiohttp.web.FileResponse(os.path.join(state.moddir, 'static/index.html'))


def normalize_webpath(webpath: str) -> str:
    # Leading '/'
    while len(webpath) > 1 and webpath.startswith('/'):
        webpath = webpath[1:]

    # Trailing '/'
    while len(webpath) > 1 and webpath.endswith('/'):
        webpath = webpath[:-1]

    # normalize
    webpath = webpath.strip()
    if not webpath.startswith('/'):
        webpath = '/' + webpath

    # normalize to posix-style path
    return pathlib.Path(webpath).resolve(strict=False).as_posix()


def get_fspath_from_webpath(webpath: str) -> str:

    # normalize to posix-style path
    webpath = normalize_webpath(webpath)

    # Get fs path
    return os.path.join(config.path, webpath[1:])


def is_valid_subpath(fspath: str) -> bool:
    """Check if `'/s/b'` is subpath of `config.path = '/a'`"""

    return fspath.startswith(config.path + '/')


@wrap_auto('GET')
async def list(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """directory listing"""

    webpath = request.query.get('path', None)

    if webpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    # normalize to posix-style path
    webpath = normalize_webpath(webpath)

    # Get fs path
    fspath = get_fspath_from_webpath(webpath)

    # Check subdir
    if not is_valid_subpath(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    if not os.path.exists(fspath) or not os.path.isdir(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    fs_files = os.listdir(fspath)
    files = []

    for name in fs_files:
        if webpath == '/':
            web_filepath = f'/{ name }'
        else:
            web_filepath = f'{ webpath }/{ name }'

        fs_filepath = os.path.join(fspath, name)

        is_file = os.path.isfile(fs_filepath)
        is_dir = os.path.isdir(fs_filepath)

        files.append({
            'path': web_filepath,
            'name': name,
            'is_file': is_file,
            'is_dir': is_dir,
            'size': None if not is_file else os.stat(fs_filepath).st_size,
        })

    return aiohttp.web.json_response({
        'files': files,
    })


@wrap_auto('GET')
async def download(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Direct file download"""

    webpath = request.query.get('path', None)

    if webpath is None:
        raise aiohttp.web_exceptions.HTTPNotFound()

    # normalize to posix-style path
    webpath = normalize_webpath(webpath)

    # Get fs path
    fspath = get_fspath_from_webpath(webpath)

    # Check subdir
    if not is_valid_subpath(fspath):
        raise aiohttp.web_exceptions.HTTPNotFound()

    if not os.path.exists(fspath):
        raise aiohttp.web_exceptions.HTTPNotFound()

    return aiohttp.web.FileResponse(fspath)


@wrap_auto('GET')
async def move(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Move file or directory from any path to any path"""

    websrcpath = request.query.get('src_path', None)
    webdstpath = request.query.get('dst_path', None)

    if websrcpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid src_path',
        })

    if webdstpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid dst_path',
        })

    websrcpath = normalize_webpath(websrcpath)
    webdstpath = normalize_webpath(webdstpath)

    fssrcpath = get_fspath_from_webpath(websrcpath)
    fsdstpath = get_fspath_from_webpath(webdstpath)

    # Check subdirs
    if not is_valid_subpath(fssrcpath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    if not is_valid_subpath(fsdstpath):
        return aiohttp.web.json_response({
            'error': 'invalid dst_path'
        })

    # Check existing
    if not os.path.exists(fssrcpath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    # Actually move (how?)
    try:
        os.renames(fssrcpath, fsdstpath)
    except Exception as e:
        logging.error(e, exc_info=True)
        return aiohttp.web.json_response({
            'error': 'move failed'
        })

    return aiohttp.web.json_response({
        'result': 'ok'
    })


@wrap_auto('GET')
async def delete(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Delete file or directory"""

    webpath = request.query.get('path', None)

    if webpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid src_path',
        })

    webpath = normalize_webpath(webpath)

    fspath = get_fspath_from_webpath(webpath)

    # Check subdirs
    if not is_valid_subpath(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    # Check existing
    if not os.path.exists(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid src_path'
        })

    # Actually move (how?)
    try:
        if os.path.isdir(fspath):
            shutil.rmtree(fspath)
        else:
            os.remove(fspath)
    except Exception as e:
        logging.error(e, exc_info=True)
        return aiohttp.web.json_response({
            'error': 'delete failed'
        })

    return aiohttp.web.json_response({
        'result': 'ok'
    })


FS_NODE_TEST_RE = re.compile(r'^(?!^(?:PRN|AUX|CLOCK\$|NUL|CON|COM\d|LPT\d)(?:\..+)?$)(?:\.*?(?!\.))[^\x00-\x1f\\?*:\";|\/<>]+(?<![\s.])$')

@wrap_auto('GET')
async def mkdir(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Create directory"""

    webpath = request.query.get('path', None)
    name = request.query.get('name', None)

    if webpath is None:
        return aiohttp.web.json_response({
            'error': 'invalid path',
        })

    if not FS_NODE_TEST_RE.match(name):
        return aiohttp.web.json_response({
            'error': 'invalid name',
        })

    webpath = normalize_webpath(webpath)

    fspath = get_fspath_from_webpath(webpath)

    # Check subdirs
    if not is_valid_subpath(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    # Check existing
    if not os.path.exists(fspath):
        return aiohttp.web.json_response({
            'error': 'invalid path'
        })

    # Actually move (how?)
    try:
        os.makedirs(os.path.join(fspath, name))
    except Exception as e:
        logging.error(e, exc_info=True)
        return aiohttp.web.json_response({
            'error': 'delete failed'
        })

    return aiohttp.web.json_response({
        'result': 'ok'
    })


@wrap_auto('POST')
async def upload(request: aiohttp.web.Request) -> aiohttp.web.Response:
    """Upload file in given directory"""

    webpath = request.query.get('path', None)

    if webpath is None:
        raise aiohttp.web.HTTPBadRequest()

    webpath = normalize_webpath(webpath)

    fspath = get_fspath_from_webpath(webpath)

    # Check subdirs
    if not is_valid_subpath(fspath):
        raise aiohttp.web.HTTPBadRequest()

    # Check existing
    if not os.path.exists(fspath):
        raise aiohttp.web.HTTPBadRequest()

    # Form iterator
    try:
        reader = await request.multipart()

        field = None
        while not reader.at_eof():
            local_field = await reader.next()
            if local_field.name == 'file':
                field = local_field
                break
    except Exception as e:
        logging.error(e, exc_info=True)
        raise aiohttp.web.HTTPInternalServerError()

    # Field check
    if field is None:
        raise aiohttp.web.HTTPBadRequest()

    # File check
    filename = field.filename
    if filename is None:
        raise aiohttp.web.HTTPBadRequest()

    filename = filename.strip()
    if not filename:
        raise aiohttp.web.HTTPBadRequest()

    if not FS_NODE_TEST_RE.match(filename):
        raise aiohttp.web.HTTPBadRequest()

    fspath = os.path.join(fspath, filename)

    # Prevent duplicates
    if os.path.exists(fspath):
        raise aiohttp.web.HTTPBadRequest()

    # Receive
    try:
        with open(fspath, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)

        return aiohttp.web.Response()
    except Exception as e:
        logging.error(e, exc_info=True)
        try:
            os.remove(fspath)
        except:
            pass

        raise aiohttp.web.HTTPInternalServerError()
