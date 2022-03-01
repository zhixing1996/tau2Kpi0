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
from variables.MCGenTopo import mc_gen_topo

######################################################
# Specify path to data sample and database
######################################################
arg_dataORmc = 'mc'
# arg_dataORmc = 'data'
if len(sys.argv) > 1:
  arg_dataORmc = str(sys.argv[1])

main = b2.create_path()

if arg_dataORmc == 'data':
    b2.B2INFO("CHECK: analysing data, is this correct?")
    arg_dir = '/besfs5/groups/psip/psipgroup/user/jingmq/Belle2/tau2Kpi0/rootfiles/Kpi0/exMC_Kpi0-1.root'
    if len(sys.argv) > 2:
        arg_dir = str(sys.argv[2])
    print(arg_dir)    
    ma.inputMdstList('default', '%s' % arg_dir, path = main)
    arg_outfile = 'tau2Kpi0_data.root'
    if len(sys.argv) > 3:
        arg_outfile = str(sys.argv[3])
    print(arg_outfile)
        
elif arg_dataORmc == 'mc':
    b2.B2INFO("CHECK: analysing MC, is this correct?")
    arg_dir = '/besfs5/groups/psip/psipgroup/user/jingmq/Belle2/tau2Kpi0/rootfiles/Kpi0/exMC_Kpi0-1.root'
    if len(sys.argv) > 2:
        arg_dir = str(sys.argv[2])
    print(arg_dir)
    ma.inputMdstList('default', '%s' % arg_dir, path = main)
    arg_outfile = 'tau2Kpi0_MC.root'
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
# eff50_May2020
ma.fillParticleList('gamma:good', 'clusterNHits>1.5 and -0.8660 < cosTheta < 0.9563 and E > 0.100', path = main)
ma.reconstructDecay('pi0:gg -> gamma:good gamma:good', '0.115 < InvM < 0.152', path = main)
variables.addAlias('nPi0', 'countInList(pi0:gg)')
# release-04-02-09
ma.cutAndCopyLists('gamma:notpi0', 'gamma:good', 'isDaughterOfList(pi0:gg) == 0 and E > 0.200', path = main)
ma.cutAndCopyLists('gamma:other', 'gamma:good', 'isDaughterOfList(pi0:gg) == 0 and E < 0.200', path = main)
# release-05-02-06
# ma.cutAndCopyLists('gamma:notpi0', 'gamma:good', 'isDescendantOfList(pi0:gg) == 0 and E > 0.200', path = main)
# release-05-02-06
# vertex.kFit('pi0:gg', conf_level = 0, fit_type = 'mass', daughtersUpdate = False, path = main)
# release-04-02-09
vertex.fitVertex('pi0:gg', conf_level = 0, fitter = 'kfitter', fit_type = 'mass', daughtersUpdate = False, path = main)

############################################################################################################
# track
############################################################################################################

# Define quality cuts for tracks
trackCuts = 'dr <= 1. and -3. <= dz <= 3.'

# Fill the particle lists of Kions and gammas with the quality criteria defined above
ma.fillParticleList('e-:good', trackCuts, path = main)
ma.fillParticleList('mu-:good', trackCuts, path = main)
ma.fillParticleList('K+:good', trackCuts, path = main)

modifiedIDcut = 0.5
eIDCuts = 'electronID > {}'.format(modifiedIDcut)
muIDCuts = 'muonID > {}'.format(modifiedIDcut)
KIDCuts = 'kaonID > {}'.format(modifiedIDcut)
variables.addAlias('EoverP', 'formula(ifNANgiveX(clusterE, -1)/p)')

ma.cutAndCopyLists('e-:pid', 'e-:good', eIDCuts, path = main)
ma.cutAndCopyLists('mu-:pid', 'mu-:good', muIDCuts, path = main)
ma.cutAndCopyLists('K-:pid', 'K-:good', KIDCuts, path = main)
variables.addAlias('nElectronTracks', 'countInList(e-:pid)')
variables.addAlias('nMuonTracks', 'countInList(mu-:pid)')
variables.addAlias('nKaonTracks', 'countInList(K-:pid)')

######################################################
# event based cut - 2 tracks in event
######################################################
variables.addAlias('nGoodPhotons', 'countInList(gamma:notpi0)')
# ma.applyEventCuts('((nElectronTracks == 1 and nMuonTracks == 0) or (nMuonTracks == 1 and nElectronTracks == 0))', path = main)
ma.applyEventCuts('nElectronTracks == 1 or nMuonTracks == 1', path = main)
ma.applyEventCuts('nKaonTracks == 1', path = main)

