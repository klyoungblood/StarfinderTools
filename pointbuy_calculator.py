#!/usr/bin/env python

#python 2 uses Tkinter, python 3 tkinter
try:
	import Tkinter as tk
except ImportError:
	import tkinter as tk
import json
import os
import webbrowser

themes = {}
themenames = []
races = {}
racenames = []
classes = {}
classnames = []
topframe=0
charframe=0
ctheme=0
crace=0
cclass=0
cStr=0
cDex=0
cCon=0
cInt=0
cWis=0
cCha=0
cTVar=0
cRVar=0
top=0

cVars=[]

#character = {'Str':10,'Dex':10,'Con':10,'Int':10,'Wis':10,'Cha':10}
abilities = ['Str','Dex','Con','Int','Wis','Cha']
#modstrings = ["-5","-5","-4","-4","-3","-3","-2","-2","-1","-1","0","0","+1","+1","+2","+2","+3","+3","+4"]

lowmods = [-5,-5,-4,-4,-3,-3,-2,-2,-1,-1]

def getmodstring(abmod):
	if(abmod <1):
		return str(abmod)
	else:
		return "+"+str(abmod)

def getabmod(ascore):
	mod = 0
	if ascore > 10:
		mod = (ascore - 10) / 2
	if ascore < 9:
		mod = lowmods[ascore]
	return mod
	
def clearrace(race):
	for ab in abilities:
		race[ab] = 0

def cleartheme(theme):
	for ab in abilities:
		theme[ab] = 0
		
def load_classes():
	global classes
	global classnames
	datadir="data"
	for dir in os.listdir(datadir):
		classfile = os.path.join(datadir,dir,"classes.json")
		if os.path.isfile(classfile):
			with open(classfile) as json_data:
				classset = json.load(json_data)
				for charclass in classset:
					classnames.append(charclass['name'])
					classes.setdefault(charclass['name'],charclass)
#	print classes
					
	
def load_themes():
	global themes
	global themenames
	datadir="data"
	for dir in os.listdir(datadir):
		themesfile = os.path.join(datadir,dir,"themes.json")
		if os.path.isfile(themesfile):
			with open(themesfile) as json_data:
				themeset = json.load(json_data)
				for theme in themeset:
					theme.setdefault('Str',0)
					theme.setdefault('Dex',0)
					theme.setdefault('Con',0)
					theme.setdefault('Int',0)
					theme.setdefault('Wis',0)
					theme.setdefault('Cha',0)
					theme.setdefault('Any',0)
					themenames.append(theme['name'])
					themes.setdefault(theme['name'],theme)
	#print themes
	

def load_races():
	global races
	global racenames
	datadir="data"
	for dir in os.listdir(datadir):
		racesfile = os.path.join(datadir,dir,"races.json")
		if os.path.isfile(racesfile):
			with open(racesfile) as json_data:
				raceset = json.load(json_data)
				for race in raceset:
					race.setdefault('Str',0)
					race.setdefault('Dex',0)
					race.setdefault('Con',0)
					race.setdefault('Int',0)
					race.setdefault('Wis',0)
					race.setdefault('Cha',0)
					race.setdefault('Any',0)
					race.setdefault('Boon', False)
					racenames.append(race['name'])
					races.setdefault(race['name'],race)
	#print races

