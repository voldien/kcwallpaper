# kcwallpaper #
---
kcwallpaper is a wallpaper/slideshow program for displaying images from [konachan](https://konachan.net). It can be configured for what kind of behaviour the program should be running. 

## Features ##
* Caching - The downloaded content can be cached for next time displaying the image.
* Configurable - The settings for the application can be configured with the *kcw.conf* file.
* Overridable options - Attribute of the program can be altered with short and long options.
* SSL - The program can run with using SSL/TLS for creating secure connections between server and client over HTTP.
* AutoComplete - The program support bash autocomplete for program options including tag autocomplete *iff* the *konachan* query program is install on the system. 


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
kcwallpaper
```
This will start the kcwallpaper program with its default options.

The options in kcw.conf can be override with command line options, see for the following example.
```bash
kcwallpaper -t "cat"
```
This will override the search tag cat. Remark that each search tag will be split between a whitespace. Which can be give different result. Example the tag 'short hair', if typed with the whitespace between the words will make the program believe they're two tags, short and hair. This is although solved by typing an understand score between the words. so the short hair would become 'short_hair'. See following example.
```bash
kcwallpaper -t "short_hair cat"
```


## Dependencies ##
----------------
In order to run the program, the following Debian packages has to be installed.
```bash
apt-get install python2.7 python-mysql.connector python-sqlite
```
In order to make the caching feature work the following Debian packages is needed.
```bash
apt-get install mysql-server
```

## License ##
-----
This project is licensed under the GPL+3 License - see the [LICENSE](LICENSE) file for details
