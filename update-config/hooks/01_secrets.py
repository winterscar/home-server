#!/usr/bin/env python3
import yaml
import os
import re


placeholder = re.compile(r"\$\{(?P<key>.+?)\}")

with open("/config/secrets.yaml", 'r') as stream:
  secrets = yaml.safe_load(stream)

for filepath in secrets:
  filepath = "/config/" + filepath
  with open(filepath, 'r') as config:
    configdata = config.read()
  for key in secrets[filepath]:
    configdata = configdata.replace(r"${" + key + r"}", str(secrets[filepath][key]))
  with open(filepath, 'w') as config:
    config.write(configdata)
  print("replaced secrets in " + filepath)