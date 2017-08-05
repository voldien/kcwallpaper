#!/bin/bash

# Versions
MAJOR := 0
MINOR := 9
PATCH := 0
STATE := a
VERSION := $(MAJOR).$(MINOR)$(STATE)$(PATCH)
# Utilities.
RM := rm -f
CP := cp
MKDIR := mkdir -p
CHMOD := chmod
LN := ln
# Directory paths.
DESTDIR ?=
PREFIX ?= /usr
INSTALL_LOCATION=$(DESTDIR)$(PREFIX)
INSTALL_ETC_LOCATION=$(DESTDIR)/etc
PYTHONV ?= python2.7
PIP ?= pip2
#
PYTHON := kcwsql.py kcwsimpleparser.py
PYTHONBIN := kcwallpaper.py
#
TARGET := kcwallpaper

install :
	@echo -n "Create MySQL cache server.\n"
	./sqlinstall.sh
	$(MKDIR) $(INSTALL_LOCATION)/bin
	$(CP) *.py $(INSTALL_LOCATION)/lib/$(PYTHONV)
	$(CP) -r kcw $(INSTALL_LOCATION)/lib/$(PYTHONV)
	$(CHMOD) +x $(INSTALL_LOCATION)/lib/$(PYTHONV)/$(PYTHONBIN)
	$(LN) -fs $(INSTALL_LOCATION)/lib/$(PYTHONV)/$(PYTHONBIN)  $(INSTALL_LOCATION)/bin/$(TARGET)
	$(MKDIR)  $(INSTALL_ETC_LOCATION)
	$(CP) kcw.conf $(INSTALL_ETC_LOCATION)
	$(CP) kcwallpaper.bc $(INSTALL_ETC_LOCATION)/bash_completion.d

distribution :
	@echo -n "Creating archive.\n"
	$(RM) -r $(TARGET)-$(VERSION)
	$(MKDIR) $(TARGET)-$(VERSION)
	$(CP) -r kcw $(TARGET)-$(VERSION)
	$(CP) *.py Makefile README.md *.5 *.1 *.sql kcwallpaper.bc $(TARGET)-$(VERSION)
	tar cf - $(TARGET)-$(VERSION) | gzip -c > $(TARGET)-$(VERSION).tar.gz
	$(RM) -r $(TARGET)-$(VERSION)

dep :
	$(PIP) install mysql-connector-python
	$(PIP) install pysqlite
	$(PIP) install urllib2

clean:
	@echo -n "Removing useless files.\n"
	$(RM) *.pyc

.PHONY : install distribution clean dep


