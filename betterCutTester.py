import ROOT
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
import math
import os

#get input as to what the signal file is, and basic info for how to create 
#the histograms, and how to do cuts

ROOT.gROOT.SetBatch(True)
signalfile = argv[1]
cutvar = raw_input("What variable to test: ")
top_bin = raw_input("What to make the top bin: ")
upordown = raw_input("Look above or below cut? 0 for above, 1 for below: ")
cutmin = raw_input("Bottom of cut range: ")
cutmax = raw_input("Top of cut range: ")


#library of various cross sections
EWKminusweight = 20.25
EWKplusweight = 25.62
EWKZ2JetLLweight = 3.987
EWKZ2JetNuNuweight = 10.01
ggH125weight = 44.14
ggHWWweight = 1.001
St_antitopweight = 80.95
St_topweight = 136.02
tBar_twweight = 35.6
t_tWweight = 35.6
vbfH125weight = 3.782
vbfhWWweight = 0.0858
TTweight = 831.76
WJetsHT200weight = 1345.0
WJetsHT400weight = 359.7
WJetsHT600weight = 48.91
WJetsHT800weight = 12.04
WJetsHT1200weight = 5.52
WJetsHT2500weight = 1.33
WJetsHTInfweight = 0.0322
WJetsMLMweight = 50380.0
WWTo1Lweight = 49.997
WWWweight = 0.2086
WWZweight = 0.1651
WZTo1L1Nu2Qweight = 10.71
WZTo1L3Nuweight = 3.05
WZTo2L2Qweight = 5.595
WZZweight = 0.05565
ZH125weight = 0.884




