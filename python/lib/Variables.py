#!/usr/bin/env python
import os
playonlinux_env = os.popen("printf \"$PLAYONLINUX\"", "r").read()
playonlinux_rep = os.popen("printf \"$HOME/.PlayOnLinux/\"", "r").read()
homedir = os.popen("printf \"$HOME\"", "r").read()
version = os.popen("printf \"$VERSION\"", "r").read()
current_user = os.popen("printf \"$USER\"","r").read()
offline = "0"
site = os.popen("printf $SITE").read()
