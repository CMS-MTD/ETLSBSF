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


run_number = 151353#28237
event_number = 136#166
beta = run_number>30000
Q = 21.7
ptk_multiplier =5

chain = ROOT.TChain("pulse") 
# chain_pro.Add("~/ScopeData/Reco/run_scope2725*.root")
chain.Add("~/ScopeData/Reco/run_scope%i.root"%run_number)

if not beta: h_frame = ROOT.TH2F("h_frame","",3,-227,-193,3,-130,20)
else: h_frame = ROOT.TH2F("h_frame","",3,-20,20,3,-130,20)

h_frame.SetTitle(";Time [ns];Amplitude [mV]")
c = ROOT.TCanvas("c1","",1000,600)
h_frame.Draw()


chain.SetLineWidth(2)
chain.SetMarkerStyle(20)
chain.SetMarkerSize(0.5)
# chain.SetLineColor(colors[3])
# chain.SetMarkerColor(colors[3])
#chain.Draw("channel[2]:1e9*time[0]>>h_lgad","i_evt==%i"%event_number,"lp same")

chain.SetLineColor(colors[2])
chain.SetMarkerColor(colors[2])
chain.Draw("%i*channel[3]:1e9*time[0]>>h_ptk"%ptk_multiplier,"i_evt==%i"%event_number,"lp same")
h_ptk=ROOT.h_ptk
chain.SetLineColor(colors[3])
chain.SetMarkerColor(colors[3])
chain.Draw("channel[2]:1e9*time[0]>>h_lgad","i_evt==%i"%event_number,"lp same")
h_lgad=ROOT.h_lgad
latex= ROOT.TLatex()
latex.SetTextFont(62)
latex.SetTextSize(0.045)
if not beta: latex.DrawLatexNDC(0.15,0.91,"FNAL 120 GeV proton beam")
else: latex.DrawLatexNDC(0.15,0.91,"^{106}Ru #beta^{-} source")
latex.DrawLatexNDC(0.61,0.91,"HPK type 3.1, 170V, -20 C")

leg = ROOT.TLegend(0.17,0.57,0.48,0.73)
leg.AddEntry(h_lgad,"LGAD signal (Q = %0.1f fC)"%Q,"lp")
if beta: leg.AddEntry(h_ptk,"MCP-PMT signal (%ix)"%ptk_multiplier,"lp")
else: leg.AddEntry(h_ptk,"MCP-PMT signal","lp")
leg.Draw()
# h_lgad.SetLineWidth(2)
# h_lgad.SetLineColor(colors[3])
# h_lgad.SetMarkerColor(colors[3])

# h_ptk.SetLineWidth(2)
# h_ptk.SetLineColor(colors[2])
# h_ptk.SetMarkerColor(colors[2])

#h_ptk.Draw("lp")
#h_lgad.Draw("lp same")

c.Print("displays/run%i_event%i.pdf"%(run_number,event_number))
c.Print("displays/run%i_event%i.root"%(run_number,event_number))

