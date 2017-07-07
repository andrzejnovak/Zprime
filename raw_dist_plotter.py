import sys
from optparse import OptionParser
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from Plotting_Header import *


def varplot(varname, xmin=None, xmax=None, pwd="/home/storage/andrzejnovak/FriedBacon/", cut= "(LepType<2)", stacked=False, per=0, name=""):
	
	VAR = [varname, 36, int(xmin), int(xmax)]
	YT = "events / "+str((VAR[3]-VAR[2])/VAR[1])+" GeV"
	XT = varname+" (GeV)"
	H = "Type 1 (e) control region"
	Cut = cut
	treename="tree_T1"

	lumi = str(35.9)


	Data = TH1F("McDATA", "", VAR[1], VAR[2], VAR[3])
	Data.Sumw2()
	Data.SetLineColor(1)
	Data.SetFillColor(1)
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	quickplot(pwd+"MCDATA"+str(per)+".root", treename, Data, VAR[0], Cut, "("+lumi+"*weight)")


	W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
	W.SetLineColor(kGreen)
	W.SetLineWidth(2)
	W.SetFillColor(kGreen)
	quickplot(pwd+"WJets.root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")


	TT = TH1F("TT", "", VAR[1], VAR[2], VAR[3])
	TT.SetLineColor(kRed)
	TT.SetFillColor(kRed)
	TT.SetLineWidth(2)
	quickplot(pwd+"TT.root", treename,TT, VAR[0], Cut, "("+lumi+"*weight)")

	quickplot(pwd+"ST.root", treename, TT, VAR[0], Cut, "("+lumi+"*weight)")
	

	for i in [TT]:
		W.Add(i,1.)

	FindAndSetMax([Data, W, TT])
	W.SetTitle("Fake Data w/ "+str(per)+"% ttbar, padded w/ 100% ttbar")
	#Data.GetXaxis().SetTitle(XT)
	#Data.GetYaxis().SetTitle(YT)
	#Data.GetXaxis().SetTitleOffset(1.06)
	#Data.GetYaxis().SetTitleOffset(1.06)
	W.GetXaxis().SetTitle(varname+" [GeV]")
	W.GetYaxis().SetTitle("Events")
	W.GetXaxis().SetTitleSize(0.045)
	W.GetYaxis().SetTitleSize(0.045)

	Rat1 = W.Clone("W")
	for i in range(1, Rat1.GetNbinsX()+1):
			B = Rat1.GetBinContent(i)
			S1 = TT.GetBinContent(i)
			if B > 1:
				Rat1.SetBinContent(i, S1/B)
			else: Rat1.SetBinContent(i, 0)

	Rat1.SetStats(0)
	Rat1.SetLineColor(1)
	Rat1.SetFillColor(0)

	Rat1.GetXaxis().SetNdivisions(0)
	Rat1.GetYaxis().SetNdivisions(4)
	Rat1.GetYaxis().SetTitle("TT/Total")
	Rat1.GetYaxis().SetLabelSize(85/15*Rat1.GetYaxis().GetLabelSize())
	Rat1.GetYaxis().SetTitleSize(4.2*Rat1.GetYaxis().GetTitleSize())
	Rat1.GetYaxis().SetTitleOffset(0.175)
	Rat1.GetYaxis().SetRangeUser(0.4, 1.2)
	Rat1.SetTitle("")
	Rat1.GetXaxis().SetTitle("")

	Pline = TLine(100, 0.01*per, 3000,0.01*per);
	Pline.SetLineStyle(3)

	leg = TLegend(0.5,0.65,0.89,0.89)
	leg.SetHeader(H)
	leg.SetFillColor(0)
	leg.SetLineColor(0)
	leg.AddEntry(Data, "Signal region events (Fake data)", "PL")
	leg.AddEntry(W, "Raw W+Jets", "F")
	#leg.AddEntry(QCD, "QCD", "F")
	#leg.AddEntry(TT, "t#bar{t}", "F")
	#leg.AddEntry(ST, "Single top", "F")
	leg.AddEntry(TT, "Resonant backgrounds", "F")
		
	CMSLABL, PRELABL, THILABL, CUTLABL, INTLABL = labels()
	
	C = TCanvas("C", "", 800, 600)
	#plot = TPad("pad1", "The pad 80% of the height",0,0,1,1)
	#plot.Draw()
	#plot.cd()
	plot = TPad("pad1", "The pad 80% of the height",0,0.15,1,1)
	pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.15)
	plot.Draw()
	pull.Draw()
	plot.cd()
	W.Draw()
	TT.Draw("same")
	Data.Draw("same")
	leg.Draw("same")
	CMSLABL.DrawLatex(0.1465,0.85,"CMS")
	THILABL.DrawLatex(0.81,0.91,"#bf{13 TeV}")
	PRELABL.DrawLatex(0.1465,0.812,"#bf{#it{Simulation Preliminary}}")
	CUTLABL.DrawLatex(0.1465,0.780, name)
	INTLABL.DrawLatex(0.1465, 0.74, "xT INT:"+str(TT.Integral()) )

	pull.cd()
	Rat1.Draw()
	Pline.Draw("same")

	
	make_dirs(over_dir+name+"/Pre_Est")
	C.SaveAs(over_dir+name+"/Pre_Est/"+varname+"_TT"+str(per)+".png")


names = ["MC_T300-700_mu", "MC_T300-700_el", "MC_T700_mu", "MC_T700_el" ]
root_cuts =  ["LepType>0&TPRIMEM>300&TPRIMEM<700","LepType<0&TPRIMEM>300&TPRIMEM<700","LepType>0&TPRIMEM>700","LepType<0&TPRIMEM>700"]


for eta, run in zip([20,30,40], ['eta20', 'eta30', 'eta40']):
	over_dir = "/home/storage/andrzejnovak/Analysis/"
	over_dir += run +"/"
	for name, n_cut in zip(names, root_cuts):
		cut = n_cut + "&TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV>0.46&Tau32DDT_Sig<0."

		for d_percentage in [80, 100, 120]:
			varplot("ZPRIMEM", xmin=100, xmax=3000, pwd= over_dir+name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/tt100percent/", cut=cut, stacked=True, name=name, per=d_percentage)





