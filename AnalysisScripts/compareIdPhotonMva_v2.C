// This script compares performance of photon MVA IDs
// on signal and background samples

#include "TStyle.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TMarker.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TLegend.h"

#include <iostream>

// Define constants and inputs
const int verbose = 1; // 0=silent, 1=moderate, or 2=verbose
const bool smallEventCount = false;

const bool usePileupWeights = true;
const TString fnamePileupWeights = "pileupWeights.root";
const TString hnamePUWeights80X = "weights80X";
const TString hnamePUWeights90X = "weights90X";
TH1F *histPUWeights80X = 0;
TH1F *histPUWeights90X = 0;

// Files, samples
const int nSamples = 4;
enum SampleType {SIGNAL_OLD=0, SIGNAL_NEW, BG_OLD, BG_NEW};
const TString fileNames[nSamples] = {"Gjet_Pt-20toInf_mvaID_80X_small.root",
				     "Gjet_Pt-20toInf_mvaID_80X_small.root",
				     "Gjet_Pt-20toInf_mvaID_80X_small.root",
				     "Gjet_Pt-20toInf_mvaID_80X_small.root"};
const bool isSigOrBg[nSamples] = { true,
				   true,
				   false,
				   false};
const bool is80X[nSamples] = { true,
			       false,
			       true,
			       false};

// Ntuples, trees
const int nWP = 2;
const TString dirNames[nWP] = {"ntuplerWP90",
			       "ntuplerWP80"};
const TString treeName = "PhotonTree";

const int nEtaRegions = 2;
enum EtaRegions { ETA_BARREL = 0,
		  ETA_ENDCAP };

// Cuts
const float ptMin = 20;
const float etaBarrelMax = 1.4442;
const float etaEndcapMin = 1.5660;
const float etaEndcapMax = 2.5000;

// Forward declarations
TTree *getTree(TString fileName, int indexWP);
void   getEfficiency(TTree *tree, bool do80X, bool isSignal, bool isBarrel, float &eff, float &effErr);
float  getPUWeight(int nPU, bool do80X);


