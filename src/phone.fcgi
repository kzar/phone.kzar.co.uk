#!/usr/bin/env python
# coding: utf-8

import os
from flup.server.fcgi import WSGIServer
from phone import application

if __name__ == "__main__":
  bindAddress = os.environ.get("FCGI_BIND_ADDRESS")
  WSGIServer(application, bindAddress=bindAddress).run()
