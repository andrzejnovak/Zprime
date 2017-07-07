#
import os
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import numpy as np

from Plotting_Header import *

def ComputeDDT(name, point, H):
	nXb, xmin, xmax = H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(), H.GetXaxis().GetXmax()
	nYb, ymin, ymax = H.GetYaxis().GetNbins(), H.GetYaxis().GetXmin(), H.GetYaxis().GetXmax()
	DDT = TH2F(name, "", nXb, xmin, xmax, nYb, ymin, ymax)
	DDT.SetStats(0)
	DDTsigma = TH2F(name+"_sigma", "", nXb, xmin, xmax, nYb, ymin, ymax)
	DDTsigma.SetStats(0)

	count = 0
	for x in range(nXb):
		for y in range(nYb):
			proj = H.ProjectionZ("H3"+str(x)+str(y),x+1,x+1,y+1,y+1)
			n = float(proj.Integral())			
			p = array('d', [point*0.01]) #Point is cut percentage
			q = array('d', [0.0]*len(p))
			proj.GetQuantiles(len(p), q, p)
			if n <= 0 :	DDT.SetBinContent( x+1, y+1, 0. )
			else: 	DDT.SetBinContent( x+1, y+1, q[0] )
			
			# Calculate uncertainty 
			std = np.sqrt(n*point*0.01*(1-point*0.01))/n
			DDTsigma.SetBinContent( x+1, y+1, std)

			print str(x+1) + "," + str(y+1) + ":    "+ str(proj.Integral())+"  Map value: "+str(DDT.GetBinContent( x+1, y+1))+"   Uncertainty: "+str(std)
			count += n
	return DDT, DDTsigma, str(count)

def DisplayDDT(DDT, SaveName, to_dir="", Title="DDT", cut="", diff=False, DDTsigma="", count=""):
	if diff == True: # Plotting difference
		C = TCanvas("TopCanvas", "Title", 800, 800)
		plot = TPad("pad1", "The pad 80% of the height",0.02,0.2,0.95,1) #Make plot area smaller
		Alpha = TPad("pad1", "The pad 20% of the height",0.02,0,0.95,0.2)
		plot.Draw()
		Alpha.Draw()
	else: # Plotting single map
		C = TCanvas("FullCanvas", "Title", 800, 600)
		plot = TPad("pad1", "The pad 80% of the height",0.02,0,0.95,1)	
		plot.Draw()
	plot.cd()

	# Design
	DDT.SetStats(0)
	DDT.GetXaxis().SetTitle("jet m (GeV)")
	DDT.GetXaxis().SetTitleSize(0.045)
	DDT.GetZaxis().SetTitle("#tau_{32}")
	DDT.GetZaxis().SetTitleSize(0.045)
	DDT.GetYaxis().SetTitleSize(0.045)
	DDT.GetYaxis().SetTitle("jet p_{T} (GeV)")	
	DDT.GetYaxis().SetTitleOffset(1.145)
	DDT.SetTitle(Title)
	DDT.SetTitleSize(0.045)

	# Axis range
	DDT.GetZaxis().SetRangeUser(0.4,0.8)	
	if diff == True: DDT.GetZaxis().SetRangeUser(-0.15,0.15)

	# "At least one bin needs to be non-zero	
	if abs(DDT.GetBinContent(1,1)) < 0.000001 :	DDT.SetBinContent(1,1,0.001) # Fake point b/call 0 histo doesn't get plotted
	DDT.Draw("COLZ")

	# Lables
	CMSLABL, PRELABL, THILABL, CUTLABL, INTLABL = labels()
	CMSLABL.DrawLatex(0.1465,0.85,"CMS")
	THILABL.DrawLatex(0.81,0.91,"#bf{13 TeV}")
	PRELABL.DrawLatex(0.1465,0.812,"#bf{#it{Simulation Preliminary}}")
	CUTLABL.DrawLatex(0.1465,0.780,cut)
	INTLABL.DrawLatex(0.1465,0.730, "Events measured: "+ str(count))

	# Adding Trend and uncertainty bounds
	if diff:
		n = DDT.GetXaxis().GetNbins()
		xmin, xmax = DDT.GetXaxis().GetXmin(), DDT.GetXaxis().GetXmax() 
		A = TH1F("A", "", n, xmin, xmax )
		Errbound = []
		Avgcheck = []
		for m in range(1, n+1): # For each column
			sum_diff, sum_err = 0, 0 
			for pt in range(1, DDT.GetYaxis().GetNbins()+1): # For each bin
				sum_diff += DDT.GetBinContent(m, pt)  # Add value
				err = DDTsigma.GetBinContent(m, pt) # Add unvertainty
				if err > 0 : sum_err += err
			A.SetBinContent(m, sum_diff/n)  # Record average average
			Avgcheck.append(sum_diff/n)
			Errbound.append(sum_err/n)
		
		# Design
		#A.cd()
		A.SetStats(0)
		A.GetYaxis().SetRangeUser( -np.mean(Errbound)*1.2, np.mean(Errbound)*1.2)
		A.GetYaxis().SetTitle("#bar{#Delta V (#Delta#tau_{32})}")
		A.GetYaxis().SetLabelSize(3*A.GetYaxis().GetLabelSize())
		A.GetYaxis().SetTitleSize(4.2*A.GetYaxis().GetTitleSize())
		A.GetYaxis().SetTitleOffset(0.35)
		A.GetXaxis().SetLabelSize(0)
		
		# Draw error boudnaries
		T1 = TLine(50,np.mean(Errbound),250, np.mean(Errbound))
		T1.SetLineColor(kRed)
		T1.SetLineStyle(2)	
		T2 = TLine(50,-np.mean(Errbound),250, -np.mean(Errbound))
		T2.SetLineColor(kRed)
		T2.SetLineStyle(2)

		leg = TLegend(0.65,0.5,.89,.89)
		leg.SetFillColor(0)
		leg.SetLineColor(0)
		leg.AddEntry(A, "Average difference V_{SB}-V_{SR}", "PL")
		leg.AddEntry(T1, "Average Uncertainty in V", "L")
	
		A.Draw()
		T1.Draw("same")
		T2.Draw("same")
		leg.Draw("same")

	make_dirs(to_dir)
	name = savename_cleaner(SaveName)
	C.Print(to_dir+"/MAP_"+name+".png")


