# kcwallpaper #
---
kcwallpaper is a wallpaper program for displaying images from [konachan](https://konachan.net).

###Features###
* Caching - The downloaded content can be cached for next time displaying the image.
* configurable - The settings for the application can be configured with the *kcw.conf* file.
* overridable options - Attribute of the program can be altered with short and long options.



## Installation ##
The program can be easily by invoking the following command.
```
make install
```
It will ask if you wish to run the SQL init code for creating the tables, database and user for enabling the caching feature. This is optional.


## Usage ##
--------------
Once the program has been installed successfully. The program can be invoked as followed.
```bash
kcwallpaper.py
```


## Dependencies ##
----------------
In order to run the program, the following Debian packages has to be installed.
```bash
apt-get install python2.7 python-mysql.connector
```
In order to make the caching feature work the following Debian packages is needed.
```bash
apt-get install mysql-server
```