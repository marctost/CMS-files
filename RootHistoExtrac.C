vector<string> fileloop(const char* ext, int num_files)
{
  cout << "Going to Directory" << endl;
  const char* inDir = "/hdfs/store/user/ldodd/crab_MONOHTT_PLAYPEN/April20_submission_v1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_MONOHTT_PLAYPEN_Mar17_v1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/170420_082817/0000/";
  char* dir = gSystem->ExpandPathName(inDir);
  cout << dir << endl;
  void* dirp = gSystem->OpenDirectory(dir);
  const char* entry;
  vector<string> filename;
  TString str;
  int i = 1;
  while ((entry = (char*)gSystem->GetDirEntry(dirp)))
    {
      str = entry;
      if (str.EndsWith(ext))
	{
	  string truename = string(inDir) + string(entry);
	  filename.push_back(truename);
	}
      if (i >= num_files)
	{
	  break;
	}
      i++;
    }
  return filename;
}

void RootHistoExtrac()
{
  int num_files = 10; //number of files you would like to consider

  const char* ext = ".root";

  vector<string> filename = fileloop(ext,num_files); //returns files names

  TH1F* METhisto = new TH1F("MET","MET",100,0.,400.0);//create a histogram to put your data in 
  TH1F* pt1histo = new TH1F("pt_1","pt_1", 100, 0.,400.);
  TH1F* pt2histo = new TH1F("pt_2","pt_2", 100, 0., 400.);
  TH1F* mvishisto = new TH1F("m_vis","m_vis", 100, 0., 400.);
  TH1F* mt12histo = new TH1F("mt12","mt12",100, 0., 400.);
  

  for (int i = 0; i < filename.size(); i++) //looping over all files
    {
      fprintf(stdout,"\r Processing Files:%4lld of%4lld ",i + 1,filename.size());
      fflush(stdout);

      TFile* file = TFile::Open(filename[i].c_str());
      
      TTree* eventTree = (TTree*)file->Get("muTauEventTree/eventTree");//getting tree with data
      
      TBranch* met = eventTree->GetBranch("met"); //getting specific branch with data
      TBranch* pt_1 = eventTree->GetBranch("pt_1");
      TBranch* pt_2 = eventTree->GetBranch("pt_2");
      TBranch* m_vis = eventTree->GetBranch("m_vis");
      TBranch* mt12 = eventTree->GetBranch("mt12");

      TH1F* meth = new TH1F("meth","",100,0.,400.); //creating temporary histogram for files data
      TH1F* pt_1h = new TH1F("pt_1h","",100,0.,400.);
      TH1F* pt_2h = new TH1F("pt_2h","",100,0.,400.);
      TH1F* m_vish = new TH1F("m_vish","",100,0.,400.);
      TH1F* mt12h = new TH1F("mt12h","",100,0.,400.);

      float met_var; //variable that will hold files data
      float pt_1_var;
      float pt_2_var;
      float m_vis_var;
      float mt12_var;
      
      eventTree->SetBranchAddress("met",&met_var); //tells which variable data will go in
      eventTree->SetBranchAddress("pt_1", &pt_1_var);
      eventTree->SetBranchAddress("pt_2", &pt_2_var);
      eventTree->SetBranchAddress("m_vis", &m_vis_var);
      eventTree->SetBranchAddress("mt12", &mt12_var);

      int nentries = int(eventTree->GetEntries()); //looping over each entry in branch
      for (int entry = 0; entry < nentries; entry++)
	{
	  eventTree->GetEntry(entry);
	  meth->Fill(met_var); //filling temporary histogram with file data
	  pt_1h->Fill(pt_1_var);
	  pt_2h->Fill(pt_2_var);
	  m_vish->Fill(m_vis_var);
	  mt12h->Fill(mt12_var);
	}

	     METhisto->Add(meth); //adding data to mother histogram
	     pt1histo->Add(pt_1h);
	     pt2histo->Add(pt_2h);
	     mvishisto->Add(m_vish);
	     mt12histo->Add(mt12h);
	     
	   
	   file->Close();
    }
  cout << endl;
      TFile* output = new TFile("METoutput.root","RECREATE"); //creating output root file
      METhisto->Write(); //drawing mother histogram to file
      pt1histo->Write();
      pt2histo->Write();
      mvishisto->Write();
      mt12histo->Write();
      
 
      output->Close(); //closing said file 
}
