import os
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(__file__, '../'))
rmapi_location = os.path.join(BASE_DIR, "rmapi")
print(f"rmapi location={rmapi_location}")


def check_rmapi():
    check = subprocess.run([rmapi_location, "ls"])
    logger.info(check.stdout)
    logger.error(check.stderr)
    return check.returncode == 0


def get_files(folder):
    # Get all files from a specific folder. Output is sanitized and subfolders are excluded
    files = subprocess.run([rmapi_location, "ls", folder], capture_output=True, text=True)
    logger.info(files.stdout)
    logging.error(files.stderr)
    if files.returncode == 0:
        files_list = files.stdout.split("\n")
        files_list_new = []
        for file in files_list:
            if file[:5] != " Time" and file[:3] != "[d]" and file != "":
                files_list_new.append(file[4:])
        return files_list_new
    else:
        return False


def download_file(file_path, working_dir):
    # Downloads a file (consisting of a zip file) to a specified directory
    downloader = subprocess.run([rmapi_location, "geta", file_path], cwd=working_dir)
    logger.info(downloader.stdout)
    logger.error(downloader.stderr)
    return downloader.returncode


def get_metadata(file_path):
    # Get the file's metadata from reMarkable cloud and return it in metadata format
    metadata = subprocess.run([rmapi_location, "stat", file_path], capture_output=True, text=True)
    logger.info(metadata.stdout)
    logger.error(metadata.stderr)
    if metadata.returncode == 0:
        metadata_txt = metadata.stdout
        json_start = metadata_txt.find("{")
        json_end = metadata_txt.find("}") + 1
        metadata = json.loads(metadata_txt[json_start:json_end])
        return metadata
    else:
        return False


def upload_file(file_path, target_folder):
    # Upload a file to its destination folder
    uploader = subprocess.run([rmapi_location, "put", file_path, target_folder])
    logger.info(uploader.stdout)
    logger.error(uploader.stderr)
    return uploader.returncode == 0
