#
import os, errno
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
import pdb

def make_dirs(dirname):
    """
    Ensure that a named directory exists; if it does not, attempt to create it.
    """
    try:
        os.makedirs(dirname)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

def savename_cleaner(name):
	c_name = name.replace("<", "").replace(">", "").replace(".", "").replace("&", "_").replace(" ", "")
	return c_name

def labels():
	CMSLABL = TLatex()
	CMSLABL.SetNDC()	
	CMSLABL.SetTextSize(0.045)
	PRELABL = TLatex()
	PRELABL.SetNDC()
	PRELABL.SetTextSize(0.04)
	THILABL = TLatex()
	THILABL.SetNDC()
	THILABL.SetTextSize(0.035)
	CUTLABL = TLatex()
	CUTLABL.SetNDC()
	CUTLABL.SetTextSize(0.02)
	INTLABL = TLatex()
	INTLABL.SetNDC()
	INTLABL.SetTextSize(0.02)
	return CMSLABL, PRELABL, THILABL, CUTLABL, INTLABL

def quickplot(File, tree, plot, var, Cut, Weight): # Fills  a plot from a file (needs to have a TTree called "tree"...)
        temp = plot.Clone("temp") # Allows to add multiple distributions to the plot
        chain = ROOT.TChain(tree)
        chain.Add(File)
        chain.Draw(var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff") # Actual plotting (and making of the cut + Weighing if necsr)
        plot.Add(temp)

def quick2dplot(File, tree, plot, var, var2, Cut, Weight): # Same as above, but 2D plotter
        temp = plot.Clone("temp")
        chain = ROOT.TChain(tree)
        chain.Add(File)
        chain.Draw(var2+":"+var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff")
        plot.Add(temp)

def FindAndSetMax(someset, mult=1.35):
        maximum = 0.0
        for i in someset:
                i.SetStats(0)
                t = i.GetMaximum()
                if t > maximum:
                        maximum = t
        for j in someset:
                j.GetYaxis().SetRangeUser(0,maximum*mult)
	return maximum*mult

def make_signal_point(name, cut, sig, VAR):
	S = TH1F(name[0]+"__"+name[1], "", VAR[1], VAR[2], VAR[3])
	quickplot(sig.File, sig.Tree, S, VAR[0], cut, sig.weight)
	return S

def binCalc(start,end,blindstart,blindend,binsize):
	B = []
	TB = []
	thisstart = start
	thisend = start
	while thisend < blindstart:
		thisstart = thisend
		thisend = thisend + int(binsize)
		if thisend > blindstart:
			thisend = blindstart
		B.append([thisstart,thisend])
	while thisend < blindend:
		thisstart = thisend
		thisend = thisend + int(binsize)
		if thisend > blindend:
			thisend = blindend
		TB.append([thisstart,thisend])
	while thisend < end:
		thisstart = thisend
		thisend = thisend + int(binsize)
		B.append([thisstart,thisend])
	return [B, TB]
	

def GetQuantileProfiles(Th2f, cut, name):
        q1 = []
        nxbins = Th2f.GetXaxis().GetNbins();
        xlo = Th2f.GetXaxis().GetBinLowEdge(1);
        xhi = Th2f.GetXaxis().GetBinUpEdge(Th2f.GetXaxis().GetNbins() );
        for i in range(nxbins):
                H = Th2f.ProjectionY("ProjY"+str(i),i+1,i+1)
                probSum = array('d', [cut])
                q = array('d', [0.0]*len(probSum))
                H.GetQuantiles(len(probSum), q, probSum)
                q1.append(q[0])
        H1 = TH1F(name, "", nxbins,xlo,xhi)
        for i in range(nxbins):
                H1.SetBinContent(i+1,q1[i])
        return H1

def CorrPlotter(name, Input, V0, V1, Cuts):
	print "making correlation plot ..."
        Vars = [V0[0], V1[0], V0[1],V0[2],V0[3], V1[1], V1[2],V1[3]]
        A = Alphabet.Alphabetizer("A_"+V1[0]+V1[0], Input, [])
        A.SetRegions(Vars, Cuts)
        A.TwoDPlot.SetStats(0)
        A.TwoDPlot.GetYaxis().SetTitle(V1[4])
        A.TwoDPlot.GetXaxis().SetTitle(V0[4])
        ProfsM = []
        for i in [9,8,7,6,5,4,3,2,1,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]:
                ProfsM.append(GetQuantileProfiles(A.TwoDPlot, 0.1*i, name+V1[0]+V0[0]+str(i)))
	return [A.TwoDPlot, ProfsM]

class DIST:
	def __init__(self, name, File, Tree, weight, color):
		self.name = name
		self.File = File
		self.Tree = Tree
		self.weight = weight
		self.color = color
	def plot(self, VAR, BIN, MIN, MAX, CUT, TITLE, Norm):
		Hist = TH1F(self.name+"_"+VAR, "", BIN, MIN, MAX)
		Hist.GetXaxis().SetTitle(TITLE)
		quickplot(self.File, self.Tree, Hist, VAR, CUT, self.weight)
		Hist.SetLineColor(self.color)
		#print Hist.Integral()
		if Norm:
			Hist.Scale(1/Hist.Integral())
		return Hist


