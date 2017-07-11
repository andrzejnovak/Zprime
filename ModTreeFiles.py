import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import pdb

import Plotting_Header
from Plotting_Header import *

def mod_trees(file_name, pwd, pwd_DDT, dest, analysis_dir=""):
	TransFile = TFile(pwd_DDT+"/DDT.root")
	# Get Data maps
	CorrSig_data = TransFile.Get("DDT_data_sr")
	CorrBkg_data = TransFile.Get("DDT_data_sb")
	CorrSig_data_sigma = TransFile.Get("DDT_data_sr_sigma")
	CorrBkg_data_sigma = TransFile.Get("DDT_data_sb_sigma")
	# Get MC maps
	CorrSig_W = TransFile.Get("DDT_W_sr")
	CorrBkg_W = TransFile.Get("DDT_W_sb")
	CorrSig_W_sigma = TransFile.Get("DDT_W_sr_sigma")
	CorrBkg_W_sigma = TransFile.Get("DDT_W_sb_sigma")

	if file_name.startswith("TT"):	File = TFile("root://cmsxrootd.fnal.gov/"+ analysis_dir +"TT_reweigh/"+ file_name)
	elif file_name.startswith("MCDATA"):  File = TFile("root://cmsxrootd.fnal.gov/"+ analysis_dir +"FakeData/" + file_name)
	else: File = TFile("root://cmsxrootd.fnal.gov/"+ pwd + file_name)
	Tree = File.Get("tree_T1")
	make_dirs(dest)
	f = ROOT.TFile(dest+"/"+ file_name, "recreate" )
       	tree = Tree.CloneTree(0)
		
	Tau32DDT_Bkg = array('f', [-10.0])
	tree.Branch('Tau32DDT_Bkg', Tau32DDT_Bkg, 'Tau32DDT_Bkg/F')
	Tau32DDT_Sig = array('f', [-10.0])
	tree.Branch('Tau32DDT_Sig', Tau32DDT_Sig, 'Tau32DDT_Sig/F')

	#Uncertainties
	Tau32DDT_Bkg_sigma = array('f', [-10.0])
	tree.Branch('Tau32DDT_Bkg_sigma', Tau32DDT_Bkg_sigma, 'Tau32DDT_Bkg_sigma/F')
	Tau32DDT_Sig_sigma = array('f', [-10.0])
	tree.Branch('Tau32DDT_Sig_sigma', Tau32DDT_Sig_sigma, 'Tau32DDT_Sig_sigma/F')

	# Add MC
	Tau32DDT_W_Bkg = array('f', [-10.0])
	tree.Branch('Tau32DDT_W_Bkg', Tau32DDT_W_Bkg, 'Tau32DDT_W_Bkg/F')
	Tau32DDT_W_Sig = array('f', [-10.0])
	tree.Branch('Tau32DDT_W_Sig', Tau32DDT_W_Sig, 'Tau32DDT_W_Sig/F')
	
	# Fill
	n = Tree.GetEntries()
	xmin, xmax , ymin, ymax = CorrBkg_data.GetXaxis().GetXmin(), CorrBkg_data.GetXaxis().GetXmax(), CorrBkg_data.GetYaxis().GetXmin(), CorrBkg_data.GetYaxis().GetXmax()
	for j in range(0, n): # Here is where we loop over all events.
		if j % 5000 == 0 or j==0:
			percentDone = float(j) / float(n) * 100.0
			print 'Processing '+file_name+' {0:10.0f}/{1:10.0f} : {2:5.2f} %'.format(j, n, percentDone )
		Tree.GetEntry(j)			
		TAGM = Tree.TAGM
		TAGPt = Tree.TAGPt
		if TAGM > xmin and TAGM < xmax and TAGPt > ymin and TAGPt < ymax:	
			#Signal			
			rind6 = CorrSig_data.GetXaxis().FindBin(TAGM)
			pind6 = CorrSig_data.GetYaxis().FindBin(TAGPt)
						
			Tau32DDT_Sig[0] = Tree.TAGTau32 -  CorrSig_data.GetBinContent(rind6,pind6)
			a =  CorrSig_data.GetBinContent(rind6,pind6)
			Tau32DDT_Sig_sigma[0] = CorrSig_data_sigma.GetBinContent(rind6,pind6)

			# Sideband
			rind6 = CorrBkg_data.GetXaxis().FindBin(TAGM)
			pind6 = CorrBkg_data.GetYaxis().FindBin(TAGPt)
						
			Tau32DDT_Bkg[0] = Tree.TAGTau32 -  CorrBkg_data.GetBinContent(rind6,pind6)
			Tau32DDT_Bkg_sigma[0] = CorrSig_data_sigma.GetBinContent(rind6,pind6)
			
			# MC Sideband
			rind6 = CorrBkg_W.GetXaxis().FindBin(TAGM)
			pind6 = CorrBkg_W.GetYaxis().FindBin(TAGPt)
							
			Tau32DDT_W_Bkg[0] = Tree.TAGTau32 -  CorrBkg_W.GetBinContent(rind6,pind6)

			# MC Signal
			rind6 = CorrSig_W.GetXaxis().FindBin(TAGM)
			pind6 = CorrSig_W.GetYaxis().FindBin(TAGPt)
							
			Tau32DDT_W_Sig[0] = Tree.TAGTau32 -  CorrSig_W.GetBinContent(rind6,pind6)
			b = CorrSig_W.GetBinContent(rind6,pind6)
					
			tree.Fill()

	File.Close()
	f.Write()
	f.Close()

"""

for name in ["MC_T300-700_mu", "MC_T300-700_el", "MC_T700_mu", "MC_T700_el"]:
	if not os.path.exists(name+"/Step3_ModTreeFiles"): os.system("mkdir "+name+"/Step3_ModTreeFiles")

for name in ["MC_T300-700_mu", "MC_T300-700_el", "MC_T700_mu", "MC_T700_el"][3:4]:
	for d_percentage in datalist:
		Data =[]
		if not os.path.exists(name+"/Step3_ModTreeFiles/Data"+str(d_percentage)): os.system("mkdir "+name+"/Step3_ModTreeFiles/Data"+str(d_percentage))
		reweights = [90, 100, 110]
		print d_percentage
		for percentage in reweights:
			name_dir = "tt"+str(percentage)+"percent"
			if not os.path.exists(name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/"+name_dir): os.system("mkdir "+name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/"+name_dir)

			Data = []
			Data.append("ST.root")
			Data.append("WJets.root")
			Data.append("TT.root")
			Data.append("MCDATA"+str(d_percentage)+".root")
			for d in Data:
				mod_trees(d ,pwd, name+ "/Step2_DDT/Data"+str(d_percentage)+"/"+name_dir,  name+ "/Step3_ModTreeFiles/Data"+str(d_percentage)+"/"+name_dir , "Step1_Reweight/tt"+str(percentage)+"percent/" )
				# name, from, from_DDT, to, reweighted ttbar

"""
	
