import ROOT
import CMS_lumi, tdrstyle
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
import math

ROOT.gROOT.SetBatch(True)

channel = raw_input("What channel are we using? (mu, e, di) ")
axislabel = raw_input("What to label the axis? ")
variable = raw_input("What variable are we using? ")

if channel == "di":
  label = "   #tau_{h}#tau_{h}     "
if channel == "mu":
  label = "    #mu#tau_{h}     "
if channel == "e":
  label = "    e#tau_{h}     "


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

canvas1.SetLeftMargin( L/W )
canvas1.SetRightMargin( R/W )
canvas1.SetTopMargin( T/H )
canvas1.SetBottomMargin( B/H )

canvas1.cd()

plotPad = ROOT.TPad("plotPad","",0.0,0.0,1.0,1.0)
plotPad.SetLeftMargin(L*1.4/W)
plotPad.SetRightMargin(R/W)
plotPad.SetTopMargin(T/H)
plotPad.SetBottomMargin(B/H)

plotPad.Draw()
plotPad.cd()


f = ROOT.TFile('/afs/hep.wisc.edu/home/tost/workingArea/CMSSW_8_0_24_patch1/src/Real_work/Histoshere.root')
f.cd("histosarehere")

sig = f.Get("histosarehere/sig")
smh = f.Get("histosarehere/smh")
dibos = f.Get("histosarehere/dibos")
wjet = f.Get("histosarehere/wjet")
znu = f.Get("histosarehere/znu")
zjet = f.Get("histosarehere/zjet")
tthist = f.Get("histosarehere/tthist")
dat = f.Get("histosarehere/dat")


sig.SetLineColor(ROOT.kRed)
smh.SetFillColor(ROOT.kOrange)
smh.SetLineColor(ROOT.kBlack)
dibos.SetFillColor(ROOT.kRed +3)
dibos.SetLineColor(ROOT.kBlack)
wjet.SetFillColor(ROOT.kBlue -9)
wjet.SetLineColor(ROOT.kBlack)
znu.SetFillColor(ROOT.kPink +2)
znu.SetLineColor(ROOT.kBlack)
zjet.SetFillColor(ROOT.kGreen +3)
zjet.SetLineColor(ROOT.kBlack)
tthist.SetFilColor(ROOT.kSpring)
tthist.SetLineColor(ROOT.kBlack)

dat.SetMarkerStyle(22)
dat.SetMarkerColor(ROOT.kBlack)

stacks1.Add(znu)
stacks1.Add(smh)
stacks1.Add(tthist)
stacks1.Add(wjet)
stacks1.Add(dibos)
stacks1.Add(zjet)

stacks1.Draw()
stacks1.SetMaximum(stacks1.GetMaximum()*1.3)
stacks1.GetXaxis().SetTitle(axislabel)
stacks1.GetXaxis().SetLabelSize(0.035)
stacks1.GetXaxis().SetTitleSize(0.05)
stacks1.GetYaxis().SetTitle("Events")
stacks1.GetYaxis().SetLabelSize(0.035)
stacks1.GetYaxis().SetTitleSize(0.05)

dat.Draw("sameE0")
sig.Draw("same")

legend = ROOT.TLegend(x0_l,y0_l,x1_l, y1_l,"","brNDC")
legend.SetFillColor(ROOT.kWhite)
legend.SetBorderSize(1)

legend.AddEntry(znu, "Znunu")
legend.AddEntry(smh, "smH125")
legend.AddEntry(tthist, "TT")
legend.AddEntry(wjet, "W+jets")
legend.AddEntry(dibos, "DiBoson")
legend.AddEntry(zjet, "Z+jets")
legend.AddEntry(sig, "Signal")
legend.AddEntry(dat, "Observed")


canvas1.Modified()
canvas1.cd()
canvas1.Update()
canvas1.RedrawAxis()
frame = canvas1.GetFrame()
frame.Draw()

legend.Draw("same")
saveas = saveWhere+str(channel)+str(variable)+'.root'
canvas1.Update()
canvas1.SaveAs(saveas)
canvas1





