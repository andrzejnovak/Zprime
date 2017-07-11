import os
import ROOT
from ROOT import *
from array import array

import Plotting_Header
from Plotting_Header import *

def tt_reweigh(percentages, source_dir, save_to):
	print percentages
	for percentage in percentages:
		File = TFile("root://cmsxrootd.fnal.gov/"+ source_dir +"TT.root")
		Tree = File.Get("tree_T1")

		make_dirs(save_to+"/TT_reweigh")
		f = ROOT.TFile(save_to+"/TT_reweigh/TT"+str(percentage)+".root", "recreate" )
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

		print "Finished TT reweigh:", percentage

if __name__ == '__main__':
	reweights = [90, 100, 110]
	pwd = "/home/storage/andrzejnovak/FriedBacon/"
	for p in reweights:
		tt_reweigh(p, pwd, save_to="")
