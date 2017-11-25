import ROOT
from sys import argv, exit, stdout, stderr
import math

ROOT.gROOT.SetBatch(True)

#get basic input that helps make the histograms                                                                
variable = argv[1]
topbin = argv[2]
bottombin = argv[3]
binnumber = argv[4]
channel = argv[5]

#where all the cuts and weights are inputted

#mu: met>150, pth>120, dR<1.7
#e: met>150, pth>120, dR<1.7
#di: met>160, pth>120, dR<2.1
                                                                          
if channel == "mu":
	selectioncuts = "m_vis<125&&pt_1>26&&pt_2>20&&npv>0&&diLeptons==0&&charge==0&&againstElectronVLooseMVA6_2>0&&againstMuonTight3_2>0&&iso04_1<0.15&&(HLT_IsoMu24_v_fired>0||HLT_IsoTkMu24_v_fired>0)&&byTightIsolationMVArun2v1DBoldDMwLT_2>0&&BadMuonFilter==1&&Flag_HBHENoiseFilter_fired==1&&Flag_HBHENoiseIsoFilter_fired==1&&Flag_goodVertices_fired==1&&Flag_EcalDeadCellTriggerPrimitiveFilter_fired==1&&EffCSVWeight0==1"
	weight = "__WEIGHT__*GENWEIGHT*puweight*POGid1*POGtrigger*TAUID1*trackweight*35870"
	QCDcuts = "m_vis<125&&pt_1>26&&pt_2>20&&npv>0&&diLeptons==0&&charge!=0&&againstElectronVLooseMVA6_2>0&&againstMuonTight3_2>0&&iso04_1<0.15&&(HLT_IsoMu24_v_fired>0||HLT_IsoTkMu24_v_fired>0)&&byTightIsolationMVArun2v1DBoldDMwLT_2>0&&BadMuonFilter==1&&Flag_HBHENoiseFilter_fired==1&&Flag_HBHENoiseIsoFilter_fired==1&&Flag_goodVertices_fired==1&&Flag_EcalDeadCellTriggerPrimitiveFilter_fired==1&&EffCSVWeight0==1"

elif channel == "e":
	selectioncuts = "m_vis<125&&pt_1>26&&pt_2>20&&vertices>0&&dilepton_veto==0&&iso_1<0.1&&tightElectrons<=1&&tightMuons==0&&charge==0&&againstElectronTightMVA6_2>0&&againstMuonLoose3_2>0&&HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0&&byTightIsolationMVArun2v1DBoldDMwLT_2>0&&BadMuonFilter==1&&Flag_HBHENoiseFilter_fired==1&&Flag_HBHENoiseIsoFilter_fired==1&&Flag_globalTightHalo2016Filter_fired==1&&Flag_goodVertices_fired==1&&Flag_EcalDeadCellTriggerPrimitiveFilter_fired==1&&EffCSVWeight0==1"
	weight = "__WEIGHT__*GENWEIGHT*puweight*TAUID1*idisoweight_REDO*trackweight*35870"
	QCDcuts = "m_vis<125&&pt_1>26&&pt_2>20&&vertices>0&&dilepton_veto==0&&iso_1<0.1&&tightElectrons<=1&&tightMuons==0&&charge!=0&&againstElectronTightMVA6_2>0&&againstMuonLoose3_2>0&&HLT_Ele25_eta2p1_WPTight_Gsf_v_fired>0&&byTightIsolationMVArun2v1DBoldDMwLT_2>0&&BadMuonFilter==1&&Flag_HBHENoiseFilter_fired==1&&Flag_HBHENoiseIsoFilter_fired==1&&Flag_globalTightHalo2016Filter_fired==1&&Flag_goodVertices_fired==1&&Flag_EcalDeadCellTriggerPrimitiveFilter_fired==1&&EffCSVWeight0==1"

elif channel =="di":
	selectioncuts = "m_vis<125&&pt_1>55&&pt_2>40&&npv>0&&tightMuons==0&&tightElectrons==0&&againstMuonLoose3_1>0&&againstElectronVLooseMVA6_1>0&&againstElectronVLooseMVA6_2>0&&charge==0&&(HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0||HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0)"
	weight = "__WEIGHT__*GENWEIGHT*puweight*trigweight_REDO*TAUID1*35870"
	QCDcuts = "m_vis<125&&pt_1>55&&pt_2>40&&npv>0&&tightMuons==0&&tightElectrons==0&&againstMuonLoose3_1>0&&againstElectronVLooseMVA6_1>0&&againstElectronVLooseMVA6_2>0&&charge!=0&&(HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0||HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v_fired>0)"


cuts = "("+selectioncuts+")*"+weight
datacuts = "("+selectioncuts+")*1"

#Defines all the files needed to make the histograms                                                           
signalfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/ZpBaryonic_Zp1000_MChi150.root")
smhfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/smH125.root")
dibosonfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/DiBosonAll.root")
wjetsfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/WJETS.root")
znunufile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/Znunu.root")
zjetsfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/ZJETS.root")
ttfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/TT.root")
datafilemu = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/muDATA.root")
datafilee = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/eleDATA.root")
datafiledi = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/tauDATA.root")

