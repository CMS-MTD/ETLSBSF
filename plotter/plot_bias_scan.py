
import os, sys, re
import ROOT
from array import array
import langaus as lg
import copy

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
ROOT.gStyle.SetOptFit(1)
one = ROOT.TColor(2001,0.906,0.153,0.094)
two = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four =ROOT.TColor(2004,0.071,0.694,0.18)
five =ROOT.TColor(2005,0.388,0.098,0.608)
six=ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,]

verbose = True
charge_thresh = 10 #fC
photek_res = 15 #ps for beta
photek_res_beam = 9 #ps
diodeTarget = 41. #mV
PiNCharge = 0.36 #fC
doAverage=False
doCFDScan=False
n_channels=8

def get_extra_cut(run,ch):
	extra_cut = ""
	if run>=152852 and run<= 152859: ## crosstalk in 3rd gen sergey board.
		if ch==2: extra_cut="&& amp[2]>amp[1]"
		elif ch==1: extra_cut="&& amp[1]>amp[2]"

	if run>=153504 and run<=153556:
		extra_cut="&& amp[2]>amp[1] && amp[2]>amp[0]"

	return extra_cut

def get_min_amp(run,ch):
	minAmp =15
	if run==151172 or run==151173: minAmp = 40
	if run>151244 and run <=151250: minAmp = 40
	if run>=2023 and run <=2025: minAmp=40
	if run>=2026 and run <=2028: minAmp=70
	if run==2022: minAmp=30
	if run >= 151357 and run<=151374: minAmp=10
	if run==151647 or run==151739: minAmp=30
	if run>=151639 and run<=151653: minAmp=45
	if run>=151818 and run<=151822: minAmp=45
	if run>=151866 and run<=151870: minAmp=45
	if run>=151848 and run<=151854: minAmp=45
	if run>=151835 and run<=151838: minAmp=45
	if run>=151649 and run<=151653: minAmp=45
	if run>=151168 and run<=151169: minAmp=45
	if run>=151896 and run<=151902: minAmp=45
	if run>=151994 and run<=151997: minAmp=45
	elif run>=152104 and run<=152108: minAmp=50
	if run>=27000 and run<30000: minAmp=35
	# if run>=27338 and run<30000: minAmp=60
	if run>=27250 and run<=27268: minAmp=70
	if run>=28256 and run<=28267: minAmp=15
	if run>= 152726 and run <= 152731: minAmp=45
	if run>=152782 and run <=152782: minAmp=45
	if run>=152858 and run<=152859: minAmp=55
	if run>=152856 and run<=152857: minAmp=30
	if run>=152870 and run<=152877: minAmp=45
	if run>=152884 and run<=152891: minAmp=45
	if run>=152901 and run<=152908: minAmp=45
	if run>=152917 and run<=152924: minAmp=45
	if run>=152926 and run<=152942: minAmp=45
	if run>=152945 and run<=152949: minAmp=45
	if run>=152953 and run<=152957: minAmp=45
	if run>=152961 and run<=152965: minAmp=45
	if run>=152973 and run<=152979: minAmp=45
	if run>=152980 and run<=152983: minAmp=100
	if run>=153005 and run<=153006: minAmp=60
	if run>=153010 and run<=153021: minAmp=45
	if run>=153034 and run<=153037: minAmp=50
	if run>=153038 and run<=153039: minAmp=90
	if run>=153490 and run <=153491: minAmp = 40
	if run>=153492 and run <=153493: minAmp = 65
	if run>=153499 and run <=153500: minAmp = 40
	if run>=153501 and run <=153502: minAmp = 65
	if run>=153504 and run<=153507: minAmp=30
	if run>=153508 and run<=153509: minAmp=50
	if run>=153510 and run<=153518: minAmp=30
	if run>=153519 and run<=153522: minAmp=70
	if run>=153533 and run<=153537: minAmp=40
	if run>=153538 and run<=153544: minAmp=60
	if run>=153552 and run<=153555: minAmp=50
	if run>=153556 and run<=153556: minAmp=70
	if run>=153323 and run<=153325: minAmp=30
	if run>=153440 and run<=153445: minAmp=50
	if run>=153261 and run<=153266: minAmp=50
	if run>=153283 and run<=153289: minAmp=50

	if run>=36280 and run<=36289: minAmp=30
	if run>=36210 and run<=36219: minAmp=25
	if run>=36520 and run<=36529: minAmp=30
	if run==38352 and ch==0: minAmp=50
	if run==38352 and ch==1: minAmp=30
	if run==39510 or run==43150 or run==44070: minAmp=70
	if run==44100: minAmp=100
	if run==44070 and ch==0:minAmp=100
	if run>=153302 and run<=153306: minAmp=50
	if run>=50000 and run<70000: minAmp=50
	return minAmp


def get_time_range(run,ch):
	mint = 5.8e-9
	maxt =6.8e-9

	if run>=2022 and run<= 2028:
		mint = -3.3e-9
		maxt = -1.6e-9
	if run>=151982 and run<=151997:
		mint = 6.2e-9
		maxt = 7.2e-9

	if run>=152104 and run<=152108: 
		mint = 4.7e-9
		maxt = 5.7e-9

	if run>27000 and run<30000:
		mint = 6.4e-9 
		maxt = 7.4e-9

	if run>28200 and run<30000:
		mint = 3.5e-9 
		maxt = 4.5e-9

	if run>=153485 and run<=153503:
		mint = 3.3e-9
		maxt = 4.9e-9
	
	if run>=153504 and run<=153556:
		mint=2e-9
		maxt=3e-9

	if run>=153579 and run<=153618:
		mint=0.5e-9
		maxt=1.5e-9

	if run>=826 and run<=840:
		mint=-0.3e-9
		maxt=0.7e-9

	if run>=153621 and run<=153630:
		mint=-0.3e-9
		maxt=0.7e-9

	if run>50000 and run<70000:
		mint=1.5e-9
		maxt=3.0e-9

	return mint,maxt


def get_photek_params(run):
	photek_thresh = 15
	photek_max = 200
	photek_chan=3
	if run>=2022 and run<= 2028: photek_thresh=50
	if run>27000 and run<30000:
		photek_thresh =50
		photek_max = 100
	if run>28200 and run<30000:
		photek_thresh =60
		photek_max = 120

	if run>50000 and run<70000:
		photek_thresh =200
		photek_max = 350
		photek_chan=7

	return photek_thresh,photek_max,photek_chan	

def prep_dirs():
	if not os.path.exists("plots"):
		os.makedirs("plots")	
	if not os.path.exists("plots/runs"):
		os.makedirs("plots/runs")	

def plot_single_scan(scan_num,graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias, graph_time_res,name,temp):
	cosmetic_tgraph(graph,3)
	cosmetic_tgraph(graph_MCP,6)
	cosmetic_tgraph(graph_temp,1)
	cosmetic_tgraph(graph_lgadbias,5)
	cosmetic_tgraph(graph_current_lgadbias,2)
	cosmetic_tgraph(graph_time_res,4)

	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()
	mgraph = ROOT.TMultiGraph()
	#mgraph.Add(graph_MCP)
	mgraph.Add(graph_temp)
	mgraph.Add(graph_current_lgadbias)
	mgraph.Add(graph)
	#mgraph.Add(graph_lgadbias)
	mgraph.Add(graph_time_res)

	mgraph.SetTitle("; Bias voltage [V]; MPV beta response [mV]")
	# graph.Draw("AELP")
	# graph_MCP.Draw("ELP same")
	# graph_norm.Draw("ELP same")
	# graph_temp.Draw("ELP same")
	#mgraph.SetMinimum(-5)
	mgraph.Draw("AELP")
	leg = ROOT.TLegend(0.2,0.65,0.65,0.89)
	leg.SetMargin(0.15)
	#leg.AddEntry(graph_MCP, "MCP","EP")
	leg.AddEntry(graph_temp, "Measured temperature [C]","EP")
	leg.AddEntry(graph_current_lgadbias, "Current [100 nA]","EP")
	leg.AddEntry(graph, "%s, MPV beta response [mV]" % (name),"EP")
	#leg.AddEntry(graph_lgadbias, "%s, corrected LGAD bias"%name,"EP")
	leg.AddEntry(graph_time_res, "%s, time resolution [ps]"%name,"EP")
	
	leg.Draw()
	c.Print("plots/scan%i.pdf"%scan_num)


def plot_noise(graphs_noise):
	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()
	mgraph = ROOT.TMultiGraph()
	leg = ROOT.TLegend(0.2,0.3,0.4,0.49)
	
	#leg.SetMargin(0.15)
	
	for i,graph in enumerate(graphs_noise):
		cosmetic_tgraph(graph,i)
		mgraph.Add(graph)
		leg.AddEntry(graph,"Ch %i"%i,"EP")


	mgraph.SetTitle("; Bias voltage [V]; Mean baseline RMS [mV]")	
	mgraph.Draw("AELP")
	leg.Draw()

	c.Print("plots/scan%i_noise.pdf"%scan_num)

