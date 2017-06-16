#include "rootIncludes.h"

const TString fname80X = "DYJetsToLL_cutID_80X_small_v2.root";
const TString fname90X = "DYJetsToLL_cutID_90X_small_v2.root";
const TString treeName = "ntuplerIdVeto/ElectronTree";

const TString fnameWeights = "pileupWeights.root";

// Forward declarations
TTree *getTree(TString fileName, TString treeName);

// Main method
void preparePUWeights(){

  TTree *tree80X = getTree(fname80X, treeName);
  TTree *tree90X = getTree(fname90X, treeName);

  TCanvas *c1 = new TCanvas("c1","c1", 10,10,700,500);
  gStyle->SetOptStat(0);
  TH1F *hist80X = new TH1F("hist80X","",100,-0.5, 99.5); 
  hist80X->Sumw2();
  hist80X->SetTitle(";number of pileup interactions;");
  hist80X->SetLineWidth(2);
  hist80X->SetLineColor(kBlue);

  TH1F *hist90X = (TH1F*)hist80X->Clone("hist90X");
  hist90X->SetLineColor(kRed);

  tree80X->Draw("nPU>>hist80X");
  tree90X->Draw("nPU>>hist90X");

  // Normalize to unit area
  hist80X->Scale(1.0/hist80X->GetSumOfWeights());
  hist90X->Scale(1.0/hist90X->GetSumOfWeights());

  hist80X->Draw("hist");
  hist90X->Draw("hist,same");

  TLegend *leg = new TLegend(0.5, 0.6, 0.9, 0.9);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->AddEntry(tree80X, "80X MC samples","l");
  leg->AddEntry(tree90X, "90X MC samples", "l");
  leg->Draw();

  // Compute the weights histogram
  // Note that weights for 80X are essencially 1.0
  TH1F *weights80X = (TH1F*)hist80X->Clone("weights80X");
  weights80X->GetYaxis()->SetTitle("weight");
  weights80X->Divide(hist80X);
  TH1F *weights90X = (TH1F*)hist80X->Clone("weights90X");
  weights90X->Divide(hist90X);
  weights90X->GetYaxis()->SetTitle("weight");

  // Zero the weights for PU below 20 and above 50
  int minPileUp = 20;
  int maxPileUp = 50;
  for(int i=1; i<=hist80X->GetNbinsX(); i++){
    if( hist80X->GetXaxis()->GetBinLowEdge(i) < minPileUp 
	|| hist80X->GetXaxis()->GetBinLowEdge(i) > maxPileUp ){ 
      weights80X->SetBinContent(i, 0);
      weights80X->SetBinError(i, 0);
      weights90X->SetBinContent(i, 0);
      weights90X->SetBinError(i, 0);
    }
  }

  TCanvas *c2 = new TCanvas("c2","c2", 710,10,700,500);
  weights90X->Draw("hist");

  // Go back to the first canvas and add the weights band
  c1->cd();
  TH1F *weightsBand = (TH1F*) weights80X->Clone("weightsBand");
  weightsBand->Scale(0.3/weightsBand->GetSumOfWeights());
  weightsBand->SetLineColor(33);
  weightsBand->SetFillColor(33);
  weightsBand->SetFillStyle(1001);
  weightsBand->Draw("hist,same");
  // Redraw histograms on top
  hist80X->Draw("hist,same");
  hist90X->Draw("hist,same");
  // Add entry to the legend
  leg->AddEntry(weightsBand, "range used in analysis","f");
  c1->Update();

  // Save the weights histograms
  TFile *fout = new TFile(fnameWeights, "recreate");
  fout->cd();
  weights80X->Write();
  weights90X->Write();
  fout->Close();

}


// Get a tree from a file
TTree *getTree(TString fileName, TString treeName){

  TFile *file = new TFile(fileName);
  if( !file ){
    printf("Failed to open input file %s\n", fileName.Data());
    assert(0);
  }
  
  TTree *tree = (TTree*)file->Get(treeName);
  if( !tree ){
    printf("Failed to get tree %s from file %s\n", treeName.Data(), fileName.Data());
    assert(0);
  }

  return tree;
}
