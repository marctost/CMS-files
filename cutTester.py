import ROOT
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
import sys
import math

ROOT.gROOT.SetBatch(True)
cutvar = argv[1]
top_bin = argv[2]
upordown = argv[3]
cutmin = argv[4]
cutmax = argv[5]

###################Set all weights and file names for processes##########################

signalfile = "/hdfs/store/user/tost/aug13data/ZpBaryonic_Zp1000_MChi150.root"
ZJetsfile = "/hdfs/store/user/tost/aug13data/ZJETS.root"
WJetsfile= "/hdfs/store/user/tost/aug13data/WJETS.root"
Dibosonfile = "/hdfs/store/user/tost/aug13data/DiBoson.root"
smHfile = "/hdfs/store/user/tost/aug13data/smH125.root"
Znunufile = "/hdfs/store/user/tost/aug13data/Znunu.root"
######################################################################################




#######################pre cuts##########################################

def premutaucuts(event):
  if event.dR<1.7 and event.m_vis<125 and event.met>150 and  event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True

def preeletaucuts(event):
  if event.dR<1.7 and event.m_vis<125 and event.met>150 and event.pt_1>26 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True

def preditaucuts(event):
  if event.dR<2.1 and event.m_vis<125 and event.met>160 and event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
    return True

#########################################################################

signalmutauhisto = ROOT.TH1F("signalmutauhisto","",200,0,float(top_bin))
signaleletauhisto = ROOT.TH1F("signaleletauhisto","",200,0,float(top_bin))
signalditauhisto = ROOT.TH1F("signalditauhisto","",200,0,float(top_bin))

ZJetsmutauhisto = ROOT.TH1F("ZJetsmutauhisto","",200, 0,float(top_bin))
ZJetseletauhisto = ROOT.TH1F("ZJetseletauhisto","",200,0,float(top_bin))
ZJetsditauhisto = ROOT.TH1F("ZJetsditauhisto","",200,0,float(top_bin))

Wjetsmutauhisto = ROOT.TH1F("Wjetsmutauhisto","",200,0,float(top_bin))
Wjetseletauhisto = ROOT.TH1F("Wjetseletauhisto","",200,0,float(top_bin))
Wjetsditauhisto = ROOT.TH1F("Wjetsditauhisto","",200,0,float(top_bin))

Dibosonmutauhisto = ROOT.TH1F("Dibosonmutauhisto","",200,0,float(top_bin))
Dibosoneletauhisto = ROOT.TH1F("Dibosoneletauhisto","",200,0,float(top_bin))
Dibosonditauhisto = ROOT.TH1F("Dibosonditauhisto","",200,0,float(top_bin))

smHmutauhisto = ROOT.TH1F("smHmutauhisto","",200,0,float(top_bin))
smHeletauhisto = ROOT.TH1F("smHeletauhisto","",200,0,float(top_bin))
smHditauhisto = ROOT.TH1F("smHditauhisto","",200,0,float(top_bin))

Znunumutauhisto = ROOT.TH1F("Znunumutauhisto","",200,0,float(top_bin))
Znunueletauhisto = ROOT.TH1F("Znunueletauhisto","",200,0,float(top_bin))
Znunuditauhisto = ROOT.TH1F("Znunuditauhisto","",200,0,float(top_bin))

###########################################################

