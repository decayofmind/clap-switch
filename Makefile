DESTDIR=
PREFIX=/usr
SYSCONFDIR=/etc

SYSTEMCTL:=$(shell which systemctl)
PIP:=$(shell which pip3)
PYTHON:=$(shell which python3)

.PHONY: all installdeps install

all: installdeps install

lint:
	$(PYTHON) -m flake8 clap-switch.py

install:
	# Install the main script
	install -m0755 clap-switch.py $(DESTDIR)$(PREFIX)/local/sbin/clap-switch.py
	# Install systemd unit
	install -m0644 clap-switch.systemd $(DESTDIR)$(SYSCONFDIR)/systemd/system/clap-switch.service && $(SYSTEMCTL) daemon-reload

installdeps:
	if test -x "$(PIP)"; then $(PIP) install -r requirements.txt; fi
