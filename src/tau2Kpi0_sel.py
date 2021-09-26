###########################################################################
# Selection of 1%1 prong taupair decays with loose cuts
#
#                  l nu nu
#                  |
#        e+ e- -> tau+ tau-
#                       |
#                       K pi0 nu
#
# Contributors:
# Maoqiang Jing
#
# Use cases: |Vus|
#
# created: August 2021
###########################################################################

# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import basf2 as b2
import modularAnalysis as ma
from variables import variables
import vertex
import sys

######################################################
# Specify path to data sample and database
######################################################
arg_dataORmc = 'mc'
if len(sys.argv) > 1:
  arg_dataORmc = str(sys.argv[1])

main = b2.create_path()

if arg_dataORmc == 'data':
    b2.B2INFO("CHECK: analysing data, is this correct?")
    arg_dir = '/nfs/dust/belle2/user/rbkarl/Tau/tauEDM/MC13/DataTestFiles'
    if len(sys.argv) > 2:
        arg_dir = str(sys.argv[2])
    print(arg_dir)    
    ma.inputMdstList('default', '%s/*.root' % arg_dir, path = main)
    arg_outfile = 'tau2Kpi0_data.root'
    if len(sys.argv) > 3:
        arg_outfile = str(sys.argv[3])
    print(arg_outfile)
        
elif arg_dataORmc == 'mc':
    b2.B2INFO("CHECK: analysing MC, is this correct?")
    arg_dir = '/besfs5/groups/psip/psipgroup/user/jingmq/Belle2/tau2Kpi0/rootfiles/Kpi0/exMC_Kpi0*.root'
    if len(sys.argv) > 2:
        arg_dir = str(sys.argv[2])
    print(arg_dir)
    ma.inputMdstList('default', '%s' % arg_dir, path = main)
    arg_outfile = '/besfs5/groups/psip/psipgroup/user/jingmq/Belle2/tau2Kpi0/rootfiles/Kpi0/Kpi0-source.root'
    if len(sys.argv) > 3:
        arg_outfile = str(sys.argv[3])
    print(arg_outfile)
    
else:
    b2.B2INFO("WARNING: unkown input...")

######################################################
# label-variable definition
######################################################
TotalFourMomentumParticlesInList = {
	"E":"Energy",
	"px":"Px",
	"py":"Py",
	"pz":"Pz"
}

##################################################################################
# pi0 reconstruction with loose photons 
##################################################################################
ma.fillParticleList('gamma:good', '', path = main)

gammaDetectorLocation = {
    'FWD' : 'clusterReg == 1',
    'BRL' : 'clusterReg == 2',
    'BWD' : 'clusterReg == 3'
}

gammaForPi0lists = []
for g in gammaDetectorLocation.keys():
    gammaForPi0Cuts = gammaDetectorLocation[g]
    gammaForPi0Cuts += ' and abs(clusterTiming) < 200'
    gammaForPi0Cuts += ' and -0.8660 < cosTheta < 0.9563'
    gammaForPi0Cuts += ' and clusterNHits > 1.5'
    gammaForPi0 = 'gamma:looseForPi0{}'.format(g)
    gammaForPi0lists.append(gammaForPi0)
    ma.cutAndCopyLists(gammaForPi0, 'gamma:good', gammaForPi0Cuts, path = main)

# -# -- -- cos of opening angle between the photons
variables.addAlias('cosAngle2Photons', 
                   'formula((daughter(0, px)*daughter(1, px) + daughter(0, py)*daughter(1, py) + daughter(0, pz)*daughter(1, pz))/daughter(0, p)/daughter(1, p))')
variables.addAlias('leadingclusterE', 'formula(max(daughter(0, clusterE), daughter(1, clusterE)))')
variables.addAlias('subleadingclusterE', 'formula(min(daughter(0, clusterE), daughter(1, clusterE)))')

