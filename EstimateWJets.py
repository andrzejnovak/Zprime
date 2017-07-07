#
from array import array
import optparse
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
import numpy as np

from Plotting_Header import *

lumi = str(35.9)

def error(var):
	TransFile = TFile("DDT.root")
	H = TransFile.Get("DDT_sr")
	nXb = H.GetXaxis().GetNbins()
	nYb = H.GetYaxis().GetNbins()
	xmin, xmax, varname = 0, 5000, var
	from_dir = "TreesPlus"
	sqsum, simplesum = 0, 0
	for x in range(nXb+1):
		upx =  H.GetXaxis().GetBinUpEdge(x)
		downx =  H.GetXaxis().GetBinLowEdge(x)
		for y in range(nYb+1):
			upy =  H.GetYaxis().GetBinUpEdge(y)
			downy =  H.GetYaxis().GetBinLowEdge(y)
			binned = "TAGM>"+str(downx)+"&TAGM<"+str(upx)+"&TAGPt>"+str(downy)+"&TAGPt<"+str(upy)
			FAIL_err = binned + "&lepJetCSV>0.46" + "&(Tau32DDT_Bkg+Tau32DDT_Bkg_sigma)>0"
			Failb_err = TH1F("NRF", "", 36, xmin,xmax)

			FAIL_Result = binned + "&lepJetCSV>0.46" + "&Tau32DDT_Bkg>0"
			NonResFailResult = TH1F("NRF", "", 36, xmin, xmax)	
			
			for w in [ "B_03Feb2017_ver1_v2", "C_03Feb2017_v1", "D_03Feb2017_v1", "E_03Feb2017_v1", "F_03Feb2017_v1", "G_03Feb2017_v1",  "H_03Feb2017_ver3_v1", "B_03Feb2017_ver1_v1", "H_03Feb2017_ver2_v1"]:
				D = DIST("D", from_dir + "/SingleMuonRun2016"+w+".root", "tree_T1", "1.0", 9)		

				Failb_err.Add(D.plot(varname, 36, xmin,xmax, FAIL_err, D.name+"NRP", False))
				NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result, D.name+"NRF", False))

			for t in ["ST_s", "ST_tat", "ST_tt", "ST_tW", "ST_atW", "TT"]:
				D = DIST("D", from_dir + "/"+t+".root", "tree_T1", "("+lumi+"*weight)", 9)

				Failb_err.Add(D.plot(varname, 36, xmin,xmax, FAIL_err, D.name+"NRP", False), -1)
				NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result, D.name+"NRF", False), -1)
	
			sqsum +=  (abs(Failb_err.Integral()-NonResFailResult.Integral()))**2
			simplesum +=  (abs(Failb_err.Integral()-NonResFailResult.Integral()))
			#print x,y, Failb_err.Integral(), NonResFailResult.Integral(), Failb_err.Integral()-NonResFailResult.Integral()
			#print var, x*15+y
	print sqsum, np.sqrt(sqsum)
	return sqsum, simplesum

#print error("TAGM")
#print error("TAGPt")
#print error("TPRIMEM")
#print error("ZPRIMEM") 60698243.9224 7790.90777268

TAGMerr =  0
TAGPterr = 0
TPRIMEMerr = 0
ZPRIMEMerr = 0 #np.sqrt(60698243.9224)

