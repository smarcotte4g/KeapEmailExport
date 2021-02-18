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
    amt = len(FILE_IDS)
    file = pathlib.Path("output/{}_emails/exported.log".format(appname))
    if file.exists():
        with open("output/{}_emails/exported.log".format(appname), "r") as export:
            for lines in export:
                exportlist.append(int(lines.strip('\n')))

        for id in FILE_IDS:
            if id not in exportlist:
                count += 1
                try_export(appname, id, count, amt)
                #try:
                #    with open("output/{}_emails/email_{}.html".format(appname, id), "w", encoding="utf-8") as f:
                #        string = infusionsoft.FileService('getFile', id)
                #        f.write(base64.b64decode(string).decode('utf-8'))

                #    print(f'{count}/{amt}')
                #    print("This is the current File ID: {}".format(id))
                #    with open("output/{}_emails/exported.log".format(appname), "a", encoding="utf-8") as gf:
                #        gf.write("{}\n".format(id))
                #except Exception as e:
                #    with open("output/{}_emails/errors.log".format(appname), "a", encoding="utf-8") as ef:
                #        ef.write('Exception: %s' % e)
                #        ef.write("\n!!ERROR ON ID: {}\n".format(id))
                #        if os.path.exists("output/{}_emails/email_{}.html".format(appname, id)):
                #            os.remove("output/{}_emails/email_{}.html".format(appname, id))
                #    print(f'{count}/{amt}')
                #    print("!!ERROR ON ID: {}".format(id))
            else:
                count += 1
                if os.path.exists("output/{}_emails/email_{}.html".format(appname, id)):
                    print(f'{count}/{amt}')
                    print("ID Already Exported: {}".format(id))
                else:
                    try_export(appname, id, count, amt)
                continue
    else:
        for id in FILE_IDS:
            count += 1
            try_export(appname, id, count, amt)
            #try:
            #    with open("output/{}_emails/email_{}.html".format(appname, id), "w", encoding="utf-8") as f:
            #        string = infusionsoft.FileService('getFile', id)
            #        f.write(base64.b64decode(string).decode('utf-8'))

            #    print(f'{count}/{amt}')
            #    print("This is the current File ID: {}".format(id))
            #    with open("output/{}_emails/exported.log".format(appname), "a", encoding="utf-8") as gf:
            #        gf.write("{}\n".format(id))
            #except Exception as e:
            #    with open("output/{}_emails/errors.log".format(appname), "a", encoding="utf-8") as ef:
            #        ef.write('Exception: %s' % e)
            #        ef.write("\n!!ERROR ON ID: {}\n".format(id))
                
            #    print("!!ERROR ON ID: {}".format(id))

    # Adds all emails to a ZIP file
    file = zipfile.ZipFile("output/{}_emails.zip".format(appname), "w")

    for name in glob.glob("output/{}_emails/*".format(appname)):
        file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)

    # Deletes the individual email files, leaving only the ZIP as output
    dirpath = os.path.join("output", "{}_emails".format(appname))
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    print('Export Completed and Zipped.')

def try_export(appname, id, count, amt):
    try:
        with open("output/{}_emails/email_{}.html".format(appname, id), "w", encoding="utf-8") as f:
            string = infusionsoft.FileService('getFile', id)
            f.write(base64.b64decode(string).decode('utf-8'))

        print(f'{count}/{amt}')
        print("This is the current File ID: {}".format(id))
        with open("output/{}_emails/exported.log".format(appname), "a", encoding="utf-8") as gf:
            gf.write("{}\n".format(id))
    except Exception as e:
        with open("output/{}_emails/errors.log".format(appname), "a", encoding="utf-8") as ef:
            ef.write('Exception: %s' % e)
            ef.write("\n!!ERROR ON ID: {}\n".format(id))
            if os.path.exists("output/{}_emails/email_{}.html".format(appname, id)):
                os.remove("output/{}_emails/email_{}.html".format(appname, id))
        print(f'{count}/{amt}')
        print("!!ERROR ON ID: {}".format(id))

if __name__=="__main__":
    main()