#######################################################
# EventShape and EventKinamatics modules
#######################################################
ma.buildEventShape(['K+:pid', 'e-:pid', 'mu-:pid', 'pi0:gg', 'gamma:notpi0'], path = main)
ma.buildEventKinematics(['K-:pid', 'e-:pid', 'mu-:pid', 'pi0:gg', 'gamma:notpi0'], path = main)

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
                   'formula(daughter(0, daughter(0, cosToThrustOfEvent))*daughter(1, daughter(0, cosToThrustOfEvent)))')
variables.addAlias('cosTheta2',
                   'formula(daughter(0, daughter(1, cosToThrustOfEvent))*daughter(1, daughter(0, cosToThrustOfEvent)))')

ma.applyCuts('vpho', 'cosTheta1 < 0 and cosTheta2 < 0', path = main)
ma.applyEventCuts('thrust > 0.94', path = main)

variables.addAlias('gamma_notpi0_clusterE', 'totalECLEnergyOfParticlesInList(gamma:notpi0)')
variables.addAlias('N_gamma_other', 'countInList(gamma:other)')
variables.addAlias('gamma_other_clusterE', 'totalECLEnergyOfParticlesInList(gamma:other)')
variables.addAlias('gamma_other_E', 'totalEnergyOfParticlesInList(gamma:other)')
variables.addAlias('gamma_other_Px', 'totalPxOfParticlesInList(gamma:other)')
variables.addAlias('gamma_other_Py', 'totalPyOfParticlesInList(gamma:other)')
variables.addAlias('gamma_other_Pz', 'totalPzOfParticlesInList(gamma:other)')

######################################################
# check gammas in each xxxx
######################################################

variables.addAlias('N1prong1InPosThrust', 'countInList(vpho, daughter(1, daughter(0, cosToThrustOfEvent)) > 0)')
variables.addAlias('N1prong1InNegThrust', 'countInList(vpho, daughter(1, daughter(0, cosToThrustOfEvent)) < 0)')
variables.addAlias('NGammaInPosThrust', 'countInList(gamma:notpi0, cosToThrustOfEvent > 0)')
variables.addAlias('NGammaInNegThrust', 'countInList(gamma:notpi0, cosToThrustOfEvent < 0)')

