# -*- coding:utf-8-*-
import os

BASH = os.path.dirname(os.path.dirname(__file__))

export_file = '%s/static/files/download/' %BASH
import_file_dir = '%s/static/files/upload/' %BASH
script_file = '%s/static/files/scripts/' %BASH
log_path = "%s/logs"%BASH
ansible_path = "%s/cmdbServer/ansible/"%BASH

# system start need binding host and port
host = '0.0.0.0'
port = 8000

# Services port,Accept client data
server_port = 38232 # Services port ,accept client data
listen = 5 #Enable a server to accept connections,
