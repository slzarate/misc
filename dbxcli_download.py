#!/usr/bin/env python
""""This script allows users to download entire folders from their Dropbox account using the Dropbox
CLI. You need to be logged in locally into your Dropbox account using the CLI. For more info,
please refer to the GitHub repo: https://github.com/dropbox/dbxcli

NOTE: Assumes that the DBXCLI binary is in ./dbx (named dbx in the current working directory).
Change location/name appropriately.
"""

import os
import sys
import subprocess
import argparse

def run_cmd(cmd, return_output=False):
    """Run a shell command."""
    print cmd
    if return_output:
        output = subprocess.check_output(cmd, shell=True, executable='/bin/bash').strip()
        return output
    else:
        subprocess.check_call(cmd, shell=True, executable='/bin/bash')

def download_one_file(folder_name, file_path, preserve_capitals):
    """Download one file from your Dropbox account."""
    if folder_name:
        if not os.path.isdir(folder_name):
            if preserve_capitals == "false":
                os.makedirs(folder_name.lower())
            else:
                os.makedirs(folder_name)
    print "Getting file {0}".format(file_path)
    if preserve_capitals == "false":
        run_cmd("./dbx get \"{0}\" \"{1}\"".format(file_path, file_path.lower()))
    else:
        run_cmd("./dbx get \"{0}\" \"{0}\"".format(file_path))

def recurse_download(folder_name, file_list, preserve_capitals):
    """Recursively crawl through nested folders in your Dropbox account."""
    ls_output = run_cmd("./dbx ls \"{0}\"".format(folder_name), True)
    list_of_items = ls_output.split("  ")
    # If only one item has been requested:
    if len(list_of_items) == 1 and folder_name.split('/')[-1] == list_of_items[0]:
        file_path = folder_name # the full file path has already been provided
        folder_split = folder_name.split('/')
        folder_name = '/'.join(folder_split[:-1]) # get name of folder containing item
        download_one_file(folder_name, file_path, preserve_capitals)
        if preserve_capitals == "false":
            file_path = file_path.lower()
            folder_name = folder_name.lower()
        file_list[file_path] = folder_name
    # If a folder has been requested:
    else:
        for item in list_of_items:
            if item:
                item = item.strip()
                file_path = "{0}/{1}".format(folder_name, item)
                ls_output = run_cmd("./dbx ls \"{0}\"".format(file_path), True)
                if item != ls_output: # item is folder, go into that folder
                    file_list = recurse_download(file_path, file_list, preserve_capitals)
                else: #item is file
                    download_one_file(folder_name, file_path, preserve_capitals)
                    if preserve_capitals == "false":
                        file_path = file_path.lower()
                        folder_name = folder_name.lower()
                    file_list[file_path] = folder_name
    return file_list

def main():
    """Recursively downloads contents of specified folder name."""
    parser = argparse.ArgumentParser()
    parser.add_argument("folder_name", type=str, help="the folder from which you want to download")
    parser.add_argument("-c", "--preserve_capitals", help="preserve files\' and folders\' \
                capitalization as how they were in your Dropbox folder. WARNING: Some operating \
                systems do not distinguish between upper- and lowercase. May lead to overwriting \
                files", action="store_true")
    args = parser.parse_args()
    print "Accessing folder {0}".format(args.folder_name)

    file_list = {}
    file_list = recurse_download(args.folder_name, file_list, args.preserve_capitals)
    print "Files downloaded"

main()