def checkplot(varname="TAGM", xmin=110, xmax=230, from_dir="", to_dir="", cut="", tauerror=0, TT=False, per="", ttper="", V=30, theta=False, theta_mult=1):
	make_dirs(to_dir)
	Pres =  "TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV>0.46&" + cut
	# Signal
	PASSs = Pres + "&Tau32DDT_Sig<0." 
	FAILs= Pres + "&Tau32DDT_Sig>0."
	NonResPasss = TH1F("NRPs", "", 36, xmin,xmax)
	NonResFails = TH1F("NRFs", "", 36, xmin,xmax)
	#PASSsMC= Pres + "&Tau32DDT_W_Sig<0."
	PASSsMC= Pres + "&Tau32DDT_W_Sig<0."
	NonResPasss_MC = TH1F("NRPsMC", "", 36, xmin,xmax)

	# Sideband
	Preb =  "TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV<0.46&" + cut
	PASSb = Preb + "&Tau32DDT_Bkg<0." 
	FAILb = Preb + "&Tau32DDT_Bkg>0."	
	NonResPassb = TH1F("NRPb", "", 36, xmin,xmax)
	NonResFailb = TH1F("NRFb", "", 36, xmin,xmax)

	# Errors, currently not used.
	FAIL_errup = Pres + "&Tau32DDT_Bkg+Tau32DDT_Bkg_sigma>0."
	FAIL_errdown = Pres + "&(Tau32DDT_Bkg-Tau32DDT_Bkg_sigma)>0"
	NonResFailb_errup = TH1F("NRFb_eu", "", 36, xmin,xmax)
	NonResFailb_errdown = TH1F("NRFb_ed", "", 36, xmin,xmax)

	# Signal for background
	FAIL_Result = Pres + "&Tau32DDT_Bkg>0."
	NonResFailResult = TH1F("NRFR", "", 36, xmin, xmax)

	# Estiamte from MC
	FAIL_Result_MC = Pres + "&Tau32DDT_W_Bkg>0."
	NonResFailResult_MC = TH1F("NRFRMC", "", 36, xmin, xmax)

	# Top padding 
	NonResPasss_xT = TH1F("NRFRMC", "", 36, xmin, xmax)

	# Fake data
	for d in ["MCDATA"+str(per)]:
		D = DIST("D", from_dir + "/"+d+".root", "tree_T1", "("+lumi+"*weight)", 9)
		NonResPasss.Add(D.plot(varname, 36, xmin,xmax, PASSs, D.name+"NRPs", False),1.0)  # DATA in signal region
		NonResFails.Add(D.plot(varname, 36, xmin,xmax, FAILs, D.name+"NRFs", False), 1.0)  # Estimate signal Region , Signal DDT
		NonResPassb.Add(D.plot(varname, 36, xmin,xmax, PASSb, D.name+"NRPb", False), 1.0)  # DATA sideband, nonplotted
		NonResFailb.Add(D.plot(varname, 36, xmin,xmax, FAILb, D.name+"NRFb", False), 1.0)  # Estiamte sideband region, nonplotted

		NonResFailb_errup.Add(D.plot(varname, 36, xmin,xmax, FAIL_errup, D.name+"NRFb_eu", False), 1.0) 
		NonResFailb_errdown.Add(D.plot(varname, 36, xmin,xmax, FAIL_errdown, D.name+"NRFb_ed", False), 1.0) 

		NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result, D.name+"NRFR", False), 1.0) #Estiamte signal Region, Sideband DDT
		NonResFailResult_MC.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result_MC, D.name+"NRFRMC", False), 1.0) # Estimate using W monte carlo
	
	# Substract
	for t in ["ST", "TT"]:
		D = DIST("D", from_dir + "/"+t+".root", "tree_T1", "("+lumi+"*weight)", 9)
		NonResPasss.Add(D.plot(varname, 36, xmin,xmax, PASSs, D.name+"NRPs", False), -1)  # DATA in signal region
		NonResFails.Add(D.plot(varname, 36, xmin,xmax, FAILs, D.name+"NRFs", False), -1)  # Estimate signal Region , Signal DDT
		NonResPassb.Add(D.plot(varname, 36, xmin,xmax, PASSb, D.name+"NRPb", False), -1)  # DATA sideband, nonplotted
		NonResFailb.Add(D.plot(varname, 36, xmin,xmax, FAILb, D.name+"NRFb", False), -1)  # Estiamte sideband region, nonplotted

		NonResFailb_errup.Add(D.plot(varname, 36, xmin,xmax, FAIL_errup, D.name+"NRFb_eu", False), -1) 
		NonResFailb_errdown.Add(D.plot(varname, 36, xmin,xmax, FAIL_errdown, D.name+"NRFb_eu", False), -1) 

		NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result, D.name+"NRFR", False), -1) #Estiamte signal Region, Sideband DDT
		NonResFailResult_MC.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result_MC, D.name+"NRFRMC", False), -1)
		
		
	# MC check
	for w in ["WJets"]:
		D = DIST("D", from_dir + "/"+w+".root", "tree_T1", "("+lumi+"*weight)", 9)
		NonResPasss_MC.Add(D.plot(varname, 36, xmin,xmax, PASSs, D.name+"NRPsMC", False),1) 
		#NonResFailResult_xT.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result_xT, D.name+"NRFRMC", False), 1)

	print NonResPasss.Integral(), NonResPasss_MC.Integral()
		
	# Apply scaling
	print V
	NonResFails.Scale(float(V)/(100.-float(V)))
	NonResFailb.Scale(float(V)/(100.-float(V)))
	NonResFailb_errup.Scale(float(V)/(100.-float(V)))
	NonResFailb_errdown.Scale(float(V)/(100.-float(V)))
	NonResFailResult.Scale(float(V)/(100.-float(V)))
	NonResFailResult_MC.Scale(float(V)/(100.-float(V)))

	# Save WJets Estimate to ROOT
	if not theta:
		NonResFailResult.SaveAs(to_dir+"New_WJets_est.root")

	# Stack with tt/st
	if TT:
		for t in ["ST", "TT"]:
			if t == "TT": 
				if theta: 
					print "THETA"
					pseudo_lumi = str((100 + theta_mult*10)*0.01* float(lumi) )
					D = DIST("D", from_dir + "/"+t+".root", "tree_T1", "("+pseudo_lumi+"*weight)", 9) 
				else:
					D = DIST("D", from_dir + "/"+t+".root", "tree_T1", "("+lumi+"*weight)", 9)
			else: D = DIST("D", from_dir + "/"+t+".root", "tree_T1", "("+lumi+"*weight)", 9)
			NonResPasss_xT.Add(D.plot(varname, 36,  xmin,xmax, PASSs, D.name+"NRFRMC", False), 1)
	
			NonResPasss.Add(D.plot(varname, 36, xmin,xmax, PASSs, D.name+"NRPs", False), 1)  # DATA in signal region
			NonResPasss_MC.Add(D.plot(varname, 36, xmin,xmax, PASSs, D.name+"NRFs", False), 1)  # Estimate signal Region , Signal DDT
	
			NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, PASSs, D.name+"NRFR", False), 1) #Estiamte signal Region, Sideband DDTp
			NonResFailResult_MC.Add(D.plot(varname, 36,  xmin,xmax, PASSs, D.name+"NRFRMC", False), 1)

	# Legend
	leg = TLegend(0.5,0.65,0.89,0.89)
	leg.SetHeader("Wjets (DDT~"+str(V)+"%):")
	leg.AddEntry(NonResPasss, "Signal region events (Fake data)", "PL")
	#leg.AddEntry(NonResPasss_MC, "Signal region events (MC)", "PL")
	#leg.AddEntry(NonResFails, "Estimate from signal region", "L")
	leg.AddEntry(NonResFailResult, "Estimate from sideband", "F")
	#leg.AddEntry(NonResFailResult_MC, "Estimate from MC sideband", "L")
	leg.AddEntry(NonResPasss_xT, "Resonant backgrounds", "F")
	leg.SetLineColor(0)
	leg.SetFillColor(0)

	# Plotting uncertainty
	Boxes = []
	for i in range(1, NonResFailResult.GetNbinsX()+1):
		x1 = NonResFailb.GetBinCenter(i) - (0.5*NonResFailResult.GetBinWidth(i))
		x2 = NonResFailResult.GetBinCenter(i) + (0.5*NonResFailResult.GetBinWidth(i))
		
		#err = np.sqrt(NonResFailResult.GetBinContent(i) + tauerror)
		err = 0
		y1 = NonResFailResult.GetBinContent(i) - err		
		y2 = NonResFailResult.GetBinContent(i) + err

		tempbox = TBox(x1,y1,x2,y2)
		Boxes.append(tempbox)	

	for i in Boxes:
		i.SetFillColor(12)
		i.SetFillStyle(3244)	

	# Styling
	# Signal Region events
	NonResPasss.Sumw2()
	NonResPasss.SetLineStyle(1)
	NonResPasss.SetLineColor(1)
	NonResPasss.SetFillColor(1)
	NonResPasss.SetMarkerColor(1)
	NonResPasss.SetMarkerStyle(20)

	# Signal Region events_MC
	NonResPasss_MC.Sumw2()
	NonResPasss_MC.SetStats(0)
	NonResPasss_MC.SetLineStyle(1)
	NonResPasss_MC.SetLineColor(1)
	NonResPasss_MC.SetFillColor(1)
	NonResPasss_MC.SetMarkerColor(kRed)
	NonResPasss_MC.SetMarkerStyle(20)

	# Signal Region Estimate
	NonResFails.SetStats(0)
	NonResFails.SetLineColor(kBlue)
	NonResFails.SetLineStyle(2)
	NonResFails.SetLineWidth(2)

	# Signal Estimate from Sideband
	NonResFailResult.SetStats(0)
	NonResFailResult.SetLineColor(kGreen)
	NonResFailResult.SetFillColor(kGreen)
	#NonResFailResult.SetLineStyle(3)
	NonResFailResult.SetLineWidth(2)

	# Signal Estiamte from Sideband in MC
	NonResFailResult_MC.SetStats(0)
	NonResFailResult_MC.SetLineColor(kRed)
	NonResFailResult_MC.SetLineStyle(3)
	NonResFailResult_MC.SetLineWidth(2)

	# TT bar (signal)
	NonResPasss_xT.SetStats(0)
	NonResPasss_xT.SetLineColor(kRed)
	NonResPasss_xT.SetFillColor(kRed)
	NonResPasss_xT.SetLineStyle(0)
	NonResPasss_xT.SetLineWidth(2)

	NonResFailResult.GetXaxis().SetTitle(varname+" [GeV]")
	NonResFailResult.GetYaxis().SetTitle("Events")
	NonResFailResult.GetXaxis().SetTitleSize(0.045)
	NonResFailResult.GetYaxis().SetTitleSize(0.045)

	FindAndSetMax([NonResPasss,NonResPasss_MC, NonResFailResult, NonResFailResult_MC, NonResPasss_xT],1.3)


	C = TCanvas("C", "", 800, 600)
	NonResPasss.SetMinimum(1)
	NonResFailResult.SetMinimum(1)
	NonResFailResult_MC.SetMinimum(1)
	NonResPasss_xT.SetMinimum(1)
	
	#C.SetLogy()	
	C.cd()
	
	CMSLABL, PRELABL, THILABL, CUTLABL, INTLABL = labels()
	if TT == True and theta == False: NonResFailResult.SetTitle("Fake Data w/ "+str(per)+"% ttbar, padded w/ "+str(ttper)+"% ttbar")
	else:
		if TT: NonResFailResult.SetTitle("Fake Data w/ "+str(per)+"% ttbar, padded w/ adjusted"+str(100+10*float(theta_mult))+"% ttbar")
		else: NonResFailResult.SetTitle("Fake Data w/ "+str(per)+"% ttbar")

	#NonResFailResult.GetYaxis().SetRangeUser(0,100)
	NonResFailResult.Draw("same")

	NonResPasss_xT.Draw("same")
	NonResPasss.Draw("same")
	
	#NonResFailResult_MC.Draw("same")
	#NonResFailResult_xT.Draw("same")
	#for i in Boxes:
	#	i.Draw("same")
	leg.Draw("same")
	CMSLABL.DrawLatex(0.1465,0.85,"CMS")
	THILABL.DrawLatex(0.81,0.91,"#bf{13 TeV}")
	PRELABL.DrawLatex(0.1465,0.812,"#bf{#it{Simulation Preliminary}}")
	CUTLABL.DrawLatex(0.1465,0.780,cut)
	INTLABL.DrawLatex(0.1465, 0.74, "xT INT:"+str(NonResPasss_xT.Integral()) )
	#C.SetLogy()
	C.SaveAs(to_dir+varname+".png")

