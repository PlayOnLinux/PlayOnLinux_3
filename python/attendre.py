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

from subprocess import Popen,PIPE
import wxversion, os, getopt, sys, urllib, signal
wxversion.select("2.8")
import wx

import lib.Variables as Variables
import lib.lng
lib.lng.Lang()

ID_CANCEL = 101
ID_NEXT = 102

	
class Variables:      #classe qui va contenir les différentes variables (pas de variables globales)
	if len(sys.argv) > 7:
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
		cmd = sys.argv[7]
		autoquit = sys.argv[8]
		message_fin = sys.argv[9]
		next = sys.argv[10]
		gauge = sys.argv[11]

	else:
		print "Il manque des arguments"
		exit(255)

class Ok_frame(wx.Frame): #fenêtre principale
	def __init__(self, titre):
		wx.Frame.__init__(self, None, -1, title = titre, style = wx.CLOSE_BOX | wx.MINIMIZE_BOX, size = (520, 290))
		# style = wx.CLIP_CHILDREN = pour virer les bordures
		self.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))

		self.p = Popen(Variables.cmd,shell=True,stdin=PIPE,stdout=PIPE,close_fds=True)
		self.i = 0
		self.timer = wx.Timer(self, 1)
		self.count=0
		self.panelFenp = wx.Panel(self, -1)
		self.fontTexte = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "", wx.FONTENCODING_DEFAULT)

		self.txtTitre = wx.StaticText(self.panelFenp, -1, Variables.titre, (20,25), wx.DefaultSize)
		self.txtTitre.SetFont(self.fontTexte)
		self.txtTexte = wx.StaticText(self.panelFenp, -1, Variables.texte, (155,65), wx.DefaultSize)
		self.txtTexte.Wrap(330)
		self.gauge = wx.Gauge(self.panelFenp, -1, 50, (155,120), (245, 17))
		if Variables.nombreEtape != "0":		
			self.txtEtape = wx.StaticText(self.panelFenp, -1, Variables.etape_txt, (20, 265), wx.DefaultSize)
			
		self.buttonSuivant = wx.Button(self.panelFenp, ID_NEXT, Variables.next, (425, 250), wx.DefaultSize)
		self.buttonSuivant.Enable(False)
		if Variables.cancel_present == "1":		
			self.buttonAnnuler = wx.Button(self.panelFenp, ID_CANCEL, _("Cancel"), (330, 250), wx.DefaultSize)
		self.imageLogo = wx.Bitmap(Variables.image_use)
		self.canvasLogo = wx.StaticBitmap(self.panelFenp, -1, self.imageLogo, (30,65), wx.DefaultSize)
		
		self.Bind(wx.EVT_TIMER, self.DemanderPourcent, self.timer)
		self.timer.Start(50)

		wx.EVT_BUTTON(self, ID_CANCEL,  self.Cancel)
   		wx.EVT_BUTTON(self, ID_NEXT,  self.Next)

	def DemanderPourcent(self,plouf):
		if self.p.poll() == None:
			if Variables.gauge == "0":
			        self.gauge.Pulse()
			else:
				#if i != 50:				
				self.gauge.SetValue(self.i)
				self.i = self.i+2
		else:
		        print "End"
			self.gauge.SetValue(50)
		        print self.p.stdout.read()
			self.timer.Stop()
			self.buttonSuivant.Enable(True)	
			if Variables.message_fin != "":
				self.txtTexte.Destroy()
				self.txtFin = wx.StaticText(self.panelFenp, -1, Variables.message_fin, (155,65), wx.DefaultSize)
			if Variables.autoquit == "1":
				self.Close()

	def Cancel(self, event):
		print("Canceled") #Indiquera à PlayOnLinux bash qu'il faut arreter l'instalaltion
        	self.Close()        
	
	def Next(self, event):
        	self.Close()   

class Ok_message(wx.App):        #instance principale classe application
     def OnInit(self):
        ok_boite = Ok_frame("PlayOnLinux")
	ok_boite.Center(wx.BOTH)
        ok_boite.Show(True)
	#ok_boite.DemanderPourcent()
        #self.SetTopWindow(ok_boite)
	
        return True

ok_message = Ok_message() #création de l'application
ok_message.MainLoop()
