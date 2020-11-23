import os
import shutil
import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def create_tmp_dir():
    """ create a temporary directory to save the compressed image """

    # get `tmp` directory
    temp_folder = os.path.join(settings.MEDIA_ROOT, 'tmp')

    # if does not exist, create one
    if not os.path.isdir(temp_folder):
        os.mkdir(temp_folder)
        logger.info(_('%s - directory is created' % temp_folder))

    return temp_folder


def remove_tmp_dir(directory):
    """ remove the given directory """

    try:
        shutil.rmtree(directory)
        logger.info(_(
            '%s - directory is removed with its files and folders' % directory
        ))

    except OSError as e:
        logger.error("Error: %s : %s" % (directory, e.strerror))
