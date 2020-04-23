#!/bin/bash

cd /config
git diff --name-only master origin/master > changes.txt
git pull