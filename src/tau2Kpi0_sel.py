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
import variables.collections as vc
import variables.utils as vu
from variables import variables
import sys
import vertex

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
    # arg_dir = '/nfs/dust/belle2/user/rbkarl/Tau/tauEDM/MC13/MC13TestFiles/*.root'
    arg_dir = '/group/belle2/dataprod/MC/SkimTraining/mixed_BGx1.mdst_000001_prod00009434_task10020000001.root'
    if len(sys.argv) > 2:
        arg_dir = str(sys.argv[2])
    print(arg_dir)
    ma.inputMdstList('default', '%s' % arg_dir, path = main)
    arg_outfile = 'tau1x1_Kpi0.root'
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

######################################################
# create and fill the ParticleLists
######################################################
ma.fillParticleList('e-:all', '', path = main)
ma.fillParticleList('mu-:all', '', path = main)
ma.fillParticleList('K-:all', '', path = main)
ma.fillParticleList('gamma:all', '', path = main)

##################################################################################
# pi0 reconstruction with loose photons 
##################################################################################
gammaDetectorLocation = {
    "FWD" : "clusterReg == 1",
    "BRL" : "clusterReg == 2",
    "BWD" : "clusterReg == 3"
}

gammaForPi0lists = []
for g in gammaDetectorLocation.keys():
    gammaForPi0Cuts = gammaDetectorLocation[g]
    gammaForPi0Cuts += ' and abs(clusterTiming) < 200'
    gammaForPi0Cuts += ' and -0.8660 < cosTheta < 0.9563'
    gammaForPi0Cuts += ' and clusterNHits > 1.5'
    gammaForPi0 = 'gamma:looseForPi0{}'.format(g)
    gammaForPi0lists.append(gammaForPi0)
    ma.cutAndCopyLists(gammaForPi0, 'gamma:all', gammaForPi0Cuts, path = main)

# -# -- -- cos of opening angle between the photons
variables.addAlias('cosAngle2Photons', 
                   'formula((daughter(0, px)*daughter(1, px) + daughter(0, py)*daughter(1, py) + daughter(0, pz)*daughter(1, pz))/daughter(0, p)/daughter(1, p))')
variables.addAlias('leadingclusterE', 'formula(max(daughter(0, clusterE), daughter(1, clusterE)))')
variables.addAlias('subleadingclusterE', 'formula(min(daughter(0, clusterE), daughter(1, clusterE)))')

# Determine pi0 reco for individual Detector Parts
Pi0CutLabel = ["leadingclusterE", "subleadingclusterE", "cosAngle2Photons", "p"]
Pi0CutValue = {
    "FWD,FWD"   :   [0.5625, 0.1625, 0.9458, 0.9444],
    "BRL,BRL"   :   [0.4125, 0.0625, 0.8875, 0.6333],
    "BWD,BWD"   :   [0.4125, 0.1125, 0.8708, 0.6111],
    "BRL,FWD"   :   [0.3625, 0.0875, 0.8875, 0.5889],
    "BRL,BWD"   :   [0.3625, 0.0875, 0.8875, 0.5889]
}

Pi0lists = []
for cut in Pi0CutValue.keys():
    gammalists = cut.split(",")
    CurrentPi0List = 'pi0:fromLooseGammas{}{}'.format(gammalists[0], gammalists[1])
    Pi0lists.append(CurrentPi0List)
    Pi0Cut = '0.15 < M < 0.2'
    for i, c in enumerate(Pi0CutLabel):
        Pi0Cut += ' and {} > {}'.format(c, Pi0CutValue[cut][i])
    ma.reconstructDecay('{} -> gamma:looseForPi0{} gamma:looseForPi0{}'.format(CurrentPi0List, gammalists[0], gammalists[1]), Pi0Cut, path = main)
ma.copyLists('pi0:fromLooseGammas', Pi0lists, path = main)
variables.addAlias('nPi0', 'countInList(pi0:fromLooseGammas)')
ma.cutAndCopyLists('gamma:pi0', gammaForPi0lists, 'isDescendantOfList(pi0:fromLooseGammas) == 1', path=main)
variables.addAlias('nPhotonsFromPi0', 'countInList(gamma:pi0)')
ma.applyEventCuts('nPi0 == 1', path = main)
vertex.kFit('pi0:fromLooseGammas', conf_level=0.0, fit_type = 'mass', path = main)

############################################################################################################
# track
############################################################################################################
trackCuts = '-3.0 < dz < 3.0'
trackCuts += ' and dr < 1.0'
modifiedIDcut = 0.9
variables.addAlias('ModelectronID', 'formula(electronID/(electronID + muonID + kaonID))')
variables.addAlias('ModmuonID', 'formula(muonID/(electronID + muonID + kaonID))')
variables.addAlias('ModkaonID', 'formula(kaonID/(electronID + muonID + pionID + kaonID))')
eIDCuts = 'ModelectronID > {}'.format(modifiedIDcut)
muIDCuts = 'ModmuonID > {}'.format(modifiedIDcut)
piIDCuts = 'ModkaonID > {}'.format(modifiedIDcut)
variables.addAlias('EoverP', 'formula(ifNANgiveX(clusterE, -1)/p)')