print "Creating signal histos"
ntuple_file = ROOT.TFile(signalfile)
tree = ntuple_file.Get("muTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if premutaucuts(event):
    signalmutauhisto.Fill(g, weight*0.03589)
tree = ntuple_file.Get("eleTauEventTree/eventTree")
for event in tree:
  g= getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preeletaucuts(event):
    signaleletauhisto.Fill(g, weight*0.03589)
tree = ntuple_file.Get("diTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preditaucuts(event):
    signalditauhisto.Fill(g, weight*0.03589)

n=1
print "Creating Z+Jets histos"
ntuple_file = ROOT.TFile(ZJetsfile)
tree = ntuple_file.Get("muTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if premutaucuts(event):
    ZJetsmutauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("eleTauEventTree/eventTree")
for event in tree:
  g= getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preeletaucuts(event):
    ZJetseletauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("diTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preditaucuts(event):
    ZJetsditauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1

n=1
print "Creating W+Jets histos"
ntuple_file = ROOT.TFile(WJetsfile)
tree = ntuple_file.Get("muTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if premutaucuts(event):
    Wjetsmutauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("eleTauEventTree/eventTree")
for event in tree:
  g= getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preeletaucuts(event):
    Wjetseletauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("diTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preditaucuts(event):
    Wjetsditauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1

n=1
print "Creating Diboson histos"
ntuple_file = ROOT.TFile(Dibosonfile)
tree = ntuple_file.Get("muTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if premutaucuts(event):
    Dibosonmutauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("eleTauEventTree/eventTree")
for event in tree:
  g= getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preeletaucuts(event):
    Dibosoneletauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("diTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preditaucuts(event):
    Dibosonditauhisto.Fill(g, weight*0.03589)
  if n%10000==0:
    print n
  n=n+1

n=1
print "Creating smH histos"
ntuple_file = ROOT.TFile(smHfile)
tree = ntuple_file.Get("muTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if premutaucuts(event):
    smHmutauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("eleTauEventTree/eventTree")
for event in tree:
  g= getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preeletaucuts(event):
    smHeletauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("diTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preditaucuts(event):
    smHditauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1

n=1
print "Creating Znunu histos"
ntuple_file = ROOT.TFile(Znunufile)
tree = ntuple_file.Get("muTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if premutaucuts(event):
    Znunumutauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("eleTauEventTree/eventTree")
for event in tree:
  g= getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preeletaucuts(event):
    Znunueletauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1
tree = ntuple_file.Get("diTauEventTree/eventTree")
for event in tree:
  g = getattr(event, cutvar)
  weight = getattr(event, "__WEIGHT__")
  if preditaucuts(event):
    Znunuditauhisto.Fill(g, weight*0.03589)
  if n%100000==0:
    print n
  n=n+1

##############################################################


def signalmutau(cut):
  totcounter =0
  eventcounter=0
  if upordown == "0":
    eventcounter = signalmutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = signalmutauhisto.Integral(0, int(cut))
  return float(eventcounter)
def signaleletau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = signaleletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = signaleletauhisto.Integral(0, int(cut))
  return float(eventcounter)
def signalditau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = signalditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = signalditauhisto.Integral(0, int(cut))
  return float(eventcounter)


def Zjetsmutau(cut):
  totcounter =0
  eventcounter=0
  if upordown == "0":
    eventcounter = ZJetsmutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = ZJetsmutauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Zjetseletau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = ZJetseletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = ZJetseletauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Zjetsditau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = ZJetsditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = ZJetsditauhisto.Integral(0, int(cut))
  return float(eventcounter)


def Wjetsmutau(cut):
  totcounter =0
  eventcounter=0
  if upordown == "0":
    eventcounter = Wjetsmutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Wjetsmutauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Wjetseletau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = Wjetseletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Wjetseletauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Wjetsditau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = Wjetsditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Wjetsditauhisto.Integral(0, int(cut))
  return float(eventcounter)


def Dibosonmutau(cut):
  totcounter =0
  eventcounter=0
  if upordown == "0":
    eventcounter = Dibosonmutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Dibosonmutauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Dibosoneletau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = Dibosoneletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Dibosoneletauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Dibosonditau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = Dibosonditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Dibosonditauhisto.Integral(0, int(cut))
  return float(eventcounter)


def smHmutau(cut):
  totcounter =0
  eventcounter=0
  if upordown == "0":
    eventcounter = smHmutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = smHmutauhisto.Integral(0, int(cut))
  return float(eventcounter)
def smHeletau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = smHeletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = smHeletauhisto.Integral(0, int(cut))
  return float(eventcounter)
def smHditau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = smHditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = smHditauhisto.Integral(0, int(cut))
  return float(eventcounter)


def Znunumutau(cut):
  totcounter =0
  eventcounter=0
  if upordown == "0":
    eventcounter = Znunumutauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Znunumutauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Znunueletau(cut):
  totcounter = 0
  eventcounter = 0

  if upordown == "0":
    eventcounter = Znunueletauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Znunueletauhisto.Integral(0, int(cut))
  return float(eventcounter)
def Znunuditau(cut):
  totcounter = 0
  eventcounter = 0
  if upordown == "0":
    eventcounter = Znunuditauhisto.Integral(int(cut), 200)
  if upordown == "1":
    eventcounter = Znunuditauhisto.Integral(0, int(cut))
  return float(eventcounter)

##################################################################################


cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/20
differ = float(diff)

print "\n\nMUTAU:"
while cut<float(cutmax)+1:
  cut_bin = cut/(float(top_bin)/200)
  signal = signalmutau(cut_bin)
  ZJets = Zjetsmutau(cut_bin)
  WJets = Wjetsmutau(cut_bin)
  Diboson = Dibosonmutau(cut_bin)
  smH = smHmutau(cut_bin)
  Znunu = Znunumutau(cut_bin)
  totbackground = ZJets+WJets+Diboson+smH+Znunu
  if upordown=="0":
    print cutvar+">"+str(cut)+":  "+str(signal/math.sqrt(totbackground+signal))
  if upordown=="1":
    if (totbackground==0 or signal==0):
      print "error"
    if (totbackground!=0 and signal!=0):
      print cutvar+"<"+str(cut)+":  "+str(signal/math.sqrt(totbackground+signal))
  cut = cut + differ

cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/20
differ = float(diff)

print "\n\nELETAU:"
cut = float(cutmin)
while cut<float(cutmax)+1:
  cut_bin = cut/(float(top_bin)/200)
  signal = signaleletau(cut_bin)
  ZJets = Zjetseletau(cut_bin)
  WJets = Wjetseletau(cut_bin)
  Diboson = Dibosoneletau(cut_bin)
  smH = smHeletau(cut_bin)
  Znunu = Znunueletau(cut_bin)
  totbackground = ZJets+WJets+Diboson+smH+Znunu
  if upordown=="0":
    print cutvar+">"+str(cut)+":  "+str(signal/math.sqrt(totbackground+signal))
  if upordown=="1":
    if (totbackground==0 or signal==0):
      print "error"
    if (totbackground!=0 and signal!=0):
      print cutvar+"<"+str(cut)+":  "+str(signal/math.sqrt(totbackground+signal))
  cut = cut + differ

cut = float(cutmin)
diff = (float(cutmax)-float(cutmin))/20
differ = float(diff)

print "\n\nDITAU:"
cut = float(cutmin)
while cut<float(cutmax)+1:
  cut_bin = cut/(float(top_bin)/200)
  signal = signalditau(cut_bin)
  ZJets = Zjetsditau(cut_bin)
  WJets = Wjetsditau(cut_bin)
  Diboson = Dibosonditau(cut_bin)
  smH = smHditau(cut_bin)
  Znunu = Znunuditau(cut_bin)
  totbackground = ZJets+WJets+Diboson+smH+Znunu
  if upordown=="0":
    print cutvar+">"+str(cut)+":  "+str(signal/math.sqrt(totbackground+signal))
  if upordown=="1":
    if (totbackground==0 or signal==0):
      print "error"
    if (totbackground!=0 and signal!=0):
      print cutvar+"<"+str(cut)+":  "+str(signal/math.sqrt(totbackground+signal))
  cut = cut + differ
