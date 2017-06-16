// This script compares performance of cut-based electorn IDs
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

// Files, samples
const int nSamples = 4;
enum SampleType {SIGNAL_OLD=0, SIGNAL_NEW, BG_OLD, BG_NEW};
const TString fileNames[nSamples] = {"DYJetsToLL_cutID_80X_small.root",
				     "DYJetsToLL_cutID_90X_small.root",
				     "TTJets_cutID_80X_small.root",
				     "TTJets_cutID_90X_small.root"};
const bool isSigOrBg[nSamples] = { true,
				   true,
				   false,
				   false};

// Ntuples, trees
const int nWP = 4;
const TString dirNames[nWP] = {"ntuplerIdVeto",
			       "ntuplerIdLoose",
			       "ntuplerIdMedium",
			       "ntuplerIdTight"};
const TString treeName = "ElectronTree";

// Cuts
const TString signalCuts = "(isTrue == 1)"; // gen-matched electrons
const TString bgCuts     = "(isTrue == 0 || isTrue == 3)"; // unmatched electrons or true non-prompt electrons (not from taus)

const TString ptCut      = "(pt > 20)"; 

const TString barrelCut   = "(abs(eta) < 1.4442)";
const TString endcapCut   = "(abs(eta) > 1.566 && abs(eta) < 2.5)";

const TString genWeightTerm  = "genWeight";

const TString idCut       = "(passEleId == 1)";

const int nEtaRegions = 2;
enum EtaRegions { ETA_BARREL = 0,
		  ETA_ENDCAP };

// Forward declarations
TTree *getTree(TString fileName, int indexWP);
void   getEfficiency(TTree *tree, bool isSignal, bool isBarrel, float &eff, float &effErr);

// Main method
void compareIdElectronCut(){
  
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
	getEfficiency(trees[iSample][iWP], isSigOrBg[iSample], isBarrel, 
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
    dummy[iEta] = new TH2F(TString::Format("dummy%d",iEta),"",100,0.6,1,100,0.9,1);
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

void   getEfficiency(TTree *tree, bool isSignal, bool isBarrel, float &eff, float &effErr){

  // Set up all cuts
  TString sigOrBgCut   = isSignal ? signalCuts : bgCuts;
  TString etaRegionCut = isBarrel ? barrelCut  : endcapCut;

  TString fullSelectionNum = TString::Format("%s * ( %s && %s && %s && %s )",
					     genWeightTerm.Data(),
					     sigOrBgCut.Data(), ptCut.Data(), etaRegionCut.Data(), idCut.Data());

  TString fullSelectionDen = TString::Format("%s * ( %s && %s && %s )",
					     genWeightTerm.Data(),
					     sigOrBgCut.Data(), ptCut.Data(), etaRegionCut.Data());

  if(verbose > 1){
    printf("  Numerator cut:\n     %s\n", fullSelectionNum.Data()); 
    printf("  Denominat cut:\n     %s\n", fullSelectionDen.Data()); 
  }

  TH1F *hist = new TH1F("hist", "", 1, 0, 1e9); // A dummy histogram for projections, use 1 bin! to get the error easily
  hist->Sumw2();
  TString drawString = "pt>>hist";

  // Find pass and all counts
  float num, den;
  tree->Draw(drawString, fullSelectionNum, "goff");
  num = hist->GetSumOfWeights();

  hist->Reset();
  tree->Draw(drawString, fullSelectionDen, "goff");
  den = hist->GetSumOfWeights();
  float Neff = hist->GetEffectiveEntries();

  eff = 0;
  effErr = 0;
  if(den != 0){
    eff = num/den;
    effErr = sqrt( eff * (1-eff) / Neff );
  }

  if(verbose > 0)
    printf("   Efficiency is %f +- %f, num=%f, den=%f\n", eff, effErr, num, den);

  delete hist;
  return;
}

