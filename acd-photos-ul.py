"""
This script returns AES encrypted multi volume .7z files hidden behind 
.jpg files. The .jpg files can be uploaded to Amazon Prime Photos to 
get unlimited storage for every filetype, not just pictures.

There are two program parts:
1. Encryption of a chosen directory.
2. Decryption of a chosen directory.
"""


import argparse
import base64
import csv
import os
import shutil
import subprocess
import time
from datetime import datetime
from subprocess import SubprocessError

from alive_progress import alive_bar
from PIL import Image


log_path = os.path.join(os.getcwd(), "Encryption_log.csv")


def b64_encoder(folder_name):
    """Encode a string in base64 and return base64 string."""
    folder_bytes = folder_name.encode("ascii")
    folder_base64 = base64.b64encode(folder_bytes)
    folder_encode = folder_base64.decode("ascii")
    return folder_encode


def b64_decoder(folder_name):
    """Decode a base64 string and return decoded string."""
    return base64.b64decode(folder_name.encode("ascii")).decode("ascii")


def folder_creator(path):
    """Create a folder with given path if it doesn't exists."""
    if not os.path.exists(path):
        os.makedirs(path)


def folder_clear(path):
    """Delete all files in a given folder"""
    for element in os.scandir(path):
        os.remove(element)


def log_find_folder(folder_search_name):
    """Returns True if the search_string is found in the Encryption_log.csv"""
    answer = False
    if os.path.exists(log_path):
        with open(log_path, "r") as f_log:
            f_log_reader = csv.reader(f_log, delimiter=";")
            for row in f_log_reader:
                if folder_search_name == row[1]:
                    answer = True
    return answer


def log_write_folder(folder_write_name, folder_encode_name):
    """Write the processed folder name to the Encryption_log.csv to know whether it has been processed"""
    with open(log_path, "a", newline="") as f_log:
        f_log_writer = csv.writer(f_log, delimiter=";")
        f_log_writer.writerow(
            [
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                folder_write_name,
                folder_encode_name,
            ]
        )


def jpg_encrypt(dir_input, dir_output, zip_pass, archive_flag):
    """
    Encrypt all folders in defined input path in .7z containers and hide
    them behind .jpg files.
    """

    dir_temporary = os.sep.join([dir_output, "temp"])
    folder_creator(dir_output)
    folder_creator(dir_temporary)
    folder_clear(dir_temporary)
    dir_picture = os.sep.join([dir_output, "key.jpg"])
    img = Image.new("RGB", (100, 100), color="white")
    img.save(dir_picture)

    for folder in os.scandir(dir_input):
        # Cmd for 7z compression and AES+header encryption
        command_compress = [
            "7z",
            "a",
            "-m0=lzma",
            "-mx=9",
            "-mhe",
            "-t7z",
            "-mfb=64",
            "-md=32m",
            "-ms=on",
            "-v100m",
            # "-p{}".format("password"),
        ]
        command_compress.extend(["-p{}".format(zip_pass)])
        # Check whether the considered folder has been encrypted before (has been logged) and therefore has been backupped to Amazon Photos
        not_in_log = not log_find_folder(folder.name) if archive_flag else True
        if not_in_log:
            # Create a multi volume 7z archive from the considered folder in the temp directory
            if folder.is_dir() and folder is not None:
                try:
                    folder_encode = b64_encoder(folder.name)
                    out_path = f"{dir_temporary}{os.sep}{folder_encode}.7z"
                    command_compress.extend([out_path, folder.path + r"\*"])
                    p = subprocess.Popen(
                        command_compress,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        bufsize=1,
                        universal_newlines=True,
                    )
                    print("Compressing: Command", " ".join(command_compress))
                    print("Compressing:", folder.path, "=>", out_path)
                    command_output = ""
                    with alive_bar() as bar:
                        while p.poll() is None:
                            time.sleep(0.06)
                            bar()
                            for line in p.stdout:
                                command_output += line
                                # print(line, end="", flush=True)
                    p.wait()
                    # Check if the 7z command has finished successfully
                    if not command_output.endswith("Ok\n"):
                        raise SubprocessError
                except SubprocessError as e:
                    print("A 7z archive already exists in the directory.")
                    decision = input(
                        "Exception caught in subprocess.Popen: %s\n"
                        "Archive will not be logged in the database.\n"
                        "Just continue? [Y/n]: " % e
                    )
                    if decision.lower() == "y":
                        continue

            # Merge all multi volume 7z files in the temp directory with a blank jpg and write them to a clearname folder in the output directory
            with alive_bar(len(list(os.scandir(dir_temporary)))) as bar:
                for file in os.scandir(dir_temporary):
                    if file.is_file() and not file.name.endswith(".jpg"):
                        folder_creator(f"{dir_output}{os.sep}{folder.name}")
                        # Open the 7z file in the temp directory and add the jpg
                        with open(file.path, "rb") as f_7z:
                            with open(dir_picture, "rb") as f_jpg:
                                with open(
                                    os.sep.join(
                                        [dir_output, folder.name, file.name + ".jpg"]
                                    ),
                                    "wb",
                                ) as f_out:
                                    f_out.write(f_jpg.read())
                                    f_out.write(f_7z.read())
                    bar()
            folder_clear(dir_temporary)
            # Log the encrypted folder to the Encryption_log.csv
            if archive_flag:
                log_write_folder(folder.name, b64_encoder(folder.name))
    # Remove temporary files
    if os.path.exists(dir_picture):
        os.remove(dir_picture)
    shutil.rmtree(dir_temporary)
    print("Finished creating .jpg files")