ma.cutAndCopyLists('e-:pid', 'e-:all', trackCuts + ' and ' + eIDCuts, path = main)
ma.cutAndCopyLists('mu-:pid', 'mu-:all', trackCuts + ' and ' + muIDCuts, path = main)
ma.cutAndCopyLists('K-:notpid', 'K-:all', trackCuts, path = main)
ma.cutAndCopyLists('K-:pid', 'K-:notpid', piIDCuts, path = main)
variables.addAlias('nElectronTracks', 'countInList(e-:pid)')
variables.addAlias('nMuonTracks', 'countInList(mu-:pid)')
variables.addAlias('nKaonTracks', 'countInList(K-:pid)')

gammaCuts = 'E > 0.2'
gammaCuts += ' and -0.8660 < cosTheta < 0.9563'
gammaCuts += ' and clusterNHits > 1.5'
gammaCuts += ' and isDescendantOfList(pi0:fromLooseGammas) == 0'
ma.cutAndCopyLists('gamma:notPi0', 'gamma:all', gammaCuts, path=main)

######################################################
# event based cut - 2 tracks in event
######################################################
variables.addAlias('nGoodPhotons', 'countInList(gamma:notPi0)')
variables.addAlias('nGoodTracks', 'countInList(K-:notpid)')
ma.applyEventCuts('nGoodTracks == 2', path = main)
ma.applyEventCuts('nElectronTracks == 1 or nMuonTracks == 1', path = main)
ma.applyEventCuts('nKaonTracks == 1', path = main)

#######################################################
# EventShape and EventKinamatics modules
#######################################################
ma.buildEventShape(['K-:notpid','gamma:pi0', 'gamma:notPi0'], path = main)
ma.buildEventKinematics(['K-:notpid','gamma:pi0', 'gamma:notPi0'], path = main)
ma.applyEventCuts('thrust < 0.99 and foxWolframR2 > 0.1', path = main)

######################################################
# Signal and tag sides
#######################################################
# -- 1 prong
ma.reconstructDecay('tau-:e -> e-:pid', '', path = main, dmID = 11)
ma.reconstructDecay('tau-:mu -> mu-:pid', '', path = main, dmID = 13)
ma.reconstructDecay('tau-:Kpi0 -> K-:pid pi0:fromLooseGammas', '', path = main, dmID = 321111)
ma.copyLists('tau+:1prong0', ['tau+:Kpi0'], path = main)
ma.copyLists('tau-:1prong1', ['tau-:e', 'tau-:mu'], path = main)
ma.reconstructDecay('vpho -> tau+:1prong0 tau-:1prong1', '', path = main)
variables.addAlias('dmID_1prong0', 'daughter(0, extraInfo(decayModeID))') # reconstructed tau+ 1-prong decay mode
variables.addAlias('dmID_1prong1', 'daughter(1, extraInfo(decayModeID))') # reconstructed tau- 1-prong decay mode

######################################################
# pions and lepton on the opposide sides
######################################################
variables.addAlias('prod1',
                   'formula(daughter(0, daughter(0, cosToThrustOfEvent))*daughter(1, daughter(0,cosToThrustOfEvent)))')
variables.addAlias('prod2',
                   'formula(daughter(0, daughter(1, cosToThrustOfEvent))*daughter(1, daughter(0,cosToThrustOfEvent)))')
ma.applyCuts('vpho', 'prod1 < 0 and prod2 < 0', path = main)

############################################################################################
# number of photons and pi0 on each side
# put requirements on the number of pi0s on 1-prong to choose the decay mode -> later
############################################################################################
ma.copyList('gamma:1prong0', 'gamma:notPi0', path = main)
ma.copyList('gamma:1prong1', 'gamma:notPi0', path = main)
ma.copyList('pi0:1prong0', 'pi0:fromLooseGammas', path = main)
ma.copyList('pi0:1prong1', 'pi0:fromLooseGammas', path = main)

# tau- (II daughter) on positive or negative side of thrust axis
variables.addAlias('1prong1InPosThrust', 'countInList(vpho, daughter(1, daughter(0,cosToThrustOfEvent)) > 0)')
variables.addAlias('1prong1InNegThrust', 'countInList(vpho, daughter(1, daughter(0,cosToThrustOfEvent)) < 0)')
positiveThrust = b2.create_path()
negativeThrust = b2.create_path()
ma.applyCuts('gamma:1prong1', 'cosToThrustOfEvent > 0', path = positiveThrust)
ma.applyCuts('gamma:1prong0', 'cosToThrustOfEvent < 0', path = positiveThrust)
ma.applyCuts('gamma:1prong1', 'cosToThrustOfEvent < 0', path = negativeThrust)
ma.applyCuts('gamma:1prong0', 'cosToThrustOfEvent > 0', path = negativeThrust)
ma.applyCuts('pi0:1prong1', 'cosToThrustOfEvent > 0', path = positiveThrust)
ma.applyCuts('pi0:1prong0', 'cosToThrustOfEvent < 0', path = positiveThrust)
ma.applyCuts('pi0:1prong1', 'cosToThrustOfEvent < 0', path = negativeThrust)
ma.applyCuts('pi0:1prong0', 'cosToThrustOfEvent > 0', path = negativeThrust)
# totpi0momenta = []
# for P in TotalFourMomentumParticlesInList.keys():
#     for prong in ["1prong1", "1prong0"]:	
#         variables.addAlias('pi0_{}_total_{}'.format(prong, P), 'total{}OfParticlesInList(pi0:{})'.format(TotalFourMomentumParticlesInList[P], prong))
#         totpi0momenta.append('pi0_{}_total_{}'.format(prong,P))

