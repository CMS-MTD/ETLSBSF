
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
	cosmetic_tgraph(graph_MCP,2)
	cosmetic_tgraph(graph_temp,1)
	cosmetic_tgraph(graph_lgadbias,5)
	cosmetic_tgraph(graph_current_lgadbias,6)
	cosmetic_tgraph(graph_time_res,4)

	c = ROOT.TCanvas()
	c.SetGridy()
	c.SetGridx()
	mgraph = ROOT.TMultiGraph()
	mgraph.Add(graph_MCP)
	mgraph.Add(graph_temp)
	mgraph.Add(graph_current_lgadbias)
	mgraph.Add(graph)
	mgraph.Add(graph_lgadbias)
	mgraph.Add(graph_time_res)

	mgraph.SetTitle("; Bias voltage [V]; Average beta response [mV]")
	# graph.Draw("AELP")
	# graph_MCP.Draw("ELP same")
	# graph_norm.Draw("ELP same")
	# graph_temp.Draw("ELP same")
	#mgraph.SetMinimum(-5)
	mgraph.Draw("AELP")
	leg = ROOT.TLegend(0.2,0.7,0.59,0.89)
	leg.SetMargin(0.15)
	leg.AddEntry(graph_MCP, "MCP","EP")
	leg.AddEntry(graph_temp, "Measured temperature [C]","EP")
	leg.AddEntry(graph_current_lgadbias, "Current [#muA]","EP")
	leg.AddEntry(graph, "%s, %i C" % (name,temp),"EP")
	leg.AddEntry(graph_lgadbias, "%s, corrected LGAD bias"%name,"EP")
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


	mgraph.SetTitle("; Bias voltage [V]; Average baseline RMS [mV]")	
	mgraph.Draw("AELP")
	leg.Draw()

	c.Print("plots/scan%i_noise.pdf"%scan_num)

def plot_overlay(outfile,names,temps,series_num,plottype):
	if plottype==1: filename = "gr"
	if plottype==2: filename = "grlgad"
	if plottype==3: filename = "griv"

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

	mgraph.SetTitle("; Bias voltage [V]; Average Ru106 response [mV]")
	if plottype==3: mgraph.SetTitle("; Bias voltage [V]; Current [10 #muA]")
	mgraph.Draw("AELP")
	leg.Draw()
	if plottype==1: c.Print("plots/series%i.pdf"%series_num)
	if plottype==2: c.Print("plots/series%i_corr.pdf"%series_num)
	if plottype==3: c.Print("plots/series%i_IV.pdf"%series_num)



def cosmetic_tgraph(graph,colorindex):
	graph.SetLineColor(colors[colorindex])
	graph.SetMarkerColor(colors[colorindex])
	graph.SetMarkerSize(1)
	graph.SetMarkerStyle(20)
	graph.SetTitle("; Bias voltage [V]; Average Ru106 response [mV]")


def get_time_res_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",40,5.8e-9,6.8e-9)
	tree.Project("h","LP2_15[%i]-LP2_20[3]"%ch,"amp[%i]>15 && amp[3]>15 && LP2_20[3]!=0 && LP2_20[%i]!=0"%(ch,ch))	
	f1 = ROOT.TF1("f1","gaus",5.8e-9,6.8e-9)
	hist.Fit(f1)
	if run>0:
		c = ROOT.TCanvas()
		hist.Draw()
		f1.Draw("same")
		c.Print("plots/runs/Run%i_time.pdf"%run)
	return 1e12*f1.GetParameter(2),1e12*f1.GetParError(2)


def get_mean_response_channel(tree,ch,run=-1):
	hist = ROOT.TH1D("h","",40,0,150)
	tree.Project("h","amp[%i]"%ch,"amp[%i]>15&&amp[3]>10"%ch)
	
	fitter = lg.LanGausFit()
	f1 = fitter.fit(hist)
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

	scan_txt_filename = "/home/daq/BiasScan/SBSF/VoltageScanDataRegistry/scan%i.txt" % scan_num
	with open(scan_txt_filename) as scan_txt_file:
		for line in scan_txt_file:
			if line[:1] == "#": continue
			runs.append(int(line.split("\t")[0]))		
		 	biases.append(abs(float(line.split("\t")[1])))
			biases_meas.append(abs(float(line.split("\t")[2])))
			currents_meas.append(1.e6*abs(float(line.split("\t")[3]))) ## convert to microamps

			lgad_biases.append(biases[-1] - 1.1 * currents_meas[-1]) ## 1.1 MOhm in series with LGAD

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
			sig,sigerr = get_time_res_channel(tree,chan,run)

		##MCP
		mean_MCP,err_MCP = get_mean_response_channel(tree,3)

		noise_means,noise_errs = get_mean_baseline_RMS(tree)

		means_MCP.append(mean_MCP)
		errs_MCP.append(err_MCP)
		mean_responses.append(mean)
		err_responses.append(err)

		time_res.append(sig)
		err_time_res.append(sigerr)

		mean_noise.append(noise_means)
		err_mean_noise.append(noise_errs)
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


	graph = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",mean_responses),array("d",[1 for i in biases]),array("d",err_responses))
	graph_MCP= ROOT.TGraphErrors(len(biases),array("d",biases),array("d",means_MCP),array("d",[1 for i in biases]),array("d",errs_MCP))
	graph_lgadbias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",mean_responses),array("d",[1 for i in biases]),array("d",err_responses))
	graph_current_lgadbias = ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",currents_meas),array("d",[1 for i in biases]),array("d",[1 for i in biases]))

	graph_temp = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",temps),array("d",[1 for i in biases]),array("d",[0.1 for i in biases]))
	graph_lgadbias.SetName("grlgad%i"%scan_num)
	graph_current_lgadbias.SetName("griv%i"%scan_num)

	graph_time_res = ROOT.TGraphErrors(len(biases),array("d",biases),array("d",time_res),array("d",[1 for i in biases]),array("d",err_time_res))

	##convert rows to columns
	col_mean_noise = zip(*mean_noise)
	col_err_noise = zip(*err_mean_noise)


	graphs_noise = []
	for ichan in range(4):
		graphs_noise.append( ROOT.TGraphErrors(len(biases),array("d",lgad_biases),array("d",col_mean_noise[ichan]),array("d",[1 for i in biases]),array("d",col_err_noise[ichan])))
		graphs_noise[-1].SetTitle("Noise in channel %i, scan %i" %(ichan,scan_num))
	#mgraph.Add(graph_norm)
	return graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias,graphs_noise,graph_time_res
	


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
	graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias,graphs_noise,graph_time_res = get_scan_results(scan_num,chans[i])
	graph_lgadbias.Write()
	graph_current_lgadbias.Write()
	graph_time_res.Write()
	for graph_noise in graphs_noise: graph_noise.Write()
	plot_single_scan(scan_num,graph,graph_MCP,graph_temp,graph_lgadbias,graph_current_lgadbias,graph_time_res,names[i],temps[i])
	plot_noise(graphs_noise)

outFile.Save()

#plot_overlay(outFile,names,temps,series_num,1)
plot_overlay(outFile,names,temps,series_num,2)
plot_overlay(outFile,names,temps,series_num,3)
