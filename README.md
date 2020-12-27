[![license-badge][]][license-link] [![stars-badge][]][star-link] [![issues-badge][]][issues-link] [![maintenance-badge]][maintenance-link]


# acd-photos-unlimited-backup

Unlimited cloud storage and backup off all filetypes with Amazon Prime Photos:

This script creates AES encrypted multi volume .7z files hidden behind 
.jpg files from every folder in a specified input directory. The .jpg files can be uploaded to Amazon Photos with a Prime subscription to get unlimited storage for every filetype, not just pictures. Every created picture has a size of 100 Mb.  
The file names get encrypted with BASE64.  

## Get it
Clone this repo and install all python package requirements through the pip command:  
```shell
pip install -r requirements.txt
```

## Additional requirements
You need to have [7zip](https://7-zip.org/) installed and the installation path needs to be included in the environment variables.

Since Amazon disabled the App registration for ACD, you need to install the offical [Amazon Photos App](https://www.amazon.com/b?node=16384500011) for uploading/downloading. The output path of the script should be included in the directories that are synchonized by the Amazon Photos App.

## Use it

```
usage: Uploader.py [-h] [-p pass] [-a] (-e out | -d) input

acd-photos-unlimited-backup

positional arguments:
  input          input path

optional arguments:
  -h, --help     show this help message and exit
  -p pass        password for encryption (default="")
  -a, --archive  after encryption write folders to log and skip previously logged folders
  -e out         encrypt all subfolders in the input folder - specify the output path
  -d             decrypt all .jpg archives in the input folder

Unlimited cloud storage and backup of all file types with Amazon Prime Photos.
Choose between encryption and decryption.
```

### Arguments
- For the encryption function (-e) specify the input and output path. The output path should be included in the directories that are synchonized by the Amazon Photos App.
- For the decryption function (-d) you only need to specify the input path. The encrypted JPG files get replaced with the decrypted and extracted files.
- The password of the archives can be changed with the -p tag.
- The --archive tag creates a log file. That way you can pause/cancel the script midway to upload large directories to ACD Photos. The log file makes sure you don't create duplicate archives that are already uploaded.

### Example
```
cd acd-photos-unlimited-backup
python acd-photos-ul.py -e C:\Out C:\In -p11 -a
```
## Contribute

Welcome through the Github workflow.

[license-badge]:        https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[license-link]:         https://choosealicense.com/licenses/mit/
[stars-badge]:          https://img.shields.io/github/stars/lukas0711/acd-photos-unlimited-backup?style=flat-square
[star-link]:            https://github.com/lukas0711/acd-photos-unlimited-backup/
[issues-badge]:         https://img.shields.io/github/issues/lukas0711/acd-photos-unlimited-backup?style=flat-square
[issues-link]:          https://github.com/lukas0711/acd-photos-unlimited-backup/issues/
[maintenance-badge]:    https://img.shields.io/maintenance/yes/2021?style=flat-square
[maintenance-link]:     https://github.com/lukas0711/acd-photos-unlimited-backup/graphs/commit-activity