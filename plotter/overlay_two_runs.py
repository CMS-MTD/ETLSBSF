
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
# chain_pro.Add("~/ScopeData/Reco/run_scope2725*.root")
chain_pro.Add("~/ScopeData/Reco/run_scope28237.root")
chain_pro.Add("~/ScopeData/Reco/run_scope28238.root")
chain_pro.Add("~/ScopeData/Reco/run_scope28239.root")
chain_beta = ROOT.TChain("pulse")
# chain_beta.Add("~/ScopeData/Reco/run_scope151249.root")
chain_beta.Add("~/ScopeData/Reco/run_scope151353.root")

hist_pro = ROOT.TH1D("hist_pro","",35,2,70)
hist_beta = ROOT.TH1D("hist_beta","",35,2,70)
hist_pro.StatOverflows(True)
hist_beta.StatOverflows(True)

amp_thresh = 65

# chain_pro.Project("hist_pro","-1000*integral[0]*1e9*50/4700","amp[0]>45&&amp[3]>50")
chain_pro.Project("hist_pro","-1000*integral[2]*1e9*50/4700","amp[2]>%0.2f&&amp[3]>50"%amp_thresh)
chain_beta.Project("hist_beta","-1000*integral[2]*1e9*50/4700","amp[2]>%0.2f&&amp[3]>10"%amp_thresh)

n_beta = hist_beta.Integral()
n_pro = hist_pro.Integral()

hist_pro.Scale(100.0/hist_pro.Integral())
hist_beta.Scale(100.0/hist_beta.Integral())

fitter_beta = lg.LanGausFit()
fitter_pro = lg.LanGausFit()
#fitter.SetParLimits(1,25,1000)
#f1 = fitter.fit(hist,None,None,20)
f_beta = fitter_beta.fit(hist_beta)
f_pro = fitter_pro.fit(hist_pro)
# ROOT.TF1("f1","landau",0,150)
#hist.Fit(f1)
print "proton width: ",f_pro.GetParameter(0)
print "beta width: ",f_beta.GetParameter(0)
print "proton MPV: ",f_pro.GetParameter(1)
print "beta MPV: ",f_beta.GetParameter(1)
print "proton gwidth: ",f_pro.GetParameter(3)
print "beta gwidth: ",f_beta.GetParameter(3)
c = ROOT.TCanvas("c1")
hist_beta.SetTitle(";Charge collected [fC];Fraction of events [%]")
hist_pro.SetTitle(";Charge collected [fC];Fraction of events [%]")

hist_pro.SetLineColor(colors[1])
hist_pro.SetLineWidth(2)
hist_pro.SetMarkerSize(0.75)
hist_pro.SetMarkerStyle(20)
hist_pro.SetMarkerColor(colors[1])
hist_beta.SetLineColor(colors[0])

f_beta.SetLineColor(colors[0])
f_pro.SetLineColor(colors[1])
# f_pro.SetLineStyle(7)
f_beta.SetLineStyle(2)
hist_beta.SetLineWidth(2)

leg_b = ROOT.TLegend(0.48,0.6,0.88,0.88)
leg_b.SetTextSize(0.04)
# leg_b.AddEntry(hist_beta,"#splitline{^{106}Ru #beta^{-} source}{#scale[0.8]{MPV: %0.1f #pm %0.1f fC (%i events)}}" %(f_beta.GetParameter(1),f_beta.GetParError(1),n_beta),"l")
leg_b.AddEntry(hist_beta,"#splitline{^{106}Ru #beta^{-} source}{MPV: %0.1f #pm %0.1f fC}" %(f_beta.GetParameter(1),f_beta.GetParError(1)),"l")
# leg_b.AddEntry(hist_pro,"#splitline{120 GeV proton beam}{#scale[0.8]{MPV: %0.1f #pm %0.1f fC (%i events)}}" %(f_pro.GetParameter(1),f_pro.GetParError(1),n_pro),"elp")
leg_b.AddEntry(hist_pro,"#splitline{120 GeV proton beam}{MPV: %0.1f #pm %0.1f fC }" %(f_pro.GetParameter(1),f_pro.GetParError(1)),"elp")
# leg_b.AddEntry(0, "N_{events} = %i, MPV = %0.1f fC" %(n_beta,f_beta.GetParameter(1)), "");

# leg_p = ROOT.TLegend(0.60,0.65,0.88,0.88)
# leg_p.AddEntry(hist_pro,"120 GeV proton beam","elp")
# leg_p.AddEntry(0, "N_{events} = %i, MPV = %0.1f fC" %(n_pro,f_pro.GetParameter(1)), "");



# leg.AddEntry(hist_pro,"120 GeV proton beam","elp")

latex= ROOT.TLatex()
latex.SetTextFont(62)
latex.SetTextSize(0.05)
latex.SetTextFont(42)