def jpg_decrypt(dir_input, zip_pass):
    """Extract the hidden .7z files from merged .jpg files and delete the .jpg files."""

    # dir_input = "C:\\Out\\"

    # For all jpg files in the chosen directory, delete the first 823 bytes that make up the jpg to get a normal multi volume 7z archive
    for root, _, files in os.walk(dir_input):
        for file_name in files:
            if file_name.endswith(".jpg"):
                file_path = os.path.join(root, file_name)
                with open(
                    file_path,
                    "rb",
                ) as f_in:
                    # For multipart 7z the filename is everything before the . like xxxx.7z.001
                    f_encode = file_name.split(".")[0]
                    f_extension = file_name.split(".")[1]
                    f_numbering = file_name.split(".")[2]
                    with open(
                        os.path.join(
                            root,
                            b64_decoder(f_encode)
                            + "."
                            + f_extension
                            + "."
                            + f_numbering,
                        ),
                        "wb",
                    ) as f_out:
                        f_out.write(
                            f_in.read()[823:]
                        )  # 832 is the number of bytes of the inserted image
                os.remove(file_path)
    # Extract the created multi volume 7z archives to their current directory
    with alive_bar(sum([len(files) for _, _, files in os.walk(dir_input)])) as bar:
        for root, _, files in os.walk(dir_input):
            for file_name in files:
                # The first multi volume archive ends with .001 and is the start file to extract the entire archive
                if file_name.endswith(".001"):
                    command_extract = [
                        "7z",
                        "e",
                        "-y",
                        # "-p{}".format("  "),
                    ]
                    command_extract.extend(["-p{}".format(zip_pass)])
                    file_path = os.path.join(root, file_name)
                    command_extract.extend([file_path, "-o" + root + "\\"])
                    p = subprocess.Popen(
                        command_extract,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        bufsize=1,
                        universal_newlines=True,
                    )
                    p.wait()
                    os.remove(file_path)
                bar()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="acd-photos-unlimited-backup",
        epilog="Unlimited cloud storage and backup of all file types with Amazon Prime Photos. Choose between encryption and decryption.",
    )
    parser.add_argument(
        "-p",
        metavar="pass",
        default="",
        type=str,
        help='password for encryption (default="")',
    )
    parser.add_argument(
        "-a",
        "--archive",
        action="store_true",
        help="after encryption write folders to log and skip previously logged folders",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-e",
        metavar="out",
        help="encrypt all subfolders in the input folder - specify the output path",
    )
    group.add_argument(
        "-d",
        action="store_true",
        help="decrypt all .jpg archives in the input folder",
    )
    parser.add_argument("input", help="input path")
    args = parser.parse_args()

    if args.e:
        jpg_encrypt(
            os.path.normpath(args.input), os.path.normpath(args.e), args.p, args.archive
        )
    elif args.d:
        jpg_decrypt(os.path.normpath(args.input), args.p)
    else:
        print("No arguments. Closing.")