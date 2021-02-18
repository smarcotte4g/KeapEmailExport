"""
This program exports all email history items and puts them into a zipfile
that's found in the '/output' folder.
"""

from file_ids import FILE_IDS

from infusionsoft.library import Infusionsoft

import zipfile
import glob
import base64
import os
import shutil
import pathlib
import re

import time

# Initiation
appname = ''
api_key = ''

infusionsoft = Infusionsoft(appname, api_key)

def main():
    file_path = "output/{}_emails/".format(appname)

    os.makedirs(file_path, exist_ok=True)

    # Gets all files from FileBox that have been given through the SQL
    # query from above, and writes all of the files individually
    count = 0
    exportlist = []

    # Get how many are going to export
    amt = len(FILE_IDS)
    file = pathlib.Path("output/{}_emails/exported.log".format(appname))

    # Check to see if any emails have been exported
    if file.exists():
        with open("output/{}_emails/exported.log".format(appname), "r") as export:
            for lines in export:
                # Put exported Id's into a list
                exportlist.append(int(lines.strip('\n')))

        # Get the First Id in file_ids.py
        for id in FILE_IDS:
            # Check if the Id matches what is already exported
            if id not in exportlist:
                # Add to Count for output
                count += 1
                # Run Export Function
                try_export(appname, id, count, amt)

            # If the Id has been exported
            else:
                # Still Count the Id from the list
                count += 1
                # Check to see if the html file was created even though the Id is on the list
                if os.path.exists("output/{}_emails/email_{}.html".format(appname, id)):
                    print(f'{count}/{amt}')
                    print("ID Already Exported: {}".format(id))
                else:
                    # Run Export Function if missing but on export list
                    try_export(appname, id, count, amt)
                continue

    # If no export file then export
    else:
        for id in FILE_IDS:
            count += 1
            try_export(appname, id, count, amt)

    # Adds all emails to a ZIP file
    file = zipfile.ZipFile("output/{}_emails.zip".format(appname), "w")

    for name in glob.glob("output/{}_emails/*".format(appname)):
        file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)

    # Deletes the individual email files, leaving only the ZIP as output
    dirpath = os.path.join("output", "{}_emails".format(appname))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    print('Export Completed and Zipped.')

# Export files
def try_export(appname, id, count, amt):
    try:
        # Try to actually use IS API to export file
        with open("output/{}_emails/email_{}.html".format(appname, id), "w", encoding="utf-8") as f:
            string = infusionsoft.FileService('getFile', id)
            f.write(base64.b64decode(string).decode('utf-8'))

        print(f'{count}/{amt}')
        print("This is the current File ID: {}".format(id))

        # Write the exported ID to the export file if crash
        with open("output/{}_emails/exported.log".format(appname), "a", encoding="utf-8") as gf:
            gf.write("{}\n".format(id))
    except Exception as e:
        # Write the Error and Id to a log file
        with open("output/{}_emails/errors.log".format(appname), "a", encoding="utf-8") as ef:
            ef.write('Exception: %s' % e)
            ef.write("\n!!ERROR ON ID: {}\n".format(id))
            # The try writes to a file anyway with error so delete it
            if os.path.exists("output/{}_emails/email_{}.html".format(appname, id)):
                os.remove("output/{}_emails/email_{}.html".format(appname, id))
        print(f'{count}/{amt}')
        print("!!ERROR ON ID: {}".format(id))

if __name__=="__main__":
    main()