import os
import ROOT
from ROOT import *
from array import array
import math
from math import *

from Reweight import tt_reweigh
from Plotting_Header import *

def make_fake_data(percentages, source_dir ="/home/storage/andrzejnovak/FriedBacon/", save_to=''):
	print percentages
	for percentage in percentages:
		tt_reweigh([percentage], source_dir, save_to=save_to)

		make_dirs(save_to+"FakeData")
		os.system("hadd "+save_to+"FakeData/MCDATA"+str(percentage)+".root "+source_dir+"ST.root "+source_dir+"WJets*0.root "+source_dir+"WJets*Inf.root "+save_to+"TT_reweigh/TT"+str(percentage)+".root")

		print "Finished fake data:", percentage

if __name__ == '__main__':
	percentages = []
	for i in range(0,11):
		percentages.append(75+i*5)
	percentages.append(50)
	percentages.append(150)
	make_fake_data(percentages, source_dir = "/home/storage/andrzejnovak/FriedBacon/")
