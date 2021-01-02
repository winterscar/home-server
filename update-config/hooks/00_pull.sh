#!/bin/bash
git -C /config checkout HEAD -- mopidy/mat/mopidy.conf mopidy/jessie/mopidy.conf mopidy/guest/mopidy.conf
git -C /config pull