#!/usr/bin/python 
# -*- coding:Utf-8 -*- 
# L'encodage Utf-8 sera a joindre dans tous les fichiers, sinon bug d'accents...

# Copyright (C) 2007 Pâris Quentin
#  		     Cassarin-Grand Arthur

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

import wxversion, os, getopt, sys, urllib, signal, string
wxversion.select("2.8")
import wx

ID_CANCEL = 101
ID_NEXT = 102

import lib.Variables as Variables
import lib.lng
lib.lng.Lang()

class Variables:      #classe qui va contenir les différentes variables (pas de variables globales)
	if len(sys.argv) > 8:
		titre = sys.argv[1]      #le titre dans la fenêtre
		texte = sys.argv[2]      #le contenu du message de la fenêtre
		numeroEtape = sys.argv[3]       #le numro actuel des étapes
		nombreEtape = sys.argv[4]        #Le numéro maximal d'étape
		cancel_present = sys.argv[5]	#Faut t'il afficher le bouton annuler ?
		image = sys.argv[6] # C'est cool si on peut choisir l'image ;)
		playonlinux_env = os.popen("printf $PLAYONLINUX", "r").read() #Recuperer le repertoire de PlayOnLinux
		theme_env = os.popen("printf $POL_THEME", "r").read() #Recuperer le theme utilisé
		image_use = playonlinux_env+"/themes/"+theme_env+"/"+image
		etape_txt = _("Step")+" "+numeroEtape+" "+_("of")+" "+nombreEtape
		chaine = sys.argv[7]
		where_to_cut = sys.argv[8]
		next = sys.argv[9]
		sendId = sys.argv[10]
		if(where_to_cut == "--cut-line"):
			areaList = string.split(chaine,"\n")
		else:
			areaList = string.split(chaine,where_to_cut)

	else:
		print "Il manque des arguments"
		sys.exit(255)


class Ok_frame(wx.Frame): #fenêtre principale
	def __init__(self, titre):
		wx.Frame.__init__(self, None, -1, title = titre, style = wx.CLOSE_BOX | wx.MINIMIZE_BOX, size = (520, 290))
		self.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))
		self.panelFenp = wx.Panel(self, -1)
		self.fontTexte = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "", wx.FONTENCODING_DEFAULT)

		self.txtTitre = wx.StaticText(self.panelFenp, -1, Variables.titre, (20,25), wx.DefaultSize)
		self.txtTitre.SetFont(self.fontTexte)
		self.txtTexte = wx.StaticText(self.panelFenp, -1, Variables.texte, (155,65), wx.DefaultSize)
		self.txtTexte.Wrap(330)
		if Variables.nombreEtape != "0":		
			self.txtEtape = wx.StaticText(self.panelFenp, -1, Variables.etape_txt, (20, 265), wx.DefaultSize)
			
		self.buttonSuivant = wx.Button(self.panelFenp, ID_NEXT, Variables.next, (425, 250), wx.DefaultSize)
		

		if Variables.cancel_present == "1":		
			self.buttonAnnuler = wx.Button(self.panelFenp, ID_CANCEL, _("Cancel"), (330, 250), wx.DefaultSize)
		self.Menu = wx.ListBox(self.panelFenp, 103, pos=wx.Point(145, 100),size=(345, 130), choices=Variables.areaList)
		self.Menu.Select(0)
		self.imageLogo = wx.Bitmap(Variables.image_use)
		self.canvasLogo = wx.StaticBitmap(self.panelFenp, -1, self.imageLogo, (30,65), wx.DefaultSize)


		wx.EVT_BUTTON(self, ID_CANCEL,  self.Cancel)
   		wx.EVT_BUTTON(self, ID_NEXT,  self.Next)
		wx.EVT_LISTBOX_DCLICK(self, 103, self.Next)

	def Cancel(self, event):
		#print("Canceled") #Indiquera à PlayOnLinux bash qu'il faut arreter l'instalaltion
		sys.exit(1)        	
		self.Close()        
	
	def Next(self, event):
		if Variables.sendId == "1":
			self.chaine_e = self.Menu.GetSelection()
		else :
			self.chaine_e = Variables.areaList[self.Menu.GetSelection()]

		print self.chaine_e
        	self.Close()   

class Ok_message(wx.App):        #instance principale classe application
     def OnInit(self):
        ok_boite = Ok_frame("PlayOnLinux")
	ok_boite.Center(wx.BOTH)
        ok_boite.Show(True)
        self.SetTopWindow(ok_boite)
        return True


ok_message = Ok_message() #création de l'application
ok_message.MainLoop()