totpi0momenta = []
for P in TotalFourMomentumParticlesInList.keys():
    variables.addAlias('pi0_total_{}'.format(P), 'total{}OfParticlesInList(pi0:fromLooseGammas)'.format(TotalFourMomentumParticlesInList[P]))
    totpi0momenta.append('pi0_total_{}'.format(P))

totKaonmomenta = []
for P in TotalFourMomentumParticlesInList.keys():
    variables.addAlias('pi0_total_{}'.format(P), 'total{}OfParticlesInList(pi0:fromLooseGammas)'.format(TotalFourMomentumParticlesInList[P]))
    totKaonmomenta.append('pi0_total_{}'.format(P))

variables.addAlias('gammas_clusterE', 'totalEnergyOfParticlesInList(gamma:notPi0)')

# take different paths if 1-prong in cosToThrustOfEvent > or < 0
sigThrustModule = main.add_module('VariableToReturnValue', variable = '1prong1InPosThrust')
sigThrustModule.if_value('> 0', positiveThrust, b2.AfterConditionPath.CONTINUE)
sigThrustModule = main.add_module('VariableToReturnValue', variable = '1prong1InNegThrust')
sigThrustModule.if_value('> 0', negativeThrust, b2.AfterConditionPath.CONTINUE)

# the number of photons and pi0s in 1prong0 and 1prong1 hemispheres
variables.addAlias('nPhotons_1prong0', 'nParticlesInList(gamma:1prong0)')
variables.addAlias('nPhotons_1prong1', 'nParticlesInList(gamma:1prong1)')
variables.addAlias('nPi0s_1prong0', 'nParticlesInList(pi0:1prong0)')
variables.addAlias('nPi0s_1prong1', 'nParticlesInList(pi0:1prong1)')

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
                  'nGoodTracks','nElectronTracks', 'nMuonTracks', 'nKaonTracks',
                  'nGoodPhotons', 'nPhotons_1prong0', 'nPhotons_1prong1', 'nPhotonsFromPi0',
                  'nPi0', 'nPi0s_1prong0', 'nPi0s_1prong1'
                 ]
eventVariables += ['thrust', 'foxWolframR2',
                   'visibleEnergyOfEventCMS',
                   'missingMomentumOfEvent', 'missingMomentumOfEvent_theta',
                   'missingMomentumOfEventCMS', 'missingMomentumOfEventCMS_theta',
                   'missingMass2OfEvent'
                  ]
eventVariables += totpi0momenta + totKaonmomenta + ['gammas_clusterE']

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

# -- data specific info
if arg_dataORmc == 'data':
    variables.addAlias('psnm_atleastone', 'L1Trigger')
    eventVariables += ['psnm_atleastone']

n_trigs = 160
for ix in range(n_trigs):
	variables.addAlias('psnm_%i' % ix, 'L1PSNMBit(%i)' % ix)
	eventVariables += ['psnm_%i' % ix]
	variables.addAlias('ftdl_%i' % ix, 'L1FTDLBit(%i)' % ix)
	eventVariables += ['ftdl_%i' % ix]

n_triginput = 159
for iy in range(n_triginput):
    variables.addAlias('triginput_%i' % iy, 'L1InputBit(%i)' % iy)
    eventVariables += ['triginput_%i' % iy]

vphoVariableList = vu.create_aliases_for_selected(list_of_variables = eventVariables,
                                                  decay_string = '^vpho') + \
                   vu.create_aliases_for_selected(list_of_variables = commonVariables + tauVariables,
                                                  decay_string = 'vpho -> ^tau+ ^tau-', 
                                                  prefix = ['tau_1prong0', 'tau_1prong1']) + \
                   vu.create_aliases_for_selected(list_of_variables = commonVariables + trackVariables,
                                                  decay_string = 'vpho -> [tau- -> ^pi- ^pi0] [tau+ -> ^pi+]',
                                                  prefix=['track_1prong0', 'pi0_1prong0', 'track_1prong1'])

######################################################
# Write flat ntuples
######################################################

ma.variablesToNtuple(decayString = 'vpho',
                     variables = vphoVariableList,
                     filename = arg_outfile,
                     treename = 'tau2Kpi0',
                     path = main)
# Process the events
b2.process(main)
print(b2.statistics)
