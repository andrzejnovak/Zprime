from Reweight import tt_reweigh
from MakeData import make_fake_data
from DDT import *
from ModTreeFiles import *
from EstimateWJets import *
from Plotting_Header import *
from Prep_theta import *

# Basic settings
bin_x = [100,250,8]
bin_y = [380,2000,8]
root_files = '/home/storage/andrzejnovak/FriedBacon/'
ST, Ws = [root_files+'ST.root'], [root_files+'WJets.root']

# Run specific settings
etas, eta_names = [20,30,40], ['eta20', 'eta30', 'eta40']
datalist = [80, 100, 120]
names = ["MC_T300-700_mu", "MC_T300-700_el", "MC_T700_mu", "MC_T700_el" ]
cuts = ["T.TPRIMEM>300 and T.TPRIMEM<700 and T.LepType>0", "T.TPRIMEM>300 and T.TPRIMEM<700 and T.LepType<0", "T.TPRIMEM>700 and T.LepType>0", "T.TPRIMEM>700 and T.LepType<0"]
root_cuts =  ["LepType>0&TPRIMEM>300&TPRIMEM<700","LepType<0&TPRIMEM>300&TPRIMEM<700","LepType>0&TPRIMEM>700","LepType<0&TPRIMEM>700"]

# Specify absolute folder to store analysis files/output
over_dir = "/home/storage/andrzejnovak/test_Analysis/"

# Prepare TT reweighs:
#tt_reweigh([80,90,100,110,120], root_files, over_dir)

# Prepare fake data:
#make_fake_data([80,100,120], root_files, over_dir)


def run_DDT():
	for eta, run in zip(etas, eta_names):
		run = over_dir+run
		make_dirs(run)
		print run
		for name, cut in zip(names,cuts):
			# DDT
			f = open(run+"/"+name+".html", 'w')
			f.write("<html><table>")
			table = [["TT% in data", "TT%", "Signal_data", "Signal_WJets", "Sideband_data", "Sideband_WJets"]]
			for d_percentage in datalist:
				Data =[over_dir+"FakeData/MCDATA"+str(d_percentage)+".root"]

				reweights = [90, 100, 110]
				for percentage in reweights:
					name_dir = "tt"+str(percentage)+"percent"
					folder = run+"/"+name+"/Step2_DDT/Data"+str(d_percentage)+"/"+name_dir
					TT = [over_dir+"TT_reweigh/TT"+str(percentage)+".root"]
				
					counts = study(Data, TT, ST, Ws, cut, analysis_folder = folder, toretain=eta, data=False, lumi=35.9, bins_x = bin_x, bins_y = bin_y)
					row = [str(d_percentage), str(percentage)]
					for val in counts: row.append(str(val))			
					table.append(row)
					print row

			for row in table		:
				print row
				f.write("<tr><td>"+"</td><td>".join(row)+"</td></tr>")
			f.write("</table></html>")
			f.close()
	

def run_ModTreeFiles():
	for eta, run in zip(etas, eta_names):
		run = over_dir+run
		make_dirs(run)
		print run
		for name, cut in zip(names,cuts):
			for d_percentage in datalist:	
				File_names = ["ST.root", "WJets.root", "TT"+str(d_percentage)+".root", "MCDATA"+str(d_percentage)+".root"]

				reweights = [90, 100, 110]
				for percentage in reweights:
					name_dir = "tt"+str(percentage)+"percent"
					for d in File_names:
						mod_trees(d, root_files, run+"/"+name+"/Step2_DDT/Data"+str(d_percentage)+"/"+name_dir,  run+"/"+name+ "/Step3_ModTreeFiles/Data"+str(d_percentage)+"/"+name_dir , over_dir )


# Plot Estimate
def run_EstimateWJets():
	for eta, run in zip(etas, eta_names):
		run = over_dir+run
		for name, cut in zip(names, root_cuts):
			for d_percentage in datalist:
				reweights = [90, 100, 110]
				print d_percentage
				for percentage in reweights:
					allvarcheck(run+"/"+name+"/Step3_ModTreeFiles/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent", run+"/"+name+"/Step4_EstimateWJets/Data"+str(d_percentage)+"/tt"+str(percentage)+"percent/", eta=eta, cut=cut, per = d_percentage, ttper = percentage, TT=True , theta=False, theta_mult="")


# Prep Theta
def run_Prep_theta():
	for eta, run in zip(etas, eta_names):
		run = over_dir+run
		for name, cut in zip(["MC_T300-700_", "MC_T700_"], ["TPRIMEM>300&TPRIMEM<700", "TPRIMEM>700"]):
			for d_percentage in datalist:			
				from_dir = "Data"+str(d_percentage)+"/"
				to_dir = run+"/"
				make_theta_file(name, from_dir, to_dir, str(d_percentage), cut)




#run_DDT()
run_ModTreeFiles()
run_EstimateWJets()
run_Prep_theta()
