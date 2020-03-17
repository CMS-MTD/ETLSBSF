
import os, sys, re
import ROOT
from array import array
import langaus as lg

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLabelFont(42,"xyz")
ROOT.gStyle.SetLabelSize(0.05,"xyz")
#ROOT.gStyle.SetTitleFont(42)
ROOT.gStyle.SetTitleFont(42,"xyz")
ROOT.gStyle.SetTitleFont(42,"t")
#ROOT.gStyle.SetTitleSize(0.05)
ROOT.gStyle.SetTitleSize(0.06,"xyz")
ROOT.gStyle.SetTitleSize(0.06,"t") 
ROOT.gStyle.SetPadBottomMargin(0.14)
ROOT.gStyle.SetPadLeftMargin(0.14)
ROOT.gStyle.SetTitleOffset(1,'y')
ROOT.gStyle.SetLegendTextSize(0.035)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridColor(14)
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetOptStat(0)
one = ROOT.TColor(2001,0.906,0.153,0.094)
two = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four =ROOT.TColor(2004,0.071,0.694,0.18)
five =ROOT.TColor(2005,0.388,0.098,0.608)
six=ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006]


chain_pro = ROOT.TChain("pulse") 
chain_pro.Add("~/ScopeData/Reco/run_scope2725*.root")
chain_beta = ROOT.TChain("pulse")
chain_beta.Add("~/ScopeData/Reco/run_scope151249.root")

hist_pro = ROOT.TH1D("hist_pro","",50,2,100)
hist_beta = ROOT.TH1D("hist_beta","",50,2,100)


chain_pro.Project("hist_pro","-1000*integral[0]*1e9*50/4700","amp[0]>45&&amp[3]>50")
chain_beta.Project("hist_beta","-1000*integral[2]*1e9*50/4700","amp[2]>45&&amp[3]>10")

hist_pro.Scale(1.0/hist_pro.Integral())
hist_beta.Scale(1.0/hist_beta.Integral())

fitter_beta = lg.LanGausFit()
fitter_pro = lg.LanGausFit()
#fitter.SetParLimits(1,25,1000)
#f1 = fitter.fit(hist,None,None,20)
f_beta = fitter_beta.fit(hist_beta)
f_pro = fitter_pro.fit(hist_pro)
# ROOT.TF1("f1","landau",0,150)
#hist.Fit(f1)
leg = ROOT.TLegend(0.65,0.65,0.88,0.88)
c = ROOT.TCanvas("c1")
hist_beta.SetTitle(";Integrated charge [fC];Events")
hist_pro.SetTitle(";Integrated charge [fC];Events")

hist_pro.SetLineColor(colors[1])
hist_pro.SetLineWidth(2)
hist_pro.SetMarkerSize(0.5)
hist_pro.SetMarkerStyle(20)
hist_pro.SetMarkerColor(colors[1])
hist_beta.SetLineColor(colors[0])

f_beta.SetLineColor(colors[0])
f_pro.SetLineColor(colors[1])
f_pro.SetLineStyle(7)
f_beta.SetLineStyle(2)
hist_beta.SetLineWidth(2)

leg.AddEntry(hist_beta,"Beta source","l")
leg.AddEntry(hist_pro,"Proton beam","l")

hist_beta.Draw("hist")
hist_pro.Draw("ep same")
f_beta.Draw("same")
f_pro.Draw("same")
leg.Draw("same")
c.Print("beta_proton_overlay.pdf")
	# if ch==2: c.Print("plots/runs/Run%i_charge.pdf"%run)
	# else: c.Print("plots/runs/Run%i_ch%i_charge.pdf"%(run,ch))
	# c.Print("plots/runs/Run%i_charge.root"%run)
	# c.Print("plots/runs/Run%i_charge.C"%run)
# return f1.GetParameter(1),f1.GetParError(1)
