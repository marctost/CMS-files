'''
Usage: python makeMarcPlotstacked.py file.root file.root...
Author: Marc Tost, UW Madison
'''

import ROOT
import CMS_lumi, tdrstyle
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
import math

ROOT.gROOT.SetBatch(True)

filenumber = raw_input("How many files to graph? ")
name=raw_input("name the file: ")
channel = raw_input("mu, e, or di? ")
title = raw_input("What to title the graph? ")
variable = raw_input("what variable to plot?: ")
xaxis = raw_input("what to label the xaxis? ")
ratioplot = raw_input("Add a ratio plot?(y/n) ")
topbin = raw_input("what to make top bin?: ")
bottombin = raw_input("What to make the bottom bin?: ")
binnumber = raw_input("How many bins?: ")
if xaxis == "m_vis":
  xaxis = "m_{vis}"
if xaxis == "mt12":
  xaxis = "M_{T,tot}"



if channel == "di":
  label = str(title)+"   #tau_{h}#tau_{h}     "
if channel == "mu":
  label = str(title)+"    #mu#tau_{h}     "
if channel == "e":
  label = str(title)+"    e#tau_{h}     "

infile = []
for n in range(0, int(filenumber)):
  infile.append(argv[n+1])
  n=n+1




# mutau: event.met>150 and event.m_vis<125 and event.pth>120 and event.dR<1.7 and event.pt_1>26 and event.pt_2>20 and event.npv>0 and 

# etau: event.met>150 and event.pth>120 and event.m_vis<125 and event.dR<1.7 and event.pt_1>26 and event.pt_2>20 and 

# ditau: event.met>160 and event.m_vis<125 and event.pth>120 and event.dR<2.1 and event.pt_1>55 and event.pt_2>40 and event.npv>0 and 
############################################################
def muTauCutTester(event):
  if event.met>150 and event.m_vis<125 and event.pth>120 and event.dR<1.7 and event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0 and event.BadMuonFilter==1 and event.Flag_HBHENoiseFilter_fired == 1 and event.Flag_HBHENoiseIsoFilter_fired == 1 and event.Flag_goodVertices_fired == 1 and event.Flag_EcalDeadCellTriggerPrimitiveFilter_fired == 1:
    return True
def eleTauCutTester(event):
  if event.met>150 and event.pth>120 and event.m_vis<125 and event.dR<1.7 and event.pt_1>26 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0 and event.BadMuonFilter==1 and event.Flag_HBHENoiseFilter_fired==1 and event.Flag_HBHENoiseIsoFilter_fired==1 and event.Flag_globalTightHalo2016Filter_fired==1 and event.Flag_goodVertices_fired==1 and event.Flag_EcalDeadCellTriggerPrimitiveFilter_fired==1:
    return True
def diTauCutTester(event):
  if event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
    return True
def datamuTauCutTester(event):
    if event.Flag_eeBadScFilter_fired == 1:
      return True
def dataeleTauCutTester(event):
    if event.Flag_eeBadScFilter_fired==1:
      return True

#############################################################




colors = [ROOT.kRed, ROOT.kBlue, ROOT.kMagenta, ROOT.kCyan, ROOT.kOrange, ROOT.kSpring, ROOT.kTeal, ROOT.kAzure, ROOT.kPink, ROOT.kYellow]
saveWhere='/afs/hep.wisc.edu/home/tost/workingArea/CMSSW_8_0_24_patch1/src/Real_work/'

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
B_ratio = 0.1*H_ref
T_ratio = 0.03*H_ref
B_ratio_label = 0.3*H_ref
canvas1 = ROOT.TCanvas("c2","c2",50,50,W,H)
canvas1.SetFillColor(0)
canvas1.SetBorderMode(0)
canvas1.SetFrameFillStyle(0)
canvas1.SetFrameBorderMode(0)
canvas1.SetTickx(0)
canvas1.SetTicky(0)
stacks1 = ROOT.THStack("stacks1","")
x1_l = 0.93
y1_l = 0.90
dx_l = 0.38
dy_l = 0.20
x0_l = x1_l-dx_l
y0_l = y1_l-dy_l


if (ratioplot != "y"):
  canvas1.SetLeftMargin( L/W )
  canvas1.SetRightMargin( R/W )
  canvas1.SetTopMargin( T/H )
  canvas1.SetBottomMargin( B/H )

  
canvas1.cd()