def plot_overlay(outfile,names,temps,series_num,plottype):
	if plottype==1: 
		outputtag = ""
		y_axis = "MPV amplitude [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr"
	if plottype==2: 
		outputtag = "_corr"
		y_axis = "MPV amplitude [mV]"
		x_axis = "Bias voltage [V]"
		filename = "grlgad"
	if plottype==3: 
		outputtag = "_IV"
		y_axis = "Total current [uA]"
		x_axis = "Bias voltage [V]"
		filename = "griv"
	if plottype==4: 
		outputtag = "_timeres"
		y_axis = "Time resolution [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grres"
	if plottype==5: 
		outputtag = "_snr"
		y_axis = "Signal to noise ratio"
		x_axis = "Bias voltage [V]"
		filename = "grsnr"
	if plottype==6: 
		outputtag = "_res_vs_snr"
		y_axis = "Time resolution [ps]"
		x_axis = "Signal to noise ratio"
		filename = "grres_vs_snr"
	if plottype==7: 
		outputtag = "_res_vs_amp"
		y_axis = "Time resolution, LGAD only [ps]"
		x_axis = "MPV amplitude [mV]"
		filename = "grres_vs_mpv"
	if plottype==8: 
		outputtag = "_mpv_vs_snr"
		y_axis = "MPV Ru106 response [mV]"
		x_axis = "Signal to noise ratio"
		filename = "grmpv_vs_snr"
	if plottype==9: 
		outputtag = "_slewrate"
		y_axis = "Mean slew rate [mV/ns]"
		x_axis = "Bias voltage [V]"
		filename = "grslew"
	if plottype==10: 
		outputtag = "_res_vs_slew"
		y_axis = "Time resolution, LGAD only [ps]"
		x_axis = "Mean slew rate [mV/ns]"
		filename = "grres_vs_slew"
	if plottype==11: 
		outputtag = "_risetime"
		y_axis = "Risetime [ps] (10 to 90%)"
		x_axis = "Bias voltage [V]"
		filename = "grrise"
	if plottype==12: 
		outputtag = "_risetime_vs_mpv"
		y_axis = "Risetime [ps] (10 to 90%)"
		x_axis = "MPV Ru106 response [mV]"
		filename = "grrisetime_vs_mpv"
	if plottype==13: 
		outputtag = "_lgadnoise_vs_bias"
		y_axis = "LGAD baseline noise RMS [mV]"
		x_axis = "Bias voltage [V]"
		filename = "grlgadnoise_vs_bias"
	if plottype==14: 
		outputtag = "_charge_vs_bias"
		y_axis = "MPV collected charge [fC]"
		x_axis = "Bias voltage [V]"
		filename = "grcharge"
	if plottype==15: 
		outputtag = "_charge_vs_amp"
		y_axis = "MPV collected charge [fC]"
		x_axis = "MPV amplitude [mV]"
		filename = "grcharge_vs_amp"
	if plottype==16: 
		outputtag = "_res_vs_charge"
		y_axis = "Time resolution, LGAD + MCP [ps]"
		x_axis = "MPV collected charge [fC]"
		filename = "grres_vs_charge"
	if plottype==17: 
		outputtag = "_res_corr_vs_charge"
		y_axis = "Time resolution, LGAD only [ps]"
		x_axis = "MPV collected charge [fC]"
		filename = "grres_corr_vs_charge"
	if plottype==18: 
		outputtag = "_risetime_vs_charge"
		y_axis = "Risetime [ps] (10 to 90%)"
		x_axis = "MPV collected charge [fC]"
		filename = "grrisetime_vs_charge"
	if plottype==19: 
		outputtag = "_slew_vs_charge"
		y_axis = "Mean slew rate [mV/ns]"
		x_axis = "MPV collected charge [fC]"
		filename = "grslew_vs_charge"
	if plottype==20: 
		outputtag = "_jitter"
		y_axis = "Expected jitter [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grjitter"
	if plottype==21: 
		outputtag = "_diode"
		y_axis = "Diode MPV amp [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr_diode"
	if plottype==22: 
		outputtag = "_amp_laser_norm"
		y_axis = "MPV amplitude, normalized [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr_amp_laser_norm"
	if plottype==23: 
		outputtag = "_diode_charge"
		y_axis = "Diode MPV charge [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr_diode_charge"
	if plottype==24: 
		outputtag = "_charge_laser_norm"
		y_axis = "MPV charge, normalized [fC]"
		x_axis = "Bias voltage [V]"
		filename = "gr_charge_laser_norm"
	if plottype==25: 
		outputtag = "_diode_charge_vs_amp"
		y_axis = "Diode MPV collected charge [fC]"
		x_axis = "Diode MPV amplitude [mV]"
		filename = "gr_diode_charge_vs_amp"
	if plottype==26: 
		outputtag = "_charge_amp_ratio"
		y_axis = "Approx. pulse duration (Q/0.5V) [ns]"
		x_axis = "Bias voltage [V]"
		filename = "gr_charge_amp_ratio"
	if plottype==27: 
		outputtag = "_diode_charge_amp_ratio"
		y_axis = "Approx. pulse duration (Q/0.5V) [ns]"
		x_axis = "Bias voltage [V]"
		filename = "gr_diode_charge_amp_ratio"
	if plottype==28: 
		outputtag = "_amp_average"
		y_axis = "Amplitude of average pulse [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr_amp_average"
	if plottype==29: 
		outputtag = "_diode_amp_average"
		y_axis = "Amplitude of average pulse [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr_diode_amp_average"
	if plottype==30: 
		outputtag = "_average_amp_vs_amp"
		y_axis = "Amplitude of average pulse [mV]"
		x_axis = "MPV amplitude [mV]"
		filename = "gr_average_amp_vs_amp"
	if plottype==31: 
		outputtag = "_diode_average_amp_vs_amp"
		y_axis = "Diode amplitude of average pulse [mV]"
		x_axis = "Diode MPV amplitude [mV]"
		filename = "gr_diode_average_amp_vs_amp"
	if plottype==32: 
		outputtag = "_amp_average_laser_norm"
		y_axis = "Amplitude of average pulse, normalized [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr_amp_average_laser_norm"
	if plottype==33: 
		outputtag = "_charge_average_laser_norm"
		y_axis = "Charge of average pulse, normalized [fC]"
		x_axis = "Bias voltage [V]"
		filename = "gr_charge_average_laser_norm"
	if plottype==34: 
		outputtag = "_charge_average"
		y_axis = "Charge of average pulse [fC]"
		x_axis = "Bias voltage [V]"
		filename = "gr_charge_average"
	if plottype==35: 
		outputtag = "_gain"
		y_axis = "Laser gain"
		x_axis = "Bias voltage [V]"
		filename = "gr_gain"
	if plottype==36: 
		outputtag = "_timeres_corr"
		y_axis = "Time resolution, LGAD only [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grres_corr"
	if plottype==37: 
		outputtag = "_timeres_cfd_scan"
		y_axis = "Time resolution, CFD scan [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grres_cfd_scan"
	if plottype==38: 
		outputtag = "_optimum_CFD"
		y_axis = "Optimum CFD threshold"
		x_axis = "Bias voltage [V]"
		filename = "groptimum_CFD"
	if plottype==39: 
		outputtag = "_cfd_scan_delta"
		y_axis = "Improvement from optimal CFD threshold"
		x_axis = "Bias voltage [V]"
		filename = "grres_cfd_scan_delta"
	if plottype==40: 
		outputtag = "_timeres_cfd_scan_corr"
		y_axis = "Time resolution, LGAD only, CFD scan [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grres_cfd_scan_corr"
	if plottype==41: 
		outputtag = "_lgadnoise_vs_charge"
		y_axis = "LGAD baseline noise RMS [mV]"
		x_axis = "MPV collected charge [fC]"
		filename = "grlgadnoise_vs_charge"
	if plottype==42: 
		outputtag = "_lgadnoise_vs_current"
		y_axis = "LGAD baseline noise RMS [mV]"
		x_axis = "Total current [uA]"
		filename = "grlgadnoise_vs_current"
	if plottype==43: 
		outputtag = "_charge_vs_current"
		y_axis = "MPV collected charge [fC]"
		x_axis = "Total current [uA]"
		filename = "grcharge_vs_current"
	if plottype==44: 
		outputtag = "_chi2_vs_bias"
		y_axis = "#chi^{2}"
		x_axis = "Bias voltage [V]"
		filename = "grres_chi2"
	if plottype==45: 
		outputtag = "_timeresCB"
		y_axis = "Time resolution [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grresCB"
	if plottype==46: 
		outputtag = "_timeres_corrCB"
		y_axis = "Time resolution, LGAD only [ps]"
		x_axis = "Bias voltage [V]"
		filename = "grres_corrCB"
	if plottype==47: 
		outputtag = "_chi2_vs_biasCB"
		y_axis = "#chi^{2}"
		x_axis = "Bias voltage [V]"
		filename = "grres_chi2CB"

	if plottype==48: 
		outputtag = "_timeres_corr_vs_run"
		y_axis = "Time resolution, LGAD only [ps]"
		x_axis = "Run number"
		filename = "grres_corr_vs_runnum"

	if plottype==49: 
		outputtag = "_charge_vs_run"
		y_axis = "MPV collected charge [fC]"
		x_axis = "Run number"
		filename = "grcharge_vs_runnum"
	if plottype==50: 
		outputtag = "_current_vs_run"
		y_axis = "Total current [uA]"
		x_axis = "Run number"
		filename = "grcurrent_vs_runnum"

	if plottype==51: 
		outputtag = "_temp_vs_run"
		y_axis = "Board temperature [C]"
		x_axis = "Run number"
		filename = "grtemp_vs_runnum"

	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()

	showtemp =True
	showCMS =True
	if series_num=="CMS" or series_num=="ATLAS" or series_num=="CMSATLAS": 
		showtemp=False
		showCMS = False
	if series_num=="Sergey" or series_num=="2" or series_num=="TBCold" or "HPK2_cold" or "HPK2_8e14" in series_num:
		showtemp=False
	if "temp" in series_num: showtemp=True
	mgraph = ROOT.TMultiGraph()
	if "HPK2_8e14_1p5e15" in series_num or "HPK2_repro" in series_num:
		if "split34" not in series_num: leg = ROOT.TLegend(0.2,0.7,0.83,0.89)
		else: leg = ROOT.TLegend(0.2,0.78,0.83,0.89)
	if "HPK2_split" or "FBK" in series_num:
		leg = ROOT.TLegend(0.15,0.7,0.89,0.89)

	elif( plottype == 1 or plottype== 9 or plottype == 14 or plottype==19 or plottype==22 or plottype==24 or plottype==25 or plottype==35 or plottype==39 or plottype==13 or plottype==41 or plottype==3 or plottype==38 or plottype==42 or plottype==43) and series_num!="7":
		if (plottype==1 or plottype==9 or plottype==14) and series_num=="HPK2_8e14": leg = ROOT.TLegend(0.41,0.62,0.63,0.86)
		elif "PiN" in series_num: leg = ROOT.TLegend(0.5,0.16,0.85,0.40)
		elif "LaserJune8LowBV" in series_num and plottype!=24 and plottype!=35: leg = ROOT.TLegend(0.5,0.52,0.85,0.86)
		elif showtemp: leg = ROOT.TLegend(0.17,0.52,0.42,0.86)
		else:
			if series_num=="2": leg = ROOT.TLegend(0.2,0.58,0.43,0.86)
			else: leg = ROOT.TLegend(0.15,0.62,0.4,0.86)	
	elif plottype==19 and series_num=="7":
		leg = ROOT.TLegend(0.5,0.16,0.85,0.40)
	elif plottype == 15:
		leg= ROOT.TLegend(0.5,0.16,0.86,0.4)
	else:
		if showtemp:
			leg = ROOT.TLegend(0.5,0.52,0.85,0.86)
		else:
			leg = ROOT.TLegend(0.6,0.62,0.87,0.86)
	# if series_num=="TB":
	# 	leg = ROOT.TLegend(0.17,0.56,0.50,0.86)
	leg.SetMargin(0.15)


	if not showtemp: 
		if series_num=="CMS" or series_num=="CMSATLAS": leg.SetNColumns(3)
		if "HPK2_8e14_1p5e15" in series_num or "HPK2_repro" in series_num: leg.SetNColumns(3)
		if series_num=="ATLAS": leg.SetNColumns(2)
		if "HPK2_split" in series_num: leg.SetNColumns(2)
		if "FBK" in series_num: leg.SetNColumns(2)

		#if series_num=="HPK2_8e14": leg.SetNColumns(2)
	n_legend_entries=0
	for i,scan in enumerate(scan_nums):
		#print filename+str(scan)+"_"+str(chans[i])
		#if plottype!=13:
		graph = outFile.Get(filename+str(scan)+"_"+str(chans[i]))
		#else: graph = outFile.Get(filename+str(scan))
	 	tb = scan==1
	 	cosmetic_tgraph(graph,i,tb)
	 	if "HPK2_warm" in series_num:
	 		if i < 3: cosmetic_tgraph(graph,i,tb)
	 		else: 
	 			cosmetic_tgraph(graph,i-3,tb)
	 			graph.SetMarkerStyle(24)
	 	if "HPK2_8e14" in series_num and "temp" not in series_num and "1p5" not in series_num:
	 		if i >= 4: cosmetic_tgraph(graph,i-4,tb)
	 		else: 
	 			cosmetic_tgraph(graph,i,tb)
	 			graph.SetMarkerStyle(24)
	 	if "HPK2_8e14_1p5e15" in series_num or "HPK2_repro" in series_num:
	 		i_color = 0
	 		if "Split 2" in names[i]: i_color=1
	 		if "Split 3" in names[i]: i_color=2
	 		if "Split 4" in names[i]: i_color=3

	 		i_marker = 3
	 		if "8e14" in  names[i]: i_marker=24
	 		if "1.5e15" in names[i]: i_marker =20 

	 		cosmetic_tgraph(graph,i_color,tb)
	 		graph.SetMarkerStyle(i_marker)

	 	#elif "TB" in series_num or "temp" in series_num or "Feb" in series_num or "W2" in series_num or "Sergey" in series_num or series_num=="2" or "Laser" in series_num or "HPK2" in series_num: cosmetic_tgraph(graph,i,tb)
		# cosmetic_tgraph(graph,i,tb) #### better default.
	 	#else: cosmetic_tgraph_organized(graph,names[i],tb)
		mgraph.Add(graph)
		if "(chan" in names[i]: names[i] = names[i][0:len(names[i])-7] # remove chan label
		if "repro" in series_num and n_legend_entries >= 12: continue
		if "split34" in series_num and n_legend_entries >=6: continue
		if series_num=="CMSATLAS" and "ATLAS" in names[i]: continue
		if showtemp:
		 	leg.AddEntry(graph, "%s, %i C" %(names[i].replace("(chan0)",""),temps[i]),"EP")
		elif showCMS:
			leg.AddEntry(graph, "%s" %(names[i].replace(" 8e14",", 8e14").replace(" 1.5e15",", 1.5e15")),"EP")
		else: 
			leg.AddEntry(graph, "%s" %(names[i].replace("CMS ","").replace("ATLAS ","").replace("MW","metal")),"EP")
		n_legend_entries=n_legend_entries+1


	mgraph.SetTitle("; %s; %s"%(x_axis,y_axis))
	mgraph.Draw("AP")
	if "stability" in series_num:
		currentymin = mgraph.GetYaxis().GetXmin()
		currentymax = mgraph.GetYaxis().GetXmax()
		if plottype!=51: mgraph.GetYaxis().SetRangeUser(0.7*currentymin, 1.35*currentymax)
		else: mgraph.GetYaxis().SetRangeUser(1.3*currentymin, 0.7*currentymax) ## negative

	if "HPK2_8e14_1p5e15" in series_num or "HPK2_repro" in series_num:
		currentymin = mgraph.GetYaxis().GetXmin()
		currentymax = mgraph.GetYaxis().GetXmax()
		mgraph.GetYaxis().SetRangeUser(currentymin, 1.35*currentymax)
	
	if "HPK2_split" in series_num and plottype==14: 
		mgraph.GetYaxis().SetRangeUser(0, 35.)

	if "FBK" in series_num and plottype==14: 
		mgraph.GetYaxis().SetRangeUser(0, 30.)

	if series_num=="HPK2_8e14_temp":
		currentymin = mgraph.GetYaxis().GetXmin()
		currentymax = mgraph.GetYaxis().GetXmax()
		mgraph.GetYaxis().SetRangeUser(currentymin, 1.35*currentymax)

	elif y_axis == "Risetime [ps] (10 to 90%)":
		mgraph.GetYaxis().SetRangeUser(350,1000)
		if series_num == "TB": mgraph.GetYaxis().SetRangeUser(350,850)
	elif plottype==16 or plottype==17: 
		mgraph.GetYaxis().SetRangeUser(23,65)
	
	if (plottype==1 or plottype==14) and "HPK2" in series_num:
		currentmin = mgraph.GetXaxis().GetXmin()
		currentmax = mgraph.GetXaxis().GetXmax()
		#print "current min, max ",currentmin,currentmax
		#currentmax=200
		#currentmin=70
		mgraph.GetXaxis().SetLimits(currentmin-50,currentmax)
		#mgraph.GetYaxis().SetRangeUser(5,42)
	#if plottype==3: mgraph.SetTitle("; Bias voltage [V]; Current [100 nA]")
	if "HPK2_split" in series_num and plottype==14:
		mgraph.GetXaxis().SetLimits(270,770)
	if x_axis == "Bias voltage [V]" or "current" in x_axis: mgraph.Draw("AELP")
	else: mgraph.Draw("AEP")
	if(len(scan_nums)>0): leg.Draw()
	c.Print("plots/series%s%s.pdf"%(series_num,outputtag))




