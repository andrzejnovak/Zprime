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

def make_theta_file(analysis_name, from_dir, to_dir, name, cut_in, varname="ZPRIMEM"):
	xmin, xmax = 100, 3000
	lumi = str(35.9)

	make_dirs(to_dir+"Prep_theta/"+analysis_name)
	Output = ROOT.TFile(to_dir+"Prep_theta/"+analysis_name+"/Data" + name + "_updown.root", "recreate" )	
	print "Saving file: ", to_dir+"Prep_theta/"+analysis_name+"/Data" + name + "_updown.root"

	# Get W reweight
	W_File = TFile("root://cmsxrootd.fnal.gov/"+to_dir+analysis_name+"mu/Step4_EstimateWJets/"+ from_dir + "tt100percent/" + "New_WJets_est.root")
	WJets_reweight = W_File.Get("NRFR")
	W_File1 = TFile("root://cmsxrootd.fnal.gov/"+to_dir+analysis_name+"mu/Step4_EstimateWJets/"+ from_dir + "tt90percent/" + "New_WJets_est.root")
	WJets_reweight_up = W_File1.Get("NRFR")
	W_File2 = TFile("root://cmsxrootd.fnal.gov/"+to_dir+analysis_name+"mu/Step4_EstimateWJets/"+ from_dir + "tt110percent/" + "New_WJets_est.root")
	WJets_reweight_down = W_File2.Get("NRFR")

	W_File_e = TFile("root://cmsxrootd.fnal.gov/"+to_dir+analysis_name+"el/Step4_EstimateWJets/"+ from_dir + "tt100percent/" + "New_WJets_est.root")
	WJets_reweight_e = W_File.Get("NRFR")
	W_File1_e = TFile("root://cmsxrootd.fnal.gov/"+to_dir+analysis_name+"el/Step4_EstimateWJets/"+ from_dir + "tt90percent/" + "New_WJets_est.root")
	WJets_reweight_up_e = W_File1.Get("NRFR")
	W_File2_e = TFile("root://cmsxrootd.fnal.gov/"+to_dir+analysis_name+"el/Step4_EstimateWJets/"+ from_dir + "tt110percent/" + "New_WJets_est.root")
	WJets_reweight_down_e = W_File2.Get("NRFR")
	
	cut = "TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV>0.46&Tau32DDT_Sig<0&LepType>0&" + cut_in
	cut_el = "TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV>0.46&Tau32DDT_Sig<0&LepType<0&" + cut_in
	
	# Extract other files
			
	TT = TH1F("TT1", "", 36, xmin, xmax)
	TT_up = TH1F("TT2", "", 36, xmin, xmax)
	TT_down = TH1F("TT3", "", 36, xmin, xmax)
	TT_e = TH1F("TT4", "", 36, xmin, xmax)
	TT_up_e = TH1F("TT5", "", 36, xmin, xmax)
	TT_down_e = TH1F("TT6", "", 36, xmin, xmax)
	for t in ["TT"]:
		D = DIST("D", to_dir+analysis_name+"mu/Step3_ModTreeFiles/"+from_dir + "tt100percent/" + t + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT.Add(D.plot(varname, 36, xmin,xmax, cut, D.name+"TT1", False),1) 
		D = DIST("D", to_dir+analysis_name+"mu/Step3_ModTreeFiles/"+from_dir + "tt90percent/"  + t + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT_down.Add(D.plot(varname, 36, xmin,xmax, cut, D.name+"TT2", False),1)
		D = DIST("D", to_dir+analysis_name+"mu/Step3_ModTreeFiles/"+from_dir + "tt110percent/" + t + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT_up.Add(D.plot(varname, 36, xmin,xmax, cut, D.name+"TT3", False),1)
		D = DIST("D", to_dir+analysis_name+"el/Step3_ModTreeFiles/"+from_dir + "tt100percent/" + t + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT_e.Add(D.plot(varname, 36, xmin,xmax, cut_el, D.name+"TT4", False),1) 
		D = DIST("D", to_dir+analysis_name+"el/Step3_ModTreeFiles/"+from_dir + "tt90percent/"  + t + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT_down_e.Add(D.plot(varname, 36, xmin,xmax, cut_el, D.name+"TT5", False),1)
		D = DIST("D", to_dir+analysis_name+"el/Step3_ModTreeFiles/"+from_dir + "tt110percent/" + t + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT_up_e.Add(D.plot(varname, 36, xmin,xmax, cut_el, D.name+"TT6", False),1)

	for s in ["ST"]:
		D = DIST("D",  to_dir+analysis_name+"mu/Step3_ModTreeFiles/"+from_dir + "tt100percent/" + s + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT.Add(D.plot(varname, 36, xmin,xmax, cut , D.name+"ST1", False),1) 
		TT_up.Add(D.plot(varname, 36, xmin,xmax, cut , D.name+"ST2", False),1) 
		TT_down.Add(D.plot(varname, 36, xmin,xmax, cut , D.name+"ST3", False),1) 
		D = DIST("D",  to_dir+analysis_name+"el/Step3_ModTreeFiles/"+from_dir + "tt100percent/" + s + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		TT_e.Add(D.plot(varname, 36, xmin,xmax, cut_el , D.name+"ST4", False),1) 
		TT_up_e.Add(D.plot(varname, 36, xmin,xmax, cut_el , D.name+"ST5", False),1) 
		TT_down_e.Add(D.plot(varname, 36, xmin,xmax, cut_el , D.name+"ST6", False),1) 


	DATA = TH1F("DATA1", "", 36, xmin, xmax)
	DATA_e = TH1F("DATA2", "", 36, xmin, xmax)
	for d in ["MCDATA"+name ]:
		D1 = DIST("D",  to_dir+analysis_name+"mu/Step3_ModTreeFiles/"+from_dir + "tt100percent/"+ d + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		DATA.Add(D1.plot(varname, 36, xmin,xmax, cut , D.name+"DATA", False),1) 

		D2 = DIST("D",  to_dir+analysis_name+"el/Step3_ModTreeFiles/"+from_dir + "tt100percent/"+ d + ".root", "tree_T1", "("+lumi+"*weight)", 9)
		DATA_e.Add(D2.plot(varname, 36, xmin,xmax, cut_el , D.name+"DATA", False),1) 

	# Write to a new file
	Output.cd()
	o_WJets_n = WJets_reweight.Clone("ZPRIMEM-MU__WJETS")
	o_WJets_n_u = WJets_reweight_up.Clone("ZPRIMEM-MU__WJETS__TTScale__up")
	o_WJets_n_d = WJets_reweight_down.Clone("ZPRIMEM-MU__WJETS__TTScale__down")
	o_WJets_n_e = WJets_reweight_e.Clone("ZPRIMEM-EL__WJETS")
	o_WJets_n_u_e = WJets_reweight_up_e.Clone("ZPRIMEM-EL__WJETS__TTScale__up")
	o_WJets_n_d_e = WJets_reweight_down_e.Clone("ZPRIMEM-EL__WJETS__TTScale__down")

	o_TT = TT.Clone("ZPRIMEM-MU__TTbar")
	o_TT_u = TT_up.Clone("ZPRIMEM-MU__TTbar__TTScale__up")
	o_TT_d = TT_down.Clone("ZPRIMEM-MU__TTbar__TTScale__down")
	o_DATA = DATA.Clone("ZPRIMEM-MU__DATA")
	o_TT_e = TT.Clone("ZPRIMEM-EL__TTbar")
	o_TT_u_e = TT_up_e.Clone("ZPRIMEM-EL__TTbar__TTScale__up")
	o_TT_d_e = TT_down_e.Clone("ZPRIMEM-EL__TTbar__TTScale__down")
	o_DATA_e = DATA_e.Clone("ZPRIMEM-EL__DATA")
	

	Output.Write()
	Output.Save()
