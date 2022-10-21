#!/bin/sh

# put current date as yyyy-mm-dd in $date
date=$(date '+%Y-%m-%d')

# put date in VERSION
echo $date > VERSION

# generate the *.tar.gz package
tar -cvzf qc-antivirus-$date.tar.gz -T package_filelist.txt
