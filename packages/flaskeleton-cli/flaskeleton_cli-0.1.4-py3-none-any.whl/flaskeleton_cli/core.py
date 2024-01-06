import os

from .consts import GIT_URL


def clone_flaskeleton(path, folder: str = '') -> int:
    cmd = ''
    cmd += f'mkdir -p {str(path)}'
    cmd += f' && cd {str(path)}'
    cmd += f' && git clone {str(GIT_URL)} {folder}'
    cmd += f' && rm -rf {folder}/.git'
    return os.system(cmd)
