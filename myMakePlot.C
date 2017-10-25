#include "tdrstyle.C"
#include "CMS_lumi.C"
#include "TPad.h"

void myMakePlot(TString name = "fileName",TString fileName = "analysis_1.root",TString dir = "/hdfs/store/user/ldodd/crab_MONOHTT_PLAYPEN/April20_submission_v1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_MONOHTT_PLAYPEN_Mar17_v1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/170420_082817/0000/"){
 setTDRStyle();
 gROOT->SetBatch(kTRUE);
 
 writeExtraText = true;
 extraText = "Preliminary";
 lumi_8TeV = "19.1 fb^{-1}";
 lumi_7Tev = "4.9 gb^{-1}";
 lumi_13TeV = "[decay path]     2016, 35.9 fb^{-1}";
 
 
 int H = 600;
 int W = 600;
 int H_ref = 600;
 int W_ref = 600;
 float T = 0.08*H_ref;
 float B = 0.12*H_ref;
 float L = 0.12*W_ref;
 float R = 0.04*W_ref;
 
 //set margins
 float B_ratio = 0.1*H_ref;
 float T_ratio = 0.03*H_ref;
 
 float B_ratio_label = 0.3*H_ref;
 
 
 
 TCanvas * c = new TCanvas(name, name,50,50,W,H);
 c->SetFillColor(0);
 c->SetBorderMode(0);
 c->SetFrameFillStyle(0);
 c->SetFrameBorderMode(0);
 
 c->cd();
 
 TPad * plotPad =0;
 TPad * ratioPad =0;
 
 if(true){
  plotPad = new TPad("pad1","", 0.0,0.3,1.0,1.0);
  plotPad->SetLeftMargin (L/W);
  plotPad->SetRightMargin (R/W);
  plotPad->SetTopMargin (T_ratio/H);
  plotPad->SetBottomMargin (B_ratio/H);
  plotPad->SetFillColor(0);
  plotPad->SetBottomMargin(0);
  
  ratioPad = new TPad("pad2","", 0.0,0.0, 1.0,0.31);
  ratioPad->SetLeftMargin(L/W);
  ratioPad->SetRightMargin(R/W);
  ratioPad->SetTopMargin(T_ratio/H);
  ratioPad->SetBottomMargin(B_ratio_label/H);
  ratioPad->SetGridy(1);
  ratioPad->SetFillColor(4000); 
 }
 
 plotPad->Draw();
 plotPad->cd();
 
 
 TFile *f = new TFile(fileName);
 
 TTree* myTree = (TTree*)f->Get(dir+fileName+"muTauEventTree/eventTree");
 
 myTree.Draw("m_vis:met","","COLZ");
 
 
 CMS_lumi(c,4,11);
 plotPad->Draw();
 CMS_lumi(c,4,11);
 
 
 
 
}











