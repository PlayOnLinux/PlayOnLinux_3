#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2008 Pâris Quentin
# Copyright (C) 2009 Łukasz Wojniłowicz

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


import wxversion
wxversion.select("2.8")
import wx, wx.html, webbrowser
import gettext, os, getopt, sys, urllib, signal, socket, string, time, threading
import lib.Variables as Variables, lib.lng as lng


class MainWindow(wx.Frame):
  def __init__(self,parent,id,title):
    wx.Frame.__init__(self, parent, -1, title, size = (600, 565))
    self.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))
    self.timer = wx.Timer(self, 1)


    self.images = wx.ImageList(32, 32)
   
    if(len(sys.argv) > 1):
		self.panel_games = wx.Panel(self, -1)
		self.panel_update = wx.Panel(self.panel_games, -1)
		#self.panel_update.SetBackgroundColour((255,255,225))

		self.fontText = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,False, "", wx.FONTENCODING_DEFAULT)
		self.image_logo = wx.StaticBitmap(self.panel_update, -1, wx.ArtProvider.GetBitmap("gtk-refresh", wx.ART_MENU), pos=(15,0))
		self.texte_update = wx.StaticText(self.panel_update, -1, _("An updated version of PlayOnLinux is available.")+" ("+sys.argv[1]+")",pos=(35,0))
		self.texte_update.SetFont(self.fontText)
		self.list_game = wx.TreeCtrl(self.panel_games, 105, style=wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT)

		self.sizer_games = wx.BoxSizer(wx.VERTICAL)
		self.sizer_games.Add(self.panel_update, 1, wx.EXPAND|wx.ALL, 2)
		self.sizer_games.Add(self.list_game, 20, wx.EXPAND|wx.ALL, 2)
	
		self.panel_games.SetSizer(self.sizer_games)
		self.panel_games.SetAutoLayout(True)

    else :
    		self.list_game = wx.TreeCtrl(self, 105, style=wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT)	

    self.list_game.SetSpacing(0);
    self.list_game.SetImageList(self.images)


    self.oldreload = ""
    self.oldimg = ""

    self.filemenu = wx.Menu()
    self.filemenu.Append(wx.ID_OPEN, _("Run"))
    self.filemenu.Append(wx.ID_ADD, _("Install"))
    self.filemenu.Append(wx.ID_DELETE, _("Remove"))
    self.filemenu.Append(wx.ID_REFRESH, _("Refresh the repository"))
    self.filemenu.AppendSeparator()
    self.filemenu.Append(wx.ID_EXIT, _("Exit"))

    self.expertmenu = wx.Menu()


    self.winever_item = wx.MenuItem(self.expertmenu, 107, _("Manage wine versions"))
    self.winever_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/wine.png"))
    self.expertmenu.AppendItem(self.winever_item)

    #self.wineserv_item = wx.MenuItem(self.expertmenu, 115, _("Kill wineserver process"))
    #self.wineserv_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/wineserver.png"))
    #self.expertmenu.AppendItem(self.wineserv_item)

    self.run_item = wx.MenuItem(self.expertmenu, 108, _("Run a non-official script"))
    self.run_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/run.png"))
    self.expertmenu.AppendItem(self.run_item)

    self.polshell_item = wx.MenuItem(self.expertmenu, 109, _("PlayOnLinux debugger"))
    self.polshell_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/polshell.png"))
    self.expertmenu.AppendItem(self.polshell_item)

    self.cdrom_item = wx.MenuItem(self.expertmenu, 120, _("Autorun"))
    self.cdrom_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/cdrom.png"))
    self.expertmenu.AppendItem(self.cdrom_item)

    self.optionmenu = wx.Menu()

    self.option_item = wx.MenuItem(self.expertmenu, 210, _("General"))
    self.option_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/input-gaming.png"))
    self.optionmenu.AppendItem(self.option_item)

    self.option_item = wx.MenuItem(self.expertmenu, 211, _("Internet"))
    self.option_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/internet-web-browser.png"))
    self.optionmenu.AppendItem(self.option_item)

    self.option_item = wx.MenuItem(self.expertmenu, 212, _("Environment"))
    self.option_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/user-desktop.png"))
    self.optionmenu.AppendItem(self.option_item)

    self.option_item = wx.MenuItem(self.expertmenu, 213, _("System"))
    self.option_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/application-x-executable.png"))
    self.optionmenu.AppendItem(self.option_item)

    self.option_item = wx.MenuItem(self.expertmenu, 214, _("Plugins"))
    self.option_item.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/package-x-generic.png"))
    self.optionmenu.AppendItem(self.option_item)

    self.pluginsmenu = wx.Menu()

    files=os.listdir(Variables.playonlinux_rep+"/plugins")
    files.sort()
    self.plugin_list = []
    self.i = 0
    self.j = 0
    while(self.i < len(files)):
	if(os.path.exists(Variables.playonlinux_rep+"/plugins/"+files[self.i]+"/scripts/menu")):
		if(os.path.exists(Variables.playonlinux_rep+"/plugins/"+files[self.i]+"/enabled")):
			self.plugin_item = wx.MenuItem(self.expertmenu, 300+self.j, files[self.i])

			self.icon_look_for = Variables.playonlinux_rep+"/plugins/"+files[self.i]+"/icon"
			if(os.path.exists(self.icon_look_for)):
				self.bitmap = wx.Bitmap(self.icon_look_for)
			else:	
				self.bitmap = wx.Bitmap(Variables.playonlinux_env+"/etc/playonlinux16.png")
			
			self.plugin_item.SetBitmap(self.bitmap)
			self.pluginsmenu.AppendItem(self.plugin_item)
			wx.EVT_MENU(self, 300+self.j,  self.run_plugin)
			self.plugin_list.append(files[self.i])
			self.j += 1
	self.i += 1
    
    if(self.j > 0):
	self.pluginsmenu.AppendSeparator()

    self.option_item_p = wx.MenuItem(self.expertmenu, 214, _("Plugins manager"))
    self.option_item_p.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/package-x-generic.png"))
    self.pluginsmenu.AppendItem(self.option_item_p)
 
    self.last_string = ""


    # /!\ id 115 utilisé par wineserver #
    # /!\ id 117 et 118 utilisés aussi #
    self.helpmenu = wx.Menu()
    self.helpmenu.Append(wx.ID_ABOUT, _("About"))
    self.helpmenu.Append(500, _("Donate"))
    self.menubar = wx.MenuBar()
    self.menubar.Append(self.filemenu, _("File"))
    self.menubar.Append(self.expertmenu, _("Tools"))
    self.menubar.Append(self.optionmenu, _("Settings"))
    self.menubar.Append(self.pluginsmenu, _("Plugins"))
    self.menubar.Append(self.helpmenu, _("Help"))
    self.SetMenuBar(self.menubar)

    self.toolbar = self.CreateToolBar(wx.TB_TEXT)
    self.toolbar.AddLabelTool(wx.ID_OPEN, _("Run"), wx.ArtProvider.GetBitmap("gtk-open", wx.ART_TOOLBAR))
    self.toolbar.AddLabelTool(wx.ID_ADD, _("Install"), wx.ArtProvider.GetBitmap("gtk-add", wx.ART_TOOLBAR))
    self.toolbar_remove = self.toolbar.AddLabelTool(wx.ID_DELETE, _("Remove"), wx.ArtProvider.GetBitmap("gtk-delete", wx.ART_TOOLBAR))
    #self.toolbar.AddLabelTool(wx.ID_REFRESH, _("Refresh the repository"), wx.ArtProvider.GetBitmap("gtk-refresh", wx.ART_TOOLBAR))
    self.toolbar.AddLabelTool(121, _("Configure this application"), wx.ArtProvider.GetBitmap("gtk-edit", wx.ART_TOOLBAR))
    self.toolbar_remove = self.toolbar.AddLabelTool(122, _("Close all"), wx.ArtProvider.GetBitmap("gtk-close", wx.ART_TOOLBAR))

    self.Reload(self)
    wx.EVT_MENU(self, wx.ID_OPEN,  self.Run)
    wx.EVT_MENU(self, wx.ID_ADD,  self.InstallMenu)
    wx.EVT_MENU(self, wx.ID_ABOUT,  self.About)
    wx.EVT_MENU(self,  wx.ID_EXIT,  self.ClosePol)
    wx.EVT_MENU(self,  wx.ID_REFRESH,  self.UpdatePol)
    wx.EVT_MENU(self,  wx.ID_DELETE,  self.UninstallGame)
    wx.EVT_MENU(self,  122,  self.RKillAll)

    # Expert
    wx.EVT_MENU(self, 101,  self.Reload)
    wx.EVT_MENU(self, 107,  self.WineVersion)
    wx.EVT_MENU(self, 108,  self.Executer)
    wx.EVT_MENU(self, 109,  self.PolShell)
    wx.EVT_MENU(self, 115,  self.killwineserver)
    wx.EVT_MENU(self, 120,  self.Autorun)
    wx.EVT_MENU(self, 121,  self.Configure)

    #Options
    wx.EVT_MENU(self, 210,  self.Options)
    wx.EVT_MENU(self, 211,  self.Options)
    wx.EVT_MENU(self, 212,  self.Options)
    wx.EVT_MENU(self, 213,  self.Options)
    wx.EVT_MENU(self, 214,  self.Options)
    wx.EVT_MENU(self, 215,  self.Options)

    wx.EVT_CLOSE(self, self.ClosePol)
    wx.EVT_TREE_ITEM_ACTIVATED(self, 105, self.Run)
    wx.EVT_TREE_SEL_CHANGED(self, 105, self.Select)
    #wx.EVT_TREE_ITEM_MENU(self, 105, self.OnRightDown)

    #Timer, regarde toute les secondes si il faut actualiser la liste
    self.Bind(wx.EVT_TIMER, self.AutoReload, self.timer)
    self.timer.Start(200)

    #Pop-up menu for game list: beginning
    wx.EVT_TREE_ITEM_MENU(self, 105, self.RMBInGameList)
    wx.EVT_MENU(self, 230,  self.RWineConfigurator)
    wx.EVT_MENU(self, 231,  self.RRegistryEditor)
    wx.EVT_MENU(self, 232,  self.GoToAppDir)
    wx.EVT_MENU(self, 233,  self.ChangeIcon)
    wx.EVT_MENU(self, 234,  self.UninstallGame)
    wx.EVT_MENU(self, 235,  self.RKill)
    wx.EVT_MENU(self, 500, self.donate)

  def RMBInGameList(self, event):
	self.GameListPopUpMenu = wx.Menu()

	self.ConfigureWine = wx.MenuItem(self.GameListPopUpMenu, 230, _("Configure wine"))
	self.ConfigureWine.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/run.png"))
	self.GameListPopUpMenu.AppendItem(self.ConfigureWine)

	self.RegistryEditor = wx.MenuItem(self.GameListPopUpMenu, 231, _("Registry Editor"))
	self.RegistryEditor.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/regedit.png"))
	self.GameListPopUpMenu.AppendItem(self.RegistryEditor)

	self.GotoAppDir = wx.MenuItem(self.GameListPopUpMenu, 232, _("Go to the application directory"))
	self.GotoAppDir.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/onglet/user-desktop.png"))
	self.GameListPopUpMenu.AppendItem(self.GotoAppDir)

	self.ChangeIcon = wx.MenuItem(self.GameListPopUpMenu, 233, _("Set the icon"))
	self.ChangeIcon.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/playonlinux16.png"))
	self.GameListPopUpMenu.AppendItem(self.ChangeIcon)

	self.ChangeIcon = wx.MenuItem(self.GameListPopUpMenu, 234, _("Remove"))
	self.ChangeIcon.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/options.png"))
	self.GameListPopUpMenu.AppendItem(self.ChangeIcon)

	self.ChangeIcon = wx.MenuItem(self.GameListPopUpMenu, 235, _("Close this application"))
	self.ChangeIcon.SetBitmap(wx.Bitmap(Variables.playonlinux_env+"/etc/menu/wineserver.png"))
	self.GameListPopUpMenu.AppendItem(self.ChangeIcon)

	self.PopupMenu(self.GameListPopUpMenu, event.GetPoint())

  def donate(self, event):
	webbrowser.open("http://www.playonlinux.com/donate.html");

  def RWineConfigurator(self, event):
        self.RConfigure(_("Configure wine"), "nothing")

  def RKill(self, event):
        self.RConfigure(_("KillApp"), "nothing")

  def RKillAll(self, event):
    os.system("bash \""+Variables.playonlinux_env+"/bash/killall\"&")

  def RRegistryEditor(self, event):
        self.RConfigure(_("Registry Editor"), "nothing")

  def GoToAppDir(self, event):
	game_exec = self.list_game.GetItemText(self.list_game.GetSelection())
	self.read = open(Variables.playonlinux_rep+"configurations/installed/"+game_exec,"r").readlines()

	if not len(self.read):
		print "err: Empty launcher"
		return

	self.i = 0;
	while(self.i < len(self.read)):
		if("cd \"" in self.read[self.i]):
			break
		self.i += 1

	if len(self.read) == (self.i):
		print "err: No path in launcher"
		return

	AppDir = self.read[self.i][3:]
	if AppDir != "":
		os.system("xdg-open "+AppDir)

  def ChangeIcon(self, event):
	self.IconDir = Variables.homedir+"/.local/share/icons/"
	self.SupprotedIconExt = "All|*.xpm;*.XPM;*.png;*.PNG;*.ico;*.ICO;*.jpg;*.JPG;*.jpeg;*.JPEG;*.bmp;*.BMP\
	\|XPM (*.xpm)|*.xpm;*.XPM\
	\|PNG (*.png)|*.png;*.PNG\
	\|ICO (*.ico)|*.ico;*.ICO\
	\|JPG (*.jpg)|*.jpg;*.JPG\
	\|BMP (*.bmp)|*.bmp;*.BMP\
	\|JPEG (*.jpeg)|*.jpeg;*JPEG"
	self.IconDialog = wx.FileDialog(self, "Choose a icon file", self.IconDir, "", self.SupprotedIconExt, wx.OPEN | wx.FD_PREVIEW)
        if self.IconDialog.ShowModal() == wx.ID_OK:
            self.IconFilename=self.IconDialog.GetFilename()
            self.IconDirname=self.IconDialog.GetDirectory()
            IconFile=os.path.join(self.IconDirname,self.IconFilename)
	    self.RConfigure("IconChange", IconFile)
        self.IconDialog.Destroy()
    #Pop-up menu for game list: ending

  def Select(self, event):
	game_exec = self.list_game.GetItemText(self.list_game.GetSelection())
	self.read = open(Variables.playonlinux_rep+"configurations/installed/"+game_exec,"r").readlines()
	self.i = 0;
	self.wine_present = False;
	while(self.i < len(self.read)):
		if("wine " in self.read[self.i]):
			self.wine_present = True;
		self.i += 1
  def Reload(self, event):
	 time.sleep(0.5);
	 self.games = os.listdir(Variables.playonlinux_rep+"configurations/installed/")
	 self.games.sort()
	 self.list_game.DeleteAllItems()
  	 self.images.RemoveAll()
	 root = self.list_game.AddRoot("")
	 self.i = 0
	 for game in self.games: #METTRE EN 32x32
		if(os.path.exists(Variables.playonlinux_rep+"/icones/32/"+game)):
			file_icone = Variables.playonlinux_rep+"/icones/32/"+game
		else:
			file_icone = Variables.playonlinux_rep+"/icones/32/playonlinux.png"

		self.images.Add(wx.Bitmap(file_icone))
		item = self.list_game.AppendItem(root, game, self.i)
		self.i += 1


	
	    
	
  def Options(self, event):
    print("Running options")
    onglet=event.GetId()-210
    os.system(os.popen("printf $PYTHON",'r').read()+" \""+Variables.playonlinux_env+"/python/options.py\" "+str(onglet)+"&")

  def run_plugin(self, event):
    game_exec = self.list_game.GetItemText(self.list_game.GetSelection())
    plugin=self.plugin_list[event.GetId()-300]
    try :
	os.system("bash \""+Variables.playonlinux_rep+"/plugins/"+plugin+"/scripts/menu\" \""+game_exec+"\"&")
    except : 
	print("bash \""+Variables.playonlinux_rep+"/plugins/"+plugin+"/scripts/menu\" "+game_exec+"&")

  def killwineserver(self, event):
    os.system("bash \""+Variables.playonlinux_env+"/bash/expert/kill_wineserver\"&")

  def Executer(self, event):
    os.system("bash \""+Variables.playonlinux_env+"/bash/expert/Executer\"&")

  def PolShell(self, event):
    os.system("bash \""+Variables.playonlinux_env+"/bash/expert/PolShell\"&")

  def RConfigure(self, function_to_run, firstargument):
    """Starts polconfigurator remotely."""
    game_exec = self.list_game.GetItemText(self.list_game.GetSelection())
    print game_exec
    print function_to_run
   
    if(game_exec != ""):
        print("Running (remotely) configuration of "+game_exec)
	os.system("bash \""+Variables.playonlinux_env+"/bash/polconfigurator\" \""+game_exec+"\" \""+function_to_run+"\" \""+firstargument+"\"&")

  def Configure(self, event):
    game_exec = self.list_game.GetItemText(self.list_game.GetSelection())
    if(game_exec != ""):
        print("Running configuration of "+game_exec)
   	os.system("bash \""+Variables.playonlinux_env+"/bash/polconfigurator\" \""+game_exec+"\"&")


  def UninstallGame(self, event):
    game_exec = self.list_game.GetItemText(self.list_game.GetSelection())
    if(game_exec != ""):
        print("Uninstall "+game_exec)
   	os.system("bash \""+Variables.playonlinux_env+"/bash/uninstall\" \""+game_exec+"\"&")
   	

  def AutoReload(self, event):
    reload = os.listdir(Variables.playonlinux_rep+"/configurations/installed")
    if(reload != self.oldreload):
	self.Reload(self)
	self.oldreload = reload

    reloadimg = os.listdir(Variables.playonlinux_rep+"/icones/32")
    if(reloadimg != self.oldimg):
	self.Reload(self)
	self.oldimg = reloadimg
   

  def InstallMenu(self, event):
    print("Running install menu")
    os.system("bash \""+Variables.playonlinux_env+"/bash/install\"&")
    
  def UpdatePol(self, event):
    print("Running update menu")
    os.system("bash \""+Variables.playonlinux_env+"/bash/check_maj\"&")
  
  def Autorun(self, event):
    print("Autorun")
    os.system("bash \""+Variables.playonlinux_env+"/bash/autorun\"&")

  def WineVersion(self, event):
    print("Running wineversion menu")
    os.system("bash \""+Variables.playonlinux_env+"/bash/wineversion\"&")

  def Run(self, event):
    game_exec = self.list_game.GetItemText(self.list_game.GetSelection()).encode("utf-8")
    if(game_exec != ""):
	print("Running "+game_exec)
	os.system("cd \""+Variables.playonlinux_rep+"/configurations/installed/\" && bash \""+game_exec+"\"&")


  def ClosePol(self, event):
    sys.exit(0)
    
  def About(self, event):
    self.aboutBox = wx.AboutDialogInfo()
    self.aboutBox.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))
    self.aboutBox.SetName("PlayOnLinux")
    self.aboutBox.SetVersion(Variables.version)
    self.aboutBox.SetDescription(_("Run your Windows programs on Linux !"))
    self.aboutBox.SetCopyright(_("(C) PlayOnLinux team 2008\nUnder GPL licence version 3"))
    self.aboutBox.AddDeveloper("Developer and Website : Tinou (Pâris Quentin)")	 
    self.aboutBox.AddDeveloper("Scriptors : MulX (Petit Aymeric), GNU_Raziel, NSLW")
    self.aboutBox.AddDeveloper("Packager : MulX (Petit Aymeric)")
    self.aboutBox.AddDeveloper("Script Creator : Zoloom (Cassarin-Grand Arthur)")
    self.aboutBox.AddDeveloper("Helped for the program : kiplantt, NSLW")
    self.aboutBox.AddArtist("Icons are provided by Tango Desktop Project")
    self.aboutBox.SetWebSite("http://www.playonlinux.com")
    self.aboutBox.SetLicence(open(Variables.playonlinux_env+"/LICENCE",'r').read())
    self.about = wx.AboutBox(self.aboutBox)

class PlayOnLinuxApp(wx.App):
   def OnInit(self):
	self.frame = MainWindow(None, -1, "PlayOnLinux")
        self.SetTopWindow(self.frame)
	self.frame.Center(wx.BOTH)
       	self.frame.Show(True)
        return True



lng.Lang()
app = PlayOnLinuxApp()
app.MainLoop()
sys.exit(0)