def cosmetic_tgraph(graph,colorindex,tb=False):
	graph.SetLineColor(colors[colorindex])
	graph.SetMarkerColor(colors[colorindex])
	graph.SetMarkerSize(0.75)
	graph.SetMarkerStyle(20)
	if tb:
		graph.SetMarkerSize(2.5)
		graph.SetMarkerStyle(29)
	graph.SetTitle("; Bias voltage [V]; MPV Ru106 response [mV]")

def cosmetic_tgraph_organized(graph,sensorname,tb=False):
	markerstyle=20
	colorindex=0
	linestyle = 1
	if "CMS" in sensorname:
		#filled markers
		#color based on P.
		colorindex =int(sensorname.split("P")[1].split()[0])
		if "MW" in sensorname:
			markerstyle=21
		elif "50x500" in sensorname or "50 #mum" in sensorname:
			markerstyle=23
	elif "ATLAS" in sensorname:
		linestyle=7
		if "90 #mum metal" in sensorname: colorindex=0
		elif "90 #mum" in sensorname: colorindex=1
		elif "50 #mum" in sensorname: colorindex=5
		elif "30 #mum" in sensorname: colorindex=4

		markerstyle=23 + int(sensorname[-1])


	graph.SetLineColor(colors[colorindex])
	graph.SetMarkerColor(colors[colorindex])
	graph.SetMarkerSize(0.75)
	graph.SetMarkerStyle(markerstyle)
	graph.SetLineStyle(linestyle)
	if tb:
		graph.SetMarkerSize(2.5)
		graph.SetMarkerStyle(29)
	graph.SetTitle("; Bias voltage [V]; MPV Ru106 response [mV]")

