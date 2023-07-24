import json
import logging

from csv_extract import read_file
from rules import check_duplicates, check_entries
from synapse_client import SynapseClient

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def do_import_users(csv_file_path, dry_run):
    logging.info("Importing users from " + csv_file_path + "...")

    entries = read_file(csv_file_path)

    logging.info("file read. Checking content...")
    check_duplicates(entries)
    check_entries(entries)

    logging.info("Connect to Synapse...")
    mx_client = SynapseClient()
    if not dry_run:
        for entry in entries:
            mx_client.create_user(entry["username"], entry["display_name"], entry["email"])
    else:
        logging.info("Dry run")
    
    logging.info("The end, bye!")

def do_get_users():
    client = SynapseClient()
    users = client.get_users()
    print(json.dumps(users, indent=2, sort_keys=True))

def do_get_user(userId):
    client = SynapseClient()
    user = client.get_user(userId)
    print(json.dumps(user, indent=2, sort_keys=True))