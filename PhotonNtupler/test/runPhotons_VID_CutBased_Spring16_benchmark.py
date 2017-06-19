import FWCore.ParameterSet.Config as cms

process = cms.Process("TestPhotons")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# NOTE: the pick the right global tag!
#    for Spring15 50ns MC: global tag is 'auto:run2_mc_50'
#    for Spring15 25ns MC: global tag is 'auto:run2_mc'
#    for Spring16 MC     : global tag is 'auto:run2_mc'
#    for Run 2 data: global tag is 'auto:run2_data'
#  as a rule, find the "auto" global tag in $CMSSW_RELEASE_BASE/src/Configuration/AlCa/python/autoCond.py
#  This auto global tag will look up the "proper" global tag
#  that is typically found in the DAS under the Configs for given dataset
#  (although it can be "overridden" by requirements of a given release)
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '91X_upgrade2017_realistic_v5', '')

#
# Define input data to read
#
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

inputFilesAOD = cms.untracked.vstring(
    # AOD test files from a GJet PT40 dataset
    # /Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/PhaseISpring17DR-FlatPU28to62_90X_upgrade2017_realistic_v20-v1/AODSIM
'/store/mc/PhaseISpring17DR/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/AODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/0055AEB6-0B29-E711-B3E7-549F3525C0BC.root',
'/store/mc/PhaseISpring17DR/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/AODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/005982B2-F128-E711-908C-A4BF0101DDD7.root',
'/store/mc/PhaseISpring17DR/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/AODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/00A6A43B-0329-E711-A96B-141877410B4D.root',
'/store/mc/PhaseISpring17DR/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/AODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/00BD4590-F628-E711-911F-E0071B7A48A0.root',
'/store/mc/PhaseISpring17DR/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/AODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/00F4B2FE-AC28-E711-848D-002590D0AFE4.root',
    )    

inputFilesMiniAOD = cms.untracked.vstring(
    # MiniAOD test files from a GJet PT40 dataset
    # /Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/PhaseISpring17MiniAOD-FlatPU28to62_90X_upgrade2017_realistic_v20-v1/MINIAODSIM
'/store/mc/PhaseISpring17MiniAOD/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/004F6ACC-F329-E711-8DDF-001E67A404B0.root',
'/store/mc/PhaseISpring17MiniAOD/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/0A061543-2A2A-E711-A299-001E67A3EC00.root',
'/store/mc/PhaseISpring17MiniAOD/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/0CD37897-2A2A-E711-A3A1-0242AC110004.root',
'/store/mc/PhaseISpring17MiniAOD/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/0E026519-E728-E711-AD2E-0CC47A4DE052.root',
'/store/mc/PhaseISpring17MiniAOD/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/MINIAODSIM/FlatPU28to62_90X_upgrade2017_realistic_v20-v1/00000/102F90E7-1D29-E711-B8D1-A4BF01011FD0.root',
    )

# Set up input/output depending on the format
# You can list here either AOD or miniAOD files, but not both types mixed
#
useAOD = False

if useAOD == True :
    inputFiles = inputFilesAOD
    outputFile = "photon_ntuple.root"
    pileupProductName = "addPileupInfo"
    print("AOD input files are used")
else :
    inputFiles = inputFilesMiniAOD
    outputFile = "photon_ntuple_mini.root"
    pileupProductName = "slimmedAddPileupInfo"
    print("MiniAOD input files are used")
process.source = cms.Source ("PoolSource", fileNames = inputFiles ) 

#
# Set up photon ID (VID framework)
#

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate
if useAOD == True :
    dataFormat = DataFormat.AOD
else :
    dataFormat = DataFormat.MiniAOD

switchOnVIDPhotonIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_Spring16_V2p2_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

#
# Configure an example module for user analysis of photons
#

process.ntupler = cms.EDAnalyzer(
    'PhotonNtuplerVIDDemo',
    # The module automatically detects AOD vs miniAOD, so we configure both
    #
    # Common to all formats objects
    #                                    
    pileup   = cms.InputTag( pileupProductName ),
    genEventInfoProduct = cms.InputTag('generator'),
    #
    # Objects specific to AOD format
    #
    photons = cms.InputTag("gedPhotons"),
    genParticles = cms.InputTag("genParticles"),
    vertices     = cms.InputTag("offlinePrimaryVertices"),
    #
    # Objects specific to MiniAOD format
    #
    photonsMiniAOD = cms.InputTag("slimmedPhotons"),
    genParticlesMiniAOD = cms.InputTag("prunedGenParticles"),
    verticesMiniAOD     = cms.InputTag("offlineSlimmedPrimaryVertices"),
    #
    # ID decisions (common to all formats)
    #
    phoLooseIdMap = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-loose"),
    phoMediumIdMap = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium"),
    phoTightIdMap = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-tight"),
    #
    phoMediumIdFullInfoMap = cms.InputTag("egmPhotonIDs:cutBasedPhotonID-Spring16-V2p2-medium"),
    # This is a fairly verbose mode if switched on, with full cut flow 
    # diagnostics for each candidate. Use it in a low event count test job.
    phoIdVerbose = cms.bool(False)
    )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( outputFile )
                                   )
process.p = cms.Path(process.egmPhotonIDSequence * process.ntupler)
