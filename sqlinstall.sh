#!/bin/bash
#
# SCRIPT: MySQL table install and setup.
# AUTHOR: Valdemar Lindberg
# DATE: 10/03/2017
# REV: 1.0
#
# PLATFORM: Not platform dependent.
#
# PURPOSE: Easy installation of mysql tables and creation of user
# to only modify the data table associated with the kcwallpaper.
#
# set -n
# Uncomment to check script syntax, without execution.
#
# NOTE: Do not forget to put the comment back in or
#
# the shell script will not execute!
# set -x
# Uncomment to debug this shell script
#


echo -ne "Do you want to install mysql cache server for konachan wallpaper [y|N].\n>"
read ans

if [ "$ans" == "n" ]  || [ "$ans" == "N" ] || [ "$ans" == "No" ] || [ -z "$ans"] ; then
	exit 0
fi

mysql -u root -p < init.sql