hist_beta.Draw("hist")
hist_pro.Draw("ep same")
f_beta.Draw("same")
f_pro.Draw("same")
leg_b.Draw("same")
latex.DrawLatexNDC(0.14,0.91,"HPK 3.1, 1x3 mm^{2} P2, 50 #mum IP")
latex.DrawLatexNDC(0.73,0.91,"170V, -20 C")
c.Print("beta_proton_overlay_charge.pdf")
c.Print("beta_proton_overlay_charge.root")


hist_pro_dt = ROOT.TH1D("hist_pro_dt","",40,0,700)
hist_beta_dt = ROOT.TH1D("hist_beta_dt","",40,0,700)
hist_pro_dt.StatOverflows(True)
hist_beta_dt.StatOverflows(True)

chain_pro.Project("hist_pro_dt","1e12*(LP2_20[2]-LP2_20[3]+2.424e-9)-6200","LP2_20[2]!=0 && amp[2]>%0.2f && LP2_20[3]!=0 && amp[3]>60 && amp[3]<120 && amp[2]<360"%amp_thresh)
chain_beta.Project("hist_beta_dt","1e12*(LP2_20[2]-LP2_20[3])-6200 -26","LP2_20[2]!=0 && amp[2]>%0.2f && LP2_20[3]!=0 && amp[3]>15 && amp[2]<360"%amp_thresh)
n_beta_dt = hist_beta_dt.Integral()
n_pro_dt = hist_pro_dt.Integral()

hist_pro_dt.Scale(100.0/hist_pro_dt.Integral())
hist_beta_dt.Scale(100.0/hist_beta_dt.Integral())
hist_beta_dt.SetTitle(";#DeltaT(LGAD - MCP) [ps];Fraction of events [%]")
hist_pro_dt.SetTitle(";#DeltaT(LGAD - MCP) [ps];Fraction of events [%]")

hist_pro_dt.SetLineColor(colors[1])
hist_pro_dt.SetLineWidth(2)
hist_pro_dt.SetMarkerSize(0.75)
hist_pro_dt.SetMarkerStyle(20)
hist_pro_dt.SetMarkerColor(colors[1])
hist_beta_dt.SetLineColor(colors[0])
hist_beta_dt.SetLineWidth(2)


f_beta_dt = ROOT.TF1("f1","gaus",80,300)
hist_beta_dt.Fit(f_beta_dt,"0")

f_pro_dt = ROOT.TF1("f2","gaus",80,300)
hist_pro_dt.Fit(f_pro_dt,"0")

f_beta_dt.SetLineColor(colors[0])
f_pro_dt.SetLineColor(colors[1])
# f_pro_dt.SetLineStyle(7)
f_beta_dt.SetLineStyle(2)

leg_dt = ROOT.TLegend(0.50,0.6,0.88,0.88)
leg_dt.SetTextSize(0.04)
# leg_dt.AddEntry(hist_beta_dt,"#splitline{^{106}Ru #beta^{-} source}{#scale[0.8]{#sigma: %0.1f #pm %0.1f ps (%i events)}}" %(f_beta_dt.GetParameter(2),f_beta_dt.GetParError(2),n_beta_dt),"l")
leg_dt.AddEntry(hist_beta_dt,"#splitline{^{106}Ru #beta^{-} source}{#sigma: %0.1f #pm %0.1f ps}" %(f_beta_dt.GetParameter(2),f_beta_dt.GetParError(2)),"l")
# leg_dt.AddEntry(hist_pro_dt,"#splitline{120 GeV proton beam}{#scale[0.8]{#sigma: %0.1f #pm %0.1f ps (%i events)}}" %(f_pro_dt.GetParameter(2),f_pro_dt.GetParError(2),n_pro_dt),"elp")
leg_dt.AddEntry(hist_pro_dt,"#splitline{120 GeV proton beam}{#sigma: %0.1f #pm %0.1f ps}" %(f_pro_dt.GetParameter(2),f_pro_dt.GetParError(2)),"elp")

print "proton gaus mean: ",f_pro_dt.GetParameter(1)
print "beta gaus mean: ",f_beta_dt.GetParameter(1)

hist_pro_dt.Draw("ep")
hist_beta_dt.Draw("hist same")
hist_pro_dt.Draw("ep same")
f_beta_dt.Draw("same")
f_pro_dt.Draw("same")
leg_dt.Draw("same")
latex.DrawLatexNDC(0.14,0.91,"HPK 3.1, 1x3 mm^{2} P2, 50 #mum IP")
# latex.DrawLatexNDC(0.14,0.91,"1x3 mm^{2} P2, 50 #mum")
latex.DrawLatexNDC(0.73,0.91,"170V, -20 C")
c.Print("beta_proton_overlay_dt.pdf")
c.Print("beta_proton_overlay_dt.root")



	# if ch==2: c.Print("plots/runs/Run%i_charge.pdf"%run)
	# else: c.Print("plots/runs/Run%i_ch%i_charge.pdf"%(run,ch))
	# c.Print("plots/runs/Run%i_charge.root"%run)
	# c.Print("plots/runs/Run%i_charge.C"%run)
# return f1.GetParameter(1),f1.GetParError(1)