def crystalBallTF1(f1):
	def crystalBall(x, p):
		#p[0]: normalization
		#p[1]: alpha
		#p[2]: n
		#p[3]: gaussian sigma
		#p[4]: gaussian mean
		return p[0]*ROOT.Math.crystalball_function(x[0],p[1],p[2],p[3],p[4])
	f2 = ROOT.TF1("f2",crystalBall,f1.GetXmin(),f1.GetXmax(), 5)
	f2.SetLineColor(ROOT.kBlue)	
	f2.SetParameter(0, f1.GetParameter(0))
	f2.SetParameter(1, 0.9)
	f2.SetParLimits(1, 0.0, 5.0)
	f2.SetParameter(2, 23)
	f2.SetParLimits(2, 0.0, 100.0)
	f2.SetParameter(3, f1.GetParameter(2))
	f2.SetParLimits(3, 0.1*f1.GetParameter(2), 2.0*f1.GetParameter(2))
	f2.SetParameter(4, f1.GetParameter(1))
	f2.SetParLimits(4, 0.1*f1.GetParameter(1), 2.0*f1.GetParameter(1))
	f2.SetParName(0, "Constant")
	f2.SetParName(1, "alpha")
	f2.SetParName(2, "n")
	f2.SetParName(3, "Sigma")
	f2.SetParName(4, "Mean")
	return f2

def getStats(hist):
	hist.Draw()
	ROOT.gPad.Update()
	return hist.FindObject("stats")

def drawMultiStats(st1, st2, c1=ROOT.kRed, c2=ROOT.kBlue):
	if st1 and st2:
		st1.SetTextColor(c1)
    	st2.SetTextColor(c2)
    	height = st1.GetY2NDC() - st1.GetY1NDC()
    	st2.SetY1NDC(st1.GetY1NDC() - height)
    	st2.SetY2NDC(st1.GetY1NDC() )
    	st1.Draw()
    	st2.Draw()

def get_time_res_channel(tree,ch,run=-1):
	mint,maxt = get_time_range(run,ch)

	hist = ROOT.TH1D("h","",70,mint,maxt)
	
	photek_thresh,photek_max,photek_chan = get_photek_params(run)

	CFD = 15
	extra_cut = get_extra_cut(run,ch)
	minAmp = get_min_amp(run,ch)
	if run >=152719 and run <= 152731: CFD = 30
	tree.Project("h","LP2_%i[%i]-LP2_20[%i]"%(CFD,ch,photek_chan),"amp[%i]>%i && amp[%i]<360 && amp[%i]>%i && amp[%i]<%i && LP2_20[%i]!=0 && LP2_20[%i]!=0 %s"%(ch,minAmp,ch,photek_chan,photek_thresh,photek_chan,photek_max,photek_chan,ch,extra_cut))	
	f1 = ROOT.TF1("f1","gaus",mint,maxt)
	hist.Fit(f1,"Q")
	st1 = copy.deepcopy(getStats(hist)) #Need to deep copy the first stats because root will return a pointer that is overwritten during the next fit

	f2 = crystalBallTF1(f1)
	hist.Fit(f2,"Q")
	st2 = getStats(hist)
	if run>0:
		c = ROOT.TCanvas()
		ROOT.gPad.SetLogy()
		hist.Draw()
		f1.Draw("same")
		f2.Draw("same")
		drawMultiStats(st1, st2)

		if ch==2: c.Print("plots/runs/Run%i_time.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_time.pdf"%(run,ch))
	#print 'Run NUmber %d,  %f, %f ' %(run,1e12*f1.GetParameter(2),1e12*f1.GetParError(2))
	if f2.GetParameter(3) !=0:
		CBerror = 0.0 if f2.GetParError(3) / f2.GetParameter(3) > 0.1 else f2.GetParError(3)

	else: CBerror=0.0
	#print '\033[0;31m Run NUmber %d,  %f, %f \033[0m' %(run,1e12*f2.GetParameter(3),1e12*CBerror)
	return 1e12*f1.GetParameter(2),1e12*f1.GetParError(2),f1.GetChisquare(), 1e12*f2.GetParameter(3),1e12*CBerror,f2.GetChisquare()

def get_optimum_timeres_channel(tree,ch,run=-1):
	mint,maxt = get_time_range(run,ch)

	photek_thresh,photek_max,photek_chan = get_photek_params(run)

	minAmp = get_min_amp(run,ch)
	extra_cut = get_extra_cut(run,ch)

	CFD_list = [5,10,15,20,25,30,35,40,50,60]
	res_list=[]
	unc_list =[]
	hist = ROOT.TH1D("h","",70,mint,maxt)

	for CFD in CFD_list:
		hist.Reset()	
		tree.Project("h","LP2_%i[%i]-LP2_20[%i]"%(CFD,ch,photek_chan),"amp[%i]>%i && amp[%i]<360 && amp[%i]>%i && amp[%i]<%i && LP2_20[%i]!=0 && LP2_20[%i]!=0 %s"%(ch,minAmp,ch,photek_chan,photek_thresh,photek_chan,photek_max,photek_chan,ch,extra_cut))

		f = ROOT.TF1("f%i"%CFD,"gaus",mint,maxt)

		hist.Fit(f,"Q")
		res_list.append(1e12*f.GetParameter(2))
		unc_list.append(1e12*f.GetParError(2))
		if run>0:
			c = ROOT.TCanvas()
			hist.Draw()
			f.Draw("same")
			if ch==2: c.Print("plots/runs/Run%i_time%i.pdf"%(run,CFD))
			else: c.Print("plots/runs/Run%i_ch%i_time%i.pdf"%(run,ch,CFD))

	minres, optimum_idx =  min((val, idx) for (idx, val) in enumerate(res_list))
	optimum_cfd = CFD_list[optimum_idx]
	minres_err = unc_list[optimum_idx]

	graph = ROOT.TGraphErrors(len(CFD_list),array("d",CFD_list),array("d",res_list),array("d",[0.01 for i in CFD_list]),array("d",unc_list))

	if run>0:
		c = ROOT.TCanvas()
		graph.Draw("AELP")

		if ch==2: c.Print("plots/runs/Run%i_CFDscan.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_CFDscan.pdf"%(run,ch))


	return minres,minres_err,optimum_cfd



def get_slew_rate_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",60,0,600e9)
	minAmp = get_min_amp(run,ch)
	extra_cut = get_extra_cut(run,ch)

	tree.Project("h","abs(risetime[%i])"%ch,"amp[%i]>%i %s"%(ch,minAmp,extra_cut))	### mV/ s

	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		if ch==2: c.Print("plots/runs/Run%i_slewrate.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_slewrate.pdf"%(run,ch))
	#print 'Run NUmber %d,  %f, %f ' %(run,1e12*f1.GetParameter(2),1e12*f1.GetParError(2))
	return 1e-9 * hist.GetMean(),1e-9* hist.GetMeanError()

def get_risetime_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",60,100,1200)
	minAmp = get_min_amp(run,ch)
	extra_cut = get_extra_cut(run,ch)

	#10 to 90 risetime
	tree.Project("h","1e12*abs(0.8*amp[%i]/risetime[%i])"%(ch,ch),"amp[%i]>%i %s"%(ch,minAmp,extra_cut))	### mV/ s

	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		if ch==2: c.Print("plots/runs/Run%i_risetime.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_risetime.pdf"%(run,ch))
	#print 'Run NUmber %d,  %f, %f ' %(run,1e12*f1.GetParameter(2),1e12*f1.GetParError(2))
	return hist.GetMean(),hist.GetMeanError()

def GetIdxFirstCross(value, hist, i_st, direction):
	idx_end = 0
	if direction > 0: idx_end = 1999 
	rising = value > hist.GetBinContent(i_st)#v[i_st]
	i = i_st;

	while i != idx_end: 
		if(rising and hist.GetBinContent(i) > value): break
		elif( not rising and hist.GetBinContent(i) < value): break
		i += direction;
	
	return i;

def GetProfIntegral(hist, i_init, i_end):
	integral=0
	for i in range(i_init,i_end+1):
		integral = integral + hist.GetBinContent(i)*hist.GetBinWidth(i)
	return integral