#Define trees for background, signal and data
if channel == "mu":
    signaltree = signalfile.Get("muTauEventTree/eventTree")
    smhtree = smhfile.Get("muTauEventTree/eventTree")
    dibosontree = dibosonfile.Get("muTauEventTree/eventTree")
    wjetstree = wjetsfile.Get("muTauEventTree/eventTree")
    znunutree = znunufile.Get("muTauEventTree/eventTree")
    zjetstree = zjetsfile.Get("muTauEventTree/eventTree")
    tttree = ttfile.Get("muTauEventTree/eventTree")
    datatree = datafilemu.Get("muTauEventTree/eventTree")
elif channel == "e":
    signaltree = signalfile.Get("eleTauEventTree/eventTree")
    smhtree = smhfile.Get("eleTauEventTree/eventTree")
    dibosontree = dibosonfile.Get("eleTauEventTree/eventTree")
    wjetstree = wjetsfile.Get("eleTauEventTree/eventTree")
    znunutree = znunufile.Get("eleTauEventTree/eventTree")
    zjetstree = zjetsfile.Get("eleTauEventTree/eventTree")
    tttree = ttfile.Get("eleTauEventTree/eventTree")
    datatree = datafilee.Get("eleTauEventTree/eventTree")
elif channel == "di":
    signaltree = signalfile.Get("diTauEventTree/eventTree")
    smhtree = smhfile.Get("diTauEventTree/eventTree")
    dibosontree = dibosonfile.Get("diTauEventTree/eventTree")
    wjetstree = wjetsfile.Get("diTauEventTree/eventTree")
    znunutree = znunufile.Get("diTauEventTree/eventTree")
    zjetstree = zjetsfile.Get("diTauEventTree/eventTree")
    tttree = ttfile.Get("diTauEventTree/eventTree")
    datatree = datafiledi.Get("diTauEventTree/eventTree")



#Define all the histograms you are gonna put shit in                                                           
sig = ROOT.TH1F("signal", "signal", int(binnumber), float(bottombin), float(topbin))
smh = ROOT.TH1F("smh", "smH", int(binnumber), float(bottombin), float(topbin))
dibos = ROOT.TH1F("diboson", "diboson", int(binnumber), float(bottombin), float(topbin))
wjet = ROOT.TH1F("wjets","wjets", int(binnumber), float(bottombin), float(topbin))
znu = ROOT.TH1F("znunu","znunu", int(binnumber), float(bottombin), float(topbin))
zjet = ROOT.TH1F("zjets","zjets", int(binnumber), float(bottombin), float(topbin))
tthist = ROOT.TH1F("tt", "tt", int(binnumber), float(bottombin), float(topbin))
dat = ROOT.TH1F("data","data", int(binnumber), float(bottombin), float(topbin))





##########     QCD same sign protocol! ###
QCD = ROOT.TH1F("QCD", "QCD", int(binnumber), float(bottombin), float(topbin))

smh_ss = ROOT.TH1F("smh_ss", "smH_ss", int(binnumber), float(bottombin), float(topbin))
dibos_ss = ROOT.TH1F("diboson_ss", "diboson_ss", int(binnumber), float(bottombin), float(topbin))
wjet_ss = ROOT.TH1F("wjets_ss","wjets_ss", int(binnumber), float(bottombin), float(topbin))
znu_ss = ROOT.TH1F("znunu_ss","znunu_ss", int(binnumber), float(bottombin), float(topbin))
zjet_ss = ROOT.TH1F("zjets_ss","zjets_ss", int(binnumber), float(bottombin), float(topbin))
tthist_ss = ROOT.TH1F("tt_ss", "tt_ss", int(binnumber), float(bottombin), float(topbin))

smhtree.Draw(variable+">>+smh_ss",QCDcuts)
dibosontree.Draw(variable+">>+diboson_ss",QCDcuts)
wjetstree.Draw(variable+">>+wjets_ss",QCDcuts)
znunutree.Draw(variable+">>+znunu_ss",QCDcuts)
zjetstree.Draw(variable+">>+zjets_ss",QCDcuts)
tttree.Draw(variable+">>+tt_ss",QCDcuts)
datatree.Draw(variable+">>+QCD",QCDcuts)

QCD.Add(smh_ss, -1)
QCD.Add(dibos_ss, -1)
QCD.Add(wjet_ss, -1)
QCD.Add(znu_ss, -1)
QCD.Add(zjet_ss, -1)
QCD.Add(tthist_ss, -1)


#Where the magic happens. Shove shit into the histograms                                                       
signaltree.Draw(variable+">>+signal",cuts)
smhtree.Draw(variable+">>+smh",cuts)
dibosontree.Draw(variable+">>+diboson",cuts)
wjetstree.Draw(variable+">>+wjets",cuts)
znunutree.Draw(variable+">>+znunu",cuts)
zjetstree.Draw(variable+">>+zjets",cuts)
tttree.Draw(variable+">>+tt",cuts)
datatree.Draw(variable+">>+data",datacuts)


#Make a spot to put all these histos                                                                           
outfile = ROOT.TFile("Histoshere.root","RECREATE")
outfile.mkdir("histosarehere")
outfile.cd("histosarehere")

#Now write all te histos to this file!                                                                         
sig.Write("Signal")
smh.Write("smH125")
dibos.Write("DiBosons")
wjet.Write("WJets")
znu.Write("Znunu")
zjet.Write("ZJets")
tthist.Write("TT")
dat.Write("Data")
QCD.Write("QCD")
