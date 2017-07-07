#
from numpy import genfromtxt
from ROOT import *
from array import array
import numpy as np

my_data = genfromtxt('MC_T300-700_Data.csv', delimiter=',')
my_data2 = genfromtxt('MC_T700_Data.csv', delimiter=',')

x = my_data.T[0]

mult1 = my_data.T[1]
mult2 = my_data2.T[1]

print "3-7   ", mult1
print "7-    ", mult2

e1 = my_data.T[2]
e2 = my_data2.T[2]


x = array("d", x) 

y1 = array("d", mult1)
y2 = array("d", mult2)

e1 = array("d", e1)
e2 = array("d", e2)
ex = array("d", np.zeros(len(x)))

	  	
C = TCanvas("C", "", 800, 800)
C.cd()		
P = TGraphErrors(len(x),x,y1,ex, e1)
P.SetMarkerStyle(20)
P.SetTitle("Theta results")
P.GetXaxis().SetTitle("TTbar % in fake data")
P.GetYaxis().SetTitle("Theta adjustment")
P.GetYaxis().SetRangeUser(-1.2, 0.6)

P2 = TGraphErrors(len(x),x,y2,ex, e2)
P2.SetMarkerStyle(20)
P2.SetMarkerColor(kBlue)

leg = TLegend(0.65,0.7,0.89,0.89)
leg.SetHeader("Channels")
leg.AddEntry(P, "T'(M) 300-700", "PL")
leg.AddEntry(P2, "T'(M) 700-", "PL")
leg.SetLineColor(0)
leg.SetFillColor(0)

P.Draw("AP")
P2.Draw("P")
leg.Draw("same")

C.SaveAs("Theta_res.png")
