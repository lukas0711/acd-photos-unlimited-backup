[![license-badge][]][license-link] [![stars-badge][]][star-link] [![issues-badge][]][issues-link] [![maintenance-badge]][maintenance-link]


# acd-photos-unlimited-backup

Unlimited cloud storage and backup off all filetypes with Amazon Prime Photos:

This script creates AES encrypted multi volume .7z files hidden behind 
.jpg files from every folder in a specified input directory. The .jpg files can be uploaded to Amazon Photos with a Prime subscription to get unlimited storage for every filetype, not just pictures. Every created picture has a size of 100 Mb.  
The folder names get encrypted with BASE64.  

## Installation
Install all python package requirements through the pip command:  
``pip install -r requirements.txt``

Further you need to have [7zip](https://7-zip.org/) installed and the installation path needs to be included in the environment variables.

So the requirements are
```
alive-progress
Pillow
7zip
```

## Configuration

For the encryption function specify the input and output path. The output path should be included in the directories that are synchonized by the [Amazon Photos App for Windows](https://www.amazon.com/b?node=16384500011).

```python
dir_input = "C:\\In"
dir_output = "C:\\Out\\"
```

For the decryption function specify the input path. The encrypted JPG files get replaced with the decrypted and extracted files.
```python
dir_input = "C:\\Out\\"
```

The password of the containers can be changed with the tag
```python
"-p{}".format("password"),
```

## Contribute

Welcome through the Github stream.

[license-badge]:        https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square
[license-link]:         https://choosealicense.com/licenses/mit/
[stars-badge]:          https://img.shields.io/github/stars/lukas0711/acd-photos-unlimited-backup?style=flat-square
[star-link]:            https://github.com/lukas0711/acd-photos-unlimited-backup/
[issues-badge]:         https://img.shields.io/github/issues/lukas0711/acd-photos-unlimited-backup?style=flat-square
[issues-link]:          https://github.com/lukas0711/acd-photos-unlimited-backup/issues/
[maintenance-badge]:    https://img.shields.io/maintenance/yes/2021?style=flat-square
[maintenance-link]:     https://github.com/lukas0711/acd-photos-unlimited-backup/graphs/commit-activity