if (ratioplot == "y"):
  plotPad = ROOT.TPad("plotpad","",0.0,0.3,1.0,1.0)
  plotPad.SetLeftMargin(L/W)
  plotPad.SetRightMargin(R/W)
  plotPad.SetTopMargin(T/H)
  plotPad.SetBottomMargin(B_ratio/H)
  plotPad.SetFillColor(0)
  plotPad.SetBottomMargin(0)

  ratioPad = ROOT.TPad("ratioPad","",0.0,0.0,1.0,0.31)
  ratioPad.SetLeftMargin(L/W)
  ratioPad.SetRightMargin(R/W)
  ratioPad.SetTopMargin(T_ratio/H)
  ratioPad.SetBottomMargin(B_ratio_label/H)
  ratioPad.SetGridy(1)
  ratioPad.SetFillColor(4000)

if (ratioplot != "y"):
  plotPad = ROOT.TPad("plotPad","",0.0,0.0,1.0,1.0)
  plotPad.SetLeftMargin(L*1.4/W)
  plotPad.SetRightMargin(R/W)
  plotPad.SetTopMargin(T/H)
  plotPad.SetBottomMargin(B/H)

plotPad.Draw()
plotPad.cd()

#######################################
legend =  ROOT.TLegend(x0_l,y0_l,x1_l, y1_l,"","brNDC")
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(1)

histo = {str(0):ROOT.TH1F("histo0",title,int(binnumber),float(bottombin),float(topbin)), str(1):ROOT.TH1F("histo1",title,int(binnumber),float(bottombin),float(topbin)), str(2):ROOT.TH1F("histo2",title,int(binnumber),float(bottombin),float(topbin)), str(3):ROOT.TH1F("histo3",title,int(binnumber),float(bottombin),float(topbin)), str(4):ROOT.TH1F("histo4",title,int(binnumber),float(bottombin),float(topbin)), str(5):ROOT.TH1F("histo5",title,int(binnumber),float(bottombin),float(topbin)), str(6):ROOT.TH1F("histo6",title,int(binnumber),float(bottombin),float(topbin)), str(7):ROOT.TH1F("histo7",title,int(binnumber),float(bottombin),float(topbin)), str(8):ROOT.TH1F("histo8",title,int(binnumber),float(bottombin),float(topbin)), str(9):ROOT.TH1F("histo9",title,int(binnumber),float(bottombin),float(topbin))} 

signal = ROOT.TH1F("signal",title, int(binnumber),float(bottombin), float(topbin))
signalfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/ZpBaryonic_Zp1000_MChi150.root")

################################################

if channel == "mu":
  signaltree = signalfile.Get("muTauEventTree/eventTree")
  for event in signaltree:
    g = getattr(event, variable)
    weight = getattr(event, "__WEIGHT__")
    genweight = getattr(event, "GENWEIGHT")
    puweight = getattr(event, "puweight")
    pogid1 = getattr(event, "POGid1")
    pogtrigger = getattr(event, "POGtrigger")
    tauid1 = getattr(event, "TAUID1")
    trackweight = getattr(event, "trackweight")
    if muTauCutTester(event):
      signal.Fill(g, 35870*weight*genweight*puweight*pogid1*pogtrigger*tauid1*trackweight)
elif channel == "e":
  signaltree = signalfile.Get("eleTauEventTree/eventTree")
  for event in signaltree:
    g = getattr(event, variable)
    weight = getattr(event, "__WEIGHT__")
    genweight = getattr(event, "GENWEIGHT")
    puweight = getattr(event, "puweight")
    tauid1 = getattr(event, "TAUID1")
    idisoweight = getattr(event, "idisoweight_REDO")
    trigweight = getattr(event, "trigweight_REDO")
    trackweight = getattr(event, "trackweight")
    if eleTauCutTester(event):
      signal.Fill(g, 35870*weight*genweight*puweight*tauid1*idisoweight*trigweight*trackweight)
elif channel == "di":
  signaltree = signalfile.Get("diTauEventTree/eventTree")
  for event in signaltree:
    g = getattr(event, variable)
    weight = getattr(event, "__WEIGHT__")
    genweight = getattr(event, "GENWEIGHT")
    puweight = getattr(event, "puweight")
    trigweight = getattr(event, "trigweight_REDO")
    tauid1 = getattr(event, "TAUID1")
    if diTauCutTester(event):
      signal.Fill(g, 35870*weight*genweight*puweight*trigweight*tauid1)

signal.SetLineColor(ROOT.kRed)



if channel == "mu":
  datafile1 = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/muDATA.root")
elif channel == "e":
  datafile1 = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/eleDATA.root")
elif channel == "di":
  datafile1 = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/tauDATA.root")

data = ROOT.TH1F("data",title,int(binnumber),float(bottombin),float(topbin))

if channel == "mu":
  datatree = datafile1.Get("muTauEventTree/eventTree")
elif channel =="e":
  datatree = datafile1.Get("eleTauEventTree/eventTree")
elif channel =="di":
  datatree = datafile1.Get("diTauEventTree/eventTree")