// Main method
void compareIdPhotonCut_v2(){
  
  //
  // Retrieve all trees from files
  //
  TTree *trees[nSamples][nWP];
  for(int iSample = 0; iSample < nSamples; iSample++){
    for(int iWP=0; iWP<nWP; iWP++){
      trees[iSample][iWP] = getTree(fileNames[iSample], iWP);
    }
  }

  //
  // Compute efficiencies
  //
  float effVals   [nSamples][nWP][nEtaRegions];
  float effErrVals[nSamples][nWP][nEtaRegions];
  for(int iSample = 0; iSample < nSamples; iSample++){
    for(int iWP=0; iWP<nWP; iWP++){
      for(int iEta = 0; iEta<nEtaRegions; iEta++){
	bool isBarrel = true;
	if(iEta > 0)
	  isBarrel = false;
	if(verbose>0)
	  printf("\nFind efficiency for file %s, WP=%d, isBarrel=%d, isSignal=%d\n", fileNames[iSample].Data(), iWP, 
		 (int)isBarrel, (int)isSigOrBg[iSample]);
	getEfficiency(trees[iSample][iWP], is80X[iSample], isSigOrBg[iSample], isBarrel, 
		      effVals[iSample][iWP][iEta], effErrVals[iSample][iWP][iEta]);
      } // end loop over barrel/endcap eta
    } // end loop over working points
  } // end loop over samples
  
  //
  // Display results
  //
  TCanvas *c1[nEtaRegions];
  TH2F *dummy[nEtaRegions];
  TGraphErrors *oldEffPoints[nEtaRegions];
  TGraphErrors *newEffPoints[nEtaRegions];
  TLegend *leg[nEtaRegions];
  TLatex *lat[nEtaRegions];
  for(int iEta = 0; iEta<nEtaRegions; iEta++){

    c1[iEta] = new TCanvas(TString::Format("canvas%d",iEta),"",10+100*iEta,10,800,800);
    gStyle->SetOptStat(0);
    dummy[iEta] = new TH2F(TString::Format("dummy%d",iEta),"",100,0.6,1,100,0.8,1);
    dummy[iEta]->SetTitle(";signal efficiency;background rejection");
    dummy[iEta]->GetYaxis()->SetTitleOffset(1.5);
    dummy[iEta]->Draw();

    oldEffPoints[iEta] = new TGraphErrors(nWP);
    oldEffPoints[iEta]->SetMarkerStyle(20);
    oldEffPoints[iEta]->SetMarkerSize(2);
    newEffPoints[iEta] = new TGraphErrors(nWP);
    newEffPoints[iEta]->SetMarkerStyle(24);
    newEffPoints[iEta]->SetMarkerSize(2);
    for(int iWP=0; iWP<nWP; iWP++){
      oldEffPoints[iEta]->SetPoint(iWP, effVals[SIGNAL_OLD][iWP][iEta],
			     1.0 - effVals[BG_OLD][iWP][iEta] );
      oldEffPoints[iEta]->SetPointError(iWP, effErrVals[SIGNAL_OLD][iWP][iEta],
				  effErrVals[BG_OLD][iWP][iEta] );
      
      
      newEffPoints[iEta]->SetPoint(iWP, effVals[SIGNAL_NEW][iWP][iEta],
			     1.0 - effVals[BG_NEW][iWP][iEta]);
      newEffPoints[iEta]->SetPointError(iWP, effErrVals[SIGNAL_NEW][iWP][iEta],
				  effErrVals[BG_NEW][iWP][iEta]);
      
    }
    oldEffPoints[iEta]->Draw("P,same");
    newEffPoints[iEta]->Draw("P,same");

    leg[iEta] = new TLegend(0.15, 0.2, 0.65, 0.4);
    leg[iEta]->AddEntry(oldEffPoints[iEta], "80X samples with 80X ID", "P");
    leg[iEta]->AddEntry(newEffPoints[iEta], "90X samples with 80X ID", "P");
    leg[iEta]->SetFillStyle(0);
    leg[iEta]->SetBorderSize(0);
    leg[iEta]->Draw();

    TString etaRegionLabel = (iEta == 0 ) ? "Barrel" : "Endcap";
    lat[iEta] = new TLatex(0.2, 0.6, etaRegionLabel);
    lat[iEta]->SetNDC();
    lat[iEta]->Draw();
  }// end loop over eta regions

}

// Get a tree from a file
TTree *getTree(TString fileName, int indexWP){

  TFile *file = new TFile(fileName);
  if( !file ){
    printf("Failed to open input file %s\n", fileName.Data());
    assert(0);
  }
  
  TString dirAndTreeName = dirNames[indexWP];
  dirAndTreeName += "/";
  dirAndTreeName += treeName;
  TTree *tree = (TTree*)file->Get(dirAndTreeName);
  if( !tree ){
    printf("Failed to get tree %s from file %s\n", dirAndTreeName.Data(), fileName.Data());
    assert(0);
  }

  return tree;
}

