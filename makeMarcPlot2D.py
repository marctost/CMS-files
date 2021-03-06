'''
Usage:python plot.py RootFile.root label[optional]
'''

import ROOT
import CMS_lumi, tdrstyle
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
# So things don't look like crap.
ROOT.gROOT.SetBatch(True)

#set the tdr style
tdrstyle.setTDRStyle()

infile = argv[1]
direc= argv[2]
channel = raw_input("mu, e, or di? ")
plottitle = raw_input("Title of the plot: ")
name = raw_input("What should this be saved as? ")
variable1 = raw_input("Variable x: ")
xaxis = raw_input("X-axis label: ")
variable2 = raw_input("Variable y: ")
yaxis = raw_input("Y-axis label: ")

if xaxis == "m_vis":
  xaxis = "m_{vis}"
if xaxis == "mt12":
  xaxis = "M_{T,tot}"
if yaxis == "m_vis":
  yaxis = "m_{vis}"
if yaxis == "mt12":
  yaxis = "M_{T,tot}"

if channel == "di":
  label = "#tau_{h} #tau_{h}     "
if channel == "mu":
  label = "#mu #tau_{h}     "
if channel == "e":
  label = "e#tau_{h}     "





#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = str(label)+ "35.9 fb^{-1}"
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
L = 0.16*W_ref
R = 0.16*W_ref
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



print 'Using file '+infile+' \n saving file with name:\t '+name+' \n getting directory:\t '+direc+' \n going to plot variables:\t '+variable1+' '+variable2+'  \n with xaxis label:\t '+xaxis+' ' '\n with yaxis label: \t '+yaxis+'' 
######## LABEL & SAVE WHERE #########
saveWhere='/afs/hep.wisc.edu/home/tost/workingArea/CMSSW_8_0_24_patch1/src/Real_work/'

#####################################
#Get NTUPLE                 #
#####################################
ntuple_file = ROOT.TFile(infile)
tree = ntuple_file.Get(direc+"/eventTree") 
#tree = ROOT.TTree(ntuple_file.Get(direc))
hname = name
histo = ROOT.TH2F(hname,"",20,0.,400.,20, 0.,400.)  #CHANGE XAXIS HERE!!!


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


###################################center for cuts#####################################
def mutaucuts(event):
  if event.pth>140 and event.dR<1.7 and event.met>100 and event.pt_1>40 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True
  else:
    return False

def eletaucuts(event):
  if event.pth>120 and event.dR<1.5 and event.met>100 and event.pt_1>30 and event.pt_2>30 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True
  else:
    return False

def ditaucuts(event):
  if event.pth>160 and event.dR<2.1 and event.met>100 and event.pt_1>150 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
    return True
  else:
    return False



############### plot me! ###############
if direc == "muTauEventTree":
  if variable2 == "LT":
    for event in tree:
      f = variable1
      g = variable2
      f = getattr(event, variable1)
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if mutaucuts(event)==True:
	histo.Fill(f, g+r+q)

  if variable1 == "LT":
    for event in tree:
      f = variable1
      g = variable2
      f = getattr(event, variable2)
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if mutaucuts(event)==True:
	histo.Fill(g+r+q, f)

  else:
    for event in tree:
	f = variable1
	g = variable2
	f = getattr(event, variable1)
	g = getattr(event, variable2)
	if mutaucuts(event)==True:
	  histo.Fill(f, g)

if direc == "eleTauEventTree":
  if variable2 == "LT":
    for event in tree:
      f = variable1
      g = variable2
      f = getattr(event, variable1)
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if eletaucuts(event)==True:
	histo.Fill(f, g+r+q)

  if variable1 == "LT":
    for event in tree:
      f = variable1
      g = variable2
      f = getattr(event, variable2)
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if eletaucuts(event)==True:
	histo.Fill(g+r+q, f)

  else:
    for event in tree:
	f = variable1
	g = variable2
	f = getattr(event, variable1)
	g = getattr(event, variable2)
	if eletaucuts(event)==True:
	  histo.Fill(f, g)


if direc == "diTauEventTree":
  if variable2 == "LT":
    for event in tree:
      f = variable1
      g = variable2
      f = getattr(event, variable1)
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if ditaucuts(event)==True:
	histo.Fill(f, g+r+q)

  if variable1 == "LT":
    for event in tree:
      f = variable1
      g = variable2
      f = getattr(event, variable2)
      g = getattr(event, "pt_1")
      r = getattr(event, "pt_2")
      q = getattr(event, "met")
      if ditaucuts(event)==True:
	histo.Fill(g+r+q, f)

  else:
    for event in tree:
	f = variable1
	g = variable2
	f = getattr(event, variable1)
	g = getattr(event, variable2)
	if ditaucuts(event)==True:
	  histo.Fill(f, g)
    
#histo.SetLineColor(kBlue-9)
histo.SetLineWidth(2)
histo.GetXaxis().SetTitle(xaxis)
histo.GetYaxis().SetTitle(yaxis)
histo.GetXaxis().SetNdivisions(8, 8, 0)
histo.SetTitle(plottitle)
#histo.SetTitle(infile)
#histos[i].Rebin(2)
#legend1.AddEntry(histo, name)
#if hmax<histo.GetMaximum():
#   hmax = histo.GetMaximum()

#histo.SetMaximum(hmax*1.4)
histo.Draw("COLZ")



#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

#legend1.Draw("same")
saveas=saveWhere+name+variable1+variable2+'.root'
saveas=saveWhere+name+variable1+variable2+'.png'
canvas.Update()
canvas.SaveAs(saveas)
canvas

