# -*- encoding: utf-8 -*-
"""
AddressBase Basic downloader class
"""

import logging
import ftplib
import os

from .filesystem import LocalCache
from .ftp import FtpDownloader
from .s3 import S3Cache


log = logging.getLogger(__name__)


class AddressBaseBasicDownloader(LocalCache, S3Cache, FtpDownloader):

    """
    Ordnance Survey remove the files from the download directory after 21 days,
    so we cache the files on Amazon S3 in case we need them after that time.
    """

    def __init__(self):
        if 'OS_FTP_USERNAME' not in os.environ:
            log.error('OS_FTP_USERNAME not set!')

        if 'OS_FTP_PASSWORD' not in os.environ:
            log.error('OS_FTP_PASSWORD not set!')

        super(AddressBaseBasicDownloader, self).__init__(
            'osmmftp.os.uk',
            os.environ.get('OS_FTP_USERNAME'),
            os.environ.get('OS_FTP_PASSWORD'),
            path=self.find_dir_with_latest_full_file())

    def download(self, dest_dir=None):
        """
        Execute the download.
        Returns a list of downloaded files.
        """

        return super(AddressBaseBasicDownloader, self).download(
            '*_csv.zip', dest_dir)

    # Ordnance Survey's update mechanism creates a *new* order number
    # for every update, so we cannot predict ahead of time what the
    # directory path will be.
    # So we work it out as follows:
    # - the files are all called AddressBase_FULL_YYYY-MM-DD_NNN_csv.zip
    # - get ALL the files matching that pattern in all the subidrectories
    # - split into path / filename
    # - sort by filename
    # - the last file should be the latest, so use the directory containing it
    def find_dir_with_latest_full_file(self):
        # have to create new object rather than exploiting the
        # inheritance heirarchy, as this method is called during
        # initialisation
        tmp_ftp = FtpDownloader('osmmftp.os.uk',
            os.environ.get('OS_FTP_USERNAME'),
            os.environ.get('OS_FTP_PASSWORD'),
            '../from-os/')
        # full_files = tmp_ftp._list('*/AddressBase_FULL_*')
        # parsed_file_list = map(lambda fname: {'dir': fname.split(
        #     '/')[0], 'file': fname.split('/')[-1]}, full_files)
        # latest = sorted(parsed_file_list, key=lambda key: key['file'])[-1]

        latest = tmp_ftp.find_dir_with_latest_file_matching('*/AddressBase_FULL_*')
        if latest:
            return latest['dir']
