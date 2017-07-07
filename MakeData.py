import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import pdb

from rootpy.tree import Tree, TreeModel, FloatCol, IntCol
from rootpy.io import root_open

import Plotting_Header
from Plotting_Header import *

reweights = []
for i in range(0,11):
	reweights.append(75+i*5)
reweights.append(50)
reweights.append(150)
print reweights

pwd = "/home/storage/andrzejnovak/FriedBacon/"

for percentage in reweights:
	File = TFile("root://cmsxrootd.fnal.gov/"+ pwd +"TT.root")
	Tree = File.Get("tree_T1")

	f = ROOT.TFile("Step0_MakeData/TT"+str(percentage)+".root", "recreate" )
	t = Tree.CloneTree(0)
	weight = array('f', [0.0])
	t.SetBranchAddress("weight", weight)

	for j in range(0,Tree.GetEntries()):
		Tree.GetEntry(j)
		weight[0] = Tree.weight*percentage*0.01

		t.Fill()

	t.Write()
	f.Close()
	File.Close()

	os.system("hadd Step0_MakeData/MCDATA"+str(percentage)+".root /home/storage/andrzejnovak/FriedBacon/ST* /home/storage/andrzejnovak/FriedBacon/WJets*0.root /home/storage/andrzejnovak/FriedBacon/WJets*Inf.root Step0_MakeData/TT"+str(percentage)+".root")

	print "Finished ", percentage