def getweight(filename):
  if filename.startswith("EWKminus"):
    print ("Weight match found! for: "+str(filename))
    return EWKminusweight
  if filename.startswith("EWKplus"):
    print ("Weight match found! for: "+str(filename))
    return EWKplusweight
  if filename.startswith("EWKZ2JetLL"):
    print ("Weight match found! for: "+str(filename))
    return EWKZ2JetLLweight
  if filename.startswith("EWKZ2JetNuNu"):
    print ("Weight match found! for: "+str(filename))
    return EWKZ2JetNuNuweight
  if filename.startswith("ggH125"):
    print ("Weight match found! for: "+str(filename))
    return ggH125weight
  if filename.startswith("ggHWW"):
    print ("Weight match found! for: "+str(filename))
    return ggHWWweight
  if filename.startswith("St_antitop"):
    print ("Weight match found! for: "+str(filename))
    return St_antitopweight
  if filename.startswith("St_top"):
    print ("Weight match found! for: "+str(filename))
    return St_topweight
  if filename.startswith("tBar_tW"):
    print ("Weight match found! for: "+str(filename))
    return tBar_twweight
  if filename.startswith("t_tW"):
    print ("Weight match found! for: "+str(filename))
    return t_tWweight
  if filename.startswith("vbfH125"):
    print ("Weight match found! for: "+str(filename))
    return vbfH125weight
  if filename.startswith("vbfHWW"):
    print ("Weight match found! for: "+str(filename))
    return vbfhWWweight
  if filename.startswith("TT"):
    print ("Weight match found! for: "+str(filename))
    return TTweight
  if filename.startswith("WJetsHT200"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHT200weight
  if filename.startswith("WJetsHT400"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHT400weight
  if filename.startswith("WJetsHT600"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHT600weight
  if filename.startswith("WJetsHT800"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHT800weight
  if filename.startswith("WJetsHT1200"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHT1200weight
  if filename.startswith("WJetsHT2500"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHT2500weight
  if filename.startswith("WJetsHTInf"):
    print ("Weight match found! for: "+str(filename))
    return WJetsHTInfweight
  if filename.startswith("WJetsMLM"):
    print ("Weight match found! for: "+str(filename))
    return WJetsMLMweight
  if filename.startswith("WWTo1L"):
    print ("Weight match found! for: "+str(filename))
    return WWTo1Lweight
  if filename.startswith("WWW"):
    print ("Weight match found! for: "+str(filename))
    return WWWweight
  if filename.startswith("WWZ"):
    print ("Weight match found! for: "+str(filename))
    return WWZweight
  if filename.startswith("WZTo1L1Nu2Q"):
    print ("Weight match found! for: "+str(filename))
    return WZTo1L1Nu2Qweight
  if filename.startswith("WZTo1L3Nu"):
    print ("Weight match found! for: "+str(filename))
    return WZTo1L3Nuweight
  if filename.startswith("WZTo2L2Q"):
    print ("Weight match found! for: "+str(filename))
    return WZTo2L2Qweight
  if filename.startswith("WZZ"):
    print ("Weight match found! for: "+str(filename))
    return WZZweight
  if filename.startswith("ZH125"):
    print ("Weight match found! for: "+str(filename))
    return ZH125weight
  else:
    print ("No weight match found for: "+str(filename))
    return 0
  




#functions that test the pre-cuts events must pass
def premutaucuts(event):
  if event.dR<1.5 and event.met>100 and event.pt_1>1 and event.pt_2>20 and event.npv>0 and event.charge==0 and event.diLeptons==0 and event.iso04_1<0.15 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True
# and  

def preeletaucuts(event):
  if event.dR<1.5 and event.met>100 and event.pt_1>1 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True

def preditaucuts(event):
  if event.dR<1.5 and event.met>100 and event.pt_1>1 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
    return True


#function that creates the 6 necesary histograms, and then returns the desired
#values
def makehistos(name):
  mutauhisto = ROOT.TH1F(name+"mutau","",200,0,float(top_bin))
  mutaufullhisto = ROOT.TH1F(name+"mutaufull","",200,0,float(top_bin))
  eletauhisto = ROOT.TH1F(name+"eletau","",200,0,float(top_bin))
  eletaufullhisto = ROOT.TH1F(name+"eletaufull","",200,0,float(top_bin))
  ditauhisto = ROOT.TH1F(name+"ditau","",200,0,float(top_bin))
  ditaufullhisto = ROOT.TH1F(name+"ditaufull","",200,0,float(top_bin))

#fills the created histograms
  ntuple_file = ROOT.TFile(name)
  tree = ntuple_file.Get("muTauEventTree/eventTree")
  for event in tree:
    g = getattr(event, cutvar)
    mutaufullhisto.Fill(g)
    if premutaucuts(event):
      mutauhisto.Fill(g)
  ntuple_file = ROOT.TFile(name)
  tree = ntuple_file.Get("eleTauEventTree/eventTree")
  for event in tree:
    g = getattr(event, cutvar)
    eletaufullhisto.Fill(g)
    if preeletaucuts(event):
      eletauhisto.Fill(g)
  ntuple_file = ROOT.TFile(name)
  tree = ntuple_file.Get("diTauEventTree/eventTree")
  for event in tree:
    g = getattr(event, cutvar)
    ditaufullhisto.Fill(g)
    if preditaucuts(event):
      ditauhisto.Fill(g)
  return mutauhisto, mutaufullhisto, eletauhisto, eletaufullhisto, ditauhisto, ditaufullhisto


def integrate_histos(cut, mutauhisto, mutaufullhisto, eletauhisto, eletaufullhisto, ditauhisto, ditaufullhisto):
  mutotcounter = 0
  mueventcounter = 0
  eletotcounter = 0
  eleeventcounter = 0
  ditotcounter = 0
  dieventcounter = 0
  
 #finds passed events over total events for muTau
  mutotcounter = mutaufullhisto.Integral()
  if upordown == "0":
    mueventcounter = mutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    mueventcounter = mutaihisto.Integral(0, int(cut))
  mutauratio = mueventcounter/mutotcounter

#finds passed events over total events for eleTau
  eletotcounter = eletaufullhisto.Integral()
  if upordown == "0":
    eleeventcounter = eletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eleeventcounter = eletauhisto.Integral(0, int(cut))
  eletauratio = eleeventcounter/eletotcounter

#finds passed events over total events for diTau
  ditotcounter = ditaufullhisto.Integral()
  if upordown == "0":
    dieventcounter = ditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    dieventcounter = ditauhisto.Integral(0, int(cut))
  ditauratio = dieventcounter/ditotcounter

#return a tuple of the values we're looking for
  return (mutauratio, eletauratio, ditauratio)

  

#helps with the cut cycling
cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/10
differ = float(diff)
backgroundmu = [0,0,0,0,0,0,0,0,0,0]
backgroundele = [0,0,0,0,0,0,0,0,0,0]
backgrounddi = [0,0,0,0,0,0,0,0,0,0]
signalmu = [0,0,0,0,0,0,0,0,0,0]
signalele = [0,0,0,0,0,0,0,0,0,0]
signaldi = [0,0,0,0,0,0,0,0,0,0]


directory = "/nfs_scratch/tost/monohiggs_May26Save"

#cycles through all the files in the directory. Inside this loop, it goes through all the cuts for 
#backgrounds, and pulls itegrals from the created histograms. Stores values in a list.
for filename in os.listdir(directory):
  if filename.endswith(".root") and filename!=signalfile:
    fullfilename = os.path.join(directory, filename)
    weight = getweight(str(filename))
    if weight == 0:
      continue
    mutauhisto, mutaufullhisto, eletauhisto, eletaufullhisto, ditauhisto, ditaufullhisto = makehistos(str(fullfilename))
    i = 0
    cut = float(cutmin)
    while cut<float(cutmax)+(differ/2):
      if i > 9:
	break
      cut_bin = cut/(float(top_bin)/200)
      backmutau, backeletau, backditau = integrate_histos(cut_bin, mutauhisto, mutaufullhisto, eletauhisto, eletaufullhisto, ditauhisto, ditaufullhisto)
      backgroundmu[i] = backgroundmu[i] + weight*backmutau
      backgroundele[i] = backgroundele[i] + weight*backeletau
      backgrounddi[i] = backgrounddi[i] + weight*backditau
      cut = cut + differ
      i = i + 1

#this does the same as the loop above but for the signal
cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/10
differ = float(diff)
j=0
while cut<float(cutmax)+(differ/2):
  if j > 9:
    break
  makehistos(signalfile)
  cut_bin = cut/(float(top_bin)/200)
  sigmu, sigele, sigdi = integrate_histos(cut_bin, mutauhisto, mutaufullhisto, eletauhisto, eletaufullhisto, ditauhisto, ditaufullhisto)
  signalmu[j] = signalmu[j] + sigmu
  signalele[j] = signalele[j] + sigele
  signaldi[j] = signaldi[j] + sigdi
  cut = cut + differ
  j = j+1


### All these functions just do the s/sqrt(s+b) math and print it out one by   ####
cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/10
differ = float(diff)
k=0
print "\n\nMUTAU:"
while cut<float(cutmax)+(differ/2):
  if k > 9:
    break
  if upordown=="0":
    print str(cutvar)+">"+str(cut)+str(signalmu[k]/math.sqrt(signalmu[k]+backgroundmu[k]))
  if upordown=="1":
    print str(cutvar)+"<"+str(cut)+str(signalmu[k]/math.sqrt(signalmu[k]+backgroundmu[k]))
  cut = cut + differ
  k = k+1



cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/10
differ = float(diff)
k=0
print "\n\nELETAU:"
while cut<float(cutmax)+(differ/2):
  if k > 9:
    break
  if upordown=="0":
    print str(cutvar)+">"+str(cut)+str(signalele[k]/math.sqrt(signalele[k]+backgroundele[k]))
  if upordown=="1":
    print str(cutvar)+"<"+str(cut)+str(signalele[k]/math.sqrt(signalele[k]+backgroundele[k]))
  cut = cut+differ
  k=k+1


cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/10
differ = float(diff)
k=0
print "\n\nDITAU:"
while cut<float(cutmax)+(differ/2):
  if k > 9:
    break
  if upordown=="0":
    print str(cutvar)+">"+str(cut)+str(signaldi[k]/math.sqrt(signaldi[k]+backgrounddi[k]))
  if upordown=="1":
    print str(cutvar)+"<"+str(cut)+str(signaldi[k]/math.sqrt(signaldi[k]+backgrounddi[k]))
  cut = cut+differ
  k=k+1



##### TODO: 
  #figure out a semi-elegant way to pull weights for each file
  #print everything neatly. Keep an eye on logic flow, with the cut cycling