q=0
for event in datatree:
  g = getattr(event, variable)
  if channel =="mu":
    if muTauCutTester(event) and datamuTauCutTester(event):
      data.Fill(g)
      q=q+1
  elif channel =="e":
    if eleTauCutTester(event):
      data.Fill(g)
      q=q+1
  elif channel =="di":
    if diTauCutTester(event):
      data.Fill(g)
      q=q+1
print ("Data events passing cuts: "+str(q))


data.SetMarkerStyle(20)
data.SetMarkerSize(1.0)
data.SetLineColor(ROOT.kBlack)



for i in range(0, int(filenumber)):
  ntuple_file = ROOT.TFile(infile[i])
  print channel
  if channel == "mu":
    tree = ntuple_file.Get("muTauEventTree/eventTree")
  elif channel == "e":
    tree = ntuple_file.Get("eleTauEventTree/eventTree")
  elif channel == "di":
    tree = ntuple_file.Get("diTauEventTree/eventTree")
  for event in tree:
    g = getattr(event, variable)
    if infile[i] == "/nfs_scratch/tost/monohiggs_Aug27/ZJETS.root":
      zptweight = getattr(event, "ZPt_reweight")
    elif infile != "/nfs_scratch/tost/monohiggs_Aug27/ZJETS.root":
      zptweight = 1
    if infile[i] == "/nfs_scratch/tost/monohiggs_Aug27/WJETS.root":
      wptweight = getattr(event, "WPt_reweight")
    elif infile[i] != "/nfs_scratch/tost/monohiggs_Aug27/WJETS.root":
      wptweight = 1
    if channel == "mu":
      weight = getattr(event, "__WEIGHT__")
      genweight = getattr(event, "GENWEIGHT")
      puweight = getattr(event, "puweight")
      pogid1 = getattr(event, "POGid1")
      pogtrigger = getattr(event, "POGtrigger")
      tauid1 = getattr(event, "TAUID1")
      trackweight = getattr(event, "trackweight")
      if muTauCutTester(event):
	histo[str(i)].Fill(g, weight*genweight*puweight*pogid1*pogtrigger*tauid1*trackweight*35.9*1000*zptweight*wptweight)
    elif channel == "e":
      weight = getattr(event, "__WEIGHT__")
      genweight = getattr(event, "GENWEIGHT")
      puweight = getattr(event, "puweight")
      tauid1 = getattr(event, "TAUID1")
      idisoweight = getattr(event, "idisoweight_REDO")
      trigweight = getattr(event, "trigweight_REDO")
      trackweight = getattr(event, "trackweight")
      if eleTauCutTester(event):
	histo[str(i)].Fill(g, weight*genweight*puweight*tauid1*idisoweight*trigweight*trackweight*35.9*1000*zptweight*wptweight)
    elif channel == "di":
      weight = getattr(event, "__WEIGHT__")
      genweight = getattr(event, "GENWEIGHT")
      puweight = getattr(event, "puweight")
      trigweight = getattr(event, "trigweight_REDO")
      tauid1 = getattr(event, "TAUID1")
      if diTauCutTester(event):
	histo[str(i)].Fill(g, weight*genweight*puweight*trigweight*tauid1*35.9*1000*zptweight*wptweight)




label=[]
for j in range(0,int(filenumber)):
  histo[str(j)].SetFillColor(colors[j])
  histo[str(j)].SetLineColor(ROOT.kBlack)
  label.append(raw_input("What to label "+str(infile[j])+": "))
  legend.AddEntry(histo[str(j)], label[j],"f")

legend.AddEntry(signal, "Signal", "l")
legend.AddEntry(data,"Observed","P")

for w in range(0,int(filenumber)):
  stacks1.Add(histo[str(w)])


stacks1.Draw("HIST")
signal.Draw("HIST SAME")

if (data.GetMaximum() > stacks1.GetMaximum()):
  stacks1.SetMaximum(data.GetMaximum()*1.4)
if (data.GetMaximum() <= stacks1.GetMaximum()):
  stacks1.SetMaximum(stacks1.GetMaximum()*1.4)


data.Draw("e,SAME")
CMS_lumi.CMS_lumi(canvas1, iPeriod, iPos)
stacks1.GetXaxis().SetTitle(xaxis)
stacks1.GetXaxis().SetLabelSize(0.035)
stacks1.GetYaxis().SetLabelSize(0.035)
stacks1.GetXaxis().SetTitleSize(0.05)


if (ratioplot=="y"):
  data2 = data.Clone("data")
  #Do some more things once there is a known error, useless for now


canvas1.Modified()
canvas1.cd()
canvas1.Update()
canvas1.RedrawAxis()
frame = canvas1.GetFrame()
frame.Draw()

legend.Draw("same")
saveas=saveWhere+name+variable+'.png'
canvas1.Update()
canvas1.SaveAs(saveas)
canvas1
