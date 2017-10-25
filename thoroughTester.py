import ROOT
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr
import math

ROOT.gROOT.SetBatch(True)
signalfile = argv[1]

###################Set all weights and file names for processes##########################
monoHweight = 1
ggHweight = 3.04597
vbfHweight = 0.2371314
ZHweight = 0.05542053
ZJetsweight = 5765.4
WJetsweight = 61526.7
WWweight = 12.178

ggHfile = "/hdfs/store/user/ldodd/crab_MONOHTT_PLAYPEN/Jun13_submission_v1/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GluGluHToTauTau_M125_13TeV_powheg_pythia8/crab_MONOHTT_PLAYPEN_Mar17_v1_GluGluHToTauTau_M125_13TeV_powheg_pythia8/170613_152437/0000/analysis_1.root"
vbfHfile = "/hdfs/store/user/ldodd/crab_MONOHTT_PLAYPEN/Jun13_submission_v1/VBFHToTauTau_M125_13TeV_powheg_pythia8/VBFHToTauTau_M125_13TeV_powheg_pythia8/crab_MONOHTT_PLAYPEN_Mar17_v1_VBFHToTauTau_M125_13TeV_powheg_pythia8/170613_152511/0000/analysis_1.root"
ZHfile = "/hdfs/store/user/ldodd/crab_MONOHTT_PLAYPEN/Jun13_submission_v1/ZHToTauTau_M125_13TeV_powheg_pythia8/ZHToTauTau_M125_13TeV_powheg_pythia8/crab_MONOHTT_PLAYPEN_Mar17_v1_ZHToTauTau_M125_13TeV_powheg_pythia8/170613_152542/0000/analysis_1.root"
ZJetsfile = "/nfs_scratch/laura/monohiggs_June28/ZJets_ext.root"
WJetsfile= "/nfs_scratch/laura/monohiggs_June28/WJetsMLM.root"
WWfile = "/nfs_scratch/laura/monohiggs_June28/WWTo2L2Nu.root"

######################################################################################




######################process and count the signal file found in input#############

def mutautester(infile):
  mutautotcounter = 0
  mutausinglecounter = 0
  direc = "muTauEventTree"
  ntuple_file = ROOT.TFile(infile)
  tree = ntuple_file.Get(direc+"/eventTree")
  for event in tree:
    mutautotcounter = mutautotcounter +1
    if mutaucuts(event)==True: 
      mutausinglecounter = mutausinglecounter +1
  return (float(mutausinglecounter)/float(mutautotcounter))

def eletautester(infile):
  eletautotcounter = 0
  eletausinglecounter = 0
  direc = "eleTauEventTree"
  ntuple_file = ROOT.TFile(infile)
  tree = ntuple_file.Get(direc+"/eventTree")
  for event in tree:
    eletautotcounter = eletautotcounter +1
    if eletaucuts(event)==True:
      eletausinglecounter = eletausinglecounter +1
  return (float(eletausinglecounter)/float(eletautotcounter))

def ditautester(infile):
  ditautotcounter =0
  ditausinglecounter = 0
  direc = "diTauEventTree"
  ntuple_file = ROOT.TFile(infile)
  tree = ntuple_file.Get(direc+"/eventTree")
  for event in tree:
    ditautotcounter = ditautotcounter +1
    if ditaucuts(event)==True:
      ditausinglecounter = ditausinglecounter+1
  return (float(ditausinglecounter)/float(ditautotcounter))


##################################################################################




###################################center for cuts#####################################
def mutaucuts(event):
  if event.pth>50 and event.dR<2.5 and event.met>90 and event.pt_1>40 and event.pt_2>45 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True
  else:
    return False

def eletaucuts(event):
  if event.pth>50 and event.dR<2.5 and event.met>90 and event.pt_1>40 and event.pt_2>50 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    return True
  else:
    return False

def ditaucuts(event):
  if event.pth>50 and event.dR<2.5 and event.met>90 and event.pt_1>50 and event.pt_2>50 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
    return True
  else:
    return False

# event.pth>45 and event.dR<2.5 and event.met>50 and 


###########################Where the magic happens###################################

print "analysing signal"
signalmutau = mutautester(signalfile)
signaleletau = eletautester(signalfile)
signalditau = ditautester(signalfile)
print signalmutau

print "anaylsing ggH"
ggHbackmutau = ggHweight*mutautester(ggHfile)
ggHbackeletau = ggHweight*eletautester(ggHfile)
ggHbackditau = ggHweight*ditautester(ggHfile)
print ggHbackmutau

print "analysing vbfH"
vbfHbackmutau = vbfHweight*mutautester(vbfHfile)
vbfHbackeletau = vbfHweight*eletautester(vbfHfile)
vbfHbackditau = vbfHweight*ditautester(vbfHfile)

print "analysing ZH"
ZHbackmutau = ZHweight*mutautester(ZHfile)
ZHbackeletau = ZHweight*eletautester(ZHfile)
ZHbackditau = ZHweight*ditautester(ZHfile)

print "analysing ZJets"
ZJetsbackmutau = ZJetsweight*mutautester(ZJetsfile)
ZJetsbackeletau = ZJetsweight*eletautester(ZJetsfile)
ZJetsbackditau = ZJetsweight*ditautester(ZJetsfile)

print "analysing WJets"
WJetsbackmutau = WJetsweight*mutautester(WJetsfile)
WJetsbackeletau = WJetsweight*eletautester(WJetsfile)
WJetsbackditau = WJetsweight*ditautester(WJetsfile)

print "analysing WW"
WWbackmutau = WWweight*mutautester(WWfile)
WWbackeletau = WWweight*eletautester(WWfile)
WWbackditau = WWweight*ditautester(WWfile)

totalbackgroundmutau = ggHbackmutau+vbfHbackmutau+ZHbackmutau+ZJetsbackmutau+WJetsbackmutau+WWbackmutau
totalbackgroundeletau = ggHbackeletau+vbfHbackeletau+ZHbackeletau+ZJetsbackeletau+WJetsbackeletau+WWbackeletau
totalbackgroundditau = ggHbackditau+vbfHbackditau+ZHbackditau+ZJetsbackditau+WJetsbackditau+WWbackditau

magicnumbermutau = signalmutau/math.sqrt(totalbackgroundmutau)
magicnumbereletau = signaleletau/math.sqrt(totalbackgroundeletau)
magicnumberditau = signalditau/math.sqrt(totalbackgroundditau)

print "Mutau S/sqrt(B) is: "
print magicnumbermutau
print "\nEletau S/sqrt(B) is: "
print magicnumbereletau
print "\nDitau S/sqrt(B) is: "
print magicnumberditau


###################################################################################


