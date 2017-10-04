#!/bin/bash

# Versions
MAJOR := 0
MINOR := 10
PATCH := 2
STATE := rc
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
# Compiler
CC ?= cc
#
PYTHON := kcwsql.py kcwsimpleparser.py
PYTHONBIN := kcwallpaper.py
#
TARGET := kcwallpaper
INSTALL_DEP :=

install : $(INSTALL_DEP)
	./sqlinstall.sh
	$(MKDIR)  $(INSTALL_ETC_LOCATION)
	$(CP) kcw.conf $(INSTALL_ETC_LOCATION)
	$(CP) kcwallpaper.bc $(INSTALL_LOCATION)/share/bash-completion/completions/kcwallpaper
	$(PYTHONV) setup.py build
	$(PYTHONV) setup.py install

install_dep: install_swp_deps install_konachan_deps
	@echo -n "Installed the program dependencies for kcwallpaper.\n"

install_swp_deps :
	$(MAKE) -C swp install CC=$(CC)

install_konachan_deps :
	$(MAKE) -C konachan install CC=$(CC)

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

.PHONY : install distribution clean dep install_swp_deps install_konachan_deps

ifneq (,$(swp))
    INSTALL_DEP += install_swp_deps
endif

ifneq (,$(konachan))
    INSTALL_DEP += install_konachan_deps
endif


