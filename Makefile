#!/bin/bash

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
#
MYSQL := mysql
PYTHON := kcwsql.py kcwsimpleparser.py
PYTHONBIN := kcwallpaper.py
#
TARGET := kcwallpaper
VERSION := 0.9.0

install :
	@echo -n "Create MySQL cache server.\n"
	./sqlinstall.sh
	$(MKDIR) $(INSTALL_LOCATION)/bin
	$(CP) *.py $(INSTALL_LOCATION)/lib/$(PYTHONV)
	$(CHMOD) +x $(INSTALL_LOCATION)/lib/$(PYTHONV)/$(PYTHONBIN)
	$(LN) -s $(INSTALL_LOCATION)/lib/$(PYTHONV)/$(PYTHONBIN)  $(INSTALL_LOCATION)/bin/$(TARGET)
	$(MKDIR)  $(INSTALL_ETC_LOCATION)
	$(CP) kcw.conf $(INSTALL_ETC_LOCATION)

distribution :
	@echo -n "Creating archive.\n"
	$(RM) -r $(TARGET)-$(VERSION)
	$(MKDIR) $(TARGET)-$(VERSION)
	$(CP) *.py Makefile README.md *.5 *.1 *.sql $(TARGET)-$(VERSION)
	tar cf - $(TARGET)-$(VERSION) | gzip -c > $(TARGET)-$(VERSION).tar.gz
	$(RM) -r $(TARGET)-$(VERSION)

clean:
	@echo -n "Removing useless files.\n"
	$(RM) *.pyc

.PHONY : install distribution clean
