#!/usr/bin/python 
# -*- coding:Utf-8 -*- 

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

import wxversion, os, getopt, sys, urllib, signal, time, string, urlparse, codecs
wxversion.select("2.8")
import wx
from subprocess import Popen,PIPE
import lib.Variables as Variables
import lib.lng
lib.lng.Lang()

class Ok_frame(wx.Frame): #fenêtre principale
	def __init__(self, titre):
		wx.Frame.__init__(self, None, -1, title = titre, style = wx.CLOSE_BOX | wx.CAPTION | wx.MINIMIZE_BOX, size = (520, 400))
		self.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))
		self.panel = wx.Panel(self, -1)
		self.gauge_i = 0
		self.fichier = ""
		self.file_id=Variables.playonlinux_rep+"/configurations/guis/"+os.popen('printf \"$POL_SetupWindow_ID\"','r').read()

		if(sys.argv[1] == "None"):
			self.small_image = wx.Bitmap(Variables.playonlinux_env+"/etc/setups/default/top.png")
		else:
			self.small_image = wx.Bitmap(sys.argv[1])

		self.small_x = 520 - self.small_image.GetWidth()
		#self.big_image = wx.Bitmap(sys.argv[2])
		if(sys.argv[2] == "None"):
			self.big_image = wx.Bitmap(Variables.playonlinux_env+"/etc/setups/default/left.jpg")
		else:
			self.big_image = wx.Bitmap(sys.argv[2])
		self.oldfichier = ""
		self.fontTitre = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "", wx.FONTENCODING_DEFAULT)
		self.fontText = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,False, "", wx.FONTENCODING_DEFAULT)
		
		self.footer = wx.Panel(self.panel, -1, style=wx.RAISED_BORDER, size=(522,45),pos=(-1,356))
		
		self.timer = wx.Timer(self, 1)
		

		#self.header.SetBorderColor((0,0,0))
		#self.panel.SetSizer(self.sizer)
  		#self.panel.SetAutoLayout(True)
		self.Bind(wx.EVT_TIMER, self.AutoReload, self.timer)
   		self.timer.Start(10)
		self.AutoReload(self)
		wx.EVT_CLOSE(self, self.Cancel)

	def Destroy_all(self):
		try :
			self.left_image.Destroy()
		except :
			pass
		try :
			self.header.Destroy()
		except :
			pass
		try :
			self.texte.Destroy()
		except :
			pass
		try :
			self.texte_bis.Destroy()
		except :
			pass
		try :
			self.titre.Destroy()
		except :
			pass
		try :
			self.titre_header.Destroy()
		except :
			pass
		try :
			self.MainPanel.Destroy()
		except :
			pass
		try :
			self.NextButton.Destroy()
		except :
			pass
		try :
			self.CancelButton.Destroy()
		except :
			pass
		try : 
			self.champ.Destroy()
		except :
			pass
		try : 
			self.Menu.Destroy()
		except :
			pass
		try : 
			self.gauge.Destroy()
		except :
			pass
		try : 
			self.pulsebar.Destroy()
		except :
			pass
		try : 
			self.menu.Destroy()
		except :
			pass
		try : 
			self.desktop.Destroy()
		except :
			pass
		try : 
			self.browse.Destroy()
		except :
			pass
		try :	
			self.image.Destroy()
		except :
			pass
		try :
			self.scrolled_panel.Destroy()
		except :
			pass
	def DrawImage(self):			
		self.left_image = wx.StaticBitmap(self.panel, -1, self.big_image, (0,0), wx.DefaultSize)

	def DrawHeader(self):
		self.header = wx.Panel(self.panel, -1, style=wx.RAISED_BORDER, size=(522,65))
		self.header.SetBackgroundColour((255,255,255))
		self.top_image = wx.StaticBitmap(self.header, -1, self.small_image, (self.small_x,0), wx.DefaultSize)

	def DrawCancel(self):
		self.CancelButton = wx.Button(self.footer, wx.ID_CANCEL, pos=(430,2),size=(85,37))
		wx.EVT_BUTTON(self, wx.ID_CANCEL , self.Cancel)	

	def DrawNext(self):
		self.NextButton = wx.Button(self.footer, wx.ID_FORWARD, pos=(340,2),size=(85,37))

	def SendBash(self, var):
		self.fichier_w = open(self.file_id,"w")
		self.fichier_w.write(var+"\nMsgOut\n")
		self.fichier_w.close()

	def release(self, event):
		self.SendBash("Ok")
		self.NextButton.Enable(False)

	def release_download(self, return_code):
		self.SendBash("MSG_VALUE="+return_code)
                self.NextButton.Enable(False)

	def release_checkboxes(self, event):
		self.i = 0
		self.send = []
		while(self.i < len(self.item_check)):
			if(self.item_check[self.i].IsChecked() == True):
				self.send.append(self.areaList[self.i])
			self.i += 1
		self.SendBash("MSG_VALUE="+string.join(self.send,self.fichier[5].replace("\n","")))
		self.NextButton.Enable(False)

	def release_yes(self, event):
		self.SendBash("MSG_QUESTION=TRUE")
		self.NextButton.Enable(False)

	def release_no(self, event):
		self.SendBash("MSG_QUESTION=FALSE")
		self.NextButton.Enable(False)
	
	def release_champ(self, event):
		self.SendBash("MSG_VALUE="+self.champ.GetValue().encode("utf-8"))
		self.NextButton.Enable(False)

	def release_menu(self,event):
		self.SendBash("MSG_VALUE="+self.areaList[self.Menu.GetSelection()])
		self.NextButton.Enable(False)

	def release_menu_list(self,event):
		self.SendBash("MSG_VALUE="+self.Menu.GetValue())
		self.NextButton.Enable(False)

	def release_menu_num(self,event):
		self.SendBash("MSG_VALUE="+str(self.Menu.GetSelection()))
		self.NextButton.Enable(False)

	def release_icons(self,event):
		if(self.menu.IsChecked()):
			self.SendBash("MSG_MENU=True")
		if(self.desktop.IsChecked()):
			self.SendBash("MSG_DESKTOP=True")
		if(self.desktop.IsChecked() and self.menu.IsChecked()):
			self.SendBash("MSG_DESKTOP=True\nMSG_MENU=True")
		if(self.desktop.IsChecked() == False and self.menu.IsChecked() == False):
			self.SendBash("Ok")
		self.NextButton.Enable(False)

	def release_menugame(self,event):
		self.SendBash("MSG_VALUE="+self.Menu.GetItemText(self.Menu.GetSelection()))
		self.NextButton.Enable(False)
		
	def Cancel(self, event):
		self.SendBash("MSG_RECEIVED=Cancel") #Indiquera à PlayOnLinux bash qu'il faut arreter l'installation
		#os.remove(self.file_id)
        	sys.exit()

 	def add_games(self):
		self.games = os.listdir(Variables.playonlinux_rep+"configurations/installed/")
		self.games.sort()
		self.images.RemoveAll()
		self.Menu.DeleteAllItems()
		root = self.Menu.AddRoot("")
		self.i = 0
		for game in self.games: 
			self.file = Variables.playonlinux_rep+"configurations/installed/"+game
			fichier = open(self.file,"r").read()

			if("wine " in fichier):
				if(os.path.exists(Variables.playonlinux_rep+"/icones/32/"+game)):
					file_icone = Variables.playonlinux_rep+"/icones/32/"+game
				else:
					file_icone = Variables.playonlinux_rep+"/icones/32/playonlinux.png"
				bitmap = wx.Image(file_icone)
				bitmap.Rescale(22,22,100)
				bitmap = bitmap.ConvertToBitmap()
				self.images.Add(bitmap)
				self.Menu.AppendItem(root, game, self.i)
				self.i = self.i+1

	def DemanderPourcent(self, event):
		self.NextButton.Enable(False)
		if self.p.poll() == None:
			self.gauge.Pulse()		
		else:
			#self.gauge.SetValue(50)
			self.Bind(wx.EVT_TIMER, self.AutoReload, self.timer)
			self.timer_attendre.Stop()
			self.timer_attendre.Destroy()
			self.timer.Start(10)
		        self.SendBash("Ok")
			#self.NextButton.Enable(True)
			#self.NextButton.Enable(True)

        def onHook(self, nb_blocs, taille_bloc, taille_fichier):
		Variables.nb_blocs_max = taille_fichier / taille_bloc
		self.gauge.SetRange(Variables.nb_blocs_max)
		self.gauge.SetValue(nb_blocs)
		
		tailleFichierB = float(taille_fichier / 1048576.0)
		octetsLoadedB = float((nb_blocs * taille_bloc) / 1048576.0)
		octetsLoadedN = round(octetsLoadedB, 1)
		tailleFichierN = round(tailleFichierB, 1)
		
		Variables.estimation_txt = str(octetsLoadedN) + " "+_("of")+" " + str(tailleFichierN) + _("MiB downloaded")
		
		self.txtEstimation.SetLabel(Variables.estimation_txt)
		self.txtEstimation.SetFont(self.fontText)
		wx.Yield()
         
 	def Parcourir(self, event):
		self.FileDialog = wx.FileDialog(self.panel)
		self.FileDialog.SetDirectory(self.fichier[5].replace("\n",""))
		self.FileDialog.ShowModal() 
		if(self.FileDialog.GetPath() != ""):
			self.champ.SetValue(self.FileDialog.GetPath().encode('utf-8'))
	        self.FileDialog.Destroy()
   
        def DownloadFile(self, url, localB):    #url = url a récupérer, localB le fichier où enregistrer la modification sans nom de fichier
		#self.buttonSuivant.Enable(False)
		chemin = urlparse.urlsplit(url)[2] 
		nomFichier = chemin.split('/')[-1] 
		local = localB + nomFichier 
		try:
			urllib.urlretrieve(url, local, reporthook = self.onHook)
		except IOError:			#server don't respond
			self.release_download("1")
			return

		self.FileTest = open(local, "r")
		self.FileTest.seek(0, 2)
		self.ReturnCode="0"

		if self.FileTest.tell() <= 2000:    #if file is small, test it
			self.FileTest.seek(0)
			for x in self.FileTest:
				if "404" in x and "Not Found" in x or "Could not open the requested SVN filesystem" in x or "The requested URL could not be retrieved" in x:
					os.remove(local)
					self.ReturnCode="2"
					break
		self.FileTest.close()	

		#print "Fini dans "+local
		self.txtEstimation.Destroy()
		self.release_download(self.ReturnCode)

	def agree(self, event):
		if(self.Menu.IsChecked()):
			self.NextButton.Enable(True)
		else:
			self.NextButton.Enable(False)

	def AutoReload(self, event):
		if(os.path.exists(self.file_id)):
			self.fichier = open(self.file_id,"r").readlines()
			try :
				if(self.gauge_i < 2):
					self.gauge_i += 1
				else:
					self.gauge.Pulse()
					self.gauge_i = 0
				
			except :
				pass

			if(self.fichier != self.oldfichier):
				if(len(self.fichier) > 0):
					if(self.fichier[0] == "MsgIn\n"):
						if(len(self.fichier) > 1):
							if(self.fichier[1] != "pulse\n" and self.fichier[1] != "set_text\n"):
								self.Destroy_all()

						if(len(self.fichier) > 1):
							if(self.fichier[1] == "pulse\n"):
								self.pulsebar.SetValue(int(self.fichier[2])/2)

							if(self.fichier[1] == "set_text\n"):
								try :
									self.texte_bis.Destroy()
								except :
									pass
								self.texte_bis = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80+self.gauge_space*13+18))
								self.texte_bis.SetFont(self.fontText)

							if(self.fichier[1] == "champ\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								space=self.fichier[2].count("\\n")+1
								self.champ = wx.TextCtrl(self.panel, -1, self.fichier[4].replace("\n",""),pos=(20,80+space*13),size=(300,25))
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_champ)	
							
							if(self.fichier[1] == "browse\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								space=self.fichier[2].count("\\n")+1
								self.browse = wx.Button(self.panel, 103, _("Browse"), (330, 80+space*13), (80,25))
								self.champ = wx.TextCtrl(self.panel, -1, self.fichier[4].replace("\n",""),pos=(20,80+space*13),size=(300,25))
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_champ)	
								wx.EVT_BUTTON(self, 103,  self.Parcourir)

							if(self.fichier[1] == "menu\n" or self.fichier[1] == "menu_num\n" or self.fichier[1] == "menu_list\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								space = self.fichier[2].count("\\n")+1
								cut = self.fichier[5].replace("\n","")
								self.areaList = string.split(self.fichier[4].replace("\n",""),cut)
								if(self.fichier[1] == "menu\n" or self.fichier[1] == "menu_num\n"):
									self.Menu = wx.ListBox(self.panel, 103, pos=(20,100),size=(460,230), choices=self.areaList)
									self.Menu.Select(0)
								else:
									self.Menu = wx.ComboBox(self.panel, 103, value=self.areaList[0], pos=(20, 80+space*13), choices=self.areaList, style=wx.CB_READONLY)
									if(self.fichier[6] != "\n"):
										self.Menu.SetValue(self.fichier[6].replace("\n",""))
				
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								if(self.fichier[1] == "menu\n"):
									wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_menu)	
									wx.EVT_LISTBOX_DCLICK(self, 103, self.release_menu)
								if(self.fichier[1] == "menu_num\n"):	
									wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_menu_num)	
									wx.EVT_LISTBOX_DCLICK(self, 103, self.release_menu_num)
								if(self.fichier[1] == "menu_list\n"):
									wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_menu_list)	

							if(self.fichier[1] == "checkbox_list\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								self.titre.SetFont(self.fontText)
								self.scrolled_panel = wx.ScrolledWindow(self.panel, -1, pos=(20,100), size=(460,230), style=wx.RAISED_BORDER|wx.HSCROLL|wx.VSCROLL)
								self.scrolled_panel.SetBackgroundColour((255,255,255))								
								
								cut = self.fichier[5].replace("\n","")
								self.areaList = string.split(self.fichier[4].replace("\n",""),cut)

								self.i = 0
								self.item_check = []
								while(self.i < len(self.areaList)):
									self.item_check.append(wx.CheckBox(self.scrolled_panel, -1, pos=(0,(self.i*25)),label=str(self.areaList[self.i])))
									#self.item_name = wx.StaticText(self.scrolled_panel, -1, size=(200,20), pos=(30,(self.i*20)+5))
									self.i+=1

								self.scrolled_panel.SetVirtualSize((0,self.i*(25)))
								self.scrolled_panel.SetScrollRate(0,25)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_checkboxes)	

							if(self.fichier[1] == "attendre\n"):
								self.DrawHeader()
								self.timer_attendre = wx.Timer(self, 1)
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								space=self.fichier[2].count("\\n")+1
								self.gauge = wx.Gauge(self.panel, -1, 50, pos=(20,80+space*13), size=(475, 17))
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release)	
								self.p = Popen(self.fichier[4],shell=True,stdin=PIPE,stdout=PIPE,close_fds=True)
								self.Bind(wx.EVT_TIMER, self.DemanderPourcent, self.timer_attendre)
								self.timer.Stop()						
								self.timer_attendre.Start(50)

							if(self.fichier[1] == "attendre_signal\n" or self.fichier[1] == "pulsebar\n"):
								self.DrawHeader()
								self.timer_attendre = wx.Timer(self, 1)
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								space=self.fichier[2].count("\\n")+1
								self.gauge_space = space
								if(self.fichier[1] == "attendre_signal\n"):
									self.gauge = wx.Gauge(self.panel, -1, 50, pos=(20,80+space*13), size=(475, 17))
								else :
									self.pulsebar = wx.Gauge(self.panel, -1, 50, pos=(20,80+space*13), size=(475, 17))
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								self.NextButton.Enable(False)

							if(self.fichier[1] == "download\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								space=self.fichier[2].count("\\n")+1
								self.gauge = wx.Gauge(self.panel, -1, 50, pos=(20,80+space*13), size=(475, 17))
								self.txtEstimation = wx.StaticText(self.panel, -1, "", pos=(20,98+space*13))
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								self.NextButton.Enable(False)	
								self.DownloadFile(self.fichier[4].replace("\n",""), self.fichier[5].replace("\n",""))
								#wx.EVT_BUTTON(self, 300, self.release)
						
							if(self.fichier[1] == "get_games\n"):
								self.images = wx.ImageList(22, 22)
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.texte.SetFont(self.fontText)
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
			   					self.Menu = wx.TreeCtrl(self.panel, 111, style=wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT|wx.RAISED_BORDER, pos=(20,100),size=(460,230))
			   					self.Menu.SetImageList(self.images)
			   					self.Menu.SetSpacing(0);
								self.add_games()
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_menugame)	
								wx.EVT_TREE_ITEM_ACTIVATED(self, 111, self.release_menugame)	

							if(self.fichier[1] == "message\n" or self.fichier[1] == "message_image\n"):
								self.DrawHeader()
								if(self.fichier[1] == "message\n"):
									self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								else :
									self.bitmap = wx.Bitmap(self.fichier[4].replace("\n",""))
									self.image = wx.StaticBitmap(self.panel, -1, self.bitmap, (20,80), wx.DefaultSize)
									self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(self.bitmap.GetWidth()+40,80))
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.texte.SetFont(self.fontText)
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release)	

							if(self.fichier[1] == "licence\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.champ = wx.TextCtrl(self.panel, 103, pos=(20,100),size=(460,220),style=wx.TE_MULTILINE | wx.CB_READONLY)
								self.texte.SetFont(self.fontText)
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								self.champ.SetValue(open(self.fichier[4].replace("\n",""),"r").read())
								self.titre.SetFont(self.fontText)
								self.Menu = wx.CheckBox(self.panel, 302, _("I Agree"), pos=(20,325))

								self.DrawCancel()
								self.DrawNext()
								self.NextButton.Enable(False)
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release)	
								wx.EVT_CHECKBOX(self, 302, self.agree)

							if(self.fichier[1] == "question\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, self.fichier[2].replace("\\n","\n"),pos=(20,80))
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.texte.SetFont(self.fontText)
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, self.fichier[3],pos=(20,30), size=(340,356))
								self.titre.SetFont(self.fontText)
								self.CancelButton = wx.Button(self.footer, wx.ID_NO, pos=(430,2),size=(85,37))
								self.NextButton = wx.Button(self.footer, wx.ID_YES, pos=(340,2), size=(85,37))
								wx.EVT_BUTTON(self, wx.ID_YES, self.release_yes)	
								wx.EVT_BUTTON(self, wx.ID_NO, self.release_no)	

							if(self.fichier[1] == "make_shortcut\n"):
								self.DrawHeader()
								self.texte = wx.StaticText(self.panel, -1, _("Create a shortcut: "),pos=(20,80))
								self.titre_header = wx.StaticText(self.header, -1, _("PlayOnLinux Wizard"),pos=(5,5), size=(340,356))
								self.texte.SetFont(self.fontText)
								self.titre_header.SetFont(self.fontTitre)
								self.titre = wx.StaticText(self.header, -1, _("Do you want a shortcut for: ")+self.fichier[2].replace("\n","")+" ?",pos=(20,30), size=(340,356))
								self.desktop = wx.CheckBox(self.panel, -1, _("On your desktop"),pos=(25,105))
								self.menu = wx.CheckBox(self.panel, -1, _("In your menu"),pos=(25,125))

								self.titre.SetFont(self.fontText)
								self.DrawCancel()
								self.DrawNext()
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release_icons)	

					
							if(self.fichier[1] == "free_presentation\n"):
								self.MainPanel = wx.Panel(self.panel, -1, pos=(150,0), size=(370,356))
								self.MainPanel.SetBackgroundColour((255,255,255))
								#self.titre = wx.StaticText(self.MainPanel, -1, "Welcome in PlayOnLinux installation program",pos=(5,5), size=(340,356))
								self.titre = wx.StaticText(self.MainPanel, -1, self.fichier[2],pos=(5,5), size=(340,356))
								self.titre.Wrap(280)
								self.texte = wx.StaticText(self.MainPanel, -1, self.fichier[3].replace("\\n","\n"),pos=(5,50))
								self.texte.Wrap(360)
								self.DrawCancel()
								self.DrawNext()
								self.titre.SetFont(self.fontTitre)	
								self.texte.SetFont(self.fontText)
								wx.EVT_BUTTON(self, wx.ID_FORWARD, self.release)					
								self.DrawImage()

							if(self.fichier[1] == "exit\n"):
								os.remove(self.file_id)
								sys.exit()

						self.oldfichier = self.fichier

	
	
class Ok_message(wx.App):        #instance principale classe application
     def OnInit(self):
        ok_boite = Ok_frame("PlayOnLinux")
	ok_boite.Center(wx.BOTH)
        ok_boite.Show(True)
        self.SetTopWindow(ok_boite)
        return True



ok_message = Ok_message() #création de l'application
ok_message.MainLoop()