def allvarcheck(from_dir, to_dir, cut="", per="", ttper="", eta=30, theta=False, theta_mult=0, TT=False):
	#checkplot("TAGM", xmin=50, xmax=350, from_dir=from_dir, to_dir=to_dir, cut=cut, tauerror = TAGMerr, TT=TT, per=per, ttper=ttper, theta=theta, theta_mult=theta_mult)
	#checkplot("TAGPt", xmin=380, xmax=1000, from_dir=from_dir, from_dir=from_dir, cut=cut, tauerror = TAGPterr)
	#checkplot("TPRIMEM", xmin=100, xmax=3000, from_dir=from_dir, from_dir=from_dir, cut=cut, tauerror = TPRIMEMerr)
	checkplot("ZPRIMEM", xmin=100, xmax=3000, from_dir=from_dir, to_dir=to_dir, cut=cut, tauerror = ZPRIMEMerr, TT=TT, per=per, ttper=ttper,V=eta, theta=theta, theta_mult=theta_mult)

if __name__ == "__main__":
	datalist = [50]
	for i in range(0,11):
		datalist.append(75+i*5)
	datalist.append(150)

	for name, cut in zip(["MC_T300-700_mu", "MC_T300-700_el", "MC_T700_mu", "MC_T700_el"], ["LepType>0&TPRIMEM>300&TPRIMEM<700","LepType<0&TPRIMEM>300&TPRIMEM<700","LepType>0&TPRIMEM>700","LepType<0&TPRIMEM>700"]):
	#for name, cut in zip(["MC_T700_mu", "MC_T700_el"], ["LepType>0&TPRIMEM>700","LepType<0&TPRIMEM>700"]):
		continue
		cut = cut 
		if not os.path.exists(name+"/Step4_EstimateWJets"): os.system("mkdir "+name+"/Step4_EstimateWJets")
		for d_percentage in datalist:
			if not os.path.exists(name+"/Step4_EstimateWJets/Data"+str(d_percentage)): os.system("mkdir "+name+"/Step4_EstimateWJets/Data"+str(d_percentage))
			reweights = [90, 100, 110]
			print d_percentage
			for percentage in reweights:
				if not os.path.exists(name+"/Step4_EstimateWJets/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent"): os.system("mkdir "+name+"/Step4_EstimateWJets/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent")
				allvarcheck(name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent", name+"/Step4_EstimateWJets/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent/", cut=cut, per = d_percentage, ttper = percentage, TT=True , theta=False, theta_mult="")

	##### With Theta

	for name, cut in zip(["MC_T300-700_mu", "MC_T300-700_el"], ["LepType>0&TPRIMEM>300&TPRIMEM<700","LepType<0&TPRIMEM>300&TPRIMEM<700"]):
		#continue
		if not os.path.exists(name): os.system("mkdir "+name)
		mult3_7 = [-0.15643711, -0.48724577, -0.41525396,  0.31182551, -0.47907558, -0.58681022, -0.62531646, -0.55915745, -0.57460736, -0.60871319, -0.63802833, -0.67408731, -0.78519764]

		#mult3_7 = [-0.75903969 , 0.13822555, -0.7090665,   0.38535657, -0.32161119, -0.31289817, -0.38169604, -0.45781972, -0.53846641, -0.56670386, -0.58219643]
		for d_percentage, mult in zip(datalist, mult3_7):
			#if not os.path.exists(name+"/Data"+str(d_percentage)): os.system("mkdir "+name+"/Data"+str(d_percentage))
			reweights = [100]
			print d_percentage
			for percentage in reweights:
				allvarcheck(name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent", name+"/Data"+str(d_percentage), cut=cut, per = d_percentage, ttper = percentage, TT=True , theta=True, theta_mult=mult)

	for name, cut in zip(["MC_T700_mu", "MC_T700_el"], ["LepType>0&TPRIMEM>700","LepType<0&TPRIMEM>700"]):
		#continue
		if not os.path.exists(name): os.system("mkdir "+name)
		mult7 = [ 0.56793588, -0.87834488, -0.87374568, -0.89569318, -0.89035545, -0.87904629, -0.87454649, -0.89851504, -0.92380554, -0.94765489, -0.96633587, -0.98372691,  -1.07721272]
		#mult7 = [-0.91372621, -0.98706262 , -0.90244119, -0.87706992, -0.80742297, -0.82797339,  -0.86991548, -0.91227049, -0.94476007, -0.95988757, -0.97635317]

		for d_percentage, mult in zip(datalist, mult7):
			#if not os.path.exists(name+"/Data"+str(d_percentage)): os.system("mkdir "+name+"/Data"+str(d_percentage))
			reweights = [100]
			print d_percentage
			for percentage in reweights:
				allvarcheck(name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent", name+"/Data"+str(d_percentage), cut=cut, per = d_percentage, ttper = percentage, TT=True , theta=True, theta_mult=mult)








