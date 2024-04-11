import os
import urllib.request
import zipfile
from datetime import datetime as dt

from django.core.management.base import BaseCommand
from django.conf import settings
from imap_tools import MailBox

PASSWORD = os.getenv("EMAIL_PASSWORD")
LOGIN = os.getenv("EMAIL_ADDRESS")
SUBJECT = "New NJ TRANSIT GTFS Data Available"
NJ_TRANSIT_URL = "https://www.njtransit.com/bus_data.zip"


def check_new_data():
    """
    Check if email notification about updated data has been received
    """
    with MailBox("imap.gmail.com").login(LOGIN, PASSWORD) as mailbox:
        for msg in mailbox.fetch():
            if msg.subject.lower() == SUBJECT.lower() and dt.today().date() == msg.date.date():
                print(f"New data notification: {dt.today()}")
                fetch_new_data()


def fetch_new_data():
    """
    Fetch zip file from NJ Transit and unzip it
    """
    print("Fetching new data...")
    fetched_data, _ = urllib.request.urlretrieve(NJ_TRANSIT_URL)
    archive = zipfile.ZipFile(fetched_data, "r")
    print("Extracting archive...")
    archive.extractall(f"{settings.BASE_DIR}/static")
    archive.close()
    print("New GTFS data files saved")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        check_new_data()