def get_mean_amp_charge_averaging(tree,ch,run=-1,laser=False):
	if not laser: return 0
	histname = "average_%i_%i"%(run,ch)
	hist = ROOT.TH2D(histname,"",2000,30e-9,80e-9,50,0,-1200)
	var = "channel[%i]:time[0]" % ch
	tree.Project(histname,var,"time[0]>45e-9") ## somehow failing if using all samples.
	profx = hist.ProfileX()


	i_start = profx.GetMinimumBin()

	left_edge = GetIdxFirstCross(0.05*profx.GetMinimum(),profx,i_start,-1)
	right_edge = GetIdxFirstCross(0,profx,i_start,1)
	charge =  -1e12 * GetProfIntegral(profx,left_edge,right_edge) /4700. # try to match timingDAQ
	
	if run>0:
		c = ROOT.TCanvas()
		profx.SetTitle("Average pulse shape;Time [s];Voltage [mV]")
		profx.Draw()
		if ch==2: c.Print("plots/runs/Run%i_pulse.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_pulse.pdf"%(run,ch))
	return -1.*profx.GetMinimum(),charge

def get_mean_response_channel(tree,ch,run=-1,laser=False):
	hist = ROOT.TH1D("h","",50,0,400)
	
	photek_thresh,photek_max,photek_chan = get_photek_params(run)

	if run>=152104 and run<=152108: hist = ROOT.TH1D("h","",50,2,710)

	minAmp = get_min_amp(run,ch)
	extra_cut = get_extra_cut(run,ch)

	if laser and ch==1: 
		minAmp=0.5
		hist = ROOT.TH1D("h","",350,0,350)

	if not laser: selection = "amp[%i]>%f&&amp[%i]>%i %s"%(ch,minAmp,photek_chan,photek_thresh,extra_cut)
	else: selection =  "amp[%i]>%f"%(ch,minAmp)
	print "get_mean_response selection: ",selection
	hist.StatOverflows(True)
	tree.Project("h","amp[%i]"%ch,selection)
	mean=0.
	err=0.
	if not laser:
		fitter = lg.LanGausFit()
		#fitter.SetParLimits(1,25,1000)
		#f1 = fitter.fit(hist,None,None,100)
		f1 = fitter.fit(hist)
		mean=f1.GetParameter(1)
		err=f1.GetParError(1)
	else: 
		f1 = ROOT.TF1("f1","gaus",0,500)
		hist.Fit(f1,"Q")
		mean=hist.GetMean()
		err=hist.GetMeanError()
	if run>0:
		c = ROOT.TCanvas()
		hist.SetTitle(";Amplitude [mV];Events")
		hist.Draw()
		f1.Draw("same")
		if ch==2: c.Print("plots/runs/Run%i_amp.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_amp.pdf"%(run,ch))
		#c.Print("plots/runs/Run%i_amp.root"%run)
	# return f1.GetParameter(1),f1.GetParError(1)
	return mean,err

def get_charge_channel(tree,ch,run=-1,laser=False):
	histname = "h%i"%run
	minAmp = get_min_amp(run,ch)
	extra_cut = get_extra_cut(run,ch)
	photek_thresh,photek_max,photek_chan = get_photek_params(run)

	if run >= 151357 and run<=151374: 
		hist = ROOT.TH1D(histname,"",40,1,30)
		minAmp=10.
	elif run>=151982 and run<=151997 and ch==1: hist = ROOT.TH1D(histname,"",100,2,500)
	elif run>= 152719 and run <= 152731: hist = ROOT.TH1D(histname,"",100,2,500)
	
	elif run>=152104 and run<=152108: hist = ROOT.TH1D(histname,"",100,2,900)
	else: hist = ROOT.TH1D(histname,"",50,2,100)

	if laser: minAmp=1.
	if laser and ch==1: 
		minAmp=0.5
		hist = ROOT.TH1D(histname,"",100,0,100)

	hist.StatOverflows(True)

	if not laser: selection = "amp[%i]>%f&&amp[%i]>%i %s"%(ch,minAmp,photek_chan,photek_thresh,extra_cut)
	else: selection =  "amp[%i]>%f"%(ch,minAmp)
	print "Selection is ",selection
	tree.Project(histname,"-1000*integral[%i]*1e9*50/4700"%ch,selection)
	mean=0.
	err=0.
	if not laser:
		fitter = lg.LanGausFit()
		#fitter.SetParLimits(1,25,1000)
		#f1 = fitter.fit(hist,None,None,20)
		f1 = fitter.fit(hist)
		# ROOT.TF1("f1","landau",0,150)
		#hist.Fit(f1)
		mean=f1.GetParameter(1)
		err=f1.GetParError(1)
	else: 
		f1 = ROOT.TF1("f1","gaus",0,500)
		hist.Fit(f1)
		mean=hist.GetMean()
		err=hist.GetMeanError()
		# mean=f1.GetParameter(1)
		# err=f1.GetParError(1)
	if run>0:
		c = ROOT.TCanvas("c1_%i"%run)
		hist.SetTitle(";Integrated charge [fC];Events")
		hist.Draw()
		f1.Draw("same")
		if ch==2: c.Print("plots/runs/Run%i_charge.pdf"%run)
		else: c.Print("plots/runs/Run%i_ch%i_charge.pdf"%(run,ch))
		# c.Print("plots/runs/Run%i_charge.root"%run)
		# c.Print("plots/runs/Run%i_charge.C"%run)
	#return f1.GetParameter(1),f1.GetParError(1)
	return mean,err


def get_mean_baseline_RMS_channel(tree,ch):
	hist = ROOT.TH1F("h","",20,-1000,1000)
	tree.Project("h","baseline_RMS[%i]"%ch,"")
	return hist.GetMean(),hist.GetMeanError()

def get_mean_baseline_RMS(tree):
	means_this_run=[]
	errs_this_run=[]
	for i in range(n_channels):
		mean,err = get_mean_baseline_RMS_channel(tree,i)
		means_this_run.append(mean)
		errs_this_run.append(err)

	return means_this_run,errs_this_run

def get_mean_response(tree):
	means_this_run=[]
	errs_this_run=[]
	for i in range(n_channels):
		mean,err = get_mean_response_channel(tree,i)
		means_this_run.append(mean)
		errs_this_run.append(err)
	
	best_mean =  max(means_this_run)
	best_chan = means_this_run.index(best_mean)	
	err = errs_this_run[best_chan]

	#print best_mean,err,best_chan

	return best_mean,err

def addGraph(d, name, npoints, x, y, xerr, yerr):
	d[name] = ROOT.TGraphErrors(npoints,array("d",x),array("d",y),array("d",xerr),array("d",yerr))