void   getEfficiency(TTree *tree, bool do80X, bool doSignal, bool doBarrel, float &eff, float &effErr){

  // Histograms for numerator and denominator of the efficiency
  TH1F *histNum = new TH1F("histNum", "", 1, 0, 1e9); // A dummy histogram for projections, use 1 bin! to get the error easily
  histNum->Sumw2();
  TH1F *histDen = new TH1F("histDen", "", 1, 0, 1e9); // A dummy histogram for projections, use 1 bin! to get the error easily
  histDen->Sumw2();

  // Declare variables and branches
  int nPU  = 0;
  int nPho = 0;
  std::vector <float> *pt = 0;
  std::vector <float> *eta = 0;
  std::vector <int>   *passId = 0;
  std::vector <float> *isTrue = 0;
  float genWeight = 0;

  TBranch *b_nPU       = 0;
  TBranch *b_nPho      = 0;
  TBranch *b_pt        = 0;
  TBranch *b_eta       = 0;
  TBranch *b_passId    = 0;
  TBranch *b_isTrue    = 0;
  TBranch *b_genWeight = 0;

  tree->SetBranchAddress("nPU", &nPU, &b_nPU );
  tree->SetBranchAddress("nPho", &nPho, &b_nPho );
  tree->SetBranchAddress("pt", &pt, &b_pt );
  tree->SetBranchAddress("eta", &eta, &b_eta);
  tree->SetBranchAddress("passPhoId",&passId, &b_passId );
  tree->SetBranchAddress("isTrue", &isTrue, &b_isTrue );
  tree->SetBranchAddress("genWeight", &genWeight, &b_genWeight );

  UInt_t maxEvents = tree->GetEntries();
  if( smallEventCount )
    maxEvents = std::min((float)10000, (float)maxEvents);
  if(verbose>0)
    printf("Start loop over events, total events = %lld\n", 
           tree->GetEntries() );
  for(UInt_t ievent = 0; ievent < maxEvents; ievent++){

    if( ievent%100000 == 0){
      printf("."); fflush(stdout);
    }
    Long64_t tentry = tree->LoadTree(ievent);

    b_nPho->GetEntry(tentry);
    if( nPho == 0 ) continue;

    b_nPU->GetEntry(tentry);
    b_pt->GetEntry(tentry);
    b_eta->GetEntry(tentry);
    b_passId->GetEntry(tentry);
    b_isTrue->GetEntry(tentry);
    b_genWeight->GetEntry(tentry);

    // Loop over candidates
  if(verbose>1)
    printf("Start loop over candidates, total candidates = %d\n",nPho); 
    for(int iPho=0; iPho<nPho; iPho++){

      // Selection
      if( !( pt->at(iPho) > ptMin ) ) 
	continue;

      bool doEndcap = !doBarrel;
      if( !( ( doBarrel && fabs(eta->at(iPho)) < etaBarrelMax )
	     || (doEndcap && fabs(eta->at(iPho)) > etaEndcapMin && fabs(eta->at(iPho))<etaEndcapMax ) ) )
	continue;

      // Signal or background?
      // signal: 1 gen-matched photons from GUDSCB (prompt)
      // background: 0 unmatched photons, 2 photons from pi0, 3 photons from "other sources"
      bool doBackground = !doSignal;
      if( !( (doSignal && isTrue->at(iPho)==1)
             || ( doBackground && isTrue->at(iPho) != 1 ) ) )
        continue;

      // The candidate survived and is to be counted
      if(verbose>1)
	printf("   the candidate is to be counted\n");

      float puWeight = getPUWeight(nPU, do80X);
      float weight = genWeight * puWeight;
      histDen->Fill(pt->at(iPho), weight);

      if( passId->at(iPho) == 1 ){
	// The candidate passed VID ID
	histNum->Fill(pt->at(iPho), weight);
      }
    } // end loop over photons
  } // end loop over events

  // Find pass and all counts
  float num, den;
  num = histNum->GetSumOfWeights();
  den = histDen->GetSumOfWeights();
  float Neff = histDen->GetEffectiveEntries();

  eff = 0;
  effErr = 0;
  if(den != 0){
    eff = num/den;
    effErr = sqrt( eff * (1-eff) / Neff );
  }

  if(verbose > 0)
    printf("   Efficiency is %f +- %f, num=%f, den=%f\n", eff, effErr, num, den);

  delete histNum;
  delete histDen;
  return;
}

float  getPUWeight(int nPU, bool do80X){
  
  float puWeight = 1.0;
  if( !usePileupWeights )
    return puWeight;
  
  // If this is the first time, set up the weight histograms
  if( histPUWeights80X == 0 || histPUWeights90X == 0 ){
    TFile *fWeights = new TFile(fnamePileupWeights);
    if( fWeights == 0 ){
      printf("Can't open file with PU weights %s\n", fnamePileupWeights.Data());
      assert(0);
    }
    histPUWeights80X = (TH1F*)fWeights->Get(hnamePUWeights80X);
    histPUWeights90X = (TH1F*)fWeights->Get(hnamePUWeights90X);
    if( histPUWeights80X == 0 || histPUWeights90X == 0 ){
      printf("Can't load the weights histogram %s or %s from the file %s\n", 
	     hnamePUWeights80X.Data(), hnamePUWeights90X.Data(), fnamePileupWeights.Data());
      assert(0);
    }
  }
  
  TH1F *histPUWeights = do80X ? histPUWeights80X : histPUWeights90X;
  puWeight = histPUWeights->GetBinContent( histPUWeights->GetXaxis()->FindBin( nPU ));

  return puWeight;

}

