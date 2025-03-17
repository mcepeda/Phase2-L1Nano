import FWCore.ParameterSet.Config as cms
# from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *

l1tPh2DTNanoTask = cms.Task()

### Main Ph2L1 objects
from PhysicsTools.L1Nano.l1tPh2Nanotables_cff import *

## L1 Objects
p2L1MuonTablesTask = cms.Task(
    ## Muons
    gmtTkMuTable,
    staMuTable, staDisplacedMuTable,
    KMTFpromptMuTable,
    KMTFDisplaceMuTable,
    OMTFpromptMuTable,
    OMTFDisplaceMuTable,
    EMTFpromptMuTable,
    EMTFDisplaceMuTable,

    # DT tests
    convertDTDigis,
    dtPhiTable,
    dtThetaTable

)

def addPh2L1MuonObjects(process):
    process.l1tPh2DTNanoTask.add(p2L1MuonTablesTask)
    return process

#### GENERATOR INFO
## based on https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nanogen_cff.py#L2-L36
from PhysicsTools.NanoAOD.genparticles_cff import * ## for GenParts
def addGenObjects(process):

    process.genMuons = cms.EDProducer("GenParticlePruner",
        src = cms.InputTag("genParticles"), 
        select = cms.vstring( 
        "drop  *",
        # "++keep abs(pdgId) == 13 ", # keep only muons and history (mothers of the muons) 
        "keep ( abs(pdgId) == 13 & status==1) ", # keep only final state muons 
        )
    )
    finalGenParticles.src = cms.InputTag("genMuons")

    ## add more GenVariables
    # from L1Ntuple Gen: https://github.com/artlbv/cmssw/blob/94a5ec13b8ce76afb8ea4f157bb92fb547fadee2/L1Trigger/L1TNtuples/plugins/L1GenTreeProducer.cc#L203
    genParticleTable.variables.vertX = Var("vertex.x", float, "vertex X")
    genParticleTable.variables.vertY = Var("vertex.y", float, "vertex Y")
    genParticleTable.variables.vertZ = Var("vertex.z", float, "vertex Z")
    genParticleTable.variables.lXY = Var("sqrt(vertex().x() * vertex().x() + vertex().y() * vertex().y())", float, "lXY")
    genParticleTable.variables.dXY = Var("-vertex().x() * sin(phi()) + vertex().y() * cos(phi())", float, "dXY")
    
    process.l1tPh2DTNanoTask.add(
                process.genMuons, genParticleTask, genParticleTablesTask,
    )

 
    return process

def addDTPh2L1Nano(process):
    addGenObjects(process)
    addPh2L1MuonObjects(process)

    return process

