import os

from datetime import datetime as dt
from django.core.management.base import BaseCommand
from imap_tools import MailBox

PASSWORD = os.getenv("EMAIL_PASSWORD")
LOGIN = os.getenv("EMAIL_ADDRESS")
SUBJECT = "New NJ TRANSIT GTFS Data Available"
NJ_TRANSIT_URL = "https://www.njtransit.com/bus_data.zip"


def check_email():
    with MailBox('imap.gmail.com').login(LOGIN, PASSWORD) as mailbox:
        for msg in mailbox.fetch():
            if msg.subject.lower() == SUBJECT.lower() and dt.today().date() == msg.date.date():
                print("New GTFS data received")
                break
            print("new email")


def fetch_new_data():
    pass


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        check_email()
