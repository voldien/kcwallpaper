# kcwallpaper #
---
[![Travis Build Status](https://travis-ci.org/voldien/kcwallpaper.svg?branch=master)](https://travis-ci.org/voldien/kcwallpaper)
The *kcwallpaper* program is a wallpaper/slide show program for displaying images from [konachan.net](https://konachan.net) (Anime/Manga). It can be configured for alter the behaviour of the program, such as time between image swap, using only local cache, don't cache, search tag and etc.

The *kcwallpaper* program was written towards *python2.7*. However, *python3.5* is in progress for adding support for .

## Features ##
* Caching - The downloaded content can be cached for next time displaying the same image, This is done with *SQL* and a directory storing the images.
* Configurable - The settings for the application can be configured with the *kcw.conf* file.
* Override Options - The settings of the program can be altered with the short and long options in the *command line*.
* SSL - The program can run with *SSL*/*TLS* in order to creating a secure connections between the server and the client over HTTP.
* AutoComplete - The program support bash autocomplete for the program's command options, including tag autocomplete *iff* the *konachan* query program is install on the system.


*kcwallpaper* depends on two other program. These are the [konachan](https://github.com/voldien/konachan) and [swp](https://github.com/voldien/swp) program (see more [here](#Dependencies) to install them). Firstly is the *konachan* program, that is a query tool written *c*. Its responsibility is to query information from [konachan.net](https://konachan.net). Whereas the *swp* is a small wallpaper program, that is also written in *c*. Its responsibility is to display images with effects. It usage a *FIFO* for receiving image files for displaying. Where the *kcwallpaper* simply writes the image files to this *FIFO* file. Where the *swp* gets an interrupt that in succession loads the images and transfers them to the GPU by using *OpenGL*.

# Motivation #
The motivation of this project is in order to create a light-weight image slide show for *Anime/Manga* related images. Where it can cache the images and meta data associated with the images in order to increase the overall performance. This is by reusing the image if already stored on the local storage device. In addition to be able start the program easily from the command line with little effort as possible. As well for adding support for customize the execution of the program with using the configuration file.

# Installation #
The following section cover how to install the *kcwallpaper* program onto the system using either the *GNU make* or the *python* binary. The *make* can only be used for UNIX based system. Whereas the python approach can be installed on any platform that supports *python*. However, it requires the *python-setuptools* package to be installed on the system, prior to the installation of the *kcwallpaper* program.

## GNU Make - UNIX only ##
The program can be easily be installed by invoking the following command:
```
make install
```
The make file prompt a question if you wish to run the SQL init code for creating the tables, database. This is used for adding support for *caching* feature. However, this is optionally and its only needed when using the *MySQL* implementation. Otherwise the *SQLite* implementation will handle this on its own.

## Install via Python ##
The following command will install the python dependencies and install the *kcw* module and create a program called *kcwallpaper*. Where the *kcwallpaper* will call the main function in the *kcw* module.
```
python setup.py install
```

# Usage #

Once the program has been installed successfully. The program can be invoked with the following command:
```bash
kcwallpaper
```
This will start the kcwallpaper program with its default options.

The options in the kcw.conf file can be override with the command line options, see for the following example:
```bash
kcwallpaper -t "cat"
```
This will override the search tag cat. Remark that each search tag will be split between a white-space, which can be give different result. Example the tag 'short hair', if typed with the white-space between the words, this will make the program believe they are two distinguishable tags, *short* and *hair*, which would give result of hair and short and not *short-hair*. Fortunately this is solved by typing an understand score between the words. so the short hair we saw would become *short_hair*, see following example:
```bash
kcwallpaper -t "short_hair cat"
```

# Contributing #
Please read the [CONTRIBUTING](CONTRIBUTING.md) for more details of how you can contribute.

# Dependencies #
The following section cover the dependencies for Linux distributions, using the Debian package system.

In order to run the program, the following Debian packages are required:
```bash
apt-get install python2.7 python-mysql.connector python-sqlite
```
In order to make the caching feature work the following Debian packages is needed:
```bash
apt-get install mysql-server sqlite3
```

## Sub Program Dependencies ##

The *kcwallpaper* has two additional program dependencies as mention in the first section, because they are not yet available as *Debian* packages. This can however be resolved easily be invoking the following command. Where git will clone the *swp* and *konachan* git repository to the current repository, see following command:
```
git submodule update
```
Where the program can either be installed by following instruction for both of the git repository individually. Otherwise the program can be easily be installed by using the following command:
```
make install_dep
```
The command will invoked the make in both *swp* and *konachan*.

# License #
This project is licensed under the GPL+3 License - see the [LICENSE](LICENSE) file for details.