# Fill histogram
def histo(Bkgs, bins_x, bins_y, cut="T.lepJetCSV<100", lumi=1):
	xmin, xmax, xbins = bins_x[0], bins_x[1], bins_x[2]
	ymin, ymax, ybins = bins_y[0], bins_y[1], bins_y[2]
	H3 = TH3F("", "", xbins, xmin, xmax, ybins, ymin, ymax, 1000, 0, 1)
	H3.SetStats(0)
	for B in Bkgs:
		F = TFile(B)
		T = F.Get("tree_T1")
		n = T.GetEntries()
		for j in range(0, n): # Here is where we loop over all events.
			T.GetEntry(j)
			if T.TAGTau32 > 0:
				if eval(cut):
					weight = T.weight*lumi
					PT = T.TAGPt
					M = T.TAGM
					H3.Fill(M, PT, T.TAGTau32, weight)
	return H3


def study(Data, TT, ST, Ws, cut, analysis_folder = "", toretain=30, data=False, lumi=35.9, bins_x = [100, 250, 8], bins_y = [380, 2000,8]): #toretain Percentage to keep
	#Set-up
	Tcut = cut + " and "
	lumi, d_lumi = lumi, lumi
	if data: d_lumi = 1.

	signal_cut = "T.lepJetCSV >0.46"
	sideband_cut = "T.lepJetCSV <0.46"

	# histo(Bkgs, bins_x, bins_y, cut="T.lepJetCSV<100", lumi=1):
	# ComputeDDT(name, point, H):
	# DisplayDDT(DDT, SaveName, to_dir="", Title="DDT", cut="", diff=False, DDTsigma="", count=""):	
 
	##############
	# Signal Region 

	# Data
	def s_data():
		H1 = histo(Data, bins_x, bins_y, cut=Tcut + signal_cut, lumi=d_lumi) - histo(TT, bins_x, bins_y, cut=Tcut + signal_cut, lumi=lumi) - histo(ST, bins_x, bins_y, cut=Tcut + signal_cut, lumi=lumi)
		DDT_data_sr, DDT_data_sr_sigma, DDTcount1 = ComputeDDT("DDT_data_sr", toretain, H1)
		DisplayDDT(DDT_data_sr, "Data_DDT_SR"+cut, to_dir=analysis_folder, Title="V = #tau_{32} at "+str(toretain)+"% efficiency (signal region)",  cut=cut, count=DDTcount1)
		return DDT_data_sr, DDT_data_sr_sigma, DDTcount1
	#W
	def s_W():
		H2 = histo(Ws, bins_x, bins_y, cut=Tcut + signal_cut , lumi=lumi)
		DDT_W_sr, DDT_W_sr_sigma, DDTcount2 = ComputeDDT("DDT_W_sr", toretain,  H2)
		DisplayDDT(DDT_W_sr, "W_DDT_SR"+cut, to_dir=analysis_folder, Title="V = #tau_{32} at "+str(toretain)+"% efficiency (signal region)",  cut=cut,  count=DDTcount2)
		return DDT_W_sr, DDT_W_sr_sigma, DDTcount2
	###########
	# Sidebands

	
	# Data
	def sb_data():
		H3 =  histo(Data, bins_x, bins_y, cut=Tcut + sideband_cut, lumi=d_lumi) - histo(TT, bins_x, bins_y, cut=Tcut + sideband_cut, lumi=lumi) - histo(ST, bins_x, bins_y, cut=Tcut + sideband_cut, lumi=lumi)
		DDT_data_sb, DDT_data_sb_sigma, DDTcount3 = ComputeDDT("DDT_data_sb", toretain, H3)
		DisplayDDT(DDT_data_sb, "Data_DDT_SB"+cut, to_dir=analysis_folder, Title="V = #tau_{32} at "+str(toretain)+"% efficiency (sideband)",  cut=cut,  count=DDTcount3)
		return DDT_data_sb, DDT_data_sb_sigma, DDTcount3
	# W
	def sb_W():
		H4 =  histo(Ws, bins_x, bins_y, cut=Tcut + sideband_cut , lumi=lumi)
		DDT_W_sb, DDT_W_sb_sigma, DDTcount4 = ComputeDDT("DDT_W_sb", toretain, H4)
		DisplayDDT(DDT_W_sb, "W_DDT_SB"+cut, to_dir=analysis_folder, Title="V = #tau_{32} at "+str(toretain)+"% efficiency (sideband)",  cut=cut, count=DDTcount4)
		return DDT_W_sb, DDT_W_sb_sigma, DDTcount4

	DDT_data_sr, DDT_data_sr_sigma, DDTcount1 = s_data()
	DDT_W_sr, DDT_W_sr_sigma, DDTcount2 = s_W()
	DDT_data_sb, DDT_data_sb_sigma, DDTcount3 = sb_data()
	DDT_W_sb, DDT_W_sb_sigma, DDTcount4 = sb_W()

	########
	# Difference in Data
	DisplayDDT(DDT_data_sr-DDT_data_sb, "DDT_diff_Data"+cut, to_dir=analysis_folder, Title="#Delta V (#Delta#tau_{32})" ,cut=cut, diff=True, DDTsigma=DDT_data_sb_sigma)
	# Difference in W
	DisplayDDT(DDT_W_sr-DDT_W_sb, "DDT_diff_W"+cut, to_dir=analysis_folder, Title="#Delta V (#Delta#tau_{32})" ,cut=cut, diff=True, DDTsigma=DDT_W_sb_sigma)

	# Closure between Data and W
	DisplayDDT(DDT_data_sb-DDT_W_sb, "DDT_diff_Data_W"+cut, to_dir=analysis_folder, Title="#Delta V (#Delta#tau_{32})" ,cut=cut, diff=True, DDTsigma=DDT_W_sb_sigma)
	
	
	# Saving it all
	make_dirs(analysis_folder)
	Fout = TFile(analysis_folder+"/DDT.root", "recreate")
	Fout.cd()
	DDT_data_sr.Write()
	DDT_data_sb.Write()
	DDT_data_sr_sigma.Write()
	DDT_data_sb_sigma.Write()
	DDT_W_sr.Write()
	DDT_W_sb.Write()
	DDT_W_sr_sigma.Write()
	DDT_W_sb_sigma.Write()
	Fout.Close()

	return [DDTcount1, DDTcount2, DDTcount3, DDTcount4]

if __name__ == "__main__":
	pwd = '/home/storage/andrzejnovak/FriedBacon/'
	Data, TT, ST, Ws = [pwd+'MCDATA.root'], [pwd+'TT.root'], [pwd+'ST.root'], [pwd+'WJets.root']
	cut = "T.LepType<10"
	analysis_folder = "test"

	counts = study(Data, TT, ST, Ws, cut, analysis_folder = analysis_folder, toretain=30, data=False, lumi=35.9, bins_x = [100, 250, 8], bins_y = [380, 2000,8])
	
