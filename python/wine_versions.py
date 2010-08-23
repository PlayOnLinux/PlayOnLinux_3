#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2007 Pâris Quentin

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. 

import wxversion, os, getopt, sys, urllib, signal, socket, codecs, string, shutil, time, urllib, urllib2
wxversion.select("2.8")
import wx, wx.animate

import lib.Variables as Variables
import lib.lng, threading
lib.lng.Lang()
timeout = 2
socket.setdefaulttimeout(timeout)

def keynat(string):
    r'''A natural sort helper function for sort() and sorted()
    without using regular expressions or exceptions.

    >>> items = ('Z', 'a', '10th', '1st', '9')
    >>> sorted(items)
    ['10th', '1st', '9', 'Z', 'a']
    >>> sorted(items, key=keynat)
    ['1st', '9', '10th', 'a', 'Z']    

    Borrowed from http://code.activestate.com/recipes/285264/#c6
    by paul clinch.  

    License is the PSF Python License, http://www.python.org/psf/license/ (GPL compatible)
    '''
    it = type(1)
    r = []
    for c in string:
        if c.isdigit():
            d = int(c)
            if r and type( r[-1] ) == it: 
                r[-1] = r[-1] * 10 + d
            else: 
                r.append(d)
        else:
            r.append(c.lower())
    return r



class getVersions(threading.Thread):
  def __init__(self):
	threading.Thread.__init__(self)
	self.thread_message = "#WAIT#"
	self.versions = []
	self.start()

  def download(self, game):
	self.getDescription = game
	
  def run(self):
	self.thread_running = True
	while(self.thread_running):
		if(self.thread_message == "get"):
			try :
				url = 'http://mulx.playonlinux.com/wine/linux-i386/LIST'
				req = urllib2.Request(url)
				handle = urllib2.urlopen(req)
				time.sleep(1)
				available_versions = handle.read()
				available_versions = string.split(available_versions,"\n")
				self.i = 0
				self.versions_ = []
				while(self.i < len(available_versions) - 1):
					informations = string.split(available_versions[self.i], ";")
					version = informations[1]
					package = informations[0]
					sha1sum = informations[2]
					if(not os.path.exists(Variables.playonlinux_rep+"/WineVersions/"+version)):
						self.versions_.append(version)
					self.i += 1	
				self.versions_.reverse()
				self.versions = self.versions_[:]

				self.thread_message = "Ok"
			except :
				time.sleep(1)
				self.thread_message = "Err"
				self.versions = ["Wine packages website is unavailable"]
		else:
			time.sleep(0.2)