# Determine pi0 reco for individual Detector Parts
Pi0CutLabel = ['leadingclusterE', 'subleadingclusterE', 'cosAngle2Photons', 'p']
Pi0CutValue = {
    'FWD,FWD'   :   [0.5625, 0.1625, 0.9458, 0.9444],
    'BRL,BRL'   :   [0.4125, 0.0625, 0.8875, 0.6333],
    'BWD,BWD'   :   [0.4125, 0.1125, 0.8708, 0.6111],
    'BRL,FWD'   :   [0.3625, 0.0875, 0.8875, 0.5889],
    'BRL,BWD'   :   [0.3625, 0.0875, 0.8875, 0.5889]
}

Pi0lists = []
for cut in Pi0CutValue.keys():
    gammalists = cut.split(',')
    CurrentPi0List = 'pi0:gg{}{}'.format(gammalists[0], gammalists[1])
    Pi0lists.append(CurrentPi0List)
    Pi0Cut = '0.08 < M < 0.20'
    for i, c in enumerate(Pi0CutLabel):
        Pi0Cut += ' and {} > {}'.format(c, Pi0CutValue[cut][i])
    ma.reconstructDecay('{} -> gamma:looseForPi0{} gamma:looseForPi0{}'.format(CurrentPi0List, gammalists[0], gammalists[1]), Pi0Cut, path = main)
ma.copyLists('pi0:gg', Pi0lists, path = main)
variables.addAlias('nPi0', 'countInList(pi0:gg)')
ma.cutAndCopyLists('gamma:pi0', gammaForPi0lists, 'isDescendantOfList(pi0:gg) == 1', path=main)
ma.applyEventCuts('nPi0 == 1', path = main)
vertex.kFit('pi0:gg', conf_level = 0.0, fit_type = 'mass', daughtersUpdate = False, path = main)


############################################################################################################
# track
############################################################################################################

# Define quality cuts for tracks
trackCuts = 'dr <= 1. and -5. <= dz <= 5. and nCDCHits > 0'

# Fill the particle lists of Kions and gammas with the quality criteria defined above
ma.fillParticleList('e-:good', trackCuts, path = main)
ma.fillParticleList('mu-:good', trackCuts, path = main)
ma.fillParticleList('K+:good', trackCuts, path = main)

modifiedIDcut = 0.9
variables.addAlias('ModelectronID', 'formula(electronID/(electronID + muonID + kaonID + pionID))')
variables.addAlias('ModmuonID', 'formula(muonID/(electronID + muonID + kaonID + pionID))')
variables.addAlias('ModkaonID', 'formula(kaonID/(electronID + muonID + pionID + kaonID))')
eIDCuts = 'ModelectronID > {}'.format(modifiedIDcut)
muIDCuts = 'ModmuonID > {}'.format(modifiedIDcut)
KIDCuts = 'ModkaonID > {}'.format(modifiedIDcut)
variables.addAlias('EoverP', 'formula(ifNANgiveX(clusterE, -1)/p)')

ma.cutAndCopyLists('e-:pid', 'e-:good', eIDCuts, path = main)
ma.cutAndCopyLists('mu-:pid', 'mu-:good', muIDCuts, path = main)
ma.cutAndCopyLists('K-:pid', 'K-:good', KIDCuts, path = main)
variables.addAlias('nElectronTracks', 'countInList(e-:pid)')
variables.addAlias('nMuonTracks', 'countInList(mu-:pid)')
variables.addAlias('nKaonTracks', 'countInList(K-:pid)')

gammaCuts = 'E > 0.2'
gammaCuts += ' and -0.8660 < cosTheta < 0.9563'
gammaCuts += ' and clusterNHits > 1.5'
gammaCuts += ' and isDescendantOfList(pi0:gg) == 0'
ma.cutAndCopyLists('gamma:notPi0', 'gamma:good', gammaCuts, path=main)

