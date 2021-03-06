import ROOT
import CMS_lumi, tdrstyle
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
from numpy import *

ROOT.gROOT.SetBatch(True)

name = raw_input("What name to save file under? ")
coord = raw_input("How many points to graph? ")
label = raw_input("What label to add to the plot? ")
x=[]
y=[]
n=0
while n<int(coord):
  x.append(float(raw_input("x coordinate "+str(n+1)+": ")))
  y.append(float(raw_input("y coordinate "+str(n+1)+": ")))
  n=n+1


tdrstyle.setTDRStyle()
ROOT.gStyle.SetOptStat(2210)
ROOT.gStyle.SetTitleAlign(13)

CMS_lumi.lumi_13TeV =label+ "    35.9 fb^{-1}"
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

canvas.cd()

graph = ROOT.TGraph(int(coord))
n=0
while n<int(coord):
  graph.SetPoint(int(n), double(x[n]), double(y[n]))
  n=n+1

graph.Draw("A*")

CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
canvas.Update()
canvas.SaveAs("/afs/hep.wisc.edu/home/tost/workingArea/CMSSW_8_0_24_patch1/src/Real_work/"+name+".png")
canvas

