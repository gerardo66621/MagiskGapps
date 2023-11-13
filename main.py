import os
import json
import shutil
import zipfile
import fnmatch
import pysftp
import subprocess

with open('module-info.json') as f:
    contents = json.load(f)
id = contents['result']['id']
name = contents['result']['name']
version = contents['result']['version']
versionCode = contents['result']['versionCode']
author = contents['result']['author']
description = contents['result']['description']
SF_folder = contents['result']['SF_folder']
SF_version = contents['result']['SF_version']
SF_user = contents['result']['SF_user']
SF_pass = contents['result']['SF_pass']

# Create module.prop
with open('template/module.prop', 'w') as f:
    f.write('id=' + id +"\n" + 'name=' + name +"\n" + 'version=' + version +"\n" + 'versionCode=' + versionCode +"\n" + 'author=' + author +"\n" + 'description=' + description)

# Unzip and move AppSet files
with zipfile.ZipFile("gapps.zip", 'r') as zip_ref:
    zip_ref.extractall("gapps")
os.mkdir("AppSet")

rootPath = r"gapps/AppSet"
pattern = '*.zip'
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        print("Moving " + os.path.join(root, filename))
        zipfile.ZipFile(os.path.join(root, filename)).extractall(os.path.join("appset/"))
        os.remove("appset/installer.sh")
os.remove("appset/uninstaller.sh")
print("Moving files")

# Renames Files from ___ to /
path = "appset"
os.chmod(path, 0o777)
filenames = os.listdir(path)
for filename in filenames:
    src_file = os.path.join(path, filename)
    dst_file = 'appset\\' + filename.replace('___', '\\')
    print(f"Renaming {src_file} to {dst_file}")
    shutil.move(src_file, dst_file)

# Combines everything
source_folder = r"template"
destination_folder = r"builds"
shutil.copytree(source_folder, destination_folder)

source_folder = r"appset"
destination_folder = r"builds/system"
shutil.copytree(source_folder, destination_folder)
print("Building Module")

shutil.make_archive("releases/MagiskGApps-"+ version, 'zip', "builds")
print("Building Zip and archiving")
os.chmod("gapps", 0o777)
os.chmod("builds", 0o777)
os.chmod("AppSet", 0o777)

shutil.rmtree("gapps", ignore_errors=True)
shutil.rmtree("builds", ignore_errors=True)
os.remove("template/module.prop")
os.remove("gapps.zip")
shutil.rmtree("AppSet", ignore_errors=True)


# Closes the connection
srv.close()