######################################################
# event based cut - 2 tracks in event
######################################################
variables.addAlias('nGoodPhotons', 'countInList(gamma:notPi0)')
ma.applyEventCuts('nElectronTracks == 1 or nMuonTracks == 1', path = main)
ma.applyEventCuts('nKaonTracks == 1', path = main)

#######################################################
# EventShape and EventKinamatics modules
#######################################################
ma.buildEventShape(['K+:pid', 'e-:pid', 'mu-:pid', 'gamma:pi0'], path = main)
ma.buildEventKinematics(['K-:pid', 'e-:pid', 'mu-:pid', 'gamma:pi0'], path = main)
ma.applyEventCuts('thrust < 0.99 and foxWolframR2 > 0.1', path = main)

######################################################
# Signal and tag sides
#######################################################
# -- 1 prong
ma.reconstructDecay('tau-:e -> e-:pid', '', path = main, dmID = 11)
ma.reconstructDecay('tau-:mu -> mu-:pid', '', path = main, dmID = 13)
ma.reconstructDecay('tau-:Kpi0 -> K-:pid pi0:gg', '', path = main, dmID = 321111)
ma.copyLists('tau+:1prong0', ['tau+:Kpi0'], path = main)
ma.copyLists('tau-:1prong1', ['tau-:e', 'tau-:mu'], path = main)
ma.reconstructDecay('vpho -> tau+:1prong0 tau-:1prong1', '', path = main)
variables.addAlias('dmID_1prong0', 'daughter(0, extraInfo(decayModeID))') # reconstructed tau+ 1-prong decay mode
variables.addAlias('dmID_1prong1', 'daughter(1, extraInfo(decayModeID))') # reconstructed tau- 1-prong decay mode

# Select vpho candidates with signal and tag in opposite sides of the event.
variables.addAlias('cosTheta1',
                   'formula(daughter(0, daughter(0, cosToThrustOfEvent))*daughter(1, daughter(0,cosToThrustOfEvent)))')
variables.addAlias('cosTheta2',
                   'formula(daughter(0, daughter(1, cosToThrustOfEvent))*daughter(1, daughter(0,cosToThrustOfEvent)))')

ma.applyCuts('vpho', 'cosTheta1 < 0 and cosTheta2 < 0', path = main)

variables.addAlias('gammas_clusterE', 'totalEnergyOfParticlesInList(gamma:notPi0)')