class Onglets(wx.Notebook):
	# Classe dérivée du wx.Notebook
	def __init__(self, parent):
		self.notebook = wx.Notebook.__init__(self, parent, -1)
		self.images_onglets = wx.ImageList(16, 16)
		self.images_onglets.Add(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/wine.png"))
		self.images_onglets.Add(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/input-gaming.png"))
		self.SetImageList(self.images_onglets)

	def liste_versions(self):
	    self.panelFenp = wx.Panel(self, -1)
	    self.imagesapps = wx.ImageList(22, 22)
	    self.imagesapps_i = wx.ImageList(22, 22)

	    # self.searchbox = wx.TextCtrl(self.panelFenp, 110, size=(464,25), pos=(319,9))
	    # self.searchcaption = wx.StaticText(self.panelFenp, -1, Lng.search, (220,15), wx.DefaultSize)
	    self.list_apps = wx.TreeCtrl(self.panelFenp, 106, style=wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT|wx.RAISED_BORDER, size=(562, 212), pos=(10,30))
	    self.list_apps.SetImageList(self.imagesapps)
	    self.list_apps.SetSpacing(0);

 	    self.new_panel = wx.Panel(self.panelFenp, -1, pos=(10,505), size=(100,100))
   	    self.animation = wx.animate.GIFAnimationCtrl(self.new_panel, -1, Variables.playonlinux_env+"/etc/24-0.gif", (0,0))
	    self.animation.Play()

	    self.list_ver_installed = wx.TreeCtrl(self.panelFenp, 107, style=wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT|wx.RAISED_BORDER, size=(562, 212), pos=(10,281))
	    self.list_ver_installed.SetImageList(self.imagesapps_i)
	    self.list_ver_installed.SetSpacing(0);
	    wx.StaticText(self.panelFenp, -1, _("Installed Wine Versions :"),(10,261))
	    wx.StaticText(self.panelFenp, -1, _("Available Wine Versions :"),(10,10))
	    # self.content =  wx.TextCtrl(self.panelFenp, 107, pos=(10,301), size=(562,212), style = wx.TE_MULTILINE | wx.TE_RICH2 | wx.CB_READONLY | wx.RAISED_BORDER)

	    self.button_rm = wx.Button(self.panelFenp, wx.ID_REMOVE, pos=(388, 500), size=wx.DefaultSize)
	    self.button_in = wx.Button(self.panelFenp, wx.ID_ADD, pos=(488, 500), size=wx.DefaultSize)

	    self.button_rm.Enable(False)
	    self.button_in.Enable(False)
	    self.AddPage(self.panelFenp, _("Wine versions"), imageId=0)
  


	def VersionsLoad(self):
	    dir_v = []
	    files = os.listdir(Variables.playonlinux_rep+"/WineVersions/")
	    self.i = 0
	    while(self.i < len(files)):
		if(os.path.isdir(Variables.playonlinux_rep+"/WineVersions/"+files[self.i])):
			dir_v.append(files[self.i])
		self.i += 1	
	
	    dir_v.sort()
	    dir_v.reverse()
	    dir_v.insert(0,"System")

	    self.MenuVer.Destroy()
	    self.MenuVer = wx.ComboBox(self.panelApps, 112, value=dir_v[0], pos=wx.Point(10, 460),size=wx.DefaultSize, choices=dir_v)

        def liste_games(self):
            self.panelApps = wx.Panel(self, -1)

 	    self.images = wx.ImageList(22, 22)
	    wx.StaticText(self.panelApps, -1, _("My Applications")+" :",(10,10))
	    self.list_game = wx.TreeCtrl(self.panelApps, 111, style=wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT|wx.RAISED_BORDER, size=(562, 400), pos=(10,30))
	    self.list_game.SetImageList(self.images)
	    self.list_game.SetSpacing(0);
	    self.version = wx.StaticText(self.panelApps, -1, _("Version :"),(10,440))
	   
	    self.MenuVer = wx.ComboBox(self.panelApps, 112)
	    self.VersionsLoad()
	    self.AddPage(self.panelApps, _("My Applications"), imageId=1)

class MainWindow(wx.Frame):
  def __init__(self,parent,id,title):
    wx.Frame.__init__(self, parent, -1, title, size = (592, 633), style = wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX)
    self.timer = wx.Timer(self, 1)
    self.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))
    self.panel = wx.Panel(self, -1)
    self.panels_buttons = wx.Panel(self.panel, -1)
    self.onglets = Onglets(self.panel)
    self.sizer = wx.BoxSizer(wx.VERTICAL)   
    self.sizer.Add(self.onglets, 11, wx.EXPAND|wx.ALL, 2)
    self.sizer.Add(self.panels_buttons, 1, wx.EXPAND|wx.ALL, 2)
    
    self.getVersions()
    self.panel.SetSizer(self.sizer)
    self.panel.SetAutoLayout(True)

    self.onglets.liste_versions()
    self.onglets.liste_games()

    self.oldreload=""
    self.oldversions = []

    self.add_games()
    self.button = wx.Button(self.panels_buttons, wx.ID_CLOSE, pos=(493, 5), size=wx.DefaultSize)
    
    wx.EVT_BUTTON(self, wx.ID_CLOSE, self.closeapp)
    wx.EVT_CLOSE(self, self.closeapp)
    wx.EVT_BUTTON(self, wx.ID_REMOVE, self.delete)
    wx.EVT_BUTTON(self, wx.ID_ADD, self.install)
    wx.EVT_TREE_SEL_CHANGED(self, 106, self.unselect)
    wx.EVT_TREE_SEL_CHANGED(self, 107, self.unselect)
    wx.EVT_TREE_SEL_CHANGED(self, 111, self.select_game)
    wx.EVT_COMBOBOX(self, 112, self.assign)
    self.Bind(wx.EVT_TIMER, self.AutoReload, self.timer)
    self.timer.Start(200)

  def AutoReload(self, event):
    reload = os.listdir(Variables.playonlinux_rep+"/WineVersions")
    if(download.thread_message == "Ok" or download.thread_message == "Err"):
	self.onglets.new_panel.Hide()
	self.WriteVersions()
	download.thread_message = "Wait"
    else:
	if(download.thread_message != "Wait"):
		self.onglets.new_panel.Show()

    if(reload != self.oldreload):
	self.getVersions()
	self.onglets.VersionsLoad()
	self.oldreload = reload

    if(download.versions != self.oldversions):
	self.onglets.VersionsLoad()
	self.oldversions = download.versions[:]

  def assign(self, event):
	game = self.onglets.list_game.GetItemText(self.onglets.list_game.GetSelection()).encode('utf-8')
	self.file = Variables.playonlinux_rep+"configurations/installed/"+game
	fichier = open(self.file,"r").readlines()
	self.i = 0
	line = []
	while(self.i < len(fichier)):
		fichier[self.i] = fichier[self.i].replace("\n","")
		if("PATH=" not in fichier[self.i] or "WineVersions" not in fichier[self.i]):
			line.append(fichier[self.i])
		self.i += 1

	fichier_write = open(self.file,"w")
	
	if(self.onglets.MenuVer.GetValue() != "System"):
		line.insert(1,"PATH=\""+Variables.playonlinux_rep+"WineVersions/"+self.onglets.MenuVer.GetValue()+"/usr/bin/:$PATH\"")
	self.i = 0	
	while(self.i < len(line)):
		fichier_write.write(line[self.i]+"\n")
		self.i+=1


  def select_game(self, event):
	self.onglets.MenuVer.Enable(True)
	game = self.onglets.list_game.GetItemText(self.onglets.list_game.GetSelection()).encode('utf-8')
	self.file = Variables.playonlinux_rep+"configurations/installed/"+game
	fichier = open(self.file,"r").readlines()
	self.i = 0
	line = ""
	while(self.i < len(fichier)):
		fichier[self.i] = fichier[self.i].replace("\n","")
		if("PATH=" in fichier[self.i] and "WineVersions" in fichier[self.i]):
			line = fichier[self.i]
		self.i += 1
	
	if(line == ""):
		#self.version.Destroy()
		#self.version = wx.StaticText(self.onglets.panelApps, -1, _("Version : ")+"System",(10,440))
		self.onglets.MenuVer.SetValue("System")
	else:
		version=line.replace("PATH=","").replace("\"","").replace(Variables.playonlinux_rep,"")
		version = string.split(version,"/")
		version = version[1]
		self.onglets.MenuVer.SetValue(version)		
		#self.version.Destroy()
		#self.version = wx.StaticText(self.onglets.panelApps, -1, _("Version : ")+version,(10,440))


  def add_games(self):
	self.onglets.MenuVer.Enable(False)
	self.games = os.listdir(Variables.playonlinux_rep+"configurations/installed/")
	self.games.sort()
	self.onglets.images.RemoveAll()
	self.onglets.list_game.DeleteAllItems()
	root = self.onglets.list_game.AddRoot("")
	self.i = 0
	for game in self.games: 
		self.file = Variables.playonlinux_rep+"configurations/installed/"+game
		if(not os.path.isdir(self.file)):
			fichier = open(self.file,"r").read()

			if("wine " in fichier):
				if(os.path.exists(Variables.playonlinux_rep+"/icones/32/"+game)):
					file_icone = Variables.playonlinux_rep+"/icones/32/"+game
				else:
					file_icone = Variables.playonlinux_rep+"/icones/32/playonlinux.png"
				bitmap = wx.Image(file_icone)
				bitmap.Rescale(22,22,100)
				bitmap = bitmap.ConvertToBitmap()
				self.onglets.images.Add(bitmap)
				self.onglets.list_game.AppendItem(root, game, self.i)
				self.i = self.i+1
		

  def sizedirectory(self, path): 
    size = 0 
    for root, dirs, files in os.walk(path): 
        for fic in files: 
            size += os.path.getsize(os.path.join(root, fic))
    return size

  def unselect(self, event):
	if(event.GetId() == 106):
		self.onglets.list_ver_installed.UnselectAll()
		self.onglets.button_rm.Enable(False)
		self.onglets.button_in.Enable(True)
	if(event.GetId() == 107):
		self.onglets.list_apps.UnselectAll()
		self.onglets.button_rm.Enable(True)
		self.onglets.button_in.Enable(False)
		
  def delete(self, event):
	version = self.onglets.list_ver_installed.GetItemText(self.onglets.list_ver_installed.GetSelection()).encode('utf-8')
	if(wx.YES == wx.MessageBox("Are you sure you want to delete wine "+version+"?", style=wx.YES_NO | wx.ICON_QUESTION)):
			shutil.rmtree(Variables.playonlinux_rep+"/WineVersions/"+version)

	self.onglets.VersionsLoad()
	self.add_games()

  def install(self, event):
	install = self.onglets.list_apps.GetItemText(self.onglets.list_apps.GetSelection()).encode('utf-8')
	os.system("bash \""+Variables.playonlinux_env+"/bash/install_wver\" "+install+" &")
	self.add_games()

  def getVersions(self):
	download.thread_message = "get"

  def WriteVersions(self):
	self.onglets.imagesapps.RemoveAll()
	self.onglets.imagesapps_i.RemoveAll()
	self.onglets.list_apps.DeleteAllItems()	
	self.onglets.list_ver_installed.DeleteAllItems()	
	
	root = self.onglets.list_apps.AddRoot("")
	self.i = 0
	while(self.i < len(download.versions)):
		self.onglets.imagesapps.Add(wx.Bitmap(Variables.playonlinux_env+"/etc/install/wine-packages.png"))
		self.onglets.list_apps.AppendItem(root,download.versions[self.i],self.i)
		self.i += 1

	root2 = self.onglets.list_ver_installed.AddRoot("")
	installed_versions = os.listdir(Variables.playonlinux_rep+"/WineVersions/")
	installed_versions.sort(key=keynat)
	installed_versions.reverse()
	self.i = 0
	self.j = 0
	while(self.i < len(installed_versions)):
		if(os.path.isdir(Variables.playonlinux_rep+"/WineVersions/"+installed_versions[self.i])):
			if(len(os.listdir(Variables.playonlinux_rep+"/WineVersions/"+installed_versions[self.i])) == 0):
				self.onglets.imagesapps_i.Add(wx.Bitmap(Variables.playonlinux_env+"/etc/install/wine-warning.png"))
			else:
				self.onglets.imagesapps_i.Add(wx.Bitmap(Variables.playonlinux_env+"/etc/install/wine.png"))
			self.onglets.list_ver_installed.AppendItem(root2,installed_versions[self.i],self.j)
			self.j += 1
		self.i += 1
	try :
		if(versions[0] == "Wine packages website is unavailable"):
			self.onglets.list_apps.Enable(False)
			self.onglets.imagesapps.RemoveAll()
	except :
		pass
	self.onglets.button_rm.Enable(False)
	self.onglets.button_in.Enable(False)
   
  def closeapp(self, event):
	download.thread_running = False
	sys.exit(1)   

  

class PlayOnLinuxApp(wx.App):
   def OnInit(self):
	frame = MainWindow(None, -1, "PlayOnLinux Wine Versions Settings")
        self.SetTopWindow(frame)
	frame.Center(wx.BOTH)
        frame.Show(True)
        return True

download = getVersions()
app = PlayOnLinuxApp()
app.MainLoop()
