# kcwallpaper #
---
The *kcwallpaper* program is a wallpaper/slide show program for displaying images from [konachan.net](https://konachan.net) (Anime/Manga). It can be configured for alter the behavior the program, such as time between image swap, using only local cache, don't cache and search tag.

The *kcwallpaper* program was written for *python2.7* and in progress for adding support for python3.5.

## Features ##
* Caching - The downloaded content can be cached for next time displaying the same image, This is done with *SQL*.
* Configurable - The settings for the application can be configured with the *kcw.conf* file.
* Override Options - The settings of the program can be altered with the short and long options.
* SSL - The program can run with *SSL*/*TLS* in order to creating a secure connections between the server and the client over HTTP.
* AutoComplete - The program support bash autocomplete for program options including tag autocomplete *iff* the *konachan* query program is install on the system.


The *kcwallpaper* is dependent on two program. These are the [konachan](https://github.com/voldien/konachan) and [swp](https://github.com/voldien/swp)  program (see more [here](#Dependencies) to install them). Where the *konachan* program is a query tool written *c*. Where its responsibility is to query information from [konachan.net](https://konachan.net). Whereas the *swp* is a small wallpaper program also written in *c*. Where its responsibility is to display the images. It usage a *FIFO* file, where the *kcwallpaper* simply write the image file to this *FIFO* file. Where the *swp* get an interrupt which in succession loads the image and transfer it to the GPU by using *OpenGL*.

# Motivation #
The motivation of this project is in order to create a light-weight image slide show for *Anime/Manga* related images. Where it can cache the images and meta data associated with the images in order to increase the overall performance. This is by reusing the image if already located on the local storage device.

The motivation of the project is to be able start the program from the command line easily with little effort as possible.

# Installation #
The following section cover how the install the *kcwallpaper* program onto the system using either the *GNU make*. The make can only be used for UNIX based system. Whereas the python approach can be installed on any platform that supports *python*. However it requires the ** to be installed on the system prior to installing the *kcwallpaper*.

## GNU Make - UNIX only ##
The program can be easily be installed by invoking the following command.
```
make install
```
The make file prompt a question if you wish to run the SQL init code for creating the tables, database. This for adding support for caching feature. This is however optionally and its only when using *MySQL*, the *SQLite* implementation will handle this on its own.

## Install via Python ##
The following command will install the python dependencies and install the *kcw* module and create a program called *kcwallpaper*. Where the *kcwallpaper* will call the main function in the *kcw* module.
```
python setup.py install
```

# Usage #

Once the program has been installed successfully. The program can be invoked with the following command.
```bash
kcwallpaper
```
This will start the kcwallpaper program with its default options.

The options in the kcw.conf file can be override with the command line options, see for the following example.
```bash
kcwallpaper -t "cat"
```
This will override the search tag cat. Remark that each search tag will be split between a whitespace. Which can be give different result. Example the tag 'short hair', if typed with the whitespace between the words will make the program believe they're two tags, short and hair. This is although solved by typing an understand score between the words. so the short hair would become 'short_hair'. See following example.
```bash
kcwallpaper -t "short_hair cat"
```

# Contributing #
Please read the [CONTRIBUTING](CONTRIBUTING.md) for more details of how you can contribute.

# Dependencies #
The following section cover the dependencies for Linux distributions using the Debian package system.

In order to run the program, the following Debian packages is required.
```bash
apt-get install python2.7 python-mysql.connector python-sqlite
```
In order to make the caching feature work the following Debian packages is needed.
```bash
apt-get install mysql-server
```

# License #
This project is licensed under the GPL+3 License - see the [LICENSE](LICENSE) file for details.

