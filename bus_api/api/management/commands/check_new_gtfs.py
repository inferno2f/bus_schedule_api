import logging
import os
import urllib.request
import zipfile
from datetime import datetime as dt

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from imap_tools import MailBox

PASSWORD = os.getenv("EMAIL_PASSWORD")
LOGIN = os.getenv("EMAIL_ADDRESS")
SUBJECT = "New NJ TRANSIT GTFS Data Available"
NJ_TRANSIT_URL = "https://www.njtransit.com/bus_data.zip"

logger = logging.getLogger(__name__)


def check_new_data():
    """
    Check if email notification about updated data has been received
    """
    with MailBox("imap.gmail.com").login(LOGIN, PASSWORD) as mailbox:
        for msg in mailbox.fetch():
            if msg.subject.lower() == SUBJECT.lower() and dt.today().date() == msg.date.date():
                logger.info(f"New data notification: {dt.today()}")
                fetch_new_data()
                return
        logger.info(f"Daily data update check completed: {dt.today()}")
        return


def fetch_new_data():
    """
    Fetch zip file from NJ Transit and unzip it
    """
    logger.info("Fetching new data...")
    fetched_data, _ = urllib.request.urlretrieve(NJ_TRANSIT_URL)
    archive = zipfile.ZipFile(fetched_data, "r")
    logger.info("Extracting archive...")
    archive.extractall(f"{settings.BASE_DIR}/static")
    archive.close()
    logger.info("New GTFS data files saved")
    call_command("gtfs_parser")
    return


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        check_new_data()
