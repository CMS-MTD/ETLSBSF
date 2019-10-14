
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
#ROOT.gStyle.SetLegendTextSize(0.05)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridColor(13)
ROOT.gStyle.SetOptFit(1)
one = ROOT.TColor(2001,0.906,0.153,0.094)
two = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four =ROOT.TColor(2004,0.071,0.694,0.18)
five =ROOT.TColor(2005,0.388,0.098,0.608)
six=ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006]

verbose = True
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
		y_axis = "MPV Ru106 response [mV]"
		x_axis = "Bias voltage [V]"
		filename = "gr"
	if plottype==2: 
		outputtag = "_corr"
		y_axis = "MPV Ru106 response [mV]"
		x_axis = "LGAD Bias voltage [V]"
		filename = "grlgad"
	if plottype==3: 
		outputtag = "_IV"
		y_axis = "Current [100 nA]"
		x_axis = "LGAD Bias voltage [V]"
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
		outputtag = "_res_vs_mpv"
		y_axis = "Time resolution [ps]"
		x_axis = "MPV Ru106 response [mV]"
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
		y_axis = "Time resolution [ps]"
		x_axis = "Mean slew rate [mV/ns]"
		filename = "grres_vs_slew"
	if plottype==11: 
		outputtag = "_risetime"
		y_axis = "Risetime [ns]"
		x_axis = "Bias voltage [V]"
		filename = "grrise"
	if plottype==12: 
		outputtag = "_risetime_vs_mpv"
		y_axis = "Risetime [ns]"
		x_axis = "MPV Ru106 response [mV]"
		filename = "grrisetime_vs_mpv"
	if plottype==13: 
		outputtag = "_lgadnoise_vs_bias"
		y_axis = "LGAD baseline noise RMS [mV] "
		x_axis = "Bias Voltage [V]"
		filename = "grlgadnoise_vs_bias"

	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()
	mgraph = ROOT.TMultiGraph()

	leg = ROOT.TLegend(0.2,0.7,0.59,0.89)
	leg.SetMargin(0.15)

	for i,scan in enumerate(scan_nums):
		graph = outFile.Get(filename+str(scan))
	 	cosmetic_tgraph(graph,i)
		mgraph.Add(graph)
	 	leg.AddEntry(graph, "%s, %i C" %(names[i],temps[i]),"EP")

	mgraph.SetTitle("; %s; %s"%(x_axis,y_axis))
	#if plottype==3: mgraph.SetTitle("; Bias voltage [V]; Current [100 nA]")
	mgraph.Draw("AELP")
	leg.Draw()
	c.Print("plots/series%i%s.pdf"%(series_num,outputtag))




def cosmetic_tgraph(graph,colorindex):
	graph.SetLineColor(colors[colorindex])
	graph.SetMarkerColor(colors[colorindex])
	graph.SetMarkerSize(0.75)
	graph.SetMarkerStyle(20)
	graph.SetTitle("; Bias voltage [V]; MPV Ru106 response [mV]")


def get_time_res_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",70,5.8e-9,6.8e-9)
	tree.Project("h","LP2_15[%i]-LP2_20[3]"%ch,"amp[%i]>15 && amp[3]>15 && LP2_20[3]!=0 && LP2_20[%i]!=0"%(ch,ch))	
	f1 = ROOT.TF1("f1","gaus",5.8e-9,6.8e-9)
	hist.Fit(f1)
	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		f1.Draw("same")
		c.Print("plots/runs/Run%i_time.pdf"%run)
	print 'Run NUmber %d,  %f, %f ' %(run,1e12*f1.GetParameter(2),1e12*f1.GetParError(2))
	return 1e12*f1.GetParameter(2),1e12*f1.GetParError(2)


