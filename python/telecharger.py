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

import wxversion, os, getopt, sys, urllib, signal, urlparse 
wxversion.select("2.8")
import wx

ID_CANCEL = 10
ID_NEXT = 11

import lib.Variables as Variables
import lib.lng
lib.lng.Lang()

class Variables:     
    if len(sys.argv) > 7:    #classe qui va contenir les différentes variables (pas de variables globales)
        titre = sys.argv[1]      #le titre dans la fenêtre
        url = sys.argv[2]        #l'url à chargé
        localB = sys.argv[3]     #le fichier en local (destination) sans le nom du fichier
        texte = sys.argv[4]      #le contenu du message de la fenêtre
        numeroEtape = sys.argv[5]        #le numro actuel des étapes
        nombreEtape = sys.argv[6]        #Le numéro maximal d'étape
        cancel_present = sys.argv[7]     #Desactivation/Activation du bouton annuler
        image = sys.argv[8]
        autoexit = sys.argv[9]
	next = sys.argv[10]
        partLoaded = ""
        taille_fichier_mo = ""
        estimation_txt = ""    #le texte en bas de la gauge
        nb_blocs_max = 0
        
        playonlinux_env = os.popen("printf $PLAYONLINUX", "r").read() #Recuperer le repertoire de PlayOnLinux
        theme_env = os.popen("printf $POL_THEME", "r").read() #Recuperer le theme utilisé
        etape_txt = _("Step")+" "+numeroEtape+" "+_("of")+" "+nombreEtape
        image_use = playonlinux_env+"/themes/"+theme_env+"/"+image
                 
    else:
		print "Arguments missing"
		exit(255)

class FenpTelechargerUrl(wx.Frame): #fenêtre principale
    
    def __init__(self, titre):
        wx.Frame.__init__(self, None, -1, title = titre, style = wx.CLOSE_BOX | wx.MINIMIZE_BOX, size = (520, 290))
	self.i = 0
	#self.timer = wx.Timer(self, 1)
	self.SetIcon(wx.Icon(Variables.playonlinux_env+"/etc/playonlinux.png", wx.BITMAP_TYPE_ANY))
        self.panelFenp = wx.Panel(self, -1)
        self.fontTexte = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "", wx.FONTENCODING_DEFAULT)
        self.txtTitre = wx.StaticText(self.panelFenp, -1, Variables.titre, (20,25), wx.DefaultSize, wx.ALIGN_CENTER)
        self.txtTitre.SetFont(self.fontTexte)
        self.txtTexte = wx.StaticText(self.panelFenp, -1, _("Click on download to start."), (155,120), wx.DefaultSize)
        self.txtTexte.Wrap(330)
        
        if Variables.nombreEtape != "0":	
            self.txtEtape = wx.StaticText(self.panelFenp, -1, Variables.etape_txt, (20, 265), wx.DefaultSize)
        self.buttonSuivant = wx.Button(self.panelFenp, ID_NEXT, _("Please wait while the game is downloaded..."), (425, 250), wx.DefaultSize)
        
        if Variables.cancel_present == "1":	
            self.buttonAnnuler = wx.Button(self.panelFenp, ID_CANCEL, _("Cancel"), (330, 250), wx.DefaultSize)
            
        self.imageLogo = wx.Bitmap(Variables.image_use)
        self.canvasLogo = wx.StaticBitmap(self.panelFenp, -1, self.imageLogo, (30,65), wx.DefaultSize)
        self.progressBar = wx.Gauge(self.panelFenp, -1, 100, (155,70), (245, 17), style = wx.GA_HORIZONTAL)
        self.txtEstimation = wx.StaticText(self.panelFenp, -1, Variables.estimation_txt, (155,90), wx.DefaultSize)
       
        #self.Bind(wx.EVT_TIMER, self.DownloadFile(Variables.url, Variables.localB), self.timer)
    	#self.timer.Start(1000)
        
        #Evenements
        wx.EVT_BUTTON(self, ID_CANCEL,  self.Cancel)
        wx.EVT_BUTTON(self, ID_NEXT,  self.Next)
	if(Variables.next == "1"):
	        wx.EVT_ACTIVATE(self, self.Next) 
        
    def Cancel(self, event):
        print("Canceled") #Indiquera à PlayOnLinux bash qu'il faut arreter l'instalaltion
       	self.Close()   
                  
    def Next(self, event):
	if(self.i == 0):
		self.txtTexte.Destroy()
		self.txtTexte = wx.StaticText(self.panelFenp, -1, Variables.texte, (155,120), wx.DefaultSize)
		self.buttonSuivant.Destroy()
		self.buttonSuivant = wx.Button(self.panelFenp, ID_NEXT, _("Next"), (425, 250), wx.DefaultSize)
		self.DownloadFile(Variables.url, Variables.localB)
		self.txtTexte.Destroy()
		self.txtTexte = wx.StaticText(self.panelFenp, -1, _("Download finished"), (155,120), wx.DefaultSize)
		
	if(self.i == 1 or Variables.autoexit == "1"):
        	self.Close()  
	self.i = 1
	
    def onHook(self, nb_blocs, taille_bloc, taille_fichier):
        Variables.nb_blocs_max = taille_fichier / taille_bloc
        self.progressBar.SetRange(Variables.nb_blocs_max)
        self.progressBar.SetValue(nb_blocs)
        
        tailleFichierB = float(taille_fichier / 1048576.0)
        octetsLoadedB = float((nb_blocs * taille_bloc) / 1048576.0)
        octetsLoadedN = round(octetsLoadedB, 1)
        tailleFichierN = round(tailleFichierB, 1)
        
        Variables.estimation_txt = "Quota : " + str(octetsLoadedN) + " "+_("sur")+" " + str(tailleFichierN) + " mo "+("downloaded")
        
        self.txtEstimation.SetLabel(Variables.estimation_txt)
        wx.Yield()
         
    
    def DownloadFile(self, url, localB):    #url = url a récupérer, localB le fichier où enregistrer la modification sans nom de fichier
        self.buttonSuivant.Enable(False)
        chemin = urlparse.urlsplit(url)[2] 
        nomFichier = chemin.split('/')[-1] 
        local = localB + nomFichier 
        urllib.urlretrieve(url, local, reporthook = self.onHook)
        self.buttonSuivant.Enable(True)
           

class TelechargerURLApp(wx.App):        #instance principale classe application
    
    def DemmarageGUI(self):
        
        return True  
     
    def OnInit(self):
        fenpTelecharger = FenpTelechargerUrl("PlayOnLinux")
        fenpTelecharger.Center(wx.BOTH)
        fenpTelecharger.Show(True)
        self.SetTopWindow(fenpTelecharger)
        
        return True
            
                                
telechargerUrl = TelechargerURLApp()        #création de l'application
telechargerUrl.MainLoop()