######################################################
# perform MC matching for MC samples
######################################################
if arg_dataORmc == 'mc':
    ma.matchMCTruth('vpho', path = main)
    ma.labelTauPairMC(path = main)
    ma.fillParticleListFromMC('tau+:gen', cut = '', addDaughters = True, path = main)
    ma.fillParticleListFromMC('gamma:gen', '', path = main)
    ma.fillParticleListFromMC('pi0:gen', '', path = main)
    # release-04-02-09
    ma.cutAndCopyLists('gamma:genisr', 'gamma:gen', 'mcMother(abs(PDG)) == 11 and isDaughterOfList(tau+:gen) == 0', path = main)
    ma.cutAndCopyLists('gamma:genisrMinus', 'gamma:gen', 'mcMother(PDG) == 11 and isDaughterOfList(tau+:gen) == 0', path = main)
    ma.cutAndCopyLists('gamma:genisrPlus', 'gamma:gen', 'mcMother(PDG) == -11 and isDaughterOfList(tau+:gen) == 0', path = main)
    ma.cutAndCopyLists('gamma:genfsr', 'gamma:gen', 'mcMother(abs(PDG)) == 15 and isDaughterOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('gamma:genfsrMinus', 'gamma:gen', 'mcMother(PDG) == 15 and isDaughterOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('gamma:genfsrPlus', 'gamma:gen', 'mcMother(PDG) == -15 and isDaughterOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('pi0:genMinus', 'pi0:gen', 'hasAncestor(15,1) and isDaughterOfList(tau+:gen) == 1', path = main)
    ma.cutAndCopyLists('pi0:genPlus', 'pi0:gen', 'hasAncestor(-15,1) and isDaughterOfList(tau+:gen) == 1', path = main)
    # release-05-02-06
    # ma.cutAndCopyLists('gamma:genisr', 'gamma:gen', 'mcMother(abs(PDG)) == 11 and isMCDescendantOfList(tau+:gen) == 0', path = main)
    # ma.cutAndCopyLists('gamma:genisrMinus', 'gamma:gen', 'mcMother(PDG) == 11 and isMCDescendantOfList(tau+:gen) == 0', path = main)
    # ma.cutAndCopyLists('gamma:genisrPlus', 'gamma:gen', 'mcMother(PDG) == -11 and isMCDescendantOfList(tau+:gen) == 0', path = main)
    # ma.cutAndCopyLists('gamma:genfsr', 'gamma:gen', 'mcMother(abs(PDG)) == 15 and isMCDescendantOfList(tau+:gen) == 1', path = main)
    # ma.cutAndCopyLists('gamma:genfsrMinus', 'gamma:gen', 'mcMother(PDG) == 15 and isMCDescendantOfList(tau+:gen) == 1', path = main)
    # ma.cutAndCopyLists('gamma:genfsrPlus', 'gamma:gen', 'mcMother(PDG) == -15 and isMCDescendantOfList(tau+:gen) == 1', path = main)
    # ma.cutAndCopyLists('pi0:genMinus', 'pi0:gen', 'hasAncestor(15,1) and isMCDescendantOfList(tau+:gen) == 1', path = main)
    # ma.cutAndCopyLists('pi0:genPlus', 'pi0:gen', 'hasAncestor(-15,1) and isMCDescendantOfList(tau+:gen) == 1', path = main)
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
eventVariables += ['gamma_notpi0_clusterE', 'N_gamma_other', 'gamma_other_clusterE', 'gamma_other_E', 'gamma_other_Px', 'gamma_other_Py', 'gamma_other_Pz', 'N1prong1InPosThrust', 'N1prong1InNegThrust', 'NGammaInPosThrust', 'NGammaInNegThrust']

commonVariables = vc.kinematics 
commonVariables += ['theta', 'cosTheta', 'phi', 'pt']
commonVariables += ['E_CMS', 'p_CMS', 'px_CMS', 'py_CMS', 'pz_CMS', 'pt_CMS', 'theta_CMS', 'phi_CMS']
commonVariables += ['charge', 'cosToThrustOfEvent']

# -- tau candidate variables
tauVariables =  vc.inv_mass + vc.vertex + ['chiProb']
# -- track level variables
trackVariables = ['clusterE', 'EoverP', 'nCDCHits']
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

if arg_dataORmc == 'mc':
    vphoVariableList = vu.create_aliases_for_selected(list_of_variables = eventVariables + mc_gen_topo(200),
                                                      decay_string = '^vpho') + \
                       vu.create_aliases_for_selected(list_of_variables = commonVariables + tauVariables,
                                                      decay_string = 'vpho -> ^tau+ ^tau-',
                                                      prefix = ['tau_1prong0', 'tau_1prong1']) + \
                       vu.create_aliases_for_selected(list_of_variables = commonVariables + trackVariables + vc.inv_mass,
                                                      decay_string = 'vpho -> [tau- -> ^K- ^pi0] [tau+ -> ^pi+]',
                                                      prefix=['track_1prong0', 'pi0_1prong0', 'track_1prong1']) + \
                       vu.create_aliases_for_selected(list_of_variables = vc.kinematics + ['clusterE'],
                                                      decay_string = 'vpho -> [tau- -> K- [pi0 -> ^gamma ^gamma]] [tau+ -> pi+]',
                                                      prefix=['pi0_gamma0', 'pi0_gamma1'])
if arg_dataORmc == 'data':
    vphoVariableList = vu.create_aliases_for_selected(list_of_variables = eventVariables,
                                                      decay_string = '^vpho') + \
                       vu.create_aliases_for_selected(list_of_variables = commonVariables + tauVariables,
                                                      decay_string = 'vpho -> ^tau+ ^tau-',
                                                      prefix = ['tau_1prong0', 'tau_1prong1']) + \
                       vu.create_aliases_for_selected(list_of_variables = commonVariables + trackVariables + vc.inv_mass,
                                                      decay_string = 'vpho -> [tau- -> ^K- ^pi0] [tau+ -> ^pi+]',
                                                      prefix=['track_1prong0', 'pi0_1prong0', 'track_1prong1']) + \
                       vu.create_aliases_for_selected(list_of_variables = vc.kinematics + ['clusterE'],
                                                      decay_string = 'vpho -> [tau- -> K- [pi0 -> ^gamma ^gamma]] [tau+ -> pi+]',
                                                      prefix=['pi0_gamma0', 'pi0_gamma1'])


# Save the variables to a ROOT file
ma.variablesToNtuple(decayString = 'vpho',
                     variables = vphoVariableList,
                     filename = arg_outfile,
                     treename = 'tau2Kpi0',
                     path = main)

# Process the path
b2.process(path = main)
