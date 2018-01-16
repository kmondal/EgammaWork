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
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v10', '')

#
# Define input data to read
#
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )

inputFilesAOD = cms.untracked.vstring(
    # AOD test files from a GJet dataset
    # /GJet_DoubleEMEnriched_13TeV_pythia8/RunIISummer17DRPremix-92X_upgrade2017_realistic_v10-v3/AODSIM
    '/store/mc/RunIISummer17DRPremix/GJet_DoubleEMEnriched_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v3/10000/001C7B26-A694-E711-B121-0CC47A7E6A88.root',
    '/store/mc/RunIISummer17DRPremix/GJet_DoubleEMEnriched_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v3/10000/0036F4BC-7695-E711-BC85-5065F3812261.root',
    '/store/mc/RunIISummer17DRPremix/GJet_DoubleEMEnriched_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v3/10000/0046796A-7095-E711-8D19-001F29086E48.root',
    '/store/mc/RunIISummer17DRPremix/GJet_DoubleEMEnriched_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v3/10000/0068EEB5-B194-E711-A18E-D4AE526A091F.root',
    '/store/mc/RunIISummer17DRPremix/GJet_DoubleEMEnriched_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v3/10000/0077DB07-7295-E711-AD20-0025905A6084.root',
    )    

inputFilesMiniAOD = cms.untracked.vstring(
    # MiniAOD test files from a GJet dataset
    # /GJet_DoubleEMEnriched_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM
    '/store/mc/RunIISummer17MiniAOD/GJet_DoubleEMEnriched_13TeV_pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v3/10000/004C2147-0D96-E711-9DEF-3417EBE64AFE.root',
    '/store/mc/RunIISummer17MiniAOD/GJet_DoubleEMEnriched_13TeV_pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v3/10000/0238C4A4-2995-E711-B257-001517FB1944.root',
    '/store/mc/RunIISummer17MiniAOD/GJet_DoubleEMEnriched_13TeV_pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v3/10000/02416219-AE95-E711-8860-0025905A610A.root',
    '/store/mc/RunIISummer17MiniAOD/GJet_DoubleEMEnriched_13TeV_pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v3/10000/02C73BB1-0795-E711-B99B-0CC47A4C8E3C.root',
    '/store/mc/RunIISummer17MiniAOD/GJet_DoubleEMEnriched_13TeV_pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10-v3/10000/02CE7B2D-BE98-E711-95D5-002590D9D8AA.root',
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
my_id_modules = ['RecoEgamma.PhotonIdentification.Identification.mvaPhotonID_RunIIFall17_v1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)

#
# Configure an example module for user analysis with photons
#

process.ntupler = cms.EDAnalyzer(
    'PhotonNtuplerVIDwithMVADemo',
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
    vertices = cms.InputTag("offlinePrimaryVertices"),
    #
    # Objects specific to MiniAOD format
    #
    photonsMiniAOD = cms.InputTag("slimmedPhotons"),
    genParticlesMiniAOD = cms.InputTag("prunedGenParticles"),
    verticesMiniAOD = cms.InputTag("offlineSlimmedPrimaryVertices"),
    #
    # ID decisions (common to all formats)
    #
    # (the names of the ValueMaps for just decision and full info are the same,
    # they are distinguished by the type of the info)
    phoIdBoolMap = cms.InputTag("egmPhotonIDs:mvaPhoID-RunIIFall17-v1-wp90"),
    phoIdFullInfoMap = cms.InputTag("egmPhotonIDs:mvaPhoID-RunIIFall17-v1-wp90"),
    # This is a fairly verbose mode if switched on, with full cut flow 
    # diagnostics for each candidate. Use it in a low event count test job.
    phoIdVerbose = cms.bool(False),
    #
    # ValueMaps with MVA results
    #
    mvaValuesMap     = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v1Values"),
    mvaCategoriesMap = cms.InputTag("photonMVAValueMapProducer:PhotonMVAEstimatorRunIIFall17v1Categories")
    )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string( outputFile )
                                   )

# Make sure to add the ID sequence upstream from the user analysis module
process.p = cms.Path(process.egmPhotonIDSequence * process.ntupler)