class Application(tk.Frame):
	global top
	global topframe
	global charframe
	
	def __init__(self, master, **kwargs):
		global topframe
		global charframe
		global cStr
		global cDex
		global cCon
		global cInt
		global cWis
		global cCha
		global cTVar
		global cRVar
		global cVars
		master.minsize(width=200, height=200)
		top=tk.Frame.__init__(self, master)
		top=self.winfo_toplevel()
		top.rowconfigure(2, weight=1)            
		top.columnconfigure(1, weight=1)       
		#self.rowconfigure(0, weight=1)           
		topframe=tk.Frame(top)
		topframe.grid(row=1,column=1,sticky=tk.N)
		charframe=tk.Frame(top)
		charframe.grid(row=2,column=1,sticky=tk.NW)
		cStr = tk.IntVar(charframe)
		cDex = tk.IntVar(charframe)
		cCon = tk.IntVar(charframe)
		cInt = tk.IntVar(charframe)
		cWis = tk.IntVar(charframe)
		cCha = tk.IntVar(charframe)
		cStr.set(0)
		cDex.set(0)
		cCon.set(0)
		cInt.set(0)
		cWis.set(0)
		cCha.set(0)
		cStr.trace("w",self.refreshchar)
		cDex.trace("w",self.refreshchar)
		cCon.trace("w",self.refreshchar)
		cInt.trace("w",self.refreshchar)
		cWis.trace("w",self.refreshchar)
		cCha.trace("w",self.refreshchar)
		cVars.append(cStr)
		cVars.append(cDex)
		cVars.append(cCon)
		cVars.append(cInt)
		cVars.append(cWis)
		cVars.append(cCha)
		cTVar = tk.StringVar(charframe)
		cTVar.set(abilities[0])
		cTVar.trace("w",self.refreshchar)
		cRVar = tk.StringVar(charframe)
		cRVar.set(abilities[0])
		cRVar.trace("w",self.refreshchar)
		
		self.menubar()
		self.racesmenu()
		self.themesmenu()
		self.classesmenu()
		self.refreshchar(top)
		
	def about(self):
		webbrowser.open_new(r"about.html")
		
	def confirmquit(self):
		toplevel = tk.Toplevel()
		label1 = tk.Label(toplevel, text="Really exit Starfinder tools?")
		label1.grid(row=1,column=0,columnspan=4)
		but1 = tk.Button(toplevel, text="Quit", command=root.quit)
		but1.grid(row=2,column=1, sticky=tk.S,pady=5)
		but2 = tk.Button(toplevel, text="Cancel", command=toplevel.destroy)
		but2.grid(row=2,column=2, sticky=tk.S, pady=5)
		
		toplevel.focus_force()
		
	def menubar(self):
		menubar = tk.Menu(root)
		menubar.add_command(label="Quit", command=self.confirmquit)
		menubar.add_command(label="About", command=self.about)
		root.config(menu=menubar)
		
	def refreshchar(self, dummy1=None, dummy2=None, dummy3=None):
		global charframe
		global topframe
		global top
		charframe.destroy()
		charframe=tk.Frame(top)
		charframe.grid(row=2,column=1,sticky=tk.NW)
		self.charstats()
		
	def racesmenu(self):
		global crace
		crace = tk.StringVar(topframe)
		crace.set(racenames[0])
		crace.trace("w",self.refreshchar)
		w = tk.OptionMenu(topframe, crace, *racenames)
		w.grid(row=0,column=0, sticky=tk.NW)
		
	def themesmenu(self):
		global ctheme
		ctheme = tk.StringVar(topframe)
		ctheme.set(themenames[0])
		ctheme.trace("w",self.refreshchar)
		w = tk.OptionMenu(topframe, ctheme, *themenames)
		w.grid(row=0,column=1, sticky=tk.N)
		
	def classesmenu(self):
		global cclass
		cclass = tk.StringVar(topframe)
		cclass.set(classnames[0])
		cclass.trace("w",self.refreshchar)
		w = tk.OptionMenu(topframe, cclass, *classnames)
		w.grid(row=0,column=2, sticky=tk.NE)
		
	def charstats(self):
		i=1
		settheme = ctheme.get()
		setrace = crace.get()
		setclass = cclass.get()
		keyab = classes[setclass]['Key']
		abiwarning=False
		abtotals={}
		
		if themes[settheme]['Any'] > 0:
			dTVar = tk.OptionMenu(charframe, cTVar, *abilities)
			dTVar.grid(row=0, column=3, sticky=tk.W)
			cleartheme(themes[settheme])
			themes[settheme][cTVar.get()]=themes[settheme]['Any']
			
		if races[setrace]['Any'] > 0:
			dRVar = tk.OptionMenu(charframe, cRVar, *abilities)
			dRVar.grid(row=0, column=2, sticky=tk.W)
			clearrace(races[setrace])
			races[setrace][cRVar.get()]=races[setrace]['Any']
		
		for ab in abilities:
			if(ab == keyab):
				lab=tk.Label(charframe, text=ab, fg="blue")
			else:
				lab=tk.Label(charframe, text=ab)
			lab.grid(row=i, column=0, sticky=tk.E)
			lbscore=tk.Label(charframe, text="10")
			lbscore.grid(row=i, column=1, sticky=tk.W)
			if races[setrace][ab] > 0:
				lrscore=tk.Label(charframe, text="+"+str(races[setrace][ab]))
				lrscore.grid(row=i, column=2, sticky=tk.W)
			elif races[setrace][ab] < 0:
				lrscore=tk.Label(charframe, text=str(races[setrace][ab]))
				lrscore.grid(row=i, column=2, sticky=tk.W)
			if themes[settheme][ab] > 0:
				ltscore=tk.Label(charframe, text="+"+str(themes[settheme][ab]))
				ltscore.grid(row=i, column=3, sticky=tk.W)
			
			lplus=tk.Label(charframe, text="+")
			lplus.grid(row=i, column=4, sticky=tk.W)
			
			
			lequals=tk.Label(charframe, text="=")
			lequals.grid(row=i, column=6, sticky=tk.W)
			
			tAB = 10 + races[setrace][ab] + themes[settheme][ab] + cVars[i-1].get()
			abtotals.setdefault(ab,tAB)
			if tAB > 18:
				lAB = tk.Label(charframe, text=str(tAB)+" (illegal)",fg="red")
				abiwarning=True
			else:
				lAB = tk.Label(charframe, text=str(tAB)+" ("+getmodstring(getabmod(tAB))+")")
			lAB.grid(row=i, column=7, sticky=tk.W)
			i+=1
				
		pointarray = [0,1,2,3,4,5,6,7,8,9,10]
		dStr = tk.OptionMenu(charframe,cStr, *pointarray)
		dStr.grid(row=1, column=5, sticky=tk.W)
		
		dDex = tk.OptionMenu(charframe,cDex, *pointarray)
		dDex.grid(row=2, column=5, sticky=tk.W)
		
		dCon = tk.OptionMenu(charframe,cCon, *pointarray)
		dCon.grid(row=3, column=5, sticky=tk.W)
				
		dInt = tk.OptionMenu(charframe,cInt, *pointarray)
		dInt.grid(row=4, column=5, sticky=tk.W)
				
		dWis = tk.OptionMenu(charframe,cWis, *pointarray)
		dWis.grid(row=5, column=5, sticky=tk.W)
				
		dCha = tk.OptionMenu(charframe,cCha, *pointarray)
		dCha.grid(row=6, column=5, sticky=tk.W)

		points = cStr.get() + cDex.get() + cCon.get() + cInt.get() + cWis.get() + cCha.get()
		
		tHP = races[setrace]['HP'] + classes[setclass]['HP']
		tSP = classes[setclass]['SP'] + getabmod(abtotals['Con'])
		tRP = 1 + getabmod(abtotals[keyab])
		
		statslabel = tk.Label(charframe, text="Hit Points (HP): "+str(tHP)+"\nStamina (SP): "+str(tSP)+"\nResolve (RP): "+str(tRP))
		statslabel.grid(row=8, column=0, columnspan=8, sticky=tk.S)
		
		if points == 10:
			plabel=tk.Label(charframe, text=str(points)+"/10 points spent.")
		else:
			plabel=tk.Label(charframe, text=str(points)+"/10 points spent.",fg="red")
		plabel.grid(row=7, column=0, columnspan=8, sticky=tk.S)
		
		if abiwarning:
			alabel=tk.Label(charframe, text="No starting ability score may exceed 18!",fg="red")
			alabel.grid(row=9, column=0, columnspan=8, sticky=tk.S)
			
		if races[setrace]['Boon']:
			wlabel=tk.Label(charframe, text="Boon required to play this character in Starfinder Society.")
			wlabel.grid(row=10, column=0, columnspan=8, sticky=tk.S)
		
load_classes()
load_themes()		
load_races()
root=tk.Tk()
app = Application(root)
app.master.title('Starfinder Point Buy Calculator')
app.mainloop()