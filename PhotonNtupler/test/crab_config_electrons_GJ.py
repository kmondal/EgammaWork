from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'photon_cutID_benchmark_GJ_90X_v1'
config.General.workArea = 'crab_projects'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'runPhotons_VID_CutBased_Spring16_benchmark.py'

config.section_("Data")
config.Data.inputDataset = '/Gjet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/PhaseISpring17MiniAOD-FlatPU28to62_90X_upgrade2017_realistic_v20-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
# Comment out the line for totalUnits to run on the full dataset
config.Data.totalUnits = 100
config.Data.publication = False
config.Data.ignoreLocality = False

config.section_("Site")
# Limit to US Tier2 sites. It appears to give more reliable performance.
#config.Site.whitelist = ['T2_US_MIT','T2_US_UCSD','T2_US_Florida','T2_US_Wisconsin','T2_US_Caltech','T2_US_Purdue']
config.Site.storageSite = 'T2_US_Nebraska'
