# coding:utf-8

__author__ = 'xinchun.li'

import os

from werkzeug.utils import secure_filename

from config import constant
from common import config, logger
from common.decorator import error_log


diagnose = logger.get_logger(logger.DIAGNOSE)

UPLOAD_FOLDER = config.get(constant.FILE_UPLOAD_PATH)
diagnose.info("upload_folder=" + UPLOAD_FOLDER)
UPLOAD_NAME = config.get(constant.FILE_UPLOAD_NAME)
diagnose.info("upload_name=" + UPLOAD_NAME)
ALLOWED_EXTENSIONS = set(config.get(constant.UPLOAD_ALLOW_EXTS))
diagnose.info("allowed_extensions=" + str(ALLOWED_EXTENSIONS))


@error_log(False)
def allowed_file(filename):
    """

    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@error_log(False)
def upload_file(file_):
    """

    :param file_:
    :return:
    """
    if file_ and allowed_file(file_.filename):
        # filename = secure_filename(file_.filename)
        file_.save(os.path.join(UPLOAD_FOLDER, UPLOAD_NAME))
        return True
    else:
        return False


@error_log(False)
def backup_file():
    pass





