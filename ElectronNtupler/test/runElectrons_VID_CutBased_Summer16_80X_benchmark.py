import FWCore.ParameterSet.Config as cms

process = cms.Process("TestElectrons")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# NOTE: the pick the right global tag!
#    for Spring15 50ns MC: global tag is 'auto:run2_mc_50'
#    for Spring15 25ns MC: global tag is 'auto:run2_mc'
#    for Run 2 data: global tag is 'auto:run2_data'
#  as a rule, find the "auto" global tag in $CMSSW_RELEASE_BASE/src/Configuration/AlCa/python/autoCond.py
#  This auto global tag will look up the "proper" global tag
#  that is typically found in the DAS under the Configs for given dataset
#  (although it can be "overridden" by requirements of a given release)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

#
# Define input data to read
#
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

inputFilesAOD = cms.untracked.vstring(
    # AOD test files from
    # DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
    # /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/PhaseISpring17DR-FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/AODSIM
'/store/mc/PhaseISpring17DR/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/003E256E-CC28-E711-8B9F-0242AC130002.root',
'/store/mc/PhaseISpring17DR/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/004AFB9B-A828-E711-8F7B-70106F48BA2E.root',
'/store/mc/PhaseISpring17DR/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/00696113-8428-E711-BADA-A4BF0101DCC9.root',
'/store/mc/PhaseISpring17DR/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/006D9C5D-DC28-E711-B221-B499BAAC0068.root',
'/store/mc/PhaseISpring17DR/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/00837C80-622A-E711-BA24-484D7E8DF0D3.root',
    )    

inputFilesMiniAOD = cms.untracked.vstring(
    # MiniAOD test files from 
    # DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
    # /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/PhaseISpring17MiniAOD-FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/MINIAODSIM
'/store/mc/PhaseISpring17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/0837196E-D728-E711-89CD-A4BF0102A5BD.root',
'/store/mc/PhaseISpring17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/08850370-692A-E711-8378-008CFA0A5830.root',
'/store/mc/PhaseISpring17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/0ABE6B63-C528-E711-A994-1866DAEA6CF0.root',
'/store/mc/PhaseISpring17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/0E4D8C25-C828-E711-A4AB-141877411D83.root',
'/store/mc/PhaseISpring17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/FlatPU28to62_902_90X_upgrade2017_realistic_v20_ext1-v1/00000/12A8016D-692A-E711-B349-1866DAEA8038.root',
    )

# Set up input/output depending on the format
# You can list here either AOD or miniAOD files, but not both types mixed
#
useAOD = False

if useAOD == True :
    inputFiles = inputFilesAOD
    outputFile = "electron_ntuple.root"
    print("AOD input files are used")
else :
    inputFiles = inputFilesMiniAOD
    outputFile = "electron_ntuple_mini.root"
    print("MiniAOD input files are used")
process.source = cms.Source ("PoolSource", fileNames = inputFiles )                             

#
# Set up electron ID (VID framework)
#

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
if useAOD == True :
    dataFormat = DataFormat.AOD
else :
    dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
                 'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

#
# Configure an example module for user analysis with electrons
#

# Common parameters for all IDs
commonParameters = cms.PSet(
    # The module automatically detects AOD vs miniAOD, so we configure both
    #
    # Common to all formats objects
    #
    beamSpot = cms.InputTag('offlineBeamSpot'),
    genEventInfoProduct = cms.InputTag('generator'),
    #
    # Objects specific to AOD format
    #
    electrons    = cms.InputTag("gedGsfElectrons"),
    genParticles = cms.InputTag("genParticles"),
    vertices     = cms.InputTag("offlinePrimaryVertices"),
    conversions  = cms.InputTag('allConversions'),
    #
    # Objects specific to MiniAOD format
    #
    electronsMiniAOD    = cms.InputTag("slimmedElectrons"),
    genParticlesMiniAOD = cms.InputTag("prunedGenParticles"),
    verticesMiniAOD     = cms.InputTag("offlineSlimmedPrimaryVertices"),
    conversionsMiniAOD  = cms.InputTag('reducedEgamma:reducedConversions'),
)

# Define which ID to use
idSpecification = cms.PSet(
    #
    # ID decisions (common to all formats)
    #
    # (all IDs listed below are expected to be available given the content of "my_id_modules" 
    # defined above.
    #
    eleIdMap = cms.InputTag("egmGsfElectronIDs:UNDEFINED"),
    # An example of configuration for accessing the full cut flow info for
    # one case is shown below.
    # The map name for the full info is the same as the map name of the
    # corresponding simple pass/fail map above, they are distinguished by
    # the type of the content.
    eleIdFullInfoMap = cms.InputTag("egmGsfElectronIDs:UNDEFINED"),
    # This is a fairly verbose mode if switched on, with full cut flow 
    # diagnostics for each candidate. Use it in a low event count test job.
    eleIdVerbose = cms.bool(False)
)

idString = "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"
idSpecification.eleIdMap = idString
idSpecification.eleIdFullInfoMap = idString
process.ntuplerIdVeto = cms.EDAnalyzer(
    'ElectronNtuplerVIDDemo',
    commonParameters,
    idSpecification
    )

idString = "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose"
idSpecification.eleIdMap = idString
idSpecification.eleIdFullInfoMap = idString
process.ntuplerIdLoose = cms.EDAnalyzer(
    'ElectronNtuplerVIDDemo',
    commonParameters,
    idSpecification
    )

idString = "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium"
idSpecification.eleIdMap = idString
idSpecification.eleIdFullInfoMap = idString
process.ntuplerIdMedium = cms.EDAnalyzer(
    'ElectronNtuplerVIDDemo',
    commonParameters,
    idSpecification
    )

idString = "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"
idSpecification.eleIdMap = idString
idSpecification.eleIdFullInfoMap = idString
process.ntuplerIdTight = cms.EDAnalyzer(
    'ElectronNtuplerVIDDemo',
    commonParameters,
    idSpecification
    )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( outputFile )
                                   )

# Make sure to add the ID sequence upstream from the user analysis module
process.p = cms.Path(process.egmGsfElectronIDSequence 
                     * process.ntuplerIdVeto
                     * process.ntuplerIdLoose
                     * process.ntuplerIdMedium
                     * process.ntuplerIdTight)
