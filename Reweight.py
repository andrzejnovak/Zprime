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

reweights = [90, 100, 110]
pwd = "/home/storage/andrzejnovak/FriedBacon/"

for percentage in reweights:
	name_dir = "tt"+str(percentage)+"percent"
	if not os.path.exists("Step1_Reweight/"+name_dir): os.system("mkdir Step1_Reweight/"+name_dir)
	if not os.path.exists("Step2_DDT/"+name_dir): os.system("mkdir Step2_DDT/"+name_dir)
	if not os.path.exists("Step3_ModTreeFiles/"+name_dir): os.system("mkdir Step3_ModTreeFiles/"+name_dir)
	if not os.path.exists("Step4_EstimateWJets/"+name_dir): os.system("mkdir Step4_EstimateWJets/"+name_dir)

	File = TFile("root://cmsxrootd.fnal.gov/"+ pwd +"TT.root")
	Tree = File.Get("tree_T1")

	f = ROOT.TFile("Step1_Reweight/"+name_dir+"/TT.root", "recreate" )
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

	print "Finished ", percentage

