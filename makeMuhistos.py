import ROOT
import array
from sys import argv, exit, stdout, stderr
import math

ROOT.gROOT.SetBatch(True)

#get basic input that helps make the histograms
variable = raw_input("What variable to generate histos for? ")
topbin = raw_input("What to make the top bin? ")
bottombin = raw_input("What to make the bottom bin? ")
binnumber = raw_input("How many bins to use? ")

#where all the cuts are inputed
selectioncuts = "met>150&&m_vis<125&&pth>120&&dR<1.7&&pt_1>26&&pt_2>20&&npv>0&&diLeptons==0&&charge==0&&againstElectronVLooseMVA6_2>0&&againstMuonTight3_2>0&&iso04_1<0.15&&(HLT_IsoMu24_v_fired>0||HLT_IsoTkMu24_v_fired>0)&&byTightIsolationMVArun2v1DBoldDMwLT_2>0&&BadMuonFilter==1&&Flag_HBHENoiseFilter_fired==1&&Flag_HBHENoiseIsoFilter_fired==1&&Flag_goodVertices_fired==1&&Flag_EcalDeadCellTriggerPrimitiveFilter_fired==1&&EffCSVWeight0==1"

#where all the weights are inputted 
weight = "__WEIGHT__*GENWEIGHT*puweight*POGid1*POGtrigger*TAUID1*trackweight*35870"


#Defines all the files needed to make the histograms
signalfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/ZpBaryonic_Zp1000_MChi150.root")
smhfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/smH125.root")
dibosonfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/DiBosonAll.root")
wjetsfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/WJETS.root")
znunufile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/Znunu.root")
zjetsfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/ZJETS.root")
ttfile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/TT.root")
datafile = ROOT.TFile("/nfs_scratch/tost/monohiggs_Aug27/muDATA.root")

#Define trees for background, signal and data
signaltree = signalfile.Get("muTauEventTree/eventTree")
smhtree = smhfile.Get("muTauEventTree/eventTree")
dibosontree = dibosonfile.Get("muTauEventTree/eventTree")
wjetstree = wjetsfile.Get("muTauEventTree/eventTree")
znunutree = znunufile.Get("muTauEventTree/eventTree")
zjetstree = zjetsfile.Get("muTauEventTree/eventTree")
tttree = ttfile.Get("muTauEventTree/eventTree")
datatree = datafile.Get("muTauEventTree/eventTree")



#Define all the histograms you are gonna put shit in
sig = ROOT.TH1F("signal", "signal", int(binnumber), float(bottombin), float(topbin))
smh = ROOT.TH1F("smh", "smH", int(binnumber), float(bottombin), float(topbin))
dibos = ROOT.TH1F("diboson", "diboson", int(binnumber), float(bottombin), float(topbin))
wjet = ROOT.TH1F("wjets","wjets", int(binnumber), float(bottombin), float(topbin))
znu = ROOT.TH1F("znunu","znunu", int(binnumber), float(bottombin), float(topbin))
zjet = ROOT.TH1F("zjets","zjets", int(binnumber), float(bottombin), float(topbin))
tthist = ROOT.TH1F("tt", "tt", int(binnumber), float(bottombin), float(topbin))
dat = ROOT.TH1F("data","data", int(binnumber), float(bottombin), float(topbin)) 



#Where the magic happens. Shove shit into the histograms
signaltree.Draw(variable+">>+signal","("+selectioncuts+")*"+weight)
smhtree.Draw(variable+">>+smh","("+selectioncuts+")*"+weight)
dibosontree.Draw(variable+">>+diboson","("+selectioncuts+")*"+weight)
wjetstree.Draw(variable+">>+wjets","("+selectioncuts+")*"+weight)
znunutree.Draw(variable+">>+znunu","("+selectioncuts+")*"+weight)
zjetstree.Draw(variable+">>+zjets","("+selectioncuts+")*"+weight)
tttree.Draw(variable+">>+tt","("+selectioncuts+")*"+weight)
datatree.Draw(variable+">>data","("+selectioncuts+")*"+weight)


#Make a spot to put all these histos
outfile = ROOT.TFile("muTauHistos.root","RECREATE")
outfile.mkdir("muTau")
outfile.cd("muTau")

#Now write all te histos to this file!
sig.Write("Signal")
smh.Write("smH125")
dibos.Write("DiBosons")
wjet.Write("WJets")
znu.Write("Znunu")
zjet.Write("ZJets")
tthist.Write("TT")
dat.Write("Data")