######################################################
# perform MC matching for MC samples
######################################################
if arg_dataORmc == 'mc':
    ma.matchMCTruth('vpho', path = main)
    ma.labelTauPairMC(path = main)
    ma.fillParticleListFromMC('tau+:gen', cut = '', addDaughters = True, path = main)
    ma.fillParticleListFromMC('gamma:gen', '', path = main)
    ma.fillParticleListFromMC('pi0:gen', '', path = main)
    ma.cutAndCopyLists('gamma:genisr', 'gamma:gen', 'mcMother(abs(PDG)) == 11 and isMCDescendantOfList(tau+:gen) == 0', path = main)
    ma.cutAndCopyLists('gamma:genisrMinus', 'gamma:gen', 'mcMother(PDG) == 11 and isMCDescendantOfList(tau+:gen) == 0', path = main)
    ma.cutAndCopyLists('gamma:genisrPlus', 'gamma:gen', 'mcMother(PDG) == -11 and isMCDescendantOfList(tau+:gen) == 0', path = main)
    ma.cutAndCopyLists('gamma:genfsr', 'gamma:gen', 'mcMother(abs(PDG)) == 15 and isMCDescendantOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('gamma:genfsrMinus', 'gamma:gen', 'mcMother(PDG) == 15 and isMCDescendantOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('gamma:genfsrPlus', 'gamma:gen', 'mcMother(PDG) == -15 and isMCDescendantOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('pi0:genMinus', 'pi0:gen', 'hasAncestor(15,1) and isMCDescendantOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('pi0:genPlus', 'pi0:gen', 'hasAncestor(-15,1) and isMCDescendantOfList(tau+:gen) == 1', path = main)
    variables.addAlias('nPi0s_Minus_MC', 'nParticlesInList(pi0:genMinus)')
    variables.addAlias('nPi0s_Plus_MC', 'nParticlesInList(pi0:genPlus)')
    MCtotMomentumList = []
    for P in TotalFourMomentumParticlesInList.keys():
        variables.addAlias('gamma_isr_{}_mc'.format(P), 'total{}OfParticlesInList(gamma:genisr)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('gamma_isr_{}_mc'.format(P))
        variables.addAlias('gamma_isr_Minus_{}_mc'.format(P), 'total{}OfParticlesInList(gamma:genisrMinus)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('gamma_isr_Minus_{}_mc'.format(P))
        variables.addAlias('gamma_isr_Plus_{}_mc'.format(P), 'total{}OfParticlesInList(gamma:genisrPlus)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('gamma_isr_Plus_{}_mc'.format(P))
        variables.addAlias('gamma_fsr_{}_mc'.format(P), 'total{}OfParticlesInList(gamma:genfsr)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('gamma_fsr_{}_mc'.format(P))
        variables.addAlias('gamma_fsr_Minus_{}_mc'.format(P), 'total{}OfParticlesInList(gamma:genfsrMinus)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('gamma_fsr_Minus_{}_mc'.format(P))
        variables.addAlias('gamma_fsr_Plus_{}_mc'.format(P), 'total{}OfParticlesInList(gamma:genfsrPlus)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('gamma_fsr_Plus_{}_mc'.format(P))
        variables.addAlias('pi0_tauMinus_{}_mc'.format(P), 'total{}OfParticlesInList(pi0:genMinus)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('pi0_tauMinus_{}_mc'.format(P))
        variables.addAlias('pi0_tauPlus_{}_mc'.format(P), 'total{}OfParticlesInList(pi0:genPlus)'.format(TotalFourMomentumParticlesInList[P]))
        MCtotMomentumList.append('pi0_tauPlus_{}_mc'.format(P))

#####################################################
# select the variables to be stored in the ntuple
#####################################################

import variables.collections as vc
import variables.utils as vu

# CMS variables
variables.addAlias('E_CMS', 'useCMSFrame(E)')
variables.addAlias('p_CMS', 'useCMSFrame(p)')
variables.addAlias('px_CMS', 'useCMSFrame(px)')
variables.addAlias('py_CMS', 'useCMSFrame(py)')
variables.addAlias('pz_CMS', 'useCMSFrame(pz)')
variables.addAlias('pt_CMS', 'useCMSFrame(pt)')
variables.addAlias('theta_CMS', 'useCMSFrame(theta)')
variables.addAlias('phi_CMS', 'useCMSFrame(phi)')

# expert PID
IDparticles = ['e', 'mu', 'pi']
IDdectors = ['KLM', 'ECL', 'CDC', 'ARICH', 'TOP', 'ALL']
particlePDG = {'e' : '11', 'mu' : '13', 'pi' : '211'}
IDvar = []
for D in IDdectors:
    for p in range(len(IDparticles)):
        CurrentIDvar = IDparticles[p] + "id_" + D
        IDvar.append(CurrentIDvar)
        variables.addAlias(CurrentIDvar, ('pidProbabilityExpert(' + particlePDG[IDparticles[p]] + ',' + D + ' )'))
        for pp in range(p + 1, len(IDparticles)):
            CurrentIDpair = IDparticles[p] + IDparticles[pp] + "id_" + D
            IDvar.append(CurrentIDpair)
            variables.addAlias(CurrentIDpair, ('pidDeltaLogLikelihoodValueExpert(' + particlePDG[IDparticles[p]] + ',' + particlePDG[IDparticles[pp]] + ',' + D + ' )'))
            CurrentIDbinary = IDparticles[p] + IDparticles[pp] + "pairid_" + D
            IDvar.append(CurrentIDbinary)
            variables.addAlias(CurrentIDbinary, ('pidPairProbabilityExpert(' + particlePDG[IDparticles[p]] + ',' + particlePDG[IDparticles[pp]] + ',' + D + ' )'))

# -- event based variables
eventVariables = ['dmID_1prong0', 'dmID_1prong1',
                  'nElectronTracks', 'nMuonTracks', 'nKaonTracks',
                  'nGoodPhotons', 'nPi0'
                 ]
eventVariables += ['thrust', 'foxWolframR2',
                   'visibleEnergyOfEventCMS',
                   'missingMomentumOfEvent', 'missingMomentumOfEvent_theta',
                   'missingMomentumOfEventCMS', 'missingMomentumOfEventCMS_theta',
                   'missingMass2OfEvent'
                  ]
eventVariables += ['gammas_clusterE']

commonVariables = vc.kinematics 
commonVariables += ['theta', 'cosTheta', 'phi', 'pt']
commonVariables += ['E_CMS', 'p_CMS', 'px_CMS', 'py_CMS', 'pz_CMS', 'pt_CMS', 'theta_CMS', 'phi_CMS']
commonVariables += ['charge', 'cosToThrustOfEvent']

# -- tau candidate variables
tauVariables =  vc.inv_mass + vc.vertex + ['chiProb']
# -- track level variables
trackVariables = ['clusterE', 'EoverP']
trackVariables += vc.pid + IDvar
trackVariables += vc.track_hits
trackVariables += ['dz', 'dr']

## ancestors
variables.addAlias('fromTau', 'hasAncestor(15)')
variables.addAlias('fromKS', 'hasAncestor(310)')
variables.addAlias('genMotherPDG0', 'genMotherPDG(0)')
variables.addAlias('genMotherPDG1', 'genMotherPDG(1)')
variables.addAlias('genMotherPDG2', 'genMotherPDG(2)')
variables.addAlias('genMotherPDG3', 'genMotherPDG(3)')
variables.addAlias('genMotherPDG4', 'genMotherPDG(4)')
ancestorVariables  =  ['fromTau', 'fromKS', 'genMotherPDG0', 'genMotherPDG1', 'genMotherPDG2', 'genMotherPDG3']

# -- MC specific info
if arg_dataORmc == 'mc':
    # -- event variables
    eventVariables += ['nPi0s_Minus_MC', 'nPi0s_Plus_MC']
    eventVariables += ['tauPlusMCMode', 'tauMinusMCMode', 'tauPlusMCProng', 'tauMinusMCProng']
    eventVariables += MCtotMomentumList
    # -- common variables
    commonVariables += vc.mc_variables + vc.mc_truth + ancestorVariables
    # -- tau vertex truth
    tauVariables += vc.mc_vertex
    tauVariables += vc.mc_variables

vphoVariableList = vu.create_aliases_for_selected(list_of_variables = eventVariables,
                                                  decay_string = '^vpho') + \
                   vu.create_aliases_for_selected(list_of_variables = commonVariables + tauVariables,
                                                  decay_string = 'vpho -> ^tau+ ^tau-',
                                                  prefix = ['tau_1prong0', 'tau_1prong1']) + \
                   vu.create_aliases_for_selected(list_of_variables = commonVariables + trackVariables + vc.inv_mass,
                                                  decay_string = 'vpho -> [tau- -> ^K- ^pi0] [tau+ -> ^pi+]',
                                                  prefix=['track_1prong0', 'pi0_1prong0', 'track_1prong1'])


# Save the variables to a ROOT file
ma.variablesToNtuple(decayString = 'vpho',
                     variables = vphoVariableList,
                     filename = arg_outfile,
                     treename = 'tau2Kpi0',
                     path = main)

# Process the path
b2.process(path = main)