def get_slew_rate_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",60,0,600e9)
	tree.Project("h","abs(risetime[%i])"%ch,"amp[%i]>15"%(ch))	### mV/ s

	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		c.Print("plots/runs/Run%i_slewrate.pdf"%run)
	#print 'Run NUmber %d,  %f, %f ' %(run,1e12*f1.GetParameter(2),1e12*f1.GetParError(2))
	return 1e-9 * hist.GetMean(),1e-9* hist.GetMeanError()

def get_risetime_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",60,0,1.2)
	tree.Project("h","1e9*abs(amp[%i]/risetime[%i])"%(ch,ch),"amp[%i]>15"%(ch))	### mV/ s

	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		c.Print("plots/runs/Run%i_risetime.pdf"%run)
	#print 'Run NUmber %d,  %f, %f ' %(run,1e12*f1.GetParameter(2),1e12*f1.GetParError(2))
	return hist.GetMean(),hist.GetMeanError()


def get_mean_response_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",40,0,300)
	minAmp = 15.
	if run==151172 or run==151173: minAmp = 40
	tree.Project("h","amp[%i]"%ch,"amp[%i]>%f&&amp[3]>10"%(ch,minAmp))
	
	fitter = lg.LanGausFit()
	#fitter.SetParLimits(1,25,1000)
	f1 = fitter.fit(hist,None,None,100)
	#f1 = fitter.fit(hist)
	# ROOT.TF1("f1","landau",0,150)
	#hist.Fit(f1)
	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		f1.Draw("same")
		c.Print("plots/runs/Run%i_amp.pdf"%run)
	return f1.GetParameter(1),f1.GetParError(1)

def get_mean_baseline_RMS_channel(tree,ch):
	hist = ROOT.TH1F("h","",20,-1000,1000)
	tree.Project("h","baseline_RMS[%i]"%ch,"")
	return hist.GetMean(),hist.GetMeanError()

def get_mean_baseline_RMS(tree):
	means_this_run=[]
	errs_this_run=[]
	for i in range(4):
		mean,err = get_mean_baseline_RMS_channel(tree,i)
		means_this_run.append(mean)
		errs_this_run.append(err)

	return means_this_run,errs_this_run

def get_mean_response(tree):
	means_this_run=[]
	errs_this_run=[]
	for i in range(4):
		mean,err = get_mean_response_channel(tree,i)
		means_this_run.append(mean)
		errs_this_run.append(err)
	
	best_mean =  max(means_this_run)
	best_chan = means_this_run.index(best_mean)	
	err = errs_this_run[best_chan]

	print best_mean,err,best_chan

	return best_mean,err


