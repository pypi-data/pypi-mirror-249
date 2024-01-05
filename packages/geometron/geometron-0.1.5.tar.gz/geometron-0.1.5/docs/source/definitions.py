from pathlib import Path
from subprocess import check_output

def get_version():
    cmd = ['git', 'describe', '--tags', '--abbrev=0']
    output = check_output(cmd)
    return output.decode('latin1').strip()
    
def get_release():
    cmd = ['git', 'describe', '--tags']
    output = check_output(cmd)
    return output.decode('latin1').strip()

PROJECT = u'geometron'
AUTHOR = u'O. KAUFMANN'
VERSION = get_version()
RELEASE = get_release()
LICENSE = u'GPLv3'
SHORT_DESCRIPTION = u'Geometron is a bundle of tools to manipulate and display objects in 2D and 3D.'
ROOT_DIR = Path(__file__).parent.absolute()
URL = u'https://gfa-gitlab.umons.ac.be/kaufmanno' + f'/{PROJECT}'