def get_scan_results(scan_num,chan,laser):
	runs=[]
	biases=[]
	biases_meas=[]
	lgad_biases=[]
	currents_meas=[]
	temps =[] 
	
	mean_responses=[]
	err_responses=[]
	mean_responses_laser_norm=[]
	err_responses_laser_norm=[]

	mean_amps_averaging = []
	err_amps_averaging = []
	mean_charge_averaging = []
	err_charge_averaging = []

	mean_amps_averaging_laser_norm = []
	err_amps_averaging_laser_norm = []
	mean_charge_averaging_laser_norm = []
	err_charge_averaging_laser_norm = []

	mean_diode_amps_averaging = []
	err_diode_amps_averaging = []

	mean_diode_amps=[]
	err_diode_amps=[]

	mean_diode_charge=[]
	err_diode_charge=[]

	mean_charges=[]
	err_charges=[]

	mean_charge_laser_norm=[]
	err_charge_laser_norm=[]

	gains =[]
	err_gains=[]

	time_res=[]
	time_resCB=[]
	err_time_res=[]
	err_time_resCB=[]

	time_res_corr=[]
	time_res_chi2=[]	
	time_res_corrCB=[]
	time_res_chi2CB=[]

	CFD_scan_res=[]
	CFD_scan_res_corr=[]
	err_CFD_scan_res=[]

	optimum_CFD=[]

	optimum_res_delta=[]

	means_MCP=[]
	errs_MCP=[]

	mean_noise=[]
	err_mean_noise=[]

	snr =[] 
	snr_err =[]

	slewrates =[]
	slewrate_errs =[]

	risetimes=[]
	risetime_errs=[]

	mean_charge_amp_ratio=[]
	mean_charge_amp_ratio_err=[]
	mean_diode_charge_amp_ratio=[]
	mean_diode_charge_amp_ratio_err=[]

	jitters=[]
	jitter_errs=[]

	scan_txt_filename = "../VoltageScanDataRegistry/scan%i.txt" % scan_num
	with open(scan_txt_filename) as scan_txt_file:
		for line in scan_txt_file:
			if line[:1] == "#": continue
			this_run = line.split("\t")[0]

			if "-" not in this_run: 
				runs.append(int(line.split("\t")[0]))
			else:
				run_start = int(this_run.split("-")[0])
				run_end = int(this_run.split("-")[1])
				runs.append(range(run_start,run_end+1))


		 	biases.append(abs(float(line.split("\t")[1])))
		 	if scan_num==165: biases[-1] = biases[-1]-5. ### 20 degrees to 16 degrees on chiller.
			# if scan_num==10002: biases[-1] = biases[-1]+2. ### probably 2 degrees colder at MTEST
			biases_meas.append(abs(float(line.split("\t")[2])))

			current_units_conversion = 1. # 10= 100 nanoamps scale
			board_resistance = 10e-3 ## megaohms (1.1 for FNAL)

			currents_meas.append(current_units_conversion*1.e6*abs(float(line.split("\t")[3]))) ## convert to microamps

			lgad_biases.append(biases[-1] - board_resistance * currents_meas[-1]/current_units_conversion) ## 1.1 MOhm in series with LGAD

			temps.append(float(line.split("\t")[4]))

			# if biases[-1]>0 and abs(biases_meas[-1]-biases[-1])/biases[-1] > 0.1:
				# print "[WARNING]: Scan %i, run %i set to %.0f V, measured at %.0f V" % (scan_num, runs[-1],biases[-1],biases_meas[-1])


	for i,run in enumerate(runs):
		#open root file/tree
		tree = ROOT.TChain("pulse")
		if type(run) is list:
			# for r in run: tree.Add("/home/daq/ScopeData/Reco/run_scope%i.root" % r)
			for r in run: tree.Add("root://cmseos.fnal.gov//store/group/cmstestbeam/SensorBeam2022/LecroyScope/RecoData/TimingDAQRECO/RecoWithTracks/v1/run%i_info.root" % r)
			run = run[0]
		else:
			tree.Add("/home/daq/ScopeData/Reco/run_scope%i.root" % run)
		
		if chan < 0:
			mean,err = get_mean_response(tree) ### find max amp channel
		else: 
			mean,err = get_mean_response_channel(tree,chan,run,laser) ## use specified channel from series txt file
			if doAverage:
				mean_amp_avg,mean_charge_avg = get_mean_amp_charge_averaging(tree,chan,run,laser) ## use specified channel from series txt file
				mean_diode_amp_avg,mean_diode_charge_avg = get_mean_amp_charge_averaging(tree,1,run,laser) ## use specified channel from series txt file
			else:
				mean_amp_avg=0
				mean_charge_avg=0
				mean_diode_amp_avg=0
				mean_diode_charge_avg=0
			err_amp_avg=0
			err_charge_avg=0
			err_diode_charge_avg=0
			err_diode_amp_avg=0
			diodemean,diodeerr= get_mean_response_channel(tree,1,run,laser)
			diode_charge_mean,diode_charge_err= get_charge_channel(tree,1,run,laser)
			mean_charge,err_charge = get_charge_channel(tree,chan,run,laser) ## use specified channel from series txt file
			sigma,sigmaerr,chi2,sigmaCB,sigmaerrCB,chi2CB = get_time_res_channel(tree,chan,run)
			slewrate,slewerr = get_slew_rate_channel(tree,chan,run)
			risetime,riseerr = get_risetime_channel(tree,chan,run)

		##MCP
		mean_MCP,err_MCP = get_mean_response_channel(tree,3)

		noise_means,noise_errs = get_mean_baseline_RMS(tree)

		if doCFDScan:
			this_CFD_scan_res,this_err_CFD_scan_res,this_optimum_CFD = get_optimum_timeres_channel(tree,chan,run)
		else:
			this_CFD_scan_res=20
			this_err_CFD_scan_res=0
			this_optimum_CFD=0

		CFD_scan_res.append(this_CFD_scan_res)
		err_CFD_scan_res.append(this_err_CFD_scan_res)
		optimum_CFD.append(this_optimum_CFD)

		means_MCP.append(mean_MCP)
		errs_MCP.append(err_MCP)
		mean_responses.append(mean)
		err_responses.append(err)
		mean_diode_amps.append(diodemean)
		err_diode_amps.append(diodeerr)
		mean_diode_charge.append(diode_charge_mean)
		err_diode_charge.append(diode_charge_err)

		mean_diode_amps_averaging.append(mean_diode_amp_avg)
		mean_amps_averaging.append(mean_amp_avg)
		mean_charge_averaging.append(mean_charge_avg)
		err_diode_amps_averaging.append(err_diode_amp_avg)
		err_amps_averaging.append(err_amp_avg)
		err_charge_averaging.append(err_charge_avg)


		if (diodemean>0 and laser):
			mean_responses_laser_norm.append(mean * diodeTarget/diodemean)
			err_responses_laser_norm.append(err * diodeTarget/diodemean)
			mean_charge_laser_norm.append(mean_charge * diodeTarget/diodemean)
			err_charge_laser_norm.append(err_charge * diodeTarget/diodemean)
			mean_amps_averaging_laser_norm.append(mean_amp_avg * diodeTarget/diodemean)
			mean_charge_averaging_laser_norm.append(mean_charge_avg * diodeTarget/diodemean)
			err_amps_averaging_laser_norm.append(err_amp_avg * diodeTarget/diodemean)
			err_charge_averaging_laser_norm.append(err_charge_avg * diodeTarget/diodemean)
			mean_diode_charge_amp_ratio.append(4700.*diode_charge_mean/(1000. * 0.5 * diodemean))
			mean_diode_charge_amp_ratio_err.append( (4700.*diode_charge_mean/(1000. * 0.5 * diodemean)) * diodeerr/diodemean )
			gains.append(mean_charge * diodeTarget/(diodemean * PiNCharge))
			err_gains.append(err_charge * diodeTarget/(diodemean * PiNCharge))
		else:
			mean_responses_laser_norm.append(mean)
			err_responses_laser_norm.append(err)
			mean_charge_laser_norm.append(mean_charge)
			err_charge_laser_norm.append(err_charge)
			mean_diode_charge_amp_ratio_err.append(0)
			mean_diode_charge_amp_ratio.append(0)
			mean_charge_averaging_laser_norm.append(0)
			err_charge_averaging_laser_norm.append(0)
			mean_amps_averaging_laser_norm.append(0)
			err_amps_averaging_laser_norm.append(0)
			gains.append(0)
			err_gains.append(0)

		mean_charges.append(mean_charge)
		err_charges.append(err_charge)

		if (mean>0):
			mean_charge_amp_ratio.append(4700.*mean_charge/(1000. * 0.5 * mean))
			mean_charge_amp_ratio_err.append( (4700.*mean_charge/(1000. * 0.5 * mean)) * err/mean )
		else:
			mean_charge_amp_ratio.append(0)
			mean_charge_amp_ratio_err.append(0)


		time_res.append(sigma)
		time_resCB.append(sigmaCB)
		time_res_chi2.append(chi2)
		time_res_chi2CB.append(chi2CB)
		if scan_num<10000:
			if (pow(sigma,2)-pow(photek_res,2)) > 0: 
				time_res_corr.append(pow(pow(sigma,2)-pow(photek_res,2),0.5))
				time_res_corrCB.append(pow(pow(sigmaCB,2)-pow(photek_res,2),0.5))
			else:
				time_res_corr.append(0)
				time_res_corrCB.append(0)
				
			if (pow(this_CFD_scan_res,2)-pow(photek_res,2)) > 0:
				CFD_scan_res_corr.append(pow(pow(this_CFD_scan_res,2)-pow(photek_res,2),0.5))
			else:
				CFD_scan_res_corr.append(0)


		else: ##test beam data 
			if (pow(sigma,2)-pow(photek_res_beam,2)) > 0: 
				time_res_corr.append(pow(pow(sigma,2)-pow(photek_res_beam,2),0.5))
				time_res_corrCB.append(pow(pow(sigmaCB,2)-pow(photek_res_beam,2),0.5))
			else:
				time_res_corr.append(0)
				time_res_corrCB.append(0)
	
			if (pow(this_CFD_scan_res,2)-pow(photek_res,2)) > 0:
				CFD_scan_res_corr.append(pow(pow(this_CFD_scan_res,2)-pow(photek_res,2),0.5))
			else:
				CFD_scan_res_corr.append(0)


		err_time_res.append(sigmaerr)
		err_time_resCB.append(sigmaerrCB)

		optimum_res_delta.append(sigma - this_CFD_scan_res)

		mean_noise.append(noise_means)
		err_mean_noise.append(noise_errs)

		if len(noise_means)>chan and noise_means[chan]>0:
			snr_lgad_channel = mean/noise_means[chan]
			snr_err_lgad_channel = err/noise_means[chan]
		else:
			snr_lgad_channel=0
			snr_err_lgad_channel=0			

		if slewrate>0:
			jitter = 1000.*noise_means[chan]/slewrate
			jitter_err = pow(pow(noise_errs[chan]/noise_means[chan],2)+ pow(slewerr/slewrate,2),0.5)* jitter 
		else:
			jitter=0
			jitter_err=0

		jitters.append(jitter)
		jitter_errs.append(jitter_err)

		snr.append(snr_lgad_channel)
		snr_err.append(snr_err_lgad_channel)
		slewrates.append(slewrate)
		slewrate_errs.append(slewerr)

		risetimes.append(risetime)
		risetime_errs.append(riseerr)
		#print mean_responses
		#print mean_diode_amps
		#print mean_responses_laser_norm
		if verbose:
				print "Scan %i, run %i, voltage %0.2f, raw signal %0.2f, pd %0.2f" % (scan_num,run,biases_meas[i],mean,means_MCP[i])
		else: 
			print "ERROR: run %i has 0 mean_MCP"%run
			del biases[i]
			del biases_meas[i]
			del currents_meas[i]
			del temps[i]
			del lgad_biases[i]
	



	if(len(mean_responses)!=len(biases)): print "ERROR: length of gains does not match length of biases."

	graph_Dict = {}
	addGraph(graph_Dict, "graph", len(biases), biases, mean_responses, [0.1 for i in biases], err_responses)
	addGraph(graph_Dict, "graph_gain", len(biases), biases, gains, [0.1 for i in biases], err_gains)
	addGraph(graph_Dict, "graph_amp_average", len(biases), biases, mean_amps_averaging, [0.1 for i in biases], err_amps_averaging)
	addGraph(graph_Dict, "graph_charge_average", len(biases), biases, mean_charge_averaging, [0.1 for i in biases], err_charge_averaging)
	addGraph(graph_Dict, "graph_amp_average_laser_norm", len(biases), biases, mean_amps_averaging_laser_norm, [0.1 for i in biases], err_amps_averaging_laser_norm)
	addGraph(graph_Dict, "graph_charge_average_laser_norm", len(biases), biases, mean_charge_averaging_laser_norm, [0.1 for i in biases], err_charge_averaging_laser_norm)
	addGraph(graph_Dict, "graph_diode_amp_average", len(biases), biases, mean_diode_amps_averaging, [0.1 for i in biases], err_diode_amps_averaging)
	addGraph(graph_Dict, "graph_charge_amp_ratio", len(biases), biases, mean_charge_amp_ratio, [0.1 for i in biases], mean_charge_amp_ratio_err)
	addGraph(graph_Dict, "graph_average_amp_vs_amp", len(biases), mean_responses, mean_amps_averaging, err_responses, err_amps_averaging)
	addGraph(graph_Dict, "graph_diode_average_amp_vs_amp", len(biases), mean_diode_amps, mean_diode_amps_averaging, err_diode_amps, err_diode_amps_averaging)
	addGraph(graph_Dict, "graph_diode", len(biases), biases, mean_diode_amps, [0.1 for i in biases], err_diode_charge)
	addGraph(graph_Dict, "graph_diode_charge", len(biases), biases, mean_diode_charge, [0.1 for i in biases], err_diode_charge)
	addGraph(graph_Dict, "graph_diode_charge_amp_ratio", len(biases), biases, mean_diode_charge_amp_ratio, [0.1 for i in biases], mean_diode_charge_amp_ratio_err)
	addGraph(graph_Dict, "graph_diode_charge_vs_amp", len(biases), mean_diode_amps, mean_diode_charge, err_diode_amps, err_diode_charge)
	addGraph(graph_Dict, "graph_amp_laser_norm", len(biases), biases, mean_responses_laser_norm, [0.1 for i in biases], err_responses_laser_norm)
	addGraph(graph_Dict, "graph_charge_laser_norm", len(biases), biases, mean_charge_laser_norm, [0.1 for i in biases], err_charge_laser_norm)
	addGraph(graph_Dict, "graph_charge", len(biases), biases, mean_charges, [0.1 for i in biases], err_charges)
	addGraph(graph_Dict, "graph_charge_transpose", len(biases), mean_charges, biases, err_charges, [0.1 for i in biases])
	addGraph(graph_Dict, "graph_MCP", len(biases), biases, means_MCP, [0.1 for i in biases], errs_MCP)
	addGraph(graph_Dict, "graph_lgadbias", len(biases), lgad_biases, mean_responses, [0.1 for i in biases], err_responses)
	#addGraph(graph_Dict, "graph_current_lgadbias", len(biases), lgad_biases, currents_meas, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_current_lgadbias", len(biases), biases, currents_meas, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_temp", len(biases), biases, temps, [0.1 for i in biases], [0.1 for i in biases])
	#addGraph(graph_Dict, "graph_temp_bias", len(biases), temps, biases, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_temp_bias", len(biases), mean_charges, temps, err_charges, [0.1 for i in biases])
	addGraph(graph_Dict, "graph_charge_vs_current", len(biases), currents_meas, mean_charges, [0.1 for i in biases], err_charges)
	addGraph(graph_Dict, "graph_time_res", len(biases), biases, time_res, [0.1 for i in biases], err_time_res)
	addGraph(graph_Dict, "graph_time_resCB", len(biases), biases, time_resCB, [0.1 for i in biases], err_time_resCB)
	addGraph(graph_Dict, "graph_time_res_corr", len(biases), biases, time_res_corr, [0.1 for i in biases], err_time_res)
	addGraph(graph_Dict, "graph_time_res_corrCB", len(biases), biases, time_res_corrCB, [0.1 for i in biases], err_time_resCB)
	addGraph(graph_Dict, "graph_time_res_chi2", len(biases), biases, time_res_chi2, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_time_res_chi2CB", len(biases), biases, time_res_chi2CB, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_time_res_cfd_scan", len(biases), biases, CFD_scan_res, [0.1 for i in biases], err_CFD_scan_res)
	addGraph(graph_Dict, "graph_time_res_cfd_scan_corr", len(biases), biases, CFD_scan_res_corr, [0.1 for i in biases], err_CFD_scan_res)
	addGraph(graph_Dict, "graph_time_res_cfd_scan_delta", len(biases), biases, optimum_res_delta, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_optimum_CFD", len(biases), biases, optimum_CFD, [0.1 for i in biases], [0.1 for i in biases])
	addGraph(graph_Dict, "graph_slew_rate", len(biases), biases, slewrates, [0.1 for i in biases], slewrate_errs)
	addGraph(graph_Dict, "graph_risetime", len(biases), biases, risetimes, [0.1 for i in biases], risetime_errs)
	addGraph(graph_Dict, "graph_snr", len(biases), biases, snr, [0.1 for i in biases], snr_err)
	addGraph(graph_Dict, "graph_jitter", len(biases), biases, jitters, [0.1 for i in biases], jitter_errs)
	addGraph(graph_Dict, "graph_res_vs_snr", len(biases), snr, time_res, snr_err, err_time_res)
	addGraph(graph_Dict, "graph_res_vs_slew", len(biases), slewrates, time_res_corr, slewrate_errs, err_time_res)
	addGraph(graph_Dict, "graph_res_vs_mpv", len(biases), mean_responses, time_res_corr, err_responses, err_time_res)
	addGraph(graph_Dict, "graph_mpv_vs_snr", len(biases), snr, mean_responses, snr_err, err_responses)
	addGraph(graph_Dict, "graph_risetime_vs_mpv", len(biases), mean_responses, risetimes, err_responses, risetime_errs)
	addGraph(graph_Dict, "graph_risetime_vs_charge", len(biases), mean_charges, risetimes, err_charges, risetime_errs)
	addGraph(graph_Dict, "graph_slew_vs_charge", len(biases), mean_charges, slewrates, err_charges, slewrate_errs)
	addGraph(graph_Dict, "graph_charge_vs_amp", len(biases), mean_responses, mean_charges, err_responses, err_charges)
	addGraph(graph_Dict, "graph_res_vs_charge", len(biases), mean_charges, time_res, err_charges, err_time_res)
	addGraph(graph_Dict, "graph_res_corr_vs_charge", len(biases), mean_charges, time_res_corr, err_charges, err_time_res)

	#vs run number
	if type(runs[0]) is not list:
		addGraph(graph_Dict, "graph_charge_vs_runnum", len(biases), [1+i - runs[0] for i in runs], mean_charges, [0.01 for i in biases], err_charges)
		addGraph(graph_Dict, "graph_res_corr_vs_runnum", len(biases), [1+i - runs[0] for i in runs], time_res_corr, [0.01 for i in biases], err_time_res)
		addGraph(graph_Dict, "graph_temp_vs_runnum", len(biases), [1+i - runs[0] for i in runs], temps, [0.01 for i in biases], [0.01 for i in biases])
		addGraph(graph_Dict, "graph_current_vs_runnum", len(biases), [1+i - runs[0] for i in runs], currents_meas, [0.01 for i in biases], [0.01 for i in biases])
	else:
		addGraph(graph_Dict, "graph_charge_vs_runnum", len(biases), [1+i[0] - runs[0][0] for i in runs], mean_charges, [0.01 for i in biases], err_charges)
		addGraph(graph_Dict, "graph_res_corr_vs_runnum", len(biases), [1+i[0] - runs[0][0] for i in runs], time_res_corr, [0.01 for i in biases], err_time_res)
		addGraph(graph_Dict, "graph_temp_vs_runnum", len(biases), [1+i[0] - runs[0][0] for i in runs], temps, [0.01 for i in biases], [0.01 for i in biases])
		addGraph(graph_Dict, "graph_current_vs_runnum", len(biases), [1+i[0] - runs[0][0] for i in runs], currents_meas, [0.01 for i in biases], [0.01 for i in biases])


	## give tgraphs names so they can be saved to preserve python scope for multi-scan overlay 
	graph_Dict["graph"].SetName("gr%i_%i"%(scan_num,chan))
	graph_Dict["graph_gain"].SetName("gr_gain%i_%i"%(scan_num,chan))
	graph_Dict["graph_amp_average"].SetName("gr_amp_average%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_average"].SetName("gr_charge_average%i_%i"%(scan_num,chan))
	graph_Dict["graph_amp_average_laser_norm"].SetName("gr_amp_average_laser_norm%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_average_laser_norm"].SetName("gr_charge_average_laser_norm%i_%i"%(scan_num,chan))
	graph_Dict["graph_diode_amp_average"].SetName("gr_diode_amp_average%i_%i"%(scan_num,chan))
	graph_Dict["graph_average_amp_vs_amp"].SetName("gr_average_amp_vs_amp%i_%i"%(scan_num,chan))
	graph_Dict["graph_diode_average_amp_vs_amp"].SetName("gr_diode_average_amp_vs_amp%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_amp_ratio"].SetName("gr_charge_amp_ratio%i_%i"%(scan_num,chan))
	graph_Dict["graph_diode_charge_amp_ratio"].SetName("gr_diode_charge_amp_ratio%i_%i"%(scan_num,chan))
	graph_Dict["graph_diode"].SetName("gr_diode%i_%i"%(scan_num,chan))
	graph_Dict["graph_diode_charge"].SetName("gr_diode_charge%i_%i"%(scan_num,chan))
	graph_Dict["graph_diode_charge_vs_amp"].SetName("gr_diode_charge_vs_amp%i_%i"%(scan_num,chan))
	graph_Dict["graph_amp_laser_norm"].SetName("gr_amp_laser_norm%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_laser_norm"].SetName("gr_charge_laser_norm%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge"].SetName("grcharge%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_vs_current"].SetName("grcharge_vs_current%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_transpose"].SetName("grcharge_tranpose%i_%i"%(scan_num,chan))
	graph_Dict["graph_temp_bias"].SetName("grtemp_bias%i_%i"%(scan_num,chan))
	graph_Dict["graph_lgadbias"].SetName("grlgad%i_%i"%(scan_num,chan))
	graph_Dict["graph_current_lgadbias"].SetName("griv%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res"].SetName("grres%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_resCB"].SetName("grresCB%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_corr"].SetName("grres_corr%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_corrCB"].SetName("grres_corrCB%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_chi2"].SetName("grres_chi2%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_chi2CB"].SetName("grres_chi2CB%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_cfd_scan"].SetName("grres_cfd_scan%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_cfd_scan_corr"].SetName("grres_cfd_scan_corr%i_%i"%(scan_num,chan))
	graph_Dict["graph_time_res_cfd_scan_delta"].SetName("grres_cfd_scan_delta%i_%i"%(scan_num,chan))
	graph_Dict["graph_optimum_CFD"].SetName("groptimum_CFD%i_%i"%(scan_num,chan))
	graph_Dict["graph_slew_rate"].SetName("grslew%i_%i"%(scan_num,chan))
	graph_Dict["graph_risetime"].SetName("grrise%i_%i"%(scan_num,chan))
	graph_Dict["graph_snr"].SetName("grsnr%i_%i"%(scan_num,chan))
	graph_Dict["graph_jitter"].SetName("grjitter%i_%i"%(scan_num,chan))
	graph_Dict["graph_res_vs_snr"].SetName("grres_vs_snr%i_%i"%(scan_num,chan))
	graph_Dict["graph_res_vs_slew"].SetName("grres_vs_slew%i_%i"%(scan_num,chan))
	graph_Dict["graph_res_vs_mpv"].SetName("grres_vs_mpv%i_%i"%(scan_num,chan))
	graph_Dict["graph_mpv_vs_snr"].SetName("grmpv_vs_snr%i_%i"%(scan_num,chan))
	graph_Dict["graph_risetime_vs_mpv"].SetName("grrisetime_vs_mpv%i_%i"%(scan_num,chan))
	graph_Dict["graph_risetime_vs_charge"].SetName("grrisetime_vs_charge%i_%i"%(scan_num,chan))
	graph_Dict["graph_slew_vs_charge"].SetName("grslew_vs_charge%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_vs_amp"].SetName("grcharge_vs_amp%i_%i"%(scan_num,chan))
	graph_Dict["graph_res_vs_charge"].SetName("grres_vs_charge%i_%i"%(scan_num,chan))
	graph_Dict["graph_res_corr_vs_charge"].SetName("grres_corr_vs_charge%i_%i"%(scan_num,chan))
	
	graph_Dict["graph_res_corr_vs_runnum"].SetName("grres_corr_vs_runnum%i_%i"%(scan_num,chan))
	graph_Dict["graph_charge_vs_runnum"].SetName("grcharge_vs_runnum%i_%i"%(scan_num,chan))
	graph_Dict["graph_current_vs_runnum"].SetName("grcurrent_vs_runnum%i_%i"%(scan_num,chan))
	graph_Dict["graph_temp_vs_runnum"].SetName("grtemp_vs_runnum%i_%i"%(scan_num,chan))



	##convert rows to columns
	col_mean_noise = zip(*mean_noise)
	col_err_noise = zip(*err_mean_noise)


	graphs_noise = []
	for ichan in range(n_channels):
		graphs_noise.append( ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",col_mean_noise[ichan]),array("d",[0.1 for i in biases]),array("d",col_err_noise[ichan])))
		graphs_noise[-1].SetTitle("Noise in channel %i, scan %i" %(ichan,scan_num))
	#mgraph.Add(graph_norm)

	#chan=2
	addGraph(graph_Dict, "graph_lgadnoise_vs_bias", len(biases), lgad_biases, col_mean_noise[chan], [0.1 for i in biases], col_err_noise[chan])
	graph_Dict["graph_lgadnoise_vs_bias"].SetName("grlgadnoise_vs_bias%i_%i"%(scan_num,chan))

	addGraph(graph_Dict, "graph_lgadnoise_vs_charge", len(biases), mean_charges, col_mean_noise[chan], err_charges, col_err_noise[chan])
	graph_Dict["graph_lgadnoise_vs_charge"].SetName("grlgadnoise_vs_charge%i_%i"%(scan_num,chan))

	addGraph(graph_Dict, "graph_lgadnoise_vs_current", len(biases), currents_meas, col_mean_noise[chan], [0.1 for i in biases], col_err_noise[chan])
	graph_Dict["graph_lgadnoise_vs_current"].SetName("grlgadnoise_vs_current%i_%i"%(scan_num,chan))


	return graphs_noise, graph_Dict
	

if len(sys.argv) < 2:
    sys.exit('Please provide a series number') 

series_num = sys.argv[1]
series_txt_filename="series/series%s.txt" % series_num
scan_nums=[]
names=[]
temps=[]
chans=[]
BV_for_charges=[]
BV_for_charges15=[]
BV_for_charges25=[]
Temp_for_charges=[]
isLaserRun=[]
prep_dirs()
with open(series_txt_filename) as series_txt_file:
		for line in series_txt_file:
			if len(line.split(","))==0: continue
			if line[:1] == "#": continue
			scan_nums.append(int(line.split(",")[0]))		
			names.append(line.split(",")[1])
			temps.append(float(line.split(",")[2]))
			if scan_nums[-1]!=1: 
				if "chan" in names[-1]:
					chans.append(int(names[-1].split("chan")[1][0]))
				else: chans.append(2) # LGAD channel.
				if "Laser" in names[-1] or "laser" in names[-1]: 
					isLaserRun.append(True)
					print("Found laser scan.")
				else: isLaserRun.append(False)
			else: chans.append(0)
			# if "ch" in line.split(",")[3]: 
			# 	human_channel_num = int(line.split(",")[3].split("ch")[1].split()[0])
			# 	if human_channel_num <= 8: chans.append(human_channel_num-1)
			# 	else: chans.append(human_channel_num) 
			# else: chans.append(-1)	

outFile = ROOT.TFile("buffer.root","RECREATE")
for i,scan_num in enumerate(scan_nums):
	graphs_noise, graph_Dict = get_scan_results(scan_num,chans[i],isLaserRun[i])
	for key, graph in graph_Dict.items():
		graph.Write()

	BV_for_charges.append(round(graph_Dict["graph_charge_transpose"].Eval(charge_thresh),2))
	BV_for_charges15.append(round(graph_Dict["graph_charge_transpose"].Eval(15),2))
	BV_for_charges25.append(round(graph_Dict["graph_charge_transpose"].Eval(25),2))
	Temp_for_charges.append(round(graph_Dict["graph_temp_bias"].Eval(charge_thresh),4))

	for graph_noise in graphs_noise: graph_noise.Write()
	plot_single_scan(scan_num,graph_Dict["graph"],graph_Dict["graph_MCP"],graph_Dict["graph_temp"],graph_Dict["graph_lgadbias"],graph_Dict["graph_current_lgadbias"],graph_Dict["graph_time_res"],names[i],temps[i])
	plot_noise(graphs_noise)

outFile.Save()

for i in range(44+3+4):
	if not isLaserRun[0] and ((i >=20 and i<=24) or (i>=26 and i<=34)): continue
	plot_overlay(outFile,names,temps,series_num,i+1)


outtable_BV = open("series%s_BV_for_%ifC.txt"%(series_num,charge_thresh),"w")
for i in range(len(names)):
	print names[i], "bias to reach %i fC: "%charge_thresh,BV_for_charges[i]
	outtable_BV.write(",".join([names[i],str(BV_for_charges[i]),str(BV_for_charges15[i]),str(BV_for_charges25[i])+"\n"]))

outtable_BV.close()

#outtable_BV_temp = open("series%s_temp_for_%ifC.txt"%(series_num,charge_thresh),"w")
#for i in range(len(names)):
#	print names[i], "temp to reach %i fC: "%charge_thresh,Temp_for_charges[i]
#	outtable_BV_temp.write(",".join([names[i],str(Temp_for_charges[i])+"\n"]))

#outtable_BV_temp.close()