def get_scan_results(scan_num,chan):
	runs=[]
	biases=[]
	biases_meas=[]
	lgad_biases=[]
	currents_meas=[]
	temps =[] 
	
	mean_responses=[]
	err_responses=[]

	time_res=[]
	err_time_res=[]

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

	scan_txt_filename = "/home/daq/BiasScan/ETLSBSF/VoltageScanDataRegistry/scan%i.txt" % scan_num
	with open(scan_txt_filename) as scan_txt_file:
		for line in scan_txt_file:
			if line[:1] == "#": continue
			runs.append(int(line.split("\t")[0]))		
		 	biases.append(abs(float(line.split("\t")[1])))
			biases_meas.append(abs(float(line.split("\t")[2])))

			current_units_conversion = 10. # = 100 nanoamps scale
			board_resistance = 10e-3 ## megaohms (1.1 for FNAL)

			currents_meas.append(current_units_conversion*1.e6*abs(float(line.split("\t")[3]))) ## convert to microamps

			lgad_biases.append(biases[-1] - board_resistance * currents_meas[-1]/current_units_conversion) ## 1.1 MOhm in series with LGAD

			temps.append(float(line.split("\t")[4]))

			if biases[-1]>0 and abs(biases_meas[-1]-biases[-1])/biases[-1] > 0.1:
				print "[WARNING]: Scan %i, run %i set to %.0f V, measured at %.0f V" % (scan_num, runs[-1],biases[-1],biases_meas[-1])


	for i,run in enumerate(runs):
		#open root file/tree
		tree = ROOT.TChain("pulse")
		tree.Add("/home/daq/ScopeData/Reco/run_scope%i.root" % run)
		
		if chan <0:
			mean,err = get_mean_response(tree) ### find max amp channel
		else: 
			mean,err = get_mean_response_channel(tree,chan,run) ## use specified channel from series txt file
			sigma,sigmaerr = get_time_res_channel(tree,chan,run)
			slewrate,slewerr = get_slew_rate_channel(tree,chan,run)
			risetime,riseerr = get_risetime_channel(tree,chan,run)

		##MCP
		mean_MCP,err_MCP = get_mean_response_channel(tree,3)

		noise_means,noise_errs = get_mean_baseline_RMS(tree)

		means_MCP.append(mean_MCP)
		errs_MCP.append(err_MCP)
		mean_responses.append(mean)
		err_responses.append(err)

		time_res.append(sigma)
		err_time_res.append(sigmaerr)

		mean_noise.append(noise_means)
		err_mean_noise.append(noise_errs)

		snr_lgad_channel = mean/noise_means[chan]
		snr_err_lgad_channel = err/noise_means[chan]

		snr.append(snr_lgad_channel)
		snr_err.append(snr_err_lgad_channel)
		slewrates.append(slewrate)
		slewrate_errs.append(slewerr)

		risetimes.append(risetime)
		risetime_errs.append(riseerr)

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


	graph = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",mean_responses),array("d",[0.1 for i in biases]),array("d",err_responses))
	graph_MCP= ROOT.TGraphErrors(len(biases),array("d",biases),array("d",means_MCP),array("d",[0.1 for i in biases]),array("d",errs_MCP))
	graph_lgadbias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",mean_responses),array("d",[0.1 for i in biases]),array("d",err_responses))
	#graph_current_lgadbias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",currents_meas),array("d",[0.1 for i in biases]),array("d",[0.1 for i in biases]))
	graph_current_lgadbias = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",currents_meas),array("d",[0.1 for i in biases]),array("d",[0.1 for i in biases]))
	graph_temp = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",temps),array("d",[0.1 for i in biases]),array("d",[0.1 for i in biases]))
	

	graph_time_res = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",time_res),array("d",[0.1 for i in biases]),array("d",err_time_res))
	graph_slew_rate = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",slewrates),array("d",[0.1 for i in biases]),array("d",slewrate_errs))
	graph_risetime = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",risetimes),array("d",[0.1 for i in biases]),array("d",risetime_errs))
	
	graph_snr = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",snr),array("d",[0.1 for i in biases]),array("d",snr_err))
	graph_res_vs_snr = ROOT.TGraphErrors(len(biases),array("d",snr),array("d",time_res),array("d",snr_err),array("d",err_time_res))
	graph_res_vs_slew = ROOT.TGraphErrors(len(biases),array("d",slewrates),array("d",time_res),array("d",slewrate_errs),array("d",err_time_res))
	graph_res_vs_mpv = ROOT.TGraphErrors(len(biases),array("d",mean_responses),array("d",time_res),array("d",err_responses),array("d",err_time_res))
	graph_mpv_vs_snr = ROOT.TGraphErrors(len(biases),array("d",snr),array("d",mean_responses),array("d",snr_err),array("d",err_responses))
	graph_risetime_vs_mpv = ROOT.TGraphErrors(len(biases),array("d",mean_responses),array("d",risetimes),array("d",err_responses),array("d",risetime_errs))



	## give tgraphs names so they can be saved to preserve python scope for multi-scan overlay 
	graph.SetName("gr%i"%scan_num)
	graph_lgadbias.SetName("grlgad%i"%scan_num)
	graph_current_lgadbias.SetName("griv%i"%scan_num)
	graph_time_res.SetName("grres%i"%scan_num)
	graph_slew_rate.SetName("grslew%i"%scan_num)
	graph_risetime.SetName("grrise%i"%scan_num)
	graph_snr.SetName("grsnr%i"%scan_num)
	graph_res_vs_snr.SetName("grres_vs_snr%i"%scan_num)
	graph_res_vs_slew.SetName("grres_vs_slew%i"%scan_num)
	graph_res_vs_mpv.SetName("grres_vs_mpv%i"%scan_num)
	graph_mpv_vs_snr.SetName("grmpv_vs_snr%i"%scan_num)
	graph_risetime_vs_mpv.SetName("grrisetime_vs_mpv%i"%scan_num)

	


	##convert rows to columns
	col_mean_noise = zip(*mean_noise)
	col_err_noise = zip(*err_mean_noise)


	graphs_noise = []
	for ichan in range(4):
		graphs_noise.append( ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",col_mean_noise[ichan]),array("d",[0.1 for i in biases]),array("d",col_err_noise[ichan])))
		graphs_noise[-1].SetTitle("Noise in channel %i, scan %i" %(ichan,scan_num))
	#mgraph.Add(graph_norm)

	chan=2
	graph_lgadnoise_vs_bias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",col_mean_noise[chan]),array("d",[0.1 for i in biases]),array("d",col_err_noise[chan]))
	graph_lgadnoise_vs_bias.SetName("grlgadnoise_vs_bias%i"%scan_num)
	
	return graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias,graphs_noise,graph_time_res,graph_snr,graph_res_vs_snr,graph_res_vs_mpv,graph_mpv_vs_snr,graph_slew_rate,graph_res_vs_slew,graph_risetime,graph_risetime_vs_mpv,graph_lgadnoise_vs_bias
	


if len(sys.argv) < 2:
    sys.exit('Please provide a series number') 

series_num = int(sys.argv[1])
series_txt_filename="series/series%i.txt" % series_num
scan_nums=[]
names=[]
temps=[]
chans=[]
with open(series_txt_filename) as series_txt_file:
		for line in series_txt_file:
			if len(line.split(","))==0: continue
			if line[:1] == "#": continue
			scan_nums.append(int(line.split(",")[0]))		
			names.append(line.split(",")[1])
			temps.append(int(line.split(",")[2]))
			chans.append(2) # LGAD channel.
			# if "ch" in line.split(",")[3]: 
			# 	human_channel_num = int(line.split(",")[3].split("ch")[1].split()[0])
			# 	if human_channel_num <= 8: chans.append(human_channel_num-1)
			# 	else: chans.append(human_channel_num) 
			# else: chans.append(-1)	

outFile = ROOT.TFile("buffer.root","RECREATE")
for i,scan_num in enumerate(scan_nums):
	graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias,graphs_noise,graph_time_res,graph_snr,graph_res_vs_snr,graph_res_vs_mpv,graph_mpv_vs_snr,graph_slew_rate,graph_res_vs_slew,graph_risetime,graph_risetime_vs_mpv, graph_lgadnoise_vs_bias = get_scan_results(scan_num,chans[i])
	graph_lgadbias.Write()
	graph.Write()
	graph_current_lgadbias.Write()
	graph_time_res.Write()
	graph_snr.Write()
	graph_res_vs_snr.Write()
	graph_res_vs_mpv.Write()
	graph_mpv_vs_snr.Write()
	graph_slew_rate.Write()
	graph_res_vs_slew.Write()
	graph_risetime.Write()
	graph_risetime_vs_mpv.Write()
	graph_lgadnoise_vs_bias.Write()

	for graph_noise in graphs_noise: graph_noise.Write()
	plot_single_scan(scan_num,graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias,graph_time_res,names[i],temps[i])
	plot_noise(graphs_noise)

outFile.Save()

for i in range(13):
	plot_overlay(outFile,names,temps,series_num,i+1)


