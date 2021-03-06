'''
Usage:python plot.py RootFile.root label[optional]
Author: L. Dodd, UW Madison
'''

import ROOT
import CMS_lumi, tdrstyle
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
# So things don't look like crap.
ROOT.gROOT.SetBatch(True)


infile = argv[1]
direc = argv[2]
#plottitle=raw_input("title of the graph: ")





#set the tdr style
tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(2210)
ROOT.gStyle.SetTitleAlign(13)

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV =str(label)+ "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
H_ref = 800; 
W_ref = 800; 
W = W_ref
H  = H_ref
iPeriod = 4
# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref
canvas = ROOT.TCanvas("c2","c2",50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)



######## File #########





print 'Using file '+infile+' \n saving file with name:\t '+name+' \n getting directory:\t '+direc+' \n going to plot variable:\t '+variable+' \n with xaxis label:\t '+xaxis+' ' 
######## LABEL & SAVE WHERE #########
saveWhere='/afs/hep.wisc.edu/home/tost/workingArea/CMSSW_8_0_24_patch1/src/Real_work/'

#####################################
#Get NTUPLE                 #
#####################################
ntuple_file = ROOT.TFile(infile)
tree = ntuple_file.Get(direc+"/eventTree") 
#tree = ROOT.TTree(ntuple_file.Get(direc))
hname = name
histo = ROOT.TH1F(hname,"",100,0,2)  #CHANGE XAXIS HERE!!!

####MAKE PLOT NICE####
x1_l = 0.93
y1_l = 0.90
dx_l = 0.38
dy_l = 0.20
x0_l = x1_l-dx_l
y0_l = y1_l-dy_l

#legend1 =  ROOT.TLegend(x0_l,y0_l,x1_l, y1_l,"","brNDC")
#legend1.SetFillColor(ROOT.kWhite)
#legend1.SetBorderSize(1)

hmax=0

############### plot me! ###############3
if direc == "muTauEventTree":
  if variable == "LT":
    for event in tree:
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
	histo.Fill(g+r+q)

  if variable == "res":
    for event in tree:
      r = getattr(event, "genMass")
      q = getattr(event, "puppimt")
      if event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
	histo.Fill((q-r)/q)

  else:
    for event in tree:
	f = variable
	f = getattr(event, variable)
	#event.mt12 is the way to grab mt12 variable.
	#we have to do this to "turn a python string into code"
	if event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
	  histo.Fill(f)

if direc == "eleTauEventTree":
  if variable == "LT":
    for event in tree:
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if event.pt_1>27 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
	histo.Fill(g+r+q)

  if variable == "res":
    for event in tree:
      r = getattr(event, "genMass")
      q = getattr(event, "puppimt")
      if event.pt_1>27 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
	histo.Fill((q-r)/q)

  else:
    for event in tree:
	f = variable
	f = getattr(event, variable)
	#event.mt12 is the way to grab mt12 variable.
	#we have to do this to "turn a python string into code"
	if event.pt_1>27 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
	  histo.Fill(f)
    
if direc == "diTauEventTree":
  if variable == "LT":
    for event in tree:
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if event.pt_1>40 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
	histo.Fill(g+r+q)
      
  if variable == "res":
    for event in tree:
      g = getattr(event, "met")
      r = getattr(event, "genMass")
      q = getattr(event, "puppimt")
      if event.pt_1>40 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
	histo.Fill((g-r)/q)

  else:
    for event in tree:
	f = variable
	f = getattr(event, variable)
	#event.mt12 is the way to grab mt12 variable.
	#we have to do this to "turn a python string into code"
	if event.pt_1>40 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
	  histo.Fill(f)




#histo.SetLineColor(kBlue-9)
histo.SetLineWidth(2)
histo.GetXaxis().SetTitle(xaxis)
#histo.SetTitle(plottitle)
#histos[i].Rebin(2)
#legend1.AddEntry(variable, name)
#legend1.SetTextSize(.05)
if hmax<histo.GetMaximum():
   hmax = histo.GetMaximum()

histo.SetMaximum(hmax*1.4)
histo.Draw("HIST")
#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)


canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

#legend1.Draw("same")
saveas=saveWhere+name+variable+'.root'
#saveas=saveWhere+name+variable+'.png'
canvas.Update()
canvas.SaveAs(saveas)
canvas

