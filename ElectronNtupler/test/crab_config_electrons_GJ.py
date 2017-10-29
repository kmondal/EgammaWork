from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'electron_simple_ntupler_92X_forID_GJ_DoubleEM'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runElectrons.py'

config.section_("Data")
config.Data.inputDataset = '/GJet_DoubleEMEnriched_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM'
# config.Data.inputDataset = '/GJet_Pt-15To6000_TuneCUETP8M1-Flat_13TeV_pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publication = False
config.Data.ignoreLocality = False

config.section_("Site")
# Limit to US Tier2 sites. It appears to give more reliable performance.
#config.Site.whitelist = ['T2_US_MIT','T2_US_UCSD','T2_US_Florida','T2_US_Wisconsin','T2_US_Caltech','T2_US_Purdue']
config.Site.storageSite = 'T2_US_Nebraska'
