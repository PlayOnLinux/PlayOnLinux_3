#!/usr/bin/python
# Copyright (C) 2007-2010 PlayOnLinux Team
import wxversion
wxversion.select("2.8")
import gettext, Variables as Variables, os
import locale, string, wx
class Lang(object):
	def __init__(self):
		languages = os.listdir(Variables.playonlinux_env+'/lang/locale')

		langid = wx.LANGUAGE_DEFAULT
		basepath = os.popen("printf \"$PLAYONLINUX\"","r").read()
		localedir = os.path.join(basepath, "lang/locale")
		domain = "pol"
		mylocale = wx.Locale(langid)
		mylocale.AddCatalogLookupPathPrefix(localedir)
		mylocale.AddCatalog(domain)

		mytranslation = gettext.translation(domain, localedir, [mylocale.GetCanonicalName()], fallback = True)
		mytranslation.install()



