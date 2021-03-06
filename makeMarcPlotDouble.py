import ROOT
import CMS_lumi, tdrstyle
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetOptStat(2210)

infile = argv[1]
direc = argv[2]
#plottitle=raw_input("title of the graph: ")
name=raw_input("name the file: ")
channel = raw_input("mu, e, or di? ")
variable1 = raw_input("what variable to plot first?: ")
variable2 = raw_input("What variable to plot second?: ")
xaxis = raw_input("what to label the xaxis? ")
if xaxis == "m_vis":
  xaxis = "m_{vis}"
if xaxis == "mt12":
  xaxis = "M_{T,tot}"
if channel == "di":
  label = "#tau_{h} #tau_{h}    "
if channel == "mu":
  label = "#mu #tau_{h}    "
if channel == "e":
  label = "e#tau_{h}     "
else:
  channel = "Hi everyone!!11   "

tdrstyle.setTDRStyle()

def cutcenter(event):
  if direc == "muTauEventTree":
    if event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
      return True
  if direc == "eleTauEventTree":
    if event.pt_1>27 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
      return True
  if direc == "diTauEventTree":
    if event.pt_1>40 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
      return True



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

saveWhere = '/afs/hep.wisc.edu/home/tost/workingArea/CMSSW_8_0_24_patch1/src/Real_work/'

ntuple_file = ROOT.TFile(infile)
tree = ntuple_file.Get(direc+"/eventTree")
hname = name

histo1 = ROOT.TH1F(hname+"1","",100,0,2)
histo2 = ROOT.TH1F(hname+"2","",100,0,2)

x1_l = 0.93
y1_l = 0.90
dx_l = 0.38
dy_l = 0.20
x0_l = x1_l-dx_l
y0_l = y1_l-dy_l


if direc == "muTauEventTree":
  if variable1 == "pfres" and variable2 == "puppires":
    for event in tree:
      g = getattr(event, "mt12")
      f = getattr(event, "genMass")
      w = getattr(event, "puppimt")
      if cutcenter(event):
	histo1.Fill((g-f)/g)
	histo2.Fill((w-f)/w)
  if variable2 == "pfres" and variable1 == "puppires":
    for event in tree:
      g = getattr(event, "mt12")
      f = getattr(event, "genMass")
      w = getattr(event, "puppimt")
      if cutcenter(event):
	histo2.Fill((g-f)/g)
	histo1.Fill((w-f)/w)
#  else:
 #   for event in tree:
  #    g = getattr(event, variable1)
   #   f = getattr(event, variable2)
    #  if cutcenter(event):
	#histo1.Fill(g)
	#histo2.Fill(f)


if direc == "eleTauEventTree":
  if variable1 == "pfres" and variable2 == "puppires":
    for event in tree:
      g = getattr(event, "mt12")
      f = getattr(event, "genMass")
      w = getattr(event, "puppimt")
      if cutcenter(event):
	histo1.Fill((g-f)/g)
	histo2.Fill((w-f)/w)
  if variable2 == "pfres" and variable1 == "puppires":
    for event in tree:
      g = getattr(event, "mt12")
      f = getattr(event, "genMass")
      w = getattr(event, "puppimt")
      if cutcenter(event):
	histo2.Fill((g-f)/g)
	histo1.Fill((w-f)/w)
  else:
    for event in tree:
      g = getattr(event, variable1)
      f = getattr(event, variable2)
      if cutcenter(event):
	histo1.Fill(g)
	histo2.Fill(f)


if direc == "diTauEventTree":
  if variable1 == "pfres" and variable2 == "puppires":
    for event in tree:
      g = getattr(event, "mt12")
      f = getattr(event, "genMass")
      w = getattr(event, "puppimt")
      if cutcenter(event):
	histo1.Fill((g-f)/g)
	histo2.Fill((w-f)/w)
  if variable2 == "pfres" and variable1 == "puppires":
    for event in tree:
      g = getattr(event, "mt12")
      f = getattr(event, "genMass")
      w = getattr(event, "puppimt")
      if cutcenter(event):
	histo2.Fill((g-f)/g)
	histo1.Fill((w-f)/w)
  else:
    for event in tree:
      g = getattr(event, variable1)
      f = getattr(event, variable2)
      if cutcenter(event):
	histo1.Fill(g)
	histo2.Fill(f)


histo1.SetLineColor(ROOT.kBlue)
histo2.SetLineColor(ROOT.kRed)
histo1.SetLineWidth(2)
histo2.SetLineWidth(2)

legend1 = ROOT.TLegend(x0_l,y0_l,x1_l, y1_l,"","brNDC")
legend1.SetFillColor(ROOT.kWhite)
legend1.SetBorderSize(1)
legend1.AddEntry(histo1, str(variable1), "l")
legend1.AddEntry(histo2, str(variable2), "l")
legend1.SetTextSize(.05)

hmax1 = 0
hmax2 =0
if hmax1<histo1.GetMaximum():
  hmax1 = histo1.GetMaximum()
if hmax2<histo2.GetMaximum():
  hmax2 = histo2.GetMaximum()

if hmax1 > hmax2:
  histo1.SetMaximum(hmax1*1.4)
  histo2.SetMaximum(hmax1*1.4)
else:
  histo1.SetMaximum(hmax2*1.4)
  histo2.SetMaximum(hmax2*1.4)

histo1.Draw("HIST")
histo2.Draw("same")
legend1.Draw("same")
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

histo1.GetXaxis().SetTitle(xaxis)

canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()

saveas=saveWhere+name+variable1+'.root'
canvas.Update()
canvas.SaveAs(saveas)
canvas
