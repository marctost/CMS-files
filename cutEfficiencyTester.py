import ROOT
import array
from subprocess import Popen
from sys import argv, exit, stdout, stderr

ROOT.gROOT.SetBatch(True)

infile = argv[1]
mutautotcounter = 0
mutausinglecounter = 0
eletautotcounter = 0
eletausinglecounter = 0
ditautotcounter =0
ditausinglecounter = 0



direc = "muTauEventTree"
#print 'Evaluating file '+infile+' under tree '+direc+'\n'
ntuple_file = ROOT.TFile(infile)
tree = ntuple_file.Get(direc+"/eventTree")
for event in tree:
  mutautotcounter = mutautotcounter +1
  if event.pth>45 and event.dR<2.5 and event.met>50 and event.pt_1>26 and event.pt_2>20 and event.npv>0 and event.diLeptons==0 and event.charge==0 and event.againstElectronVLooseMVA6_2 > 0 and event.againstMuonTight3_2>0 and event.iso04_1<0.15 and (event.HLT_IsoMu24_v_fired>0 or event.HLT_IsoTkMu24_v_fired>0) and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    mutausinglecounter = mutausinglecounter +1
print mutautotcounter
print mutausinglecounter
mutauratio = (float(mutausinglecounter)/float(mutautotcounter))*100
   


direc = "eleTauEventTree"
print 'Evaluating file '+infile+' under tree '+direc+'\n'
ntuple_file = ROOT.TFile(infile)
tree = ntuple_file.Get(direc+"/eventTree")
for event in tree:
  eletautotcounter = eletautotcounter +1
  if event.pth>45 and event.dR<2.5 and event.met>50 and event.pt_1>27 and event.pt_2>20 and event.vertices>0 and event.dilepton_veto==0 and event.iso_1<0.1 and event.tightElectrons<=1 and event.tightMuons==0 and event.charge==0 and event.againstElectronTightMVA6_2 > 0 and event.againstMuonLoose3_2>0 and event.HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0 and event.byTightIsolationMVArun2v1DBoldDMwLT_2>0:
    eletausinglecounter = eletausinglecounter +1
eletauratio = (float(eletausinglecounter)/float(eletautotcounter))*100
# 



direc = "diTauEventTree"
print 'Evaluating file '+infile+' under tree '+direc+'\n'
ntuple_file = ROOT.TFile(infile)
tree = ntuple_file.Get(direc+"/eventTree")
for event in tree:
  ditautotcounter = ditautotcounter +1
  if  event.pth>45 and event.dR<2.5 and event.met>50 and event.pt_1>40 and event.pt_2>40 and event.npv>0 and event.tightMuons==0 and event.tightElectrons==0 and event.againstMuonLoose3_1>0 and event.againstElectronVLooseMVA6_1>0 and event.againstElectronVLooseMVA6_2>0 and event.charge==0 and (event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0 or event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0):
    ditausinglecounter = ditausinglecounter+1
ditauratio = (float(ditausinglecounter)/float(ditautotcounter))*100



print "RESULTS: \n"
print "muTau total events: "+str(mutautotcounter)+"  muTau events after cut: "+str(mutausinglecounter)+"    Percent kept: "+str(mutauratio)+"\n"
print "eleTau total events: "+str(eletautotcounter)+"  eleTau events after cut: "+str(eletausinglecounter)+"    Percent kept: "+str(eletauratio)+"\n"
print "diTau total events: "+str(ditautotcounter)+"  diTau events after cut: "+str(ditausinglecounter)+"    Percent kept: "+str(ditauratio)+"\n"







