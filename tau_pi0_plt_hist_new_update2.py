#!/usr/bin/env python
# coding: utf-8

############################################
# # Load MC, apply cuts, plot histograms # #
############################################

import time
import resource
start_time = time.time()


from math import *
from array import *
#import pandas as pd
import fireducks.pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from decimal import *
import numpy as np
from matplotlib.ticker import MultipleLocator
import matplotlib.colors as mc
import colorsys
import matplotlib.ticker
import matplotlib.patches as mpatches
from IPython.display import IFrame
import os


print("done.")


# In[5]:


# # Setting

#
new_data = False # if old data is selected only ECL&CDC can be selected 
trigger_name = 'ECL&CDC' # select one from: 'Pi0-study', 'ECL&CDC'
SB = True #chooses if the graphs should have SB
is_Signal = False # sets pi0all to True
if is_Signal:
    pi0_selection = ["rhorhoMVA"] # select only one from pi0_list = ["Eff50", "Eff40", "Eff30", "Nom", "Opt", "pi0pi0MVA", "rhorhoMVA"]
prong_number = '1prong' #1prong, 3prong
pi0all = False # can be True only if prong_number = 3prong, changes the value to 3prong
pi0cut = 4 #choose number of cuts you want from: 0, 1, 2, 3, 4, 5
el_or_mu = 'elmu' #elmu, el, mu
npi0 = False #creates graphs for npi0s
pi0cuts = True #chooses to create grafs of pt, thrust, visible energy CMS, npi0s, and M3_prong
pi0cuts_sel = 4 #choose which cut histogram from: 1, 2, 3, 4, 5
pi0two = False #chooses to find numbers of only 1 pi0 or at least 2pi 0 ni 3pi2pi0

if npi0:
    nPi0_sel = 'nPi0s_3prong_' + pi0_selection[0] #choose from: 'nPi0s_3prong_' + pi0_selection[0] + 'SB', 'nPi0s_3prong_' + pi0_selection[0], 'nPi0_' + pi0_selection[0]

name_add = '_update2zero'


save_file_location = '/home/judad/update2zero/'



if pi0cuts:
    name_add += "_cutsel" + str(pi0cuts_sel)
if new_data:
    mc_sample = 'taupi0_new_data' #test, taupi0
    name_add += '_new_data'
else:
    mc_sample = 'taupi0' #test, taupi0
    name_add += '_old_data'
    trigger_name = 'ECL&CDC'
    pi0all = False
if pi0cut >= 1:
    name_add += '_cut' + str(pi0cut)
name_add += '_' + trigger_name
name_add += '_' + prong_number
if is_Signal:
    pi0all = True
if pi0all:
    prong_number = '3prong'
if npi0:
    SB = False
    pi0all = True
if pi0two:
    name_add += '_Two'
    
    


name_add += '_weights'

print("-----------------------------------")
print("current settings:")
print("-----------------------------------")
print("MC sample\t",mc_sample)
print("channel:\t",el_or_mu)
print("-----------------------------------")

print("done.")

# define exact colors for each dataset


color_map = {
        'taupair_el_elmu': '#1f77b4',  # Blue
        'taupair_mu_elmu': '#ff7f0e',  # Orange
        'taupair_pi_elmu': '#355E3B',  # Hunter Green
        'taupair_pipi0_elmu': '#d62728',  # Red
        'taupair_bkg_elmu': '#9467bd',  # Purple
        'qqbar': '#8c564b',  # Brown
        'ellellgamma': '#00FFFF', #Teal Cyan 
        'twoPhotons': '#7f7f7f',  # Gray
        'eetautau': '#C7C7C7',  # Light Gray
        'taupair_3pi': '#e377c2',  # Pink
        'taupair_3pipi0': '#CCCC00',  # yellow
        'taupair_3pi2pi0': '#32CD32',  # Lime Green
        'taupair_bkg_3prong': '#17BECF',  # Ocean Blue
        'isSignal': '#2ca02c',  # Green
        'isNotSignal': '#d62728',  # Red
    }
    




# # Load data
if new_data:
    pkl_path="/work/ucjf-belle2/tau/pi0/ntuples/MC15RD/"
else:
     pkl_path="/work/ucjf-belle2/tau/lfu/ntuples/MC15ri/"
# names of data and MC samples
if new_data:
    ntuples_taupair=['taupair']
    ntuples_mcbkg=['ccbar', 'ddbar', 'ssbar', 'uubar', 'charged', 'mixed']
    pi0_list = ["Eff50", "Eff40", "Eff30", "Nom", "Opt", "pi0pi0MVA", "rhorhoMVA"]
    pi0_list_all = []
    if SB:
        for pi0_sel in pi0_list:
            pi0_list_all.append('M_'+pi0_sel+'SBPi0_3pLead')
            pi0_list_all.append('M_'+pi0_sel+'SBPi0_3pSub')
            pi0_list_all.append('M_'+pi0_sel+'SBPi0_3pThird')
    else:
        for pi0_sel in pi0_list:
            pi0_list_all.append('M_'+pi0_sel+'Pi0_3pLead')
            pi0_list_all.append('M_'+pi0_sel+'Pi0_3pSub')
            pi0_list_all.append('M_'+pi0_sel+'Pi0_3pThird')
else:
    ntuples_taupair=['taupair_ri_c1_sub00', 'taupair_ri_c1_sub01', 'taupair_ri_c1_sub02']
    ntuples_mcbkg=['ccbar', 'ddbar', 'ssbar', 'uubar', 'charged', 'mixed', 'mumu', 'ee',
         'eeee', 'eemumu', 'mumumumu', 'eepipi', 'eetautau']
    



# create a dictionary
df_grouped={}

if new_data:
    for key in ntuples_taupair+ntuples_mcbkg:
        print('Loading %s...' % (key))
        filename="tau_pi0_MC15RD_10perc_cuts_noTrig_%s" % (key) # loose eID cut, full data and MC
        df_grouped[key]=pd.read_parquet(pkl_path+filename+'.parquet')
else:
    for key in ntuples_taupair+ntuples_mcbkg:
        print('Loading %s...' % (key))
        filename="lfu_3x1_5_%s_%s_nobase_presel" % (key, 'elmu') # loose eID cut, full data and MC
        df_grouped[key]=pd.read_parquet(pkl_path+filename+'.parquet')

print('done.')


# In[8]:


# # define MC signal

# truth-matched particle ID
el_PDG = "(abs(track_1prong_mcPDG)==11)" #electron/positron
mu_PDG = "(abs(track_1prong_mcPDG)==13)" #muon/antimuon

# reconstructed particle ID
if new_data:
    electron_sample = "(track_1prong_electronID_noSVD_noTOP > 0.9)"
    muon_sample = "(track_1prong_muonID_noSVD > 0.9) and (not track_1prong_electronID_noSVD_noTOP > 0.9)"
    elmu_sample = " ( (%s) or (%s) ) " % (electron_sample, muon_sample)

    electron_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==1) or (tau_1prong_charge == -1 and tauMinusMCMode==1)' #tau->enunu
    muon_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==2) or (tau_1prong_charge == -1 and tauMinusMCMode==2)' #tau->mununu
    pi_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==303) or (tau_1prong_charge == -1 and tauMinusMCMode==303)' #tau->pinu
    pipi0_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==163) or (tau_1prong_charge == -1 and tauMinusMCMode==136)' #tau->pipi0nu
    
    other_channel = '(not ((%s) or (%s) or (%s) or (%s)))'%(electron_channel,muon_channel,pi_channel,pipi0_channel)

else:
    electron_sample = "(track_1prong_pidChargedBDTScore_e > 0.9)" #
    muon_sample = "(track_1prong_muonID_noSVD > 0.9) and (not track_1prong_pidChargedBDTScore_e > 0.9)"
    elmu_sample = " ( (%s) or (%s) ) " % (electron_sample, muon_sample)

    electron_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==1) or (tau_1prong_charge == -1 and tauMinusMCMode==1)' #tau->enunu
    muon_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==2) or (tau_1prong_charge == -1 and tauMinusMCMode==2)' #tau->mununu
    pi_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==303) or (tau_1prong_charge == -1 and tauMinusMCMode==303)' #tau->pinu
    pipi0_channel = '(tau_1prong_charge == 1 and tauPlusMCMode==163) or (tau_1prong_charge == -1 and tauMinusMCMode==136)' #tau->pipi0nu
    
    other_channel = '(not ((%s) or (%s) or (%s) or (%s)))'%(electron_channel,muon_channel,pi_channel,pipi0_channel)
    
# truth-matched tau decay mode


# truth-matched tau 3-prong decay mode
if prong_number == '3prong':
    if not new_data:
        _3pi_channel = '(tau_1prong_charge == -1 and tauPlusMCMode==112) or (tau_1prong_charge == 1 and tauMinusMCMode==112)' #tau->3pinu
        _3pipi0_channel = '(tau_1prong_charge == -1 and tauPlusMCMode==3) or (tau_1prong_charge == 1 and tauMinusMCMode==3)' #tau->3pipi0nu
        _3pi2pi0_channel = '(tau_1prong_charge == -1 and tauPlusMCMode==66) or (tau_1prong_charge == 1 and tauMinusMCMode==66)' #tau->3pi2pi0nu
        
        _other_channel = '(not ((%s) or (%s) or (%s)))'%(_3pi_channel,_3pipi0_channel,_3pi2pi0_channel)
    else:
        _3pi_channel = '(tau_3prong_charge == 1 and tauPlusMCMode==112) or (tau_3prong_charge == -1 and tauMinusMCMode==112)' #tau->3pinu
        _3pipi0_channel = '(tau_3prong_charge == 1 and tauPlusMCMode==3) or (tau_3prong_charge == -1 and tauMinusMCMode==3)' #tau->3pipi0nu
        _3pi2pi0_channel = '(tau_3prong_charge == 1 and tauPlusMCMode==66) or (tau_3prong_charge == -1 and tauMinusMCMode==66)' #tau->3pi2pi0nu
        
        _other_channel = '(not ((%s) or (%s) or (%s)))'%(_3pi_channel,_3pipi0_channel,_3pi2pi0_channel)

# is signal 3-prong
if is_Signal:                                                               
    if SB:
        
        isSignal_NomSBPi0_3pLead_channel = '(isSignal_NomSBPi0_3pLead == 1)'
        isNotSignal_NomSBPi0_3pLead_channel = '(not (%s))'%(isSignal_NomSBPi0_3pLead_channel)
        
        isSignal_NomSBPi0_3pSub_channel = '(isSignal_NomSBPi0_3pSub == 1)'
        isNotSignal_NomSBPi0_3pSub_channel = '(not (%s))'%(isSignal_NomSBPi0_3pSub_channel)
        
        isSignal_NomSBPi0_3pThird_channel = '(isSignal_NomSBPi0_3pThird == 1)'
        isNotSignal_NomSBPi0_3pThird_channel = '(not (%s))'%(isSignal_NomSBPi0_3pThird_channel)
        
        isSignal_Eff50SBPi0_3pLead_channel = '(isSignal_Eff50SBPi0_3pLead == 1)'
        isNotSignal_Eff50SBPi0_3pLead_channel = '(not (%s))'%(isSignal_Eff50SBPi0_3pLead_channel)
        
        isSignal_Eff50SBPi0_3pSub_channel = '(isSignal_Eff50SBPi0_3pSub == 1)'
        isNotSignal_Eff50SBPi0_3pSub_channel = '(not (%s))'%(isSignal_Eff50SBPi0_3pSub_channel)
        
        isSignal_Eff50SBPi0_3pThird_channel = '(isSignal_Eff50SBPi0_3pThird == 1)'
        isNotSignal_Eff50SBPi0_3pThird_channel = '(not (%s))'%(isSignal_Eff50SBPi0_3pThird_channel)
        
        isSignal_Eff40SBPi0_3pLead_channel = '(isSignal_Eff40SBPi0_3pLead == 1)'
        isNotSignal_Eff40SBPi0_3pLead_channel = '(not (%s))'%(isSignal_Eff40SBPi0_3pLead_channel)
        
        isSignal_Eff40SBPi0_3pSub_channel = '(isSignal_Eff40SBPi0_3pSub == 1)'
        isNotSignal_Eff40SBPi0_3pSub_channel = '(not (%s))'%(isSignal_Eff40SBPi0_3pSub_channel)
        
        isSignal_Eff40SBPi0_3pThird_channel = '(isSignal_Eff40SBPi0_3pThird == 1)'
        isNotSignal_Eff40SBPi0_3pThird_channel = '(not (%s))'%(isSignal_Eff40SBPi0_3pThird_channel)
        
        isSignal_Eff30SBPi0_3pLead_channel = '(isSignal_Eff30SBPi0_3pLead == 1)'
        isNotSignal_Eff30SBPi0_3pLead_channel = '(not (%s))'%(isSignal_Eff30SBPi0_3pLead_channel)
        
        isSignal_Eff30SBPi0_3pSub_channel = '(isSignal_Eff30SBPi0_3pSub == 1)'
        isNotSignal_Eff30SBPi0_3pSub_channel = '(not (%s))'%(isSignal_Eff30SBPi0_3pSub_channel)
        
        isSignal_Eff30SBPi0_3pThird_channel = '(isSignal_Eff30SBPi0_3pThird == 1)'
        isNotSignal_Eff30SBPi0_3pThird_channel = '(not (%s))'%(isSignal_Eff30SBPi0_3pThird_channel)
        
        isSignal_OptSBPi0_3pLead_channel = '(isSignal_OptSBPi0_3pLead == 1)'
        isNotSignal_OptSBPi0_3pLead_channel = '(not (%s))'%(isSignal_OptSBPi0_3pLead_channel)
        
        isSignal_OptSBPi0_3pSub_channel = '(isSignal_OptSBPi0_3pSub == 1)'
        isNotSignal_OptSBPi0_3pSub_channel = '(not (%s))'%(isSignal_OptSBPi0_3pSub_channel)
        
        isSignal_OptSBPi0_3pThird_channel = '(isSignal_OptSBPi0_3pThird == 1)'
        isNotSignal_OptSBPi0_3pThird_channel = '(not (%s))'%(isSignal_OptSBPi0_3pThird_channel)
    
        isSignal_pi0pi0MVASBPi0_3pLead_channel = '(isSignal_pi0pi0MVASBPi0_3pLead == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pLead_channel = '(not (%s))'%(isSignal_pi0pi0MVASBPi0_3pLead_channel)
        
        isSignal_pi0pi0MVASBPi0_3pSub_channel = '(isSignal_pi0pi0MVASBPi0_3pSub == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pSub_channel = '(not (%s))'%(isSignal_pi0pi0MVASBPi0_3pSub_channel)
        
        isSignal_pi0pi0MVASBPi0_3pThird_channel = '(isSignal_pi0pi0MVASBPi0_3pThird == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pThird_channel = '(not (%s))'%(isSignal_pi0pi0MVASBPi0_3pThird_channel)
        
        isSignal_rhorhoMVASBPi0_3pLead_channel = '(isSignal_rhorhoMVASBPi0_3pLead == 1)'
        isNotSignal_rhorhoMVASBPi0_3pLead_channel = '(not (%s))'%(isSignal_rhorhoMVASBPi0_3pLead_channel)
        
        isSignal_rhorhoMVASBPi0_3pSub_channel = '(isSignal_rhorhoMVASBPi0_3pSub == 1)'
        isNotSignal_rhorhoMVASBPi0_3pSub_channel = '(not (%s))'%(isSignal_rhorhoMVASBPi0_3pSub_channel)
        
        isSignal_rhorhoMVASBPi0_3pThird_channel = '(isSignal_rhorhoMVASBPi0_3pThird == 1)'
        isNotSignal_rhorhoMVASBPi0_3pThird_channel = '(not (%s))'%(isSignal_rhorhoMVASBPi0_3pThird_channel)
        '''

        isSignal_NomSBPi0_3pLead_channel = '(isSignal_NomSBPi0_3pLead == 1)'
        isNotSignal_NomSBPi0_3pLead_channel = '(isSignal_NomSBPi0_3pLead == 0)'
        
        isSignal_NomSBPi0_3pSub_channel = '(isSignal_NomSBPi0_3pSub == 1)'
        isNotSignal_NomSBPi0_3pSub_channel = '(isSignal_NomSBPi0_3pSub == 0)'
        
        isSignal_NomSBPi0_3pThird_channel = '(isSignal_NomSBPi0_3pThird == 1)'
        isNotSignal_NomSBPi0_3pThird_channel = '(isSignal_NomSBPi0_3pThird == 0)'
        
        isSignal_Eff50SBPi0_3pLead_channel = '(isSignal_Eff50SBPi0_3pLead == 1)'
        isNotSignal_Eff50SBPi0_3pLead_channel = '(isSignal_Eff50SBPi0_3pLead == 0)'
        
        isSignal_Eff50SBPi0_3pSub_channel = '(isSignal_Eff50SBPi0_3pSub == 1)'
        isNotSignal_Eff50SBPi0_3pSub_channel = '(isSignal_Eff50SBPi0_3pSub == 0)'
        
        isSignal_Eff50SBPi0_3pThird_channel = '(isSignal_Eff50SBPi0_3pThird == 1)'
        isNotSignal_Eff50SBPi0_3pThird_channel = '(isSignal_Eff50SBPi0_3pThird == 0)'
        
        isSignal_Eff40SBPi0_3pLead_channel = '(isSignal_Eff40SBPi0_3pLead == 1)'
        isNotSignal_Eff40SBPi0_3pLead_channel = '(isSignal_Eff40SBPi0_3pLead == 0)'
        
        isSignal_Eff40SBPi0_3pSub_channel = '(isSignal_Eff40SBPi0_3pSub == 1)'
        isNotSignal_Eff40SBPi0_3pSub_channel = '(isSignal_Eff40SBPi0_3pSub == 0)'
        
        isSignal_Eff40SBPi0_3pThird_channel = '(isSignal_Eff40SBPi0_3pThird == 1)'
        isNotSignal_Eff40SBPi0_3pThird_channel = '(isSignal_Eff40SBPi0_3pThird == 0)'
        
        isSignal_Eff30SBPi0_3pLead_channel = '(isSignal_Eff30SBPi0_3pLead == 1)'
        isNotSignal_Eff30SBPi0_3pLead_channel = '(isSignal_Eff30SBPi0_3pLead == 0)'
        
        isSignal_Eff30SBPi0_3pSub_channel = '(isSignal_Eff30SBPi0_3pSub == 1)'
        isNotSignal_Eff30SBPi0_3pSub_channel = '(isSignal_Eff30SBPi0_3pSub == 0)'
        
        isSignal_Eff30SBPi0_3pThird_channel = '(isSignal_Eff30SBPi0_3pThird == 1)'
        isNotSignal_Eff30SBPi0_3pThird_channel = '(isSignal_Eff30SBPi0_3pThird == 0)'
        
        isSignal_OptSBPi0_3pLead_channel = '(isSignal_OptSBPi0_3pLead == 1)'
        isNotSignal_OptSBPi0_3pLead_channel = '(isSignal_OptSBPi0_3pLead == 0)'
        
        isSignal_OptSBPi0_3pSub_channel = '(isSignal_OptSBPi0_3pSub == 1)'
        isNotSignal_OptSBPi0_3pSub_channel = '(isSignal_OptSBPi0_3pSub == 0)'
        
        isSignal_OptSBPi0_3pThird_channel = '(isSignal_OptSBPi0_3pThird == 1)'
        isNotSignal_OptSBPi0_3pThird_channel = '(isSignal_OptSBPi0_3pThird == 0)'
    
        isSignal_pi0pi0MVASBPi0_3pLead_channel = '(isSignal_pi0pi0MVASBPi0_3pLead == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pLead_channel = '(isSignal_pi0pi0MVASBPi0_3pLead == 0)'
        
        isSignal_pi0pi0MVASBPi0_3pSub_channel = '(isSignal_pi0pi0MVASBPi0_3pSub == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pSub_channel = '(isSignal_pi0pi0MVASBPi0_3pSub == 0)'
        
        isSignal_pi0pi0MVASBPi0_3pThird_channel = '(isSignal_pi0pi0MVASBPi0_3pThird == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pThird_channel = '(isSignal_pi0pi0MVASBPi0_3pThird == 0)'
        
        isSignal_rhorhoMVASBPi0_3pLead_channel = '(isSignal_rhorhoMVASBPi0_3pLead == 1)'
        isNotSignal_rhorhoMVASBPi0_3pLead_channel = '(isSignal_rhorhoMVASBPi0_3pLead == 0)'
        
        isSignal_rhorhoMVASBPi0_3pSub_channel = '(isSignal_rhorhoMVASBPi0_3pSub == 1)'
        isNotSignal_rhorhoMVASBPi0_3pSub_channel = '(isSignal_rhorhoMVASBPi0_3pSub == 0)'
        
        isSignal_rhorhoMVASBPi0_3pThird_channel = '(isSignal_rhorhoMVASBPi0_3pThird == 1)'
        isNotSignal_rhorhoMVASBPi0_3pThird_channel = '(isSignal_rhorhoMVASBPi0_3pThird == 0)' 
        '''
    
    else:                                                                                                       #without SB 
        isSignal_NomSBPi0_3pLead_channel = '(isSignal_NomPi0_3pLead == 1)'
        isNotSignal_NomSBPi0_3pLead_channel = '(isSignal_NomPi0_3pLead == 0)'
        
        isSignal_NomSBPi0_3pSub_channel = '(isSignal_NomPi0_3pSub == 1)'
        isNotSignal_NomSBPi0_3pSub_channel = '(isSignal_NomPi0_3pSub == 0)'
        
        isSignal_NomSBPi0_3pThird_channel = '(isSignal_NomPi0_3pThird == 1)'
        isNotSignal_NomSBPi0_3pThird_channel = '(isSignal_NomPi0_3pThird == 0)'
        
        isSignal_Eff50SBPi0_3pLead_channel = '(isSignal_Eff50Pi0_3pLead == 1)'
        isNotSignal_Eff50SBPi0_3pLead_channel = '(isSignal_Eff50Pi0_3pLead == 0)'
        
        isSignal_Eff50SBPi0_3pSub_channel = '(isSignal_Eff50Pi0_3pSub == 1)'
        isNotSignal_Eff50SBPi0_3pSub_channel = '(isSignal_Eff50Pi0_3pSub == 0)'
        
        isSignal_Eff50SBPi0_3pThird_channel = '(isSignal_Eff50Pi0_3pThird == 1)'
        isNotSignal_Eff50SBPi0_3pThird_channel = '(isSignal_Eff50Pi0_3pThird == 0)'
        
        isSignal_Eff40SBPi0_3pLead_channel = '(isSignal_Eff40Pi0_3pLead == 1)'
        isNotSignal_Eff40SBPi0_3pLead_channel = '(isSignal_Eff40Pi0_3pLead == 0)'
        
        isSignal_Eff40SBPi0_3pSub_channel = '(isSignal_Eff40Pi0_3pSub == 1)'
        isNotSignal_Eff40SBPi0_3pSub_channel = '(isSignal_Eff40Pi0_3pSub == 0)'
        
        isSignal_Eff40SBPi0_3pThird_channel = '(isSignal_Eff40Pi0_3pThird == 1)'
        isNotSignal_Eff40SBPi0_3pThird_channel = '(isSignal_Eff40Pi0_3pThird == 0)'
        
        isSignal_Eff30SBPi0_3pLead_channel = '(isSignal_Eff30Pi0_3pLead == 1)'
        isNotSignal_Eff30SBPi0_3pLead_channel = '(isSignal_Eff30Pi0_3pLead == 0)'
        
        isSignal_Eff30SBPi0_3pSub_channel = '(isSignal_Eff30Pi0_3pSub == 1)'
        isNotSignal_Eff30SBPi0_3pSub_channel = '(isSignal_Eff30Pi0_3pSub == 0)'
        
        isSignal_Eff30SBPi0_3pThird_channel = '(isSignal_Eff30Pi0_3pThird == 1)'
        isNotSignal_Eff30SBPi0_3pThird_channel = '(isSignal_Eff30Pi0_3pThird == 0)'
        
        isSignal_OptSBPi0_3pLead_channel = '(isSignal_OptPi0_3pLead == 1)'
        isNotSignal_OptSBPi0_3pLead_channel = '(isSignal_OptPi0_3pLead == 0)'
        
        isSignal_OptSBPi0_3pSub_channel = '(isSignal_OptPi0_3pSub == 1)'
        isNotSignal_OptSBPi0_3pSub_channel = '(isSignal_OptPi0_3pSub == 0)'
        
        isSignal_OptSBPi0_3pThird_channel = '(isSignal_OptPi0_3pThird == 1)'
        isNotSignal_OptSBPi0_3pThird_channel = '(isSignal_OptPi0_3pThird == 0)'
    
        isSignal_pi0pi0MVASBPi0_3pLead_channel = '(isSignal_pi0pi0MVAPi0_3pLead == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pLead_channel = '(isSignal_pi0pi0MVAPi0_3pLead == 0)'
        
        isSignal_pi0pi0MVASBPi0_3pSub_channel = '(isSignal_pi0pi0MVAPi0_3pSub == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pSub_channel = '(isSignal_pi0pi0MVAPi0_3pSub == 0)'
        
        isSignal_pi0pi0MVASBPi0_3pThird_channel = '(isSignal_pi0pi0MVAPi0_3pThird == 1)'
        isNotSignal_pi0pi0MVASBPi0_3pThird_channel = '(isSignal_pi0pi0MVAPi0_3pThird == 0)'
        
        isSignal_rhorhoMVASBPi0_3pLead_channel = '(isSignal_rhorhoMVAPi0_3pLead == 1)'
        isNotSignal_rhorhoMVASBPi0_3pLead_channel = '(isSignal_rhorhoMVAPi0_3pLead == 0)'
        
        isSignal_rhorhoMVASBPi0_3pSub_channel = '(isSignal_rhorhoMVAPi0_3pSub == 1)'
        isNotSignal_rhorhoMVASBPi0_3pSub_channel = '(isSignal_rhorhoMVAPi0_3pSub == 0)'
        
        isSignal_rhorhoMVASBPi0_3pThird_channel = '(isSignal_rhorhoMVAPi0_3pThird == 1)'
        isNotSignal_rhorhoMVASBPi0_3pThird_channel = '(isSignal_rhorhoMVAPi0_3pThird == 0)'



    




print('done.')


# In[9]:


# merge taupair, select MC signals

print('Merging taupair ntuples...')
if new_data:
    df_grouped['taupair_all'] = df_grouped['taupair']
else:
    df_grouped['taupair_all'] = pd.concat([df_grouped['taupair_ri_c1_sub00'],df_grouped['taupair_ri_c1_sub01'],df_grouped['taupair_ri_c1_sub02']]).query(elmu_sample).reset_index(drop=True)

    
print('done.')
print('taupair_all',len(df_grouped['taupair_all']))


# In[10]:

#print("Available columns:", df_grouped['taupair_all'].columns.tolist())
#print("Query string:", repr(_3pi_channel))

# apply signal selection on taupair sample

if el_or_mu == 'elmu':
    if is_Signal == False:
        if prong_number == '1prong':
            print('elmu channel')
            print('selecting electron mode...')
            df_grouped['taupair_el_elmu']=df_grouped['taupair_all'].query(electron_channel).reset_index(drop=True)
            print('selecting muon mode...')
            df_grouped['taupair_mu_elmu']=df_grouped['taupair_all'].query(muon_channel).reset_index(drop=True)
            print('selecting pi mode...')
            df_grouped['taupair_pi_elmu']=df_grouped['taupair_all'].query(pi_channel).reset_index(drop=True)
            print('selecting pipi0 mode...')
            df_grouped['taupair_pipi0_elmu']=df_grouped['taupair_all'].query(pipi0_channel).reset_index(drop=True)
            print('selecting background...')
            df_grouped['taupair_bkg_elmu']=df_grouped['taupair_all'].query(other_channel).reset_index(drop=True)
            
        #added 3prong
        if prong_number == '3prong':
            print('selecting 3pi mode...')
            df_grouped['taupair_3pi']=df_grouped['taupair_all'].query(_3pi_channel).reset_index(drop=True)
            print('selecting 3pipi0 mode...')
            df_grouped['taupair_3pipi0']=df_grouped['taupair_all'].query(_3pipi0_channel).reset_index(drop=True)
            print('selecting 3pi2pi0 mode...')
            df_grouped['taupair_3pi2pi0']=df_grouped['taupair_all'].query(_3pi2pi0_channel).reset_index(drop=True)
            print('selecting background...')
            df_grouped['taupair_bkg_3prong']=df_grouped['taupair_all'].query(_other_channel).reset_index(drop=True)

            

    elif npi0:   
        # selects only one from pi0_list = ["Eff50", "Eff40", "Eff30", "Nom", "Opt", "pi0pi0MVA", "rhorhoMVA"]
        pi0_list = pi0_selection
        if not pi0two:
            if pi0_list == ["Eff50"]:
                print('selecting isSignal_Eff50SBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Eff40"]:
                print('selecting isSignal_Eff40SBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Eff30"]:
                print('selecting isSignal_Eff30SBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Nom"]:
                print('selecting isSignal_NomSBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_NomSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_NomSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_NomSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Opt"]:
                print('selecting isSignal_OptSBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_OptSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_OptSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_OptSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["pi0pi0MVA"]:
                print('selecting isSignal_pi0pi0MVASBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["rhorhoMVA"]:
                print('selecting isSignal_rhorhoMVASBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pLead_3pi2pi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pSub_3pi mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                    

            
        else:
            if pi0_list == ["Eff50"]:
                print('selecting isSignal_Eff50SBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_Eff50SBPi0_3pLead_channel + ') and not (' + isSignal_Eff50SBPi0_3pSub_channel + ') and not (' + isSignal_Eff50SBPi0_3pThird_channel + ' )) or ((' + isSignal_Eff50SBPi0_3pSub_channel + ') and not (' + isSignal_Eff50SBPi0_3pLead_channel + ') and not (' + isSignal_Eff50SBPi0_3pThird_channel + ' )) or ((' + isSignal_Eff50SBPi0_3pThird_channel + ') and not (' + isSignal_Eff50SBPi0_3pLead_channel + ') and not (' + isSignal_Eff50SBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_Eff50SBPi0_3pLead_channel + ') and (' + isSignal_Eff50SBPi0_3pSub_channel  + ')) or ((' + isSignal_Eff50SBPi0_3pLead_channel + ') and (' + isSignal_Eff50SBPi0_3pThird_channel  + ')) or ((' + isSignal_Eff50SBPi0_3pSub_channel + ') and (' + isSignal_Eff50SBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_Eff50SBPi0_3pLead_channel + ') and (' + isSignal_Eff50SBPi0_3pSub_channel  + ') and (' + isSignal_Eff50SBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                
                print('selecting isNotSignal_Eff50SBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff50SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff50SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff50SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff50SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff50SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Eff40"]:
                print('selecting isSignal_Eff40SBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1 pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_Eff40SBPi0_3pLead_channel + ') and not (' + isSignal_Eff40SBPi0_3pSub_channel + ') and not (' + isSignal_Eff40SBPi0_3pThird_channel + ' )) or ((' + isSignal_Eff40SBPi0_3pSub_channel + ') and not (' + isSignal_Eff40SBPi0_3pLead_channel + ') and not (' + isSignal_Eff40SBPi0_3pThird_channel + ' )) or ((' + isSignal_Eff40SBPi0_3pThird_channel + ') and not (' + isSignal_Eff40SBPi0_3pLead_channel + ') and not (' + isSignal_Eff40SBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2 pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_Eff40SBPi0_3pLead_channel + ') and (' + isSignal_Eff40SBPi0_3pSub_channel  + ')) or ((' + isSignal_Eff40SBPi0_3pLead_channel + ') and (' + isSignal_Eff40SBPi0_3pThird_channel  + ')) or ((' + isSignal_Eff40SBPi0_3pSub_channel + ') and (' + isSignal_Eff40SBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_Eff40SBPi0_3pLead_channel + ') and (' + isSignal_Eff40SBPi0_3pSub_channel  + ') and (' + isSignal_Eff40SBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting isNotSignal_Eff40SBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff40SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff40SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff40SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff40SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff40SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Eff30"]:
                print('selecting isSignal_Eff30SBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1 pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_Eff30SBPi0_3pLead_channel + ') and not (' + isSignal_Eff30SBPi0_3pSub_channel + ') and not (' + isSignal_Eff30SBPi0_3pThird_channel + ' )) or ((' + isSignal_Eff30SBPi0_3pSub_channel + ') and not (' + isSignal_Eff30SBPi0_3pLead_channel + ') and not (' + isSignal_Eff30SBPi0_3pThird_channel + ' )) or ((' + isSignal_Eff30SBPi0_3pThird_channel + ') and not (' + isSignal_Eff30SBPi0_3pLead_channel + ') and not (' + isSignal_Eff30SBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2 pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_Eff30SBPi0_3pLead_channel + ') and (' + isSignal_Eff30SBPi0_3pSub_channel  + ')) or ((' + isSignal_Eff30SBPi0_3pLead_channel + ') and (' + isSignal_Eff30SBPi0_3pThird_channel  + ')) or ((' + isSignal_Eff30SBPi0_3pSub_channel + ') and (' + isSignal_Eff30SBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_Eff30SBPi0_3pLead_channel + ') and (' + isSignal_Eff30SBPi0_3pSub_channel  + ') and (' + isSignal_Eff30SBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting isNotSignal_Eff30SBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_Eff30SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_Eff30SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_Eff30SBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_Eff30SBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_Eff30SBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Nom"]:
                print('selecting isSignal_NomSBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_NomSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1 pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_NomSBPi0_3pLead_channel + ') and not (' + isSignal_NomSBPi0_3pSub_channel + ') and not (' + isSignal_NomSBPi0_3pThird_channel + ' )) or ((' + isSignal_NomSBPi0_3pSub_channel + ') and not (' + isSignal_NomSBPi0_3pLead_channel + ') and not (' + isSignal_NomSBPi0_3pThird_channel + ' )) or ((' + isSignal_NomSBPi0_3pThird_channel + ') and not (' + isSignal_NomSBPi0_3pLead_channel + ') and not (' + isSignal_NomSBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2 pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_NomSBPi0_3pLead_channel + ') and (' + isSignal_NomSBPi0_3pSub_channel  + ')) or ((' + isSignal_NomSBPi0_3pLead_channel + ') and (' + isSignal_NomSBPi0_3pThird_channel  + ')) or ((' + isSignal_NomSBPi0_3pSub_channel + ') and (' + isSignal_NomSBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_NomSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_NomSBPi0_3pLead_channel + ') and (' + isSignal_NomSBPi0_3pSub_channel  + ') and (' + isSignal_NomSBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting isNotSignal_NomSBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_NomSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_NomSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_NomSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_NomSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_NomSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_NomSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_NomSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["Opt"]:
                print('selecting isSignal_OptSBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_OptSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1 pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_OptSBPi0_3pLead_channel + ') and not (' + isSignal_OptSBPi0_3pSub_channel + ') and not (' + isSignal_OptSBPi0_3pThird_channel + ' )) or ((' + isSignal_OptSBPi0_3pSub_channel + ') and not (' + isSignal_OptSBPi0_3pLead_channel + ') and not (' + isSignal_OptSBPi0_3pThird_channel + ' )) or ((' + isSignal_OptSBPi0_3pThird_channel + ') and not (' + isSignal_OptSBPi0_3pLead_channel + ') and not (' + isSignal_OptSBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2 pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_OptSBPi0_3pLead_channel + ') and (' + isSignal_OptSBPi0_3pSub_channel  + ')) or ((' + isSignal_OptSBPi0_3pLead_channel + ') and (' + isSignal_OptSBPi0_3pThird_channel  + ')) or ((' + isSignal_OptSBPi0_3pSub_channel + ') and (' + isSignal_OptSBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_OptSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_OptSBPi0_3pLead_channel + ') and (' + isSignal_OptSBPi0_3pSub_channel  + ') and (' + isSignal_OptSBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting isNotSignal_OptSBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_OptSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_OptSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_OptSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_OptSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_OptSBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_OptSBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_OptSBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["pi0pi0MVA"]:
                print('selecting isSignal_pi0pi0MVASBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1 pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_pi0pi0MVASBPi0_3pLead_channel + ') and not (' + isSignal_pi0pi0MVASBPi0_3pSub_channel + ') and not (' + isSignal_pi0pi0MVASBPi0_3pThird_channel + ' )) or ((' + isSignal_pi0pi0MVASBPi0_3pSub_channel + ') and not (' + isSignal_pi0pi0MVASBPi0_3pLead_channel + ') and not (' + isSignal_pi0pi0MVASBPi0_3pThird_channel + ' )) or ((' + isSignal_pi0pi0MVASBPi0_3pThird_channel + ') and not (' + isSignal_pi0pi0MVASBPi0_3pLead_channel + ') and not (' + isSignal_pi0pi0MVASBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2 pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_pi0pi0MVASBPi0_3pLead_channel + ') and (' + isSignal_pi0pi0MVASBPi0_3pSub_channel  + ')) or ((' + isSignal_pi0pi0MVASBPi0_3pLead_channel + ') and (' + isSignal_pi0pi0MVASBPi0_3pThird_channel  + ')) or ((' + isSignal_pi0pi0MVASBPi0_3pSub_channel + ') and (' + isSignal_pi0pi0MVASBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_pi0pi0MVASBPi0_3pLead_channel + ') and (' + isSignal_pi0pi0MVASBPi0_3pSub_channel  + ') and (' + isSignal_pi0pi0MVASBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_pi0pi0MVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
            if pi0_list == ["rhorhoMVA"]:
                print('selecting isSignal_rhorhoMVASBPi0_3pLead_3pi mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pLead_3pi mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pLead_3pipi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pLead_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                
                print('selecting 1 pi0 3pi2pi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_rhorhoMVASBPi0_3pLead_channel + ') and not (' + isSignal_rhorhoMVASBPi0_3pSub_channel + ') and not (' + isSignal_rhorhoMVASBPi0_3pThird_channel + ' )) or ((' + isSignal_rhorhoMVASBPi0_3pSub_channel + ') and not (' + isSignal_rhorhoMVASBPi0_3pLead_channel + ') and not (' + isSignal_rhorhoMVASBPi0_3pThird_channel + ' )) or ((' + isSignal_rhorhoMVASBPi0_3pThird_channel + ') and not (' + isSignal_rhorhoMVASBPi0_3pLead_channel + ') and not (' + isSignal_rhorhoMVASBPi0_3pSub_channel + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 2 pi0 3pi2pi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead_3pi2pi0'] = df_grouped['taupair_all'].query('( ((' + isSignal_rhorhoMVASBPi0_3pLead_channel + ') and (' + isSignal_rhorhoMVASBPi0_3pSub_channel  + ')) or ((' + isSignal_rhorhoMVASBPi0_3pLead_channel + ') and (' + isSignal_rhorhoMVASBPi0_3pThird_channel  + ')) or ((' + isSignal_rhorhoMVASBPi0_3pSub_channel + ') and (' + isSignal_rhorhoMVASBPi0_3pThird_channel  + ')) ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                
                print('selecting 3pi0 3pi2pi0 mode... mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('( (' + isSignal_rhorhoMVASBPi0_3pLead_channel + ') and (' + isSignal_rhorhoMVASBPi0_3pSub_channel  + ') and (' + isSignal_rhorhoMVASBPi0_3pThird_channel + ') ) and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
    
                print('selecting isNotSignal_rhorhoMVASBPi0_3pSub_3pi mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pSub_3pipi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pSub_3pi2pi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pSub_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pThird_3pi mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pThird_3pi mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird_3pi'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pThird_3pipi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird_3pipi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pipi0_channel + ')').reset_index(drop=True)
                print('selecting isSignal_rhorhoMVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_Signal_rhorhoMVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)
                print('selecting isNotSignal_rhorhoMVASBPi0_3pThird_3pi2pi0 mode...')
                df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird_3pi2pi0'] = df_grouped['taupair_all'].query('(' + isNotSignal_rhorhoMVASBPi0_3pThird_channel +') and (' + _3pi2pi0_channel + ')').reset_index(drop=True)

            
    # isSignal
    elif is_Signal:
        # selects only one from pi0_list = ["Eff50", "Eff40", "Eff30", "Nom", "Opt", "pi0pi0MVA", "rhorhoMVA"]
        pi0_list = pi0_selection

        if pi0_list == ["Nom"]:
            print('selecting isSignal_NomSBPi0_3pLead mode...')
            df_grouped['is_Signal_NomSBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_NomSBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_NomSBPi0_3pLead mode...')
            df_grouped['is_NotSignal_NomSBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_NomSBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_NomSBPi0_3pSub mode...')
            df_grouped['is_Signal_NomSBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_NomSBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting isNotSignal_NomSBPi0_3pSub mode...')
            df_grouped['is_NotSignal_NomSBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_NomSBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_NomSBPi0_3pThird mode...')
            df_grouped['is_Signal_NomSBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_NomSBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting isNotSignal_NomSBPi0_3pThird mode...')
            df_grouped['is_NotSignal_NomSBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_NomSBPi0_3pThird_channel).reset_index(drop=True)
        elif pi0_list == ["Eff50"]:
            print('selecting isSignal_Eff50SBPi0_3pLead mode...')
            df_grouped['is_Signal_Eff50SBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_Eff50SBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff50SBPi0_3pLead mode...')
            df_grouped['is_NotSignal_Eff50SBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_Eff50SBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_Eff50SBPi0_3pSub mode...')
            df_grouped['is_Signal_Eff50SBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_Eff50SBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff50SBPi0_3pSub mode...')
            df_grouped['is_NotSignal_Eff50SBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_Eff50SBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_Eff50SBPi0_3pThird mode...')
            df_grouped['is_Signal_Eff50SBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_Eff50SBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff50SBPi0_3pThird mode...')
            df_grouped['is_NotSignal_Eff50SBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_Eff50SBPi0_3pThird_channel).reset_index(drop=True)
        elif pi0_list == ["Eff40"]:
            print('selecting isSignal_Eff40SBPi0_3pLead mode...')
            df_grouped['is_Signal_Eff40SBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_Eff40SBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff40SBPi0_3pLead mode...')
            df_grouped['is_NotSignal_Eff40SBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_Eff40SBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_Eff40SBPi0_3pSub mode...')
            df_grouped['is_Signal_Eff40SBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_Eff40SBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff40SBPi0_3pSub mode...')
            df_grouped['is_NotSignal_Eff40SBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_Eff40SBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_Eff40SBPi0_3pThird mode...')
            df_grouped['is_Signal_Eff40SBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_Eff40SBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting is_NotSignal_Eff40SBPi0_3pThird mode...')
            df_grouped['is_NotSignal_Eff40SBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_Eff40SBPi0_3pThird_channel).reset_index(drop=True)
        elif pi0_list == ["Eff30"]:
            print('selecting isSignal_Eff30SBPi0_3pLead mode...')
            df_grouped['is_Signal_Eff30SBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_Eff30SBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff30SBPi0_3pLead mode...')
            df_grouped['is_NotSignal_Eff30SBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_Eff30SBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_Eff30SBPi0_3pSub mode...')
            df_grouped['is_Signal_Eff30SBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_Eff30SBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting is_NotSignal_Eff30SBPi0_3pSub mode...')
            df_grouped['is_NotSignal_Eff30SBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_Eff30SBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_Eff30SBPi0_3pThird mode...')
            df_grouped['is_Signal_Eff30SBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_Eff30SBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting isNotSignal_Eff30SBPi0_3pThird mode...')
            df_grouped['is_NotSignal_Eff30SBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_Eff30SBPi0_3pThird_channel).reset_index(drop=True)
        elif pi0_list == ["Opt"]:
            print('selecting isSignal_OptSBPi0_3pLead mode...')
            df_grouped['is_Signal_OptSBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_OptSBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_OptSBPi0_3pLead mode...')
            df_grouped['is_NotSignal_OptSBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_OptSBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_OptSBPi0_3pSub mode...')
            df_grouped['is_Signal_OptSBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_OptSBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting isNotSignal_OptSBPi0_3pSub mode...')
            df_grouped['is_NotSignal_OptSBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_OptSBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_OptSBPi0_3pThird mode...')
            df_grouped['is_Signal_OptSBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_OptSBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting isNotSignal_OptSBPi0_3pThird mode...')
            df_grouped['is_NotSignal_OptSBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_OptSBPi0_3pThird_channel).reset_index(drop=True)
        elif pi0_list == ["pi0pi0MVA"]:
            print('selecting isSignal_pi0pi0MVASBPi0_3pLead mode...')
            df_grouped['is_Signal_pi0pi0MVASBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_pi0pi0MVASBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_pi0pi0MVASBPi0_3pLead mode...')
            df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_pi0pi0MVASBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_pi0pi0MVASBPi0_3pSub mode...')
            df_grouped['is_Signal_pi0pi0MVASBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_pi0pi0MVASBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting isNotSignal_pi0pi0MVASBPi0_3pSub mode...')
            df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_pi0pi0MVASBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_pi0pi0MVASBPi0_3pThird mode...')
            df_grouped['is_Signal_pi0pi0MVASBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_pi0pi0MVASBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting isNotSignal_pi0pi0MVASBPi0_3pThird mode...')
            df_grouped['is_NotSignal_pi0pi0MVASBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_pi0pi0MVASBPi0_3pThird_channel).reset_index(drop=True)
        elif pi0_list == ["rhorhoMVA"]:
            print('selecting isSignal_rhorhoMVASBPi0_3pLead mode...')
            df_grouped['is_Signal_rhorhoMVASBPi0_3pLead']=df_grouped['taupair_all'].query(isSignal_rhorhoMVASBPi0_3pLead_channel).reset_index(drop=True)
            print('selecting isNotSignal_rhorhoMVASBPi0_3pLead mode...')
            df_grouped['is_NotSignal_rhorhoMVASBPi0_3pLead']=df_grouped['taupair_all'].query(isNotSignal_rhorhoMVASBPi0_3pLead_channel).reset_index(drop=True)
            
            print('selecting isSignal_rhorhoMVASBPi0_3pSub mode...')
            df_grouped['is_Signal_rhorhoMVASBPi0_3pSub']=df_grouped['taupair_all'].query(isSignal_rhorhoMVASBPi0_3pSub_channel).reset_index(drop=True)
            print('selecting isNotSignal_rhorhoMVASBPi0_3pSub mode...')
            df_grouped['is_NotSignal_rhorhoMVASBPi0_3pSub']=df_grouped['taupair_all'].query(isNotSignal_rhorhoMVASBPi0_3pSub_channel).reset_index(drop=True)
            
            print('selecting isSignal_rhorhoMVASBPi0_3pThird mode...')
            df_grouped['is_Signal_rhorhoMVASBPi0_3pThird']=df_grouped['taupair_all'].query(isSignal_rhorhoMVASBPi0_3pThird_channel).reset_index(drop=True)
            print('selecting isNotSignal_rhorhoMVASBPi0_3pThird mode...')
            df_grouped['is_NotSignal_rhorhoMVASBPi0_3pThird']=df_grouped['taupair_all'].query(isNotSignal_rhorhoMVASBPi0_3pThird_channel).reset_index(drop=True)
        
    

print('done.')  


# In[11]:


# merge mc bkg

print('Merging non-taupair background ntuples...')
if new_data:
    df_grouped['qqbar']=pd.concat([df_grouped['ccbar'], df_grouped['ddbar'], df_grouped['ssbar'], 
                                        df_grouped['uubar'], df_grouped['charged'], df_grouped['mixed']], ignore_index=True).query(elmu_sample).reset_index(drop=True)
else:
    df_grouped['qqbar']=pd.concat([df_grouped['ccbar'], df_grouped['ddbar'], df_grouped['ssbar'], 
                                            df_grouped['uubar'], df_grouped['charged'], df_grouped['mixed']], ignore_index=True).query(elmu_sample).reset_index(drop=True)
    df_grouped['ellellgamma']=pd.concat([df_grouped['ee'],
                                            df_grouped['mumu']], ignore_index=True).query(elmu_sample).reset_index(drop=True)
    df_grouped['twoPhotons']=pd.concat([df_grouped['eeee'], df_grouped['eepipi'], df_grouped['eemumu'], 
                                            df_grouped['mumumumu']], ignore_index=True).query(elmu_sample).reset_index(drop=True)
    df_grouped['eetautau']=df_grouped['eetautau'].query(elmu_sample).reset_index(drop=True)

print('done.')  


# In[12]:


# # signal trigger
if new_data:
    # ECL-based trigger bits
    sig_trig_ECL="(((__experiment__<= 18 and psnm_lml0==1) or (__experiment__>= 20 and psnm_lml12==1)) or psnm_lml1==1 or psnm_lml2==1 or psnm_lml4==1 or psnm_lml6==1 or psnm_lml7==1 or psnm_lml8==1 or psnm_lml9==1 or psnm_lml10==1 or psnm_lml13==1 or psnm_hie==1 )"
    # CDC-based trigger bits
    sig_trig_CDC="(psnm_fff==1  or psnm_ffo==1 or psnm_ffy==1  or psnm_fyo==1)"
    # pi0-study signal trigger bits
    sig_trig_pi0="((__experiment__<= 18 and psnm_lml0==1) or (__experiment__>= 20 and psnm_lml12==1))"
else:
    # ECL-based trigger bits
    sig_trig_ECL="(ftdl_lml0==1  or ftdl_lml1==1  or ftdl_lml2==1  or ftdl_lml4==1  or ftdl_lml6==1  or ftdl_lml7==1  or ftdl_lml8==1  or ftdl_lml9==1  or ftdl_lml10==1  or ftdl_lml12==1  or ftdl_lml13==1  or ftdl_hie==1 )"
    # CDC-based trigger bits
    sig_trig_CDC="(ftdl_fff==1  or ftdl_ffo==1 or ftdl_ffy==1  or ftdl_fyo==1)"
    # pi0-study signal trigger bits
    sig_trig_pi0="(ftdl_lml0==1 or ftdl_lml12==1)"

print('done.')


# In[13]:


if new_data:
    mc_names = []
    if is_Signal == False:
        if prong_number == '1prong':
            mc_names += ['taupair_el_elmu','taupair_mu_elmu', 'taupair_pi_elmu', 'taupair_pipi0_elmu', 'taupair_bkg_elmu', 'qqbar']
        elif prong_number == '3prong':
            mc_names += ['taupair_3pi','taupair_3pipi0','taupair_3pi2pi0','taupair_bkg_3prong', 'qqbar']
    elif npi0:
        pi0_list_all_is_Signal = []
        pi0_list_all_is_NotSignal = []      
        
        
        for pi0_sel in pi0_list:
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi')

                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pLead_3pi')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pSub_3pi')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pThird_3pi')

                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pipi0')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pipi0')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pipi0')

                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pLead_3pipi0')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pSub_3pipi0')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pThird_3pipi0')

                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi2pi0')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi2pi0')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi2pi0')

                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pLead_3pi2pi0')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pSub_3pi2pi0')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pThird_3pi2pi0')


        list_isSignal = pi0_list_all_is_Signal + pi0_list_all_is_NotSignal
        
        mc_names +=  list_isSignal
            
    elif is_Signal:
        pi0_list_all_is_Signal = []
        pi0_list_all_is_NotSignal = []      
        
        
        for pi0_sel in pi0_list:
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pLead')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pSub')
                pi0_list_all_is_Signal.append('is_Signal_'+pi0_sel+'SBPi0_3pThird')

                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pLead')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pSub')
                pi0_list_all_is_NotSignal.append('is_NotSignal_'+pi0_sel+'SBPi0_3pThird')

        list_isSignal = pi0_list_all_is_Signal + pi0_list_all_is_NotSignal
        
        mc_names +=  list_isSignal
    
else:
    if prong_number == '1prong':
        mc_names = ['taupair_el_elmu','taupair_mu_elmu', 'taupair_pi_elmu', 'taupair_pipi0_elmu', 'taupair_bkg_elmu', 'qqbar','ellellgamma','twoPhotons','eetautau']
    elif prong_number == '3prong':
        mc_names = ['taupair_3pi','taupair_3pipi0','taupair_3pi2pi0','taupair_bkg_3prong', 'qqbar','ellellgamma','twoPhotons','eetautau']


# In[22]:


# # apply trigger

trigger_cuts=[]

if True :
    # Choose
    if trigger_name == 'ECL&CDC':
        trigger_cuts.append(sig_trig_ECL) 
        trigger_cuts.append(sig_trig_CDC) 
    if trigger_name == 'Pi0-study':
        trigger_cuts.append(sig_trig_pi0) 
    
     
trigger_filter_expression=''
for cut in trigger_cuts[:-1]:
    trigger_filter_expression += f"({cut}) or "
if trigger_cuts: trigger_filter_expression+=f"({trigger_cuts[-1]})"
    
df_grouped_trig={}

if trigger_filter_expression:
    print('------------------------------------------------------------------------------------------')
    print('apply expression:', trigger_filter_expression.replace(') or (', ') or \n\t\t  ('))
    print('------------------------------------------------------------------------------------------')

    #print(df_grouped.keys()) 
    
    for key in mc_names :
        df_grouped_trig[key]=(df_grouped[key].query(trigger_filter_expression).reset_index(drop=True))
    
    print('\t\t\t before \t after') 
    for key in mc_names :
        print(key,'\t\t',len(df_grouped[key]),'\t',len(df_grouped_trig[key]))

print('done.')




# In[12]:


#df_analyze=df_grouped
df_analyze=df_grouped_trig

# # cuts for pi0 efficiency study
if new_data == False:
    for key in mc_names:
        # Grab the group DataFrame
        df = df_grouped_trig[key]
        # Get the 3 track pt columns
        track_pts = df[['track1_3prong_pt', 'track2_3prong_pt', 'track3_3prong_pt']].to_numpy()
        
        # Sort each row
        sorted_pts = np.sort(track_pts, axis=1)
        
        # Create new columns
        df['third_3prong_pt'] = sorted_pts[:, 0]  # min
        df['sub_3prong_pt'] = sorted_pts[:, 1]    # middle
        df['lead_3prong_pt'] = sorted_pts[:, 2]   # max
        
        # Drop the old columns
        df.drop(columns=['track1_3prong_pt', 'track2_3prong_pt', 'track3_3prong_pt'], inplace=True)
        
        # If you're modifying it in-place within the group
        df_grouped_trig[key] = df

        
        df_grouped_trig[key]['nPi0s_1prong_Nom'] = df_grouped_trig[key]['nPi0s_1prong_ineff']
        df_grouped_trig[key]['nPhotons_1prong_Nom'] = df_grouped_trig[key]['nPhotons_1prong']

       
# define cuts    

cut_3prong_pt = '( lead_3prong_pt > 0.5 and sub_3prong_pt > 0.2 and third_3prong_pt > 0.05 )'
cut_thrust = '( thrust > 0.9 and thrust < 0.99 )'
cut_E_vis = '( visibleEnergyOfEventCMS > 4.0 and visibleEnergyOfEventCMS < 9.1 )'
cut_1prong_neutrals = '( nPi0s_1prong_Nom == 0 and nPhotons_1prong_Nom == 0 )'
cuts_3prong_M = '( M_3prong > 0.5 and M_3prong < 1.5 )'


# # apply cuts for pi0 efficiency study

pi0eff_cuts=[]

# apply one after another in steps (1st cut only, 1st and 2nd, 1st 2nd 3rd, ...)
if pi0cut >= 1:
    pi0eff_cuts.append(cut_3prong_pt)
if pi0cut >= 2:
    pi0eff_cuts.append(cut_thrust) 
if pi0cut >= 3:
    pi0eff_cuts.append(cut_E_vis) 
if pi0cut >= 4:
    pi0eff_cuts.append(cut_1prong_neutrals) 
if pi0cut >= 5:
    pi0eff_cuts.append(cuts_3prong_M)

    

pi0eff_filter_expression=''
for cut in pi0eff_cuts[:-1]:
    pi0eff_filter_expression += f"({cut}) and "
if pi0eff_cuts: pi0eff_filter_expression+=f"({pi0eff_cuts[-1]})"
    
df_grouped_pi0={}

if pi0eff_filter_expression:
    print('------------------------------------------------------------------------------------------')
    print('apply expression:', pi0eff_filter_expression.replace(') and (', ') and \n\t\t  ('))
    print('------------------------------------------------------------------------------------------')

    #print(df_grouped.keys()) 
    #print(df_grouped_trig['taupair_pipi0_elmu'].columns.values.tolist())
    
    for key in mc_names :
        df_grouped_pi0[key]=(df_grouped_trig[key].query(pi0eff_filter_expression).reset_index(drop=True))

    print('\t\t\t before \t after') 
    for key in mc_names :
        print(key,'\t\t',len(df_grouped_trig[key]),'\t',len(df_grouped_pi0[key]))
        
    df_analyze=df_grouped_pi0

print('done.')

# In[ ]:


# # MC weight

data_lumi_list=[186.75, 174.90] #/fb proc13+prompt
data_lumi=sum(data_lumi_list) #/fb, sum when referencing all data
mc_lumi=1000 #/fb
var_w='sample_luminosity'
n_cand='__ncandidates__'

if new_data:
    #print('df_analyze keys :', df_analyze.keys())
    if is_Signal == False:
        if prong_number == '1prong':
            df_analyze['taupair_el_elmu']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_mu_elmu']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_pi_elmu']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_pipi0_elmu']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_bkg_elmu']['sample_luminosity'] = 4*data_lumi
            df_analyze['qqbar']['sample_luminosity'] = 4*data_lumi
        
        elif prong_number == '3prong':
            df_analyze['taupair_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['taupair_bkg_3prong']['sample_luminosity'] = 4*data_lumi
            df_analyze['qqbar']['sample_luminosity'] = 4*data_lumi
    elif npi0:
        """
        if pi0_list == ["Nom"]:
            df_analyze['is_Signal_NomSBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi

            df_analyze['is_Signal_NomSBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
        """
        if pi0_list == ["Eff50"]:
            df_analyze['is_Signal_Eff50SBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff50SBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_Eff50SBPi0_3pLead_3pi',
                'is_NotSignal_Eff50SBPi0_3pLead_3pi',
                'is_Signal_Eff50SBPi0_3pLead_3pipi0',
                'is_NotSignal_Eff50SBPi0_3pLead_3pipi0',
                'is_Signal_Eff50SBPi0_3pLead_3pi2pi0',
                'is_NotSignal_Eff50SBPi0_3pLead_3pi2pi0',
                'is_Signal_Eff50SBPi0_3pSub_3pi',
                'is_NotSignal_Eff50SBPi0_3pSub_3pi',
                'is_Signal_Eff50SBPi0_3pSub_3pipi0',
                'is_NotSignal_Eff50SBPi0_3pSub_3pipi0',
                'is_Signal_Eff50SBPi0_3pSub_3pi2pi0',
                'is_NotSignal_Eff50SBPi0_3pSub_3pi2pi0',
                'is_Signal_Eff50SBPi0_3pThird_3pi',
                'is_NotSignal_Eff50SBPi0_3pThird_3pi',
                'is_Signal_Eff50SBPi0_3pThird_3pipi0',
                'is_NotSignal_Eff50SBPi0_3pThird_3pipi0',
                'is_Signal_Eff50SBPi0_3pThird_3pi2pi0',
                'is_NotSignal_Eff50SBPi0_3pThird_3pi2pi0'
            ]
        
        if pi0_list == ["Eff40"]:
            df_analyze['is_Signal_Eff40SBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff40SBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_Eff40SBPi0_3pLead_3pi',
                'is_Signal_Eff40SBPi0_3pLead_3pipi0',
                'is_Signal_Eff40SBPi0_3pLead_3pi2pi0',
                'is_Signal_Eff40SBPi0_3pSub_3pi',
                'is_Signal_Eff40SBPi0_3pSub_3pipi0',
                'is_Signal_Eff40SBPi0_3pSub_3pi2pi0',
                'is_Signal_Eff40SBPi0_3pThird_3pi',
                'is_Signal_Eff40SBPi0_3pThird_3pipi0',
                'is_Signal_Eff40SBPi0_3pThird_3pi2pi0',
                'is_NotSignal_Eff40SBPi0_3pLead_3pi',
                'is_NotSignal_Eff40SBPi0_3pLead_3pipi0',
                'is_NotSignal_Eff40SBPi0_3pLead_3pi2pi0',
                'is_NotSignal_Eff40SBPi0_3pSub_3pi',
                'is_NotSignal_Eff40SBPi0_3pSub_3pipi0',
                'is_NotSignal_Eff40SBPi0_3pSub_3pi2pi0',
                'is_NotSignal_Eff40SBPi0_3pThird_3pi',
                'is_NotSignal_Eff40SBPi0_3pThird_3pipi0',
                'is_NotSignal_Eff40SBPi0_3pThird_3pi2pi0'
            ]
        
        if pi0_list == ["Eff30"]:
            df_analyze['is_Signal_Eff30SBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_Eff30SBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_Eff30SBPi0_3pLead_3pi',
                'is_Signal_Eff30SBPi0_3pLead_3pipi0',
                'is_Signal_Eff30SBPi0_3pLead_3pi2pi0',
                'is_Signal_Eff30SBPi0_3pSub_3pi',
                'is_Signal_Eff30SBPi0_3pSub_3pipi0',
                'is_Signal_Eff30SBPi0_3pSub_3pi2pi0',
                'is_Signal_Eff30SBPi0_3pThird_3pi',
                'is_Signal_Eff30SBPi0_3pThird_3pipi0',
                'is_Signal_Eff30SBPi0_3pThird_3pi2pi0',
                'is_NotSignal_Eff30SBPi0_3pLead_3pi',
                'is_NotSignal_Eff30SBPi0_3pLead_3pipi0',
                'is_NotSignal_Eff30SBPi0_3pLead_3pi2pi0',
                'is_NotSignal_Eff30SBPi0_3pSub_3pi',
                'is_NotSignal_Eff30SBPi0_3pSub_3pipi0',
                'is_NotSignal_Eff30SBPi0_3pSub_3pi2pi0',
                'is_NotSignal_Eff30SBPi0_3pThird_3pi',
                'is_NotSignal_Eff30SBPi0_3pThird_3pipi0',
                'is_NotSignal_Eff30SBPi0_3pThird_3pi2pi0'
            ]
        
        if pi0_list == ["Nom"]:
            df_analyze['is_Signal_NomSBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_NomSBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_NomSBPi0_3pLead_3pi',
                'is_Signal_NomSBPi0_3pLead_3pipi0',
                'is_Signal_NomSBPi0_3pLead_3pi2pi0',
                'is_Signal_NomSBPi0_3pSub_3pi',
                'is_Signal_NomSBPi0_3pSub_3pipi0',
                'is_Signal_NomSBPi0_3pSub_3pi2pi0',
                'is_Signal_NomSBPi0_3pThird_3pi',
                'is_Signal_NomSBPi0_3pThird_3pipi0',
                'is_Signal_NomSBPi0_3pThird_3pi2pi0',
                'is_NotSignal_NomSBPi0_3pLead_3pi',
                'is_NotSignal_NomSBPi0_3pLead_3pipi0',
                'is_NotSignal_NomSBPi0_3pLead_3pi2pi0',
                'is_NotSignal_NomSBPi0_3pSub_3pi',
                'is_NotSignal_NomSBPi0_3pSub_3pipi0',
                'is_NotSignal_NomSBPi0_3pSub_3pi2pi0',
                'is_NotSignal_NomSBPi0_3pThird_3pi',
                'is_NotSignal_NomSBPi0_3pThird_3pipi0',
                'is_NotSignal_NomSBPi0_3pThird_3pi2pi0'
            ]
        
        if pi0_list == ["Opt"]:
            df_analyze['is_Signal_OptSBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_OptSBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_OptSBPi0_3pLead_3pi',
                'is_Signal_OptSBPi0_3pLead_3pipi0',
                'is_Signal_OptSBPi0_3pLead_3pi2pi0',
                'is_Signal_OptSBPi0_3pSub_3pi',
                'is_Signal_OptSBPi0_3pSub_3pipi0',
                'is_Signal_OptSBPi0_3pSub_3pi2pi0',
                'is_Signal_OptSBPi0_3pThird_3pi',
                'is_Signal_OptSBPi0_3pThird_3pipi0',
                'is_Signal_OptSBPi0_3pThird_3pi2pi0',
                'is_NotSignal_OptSBPi0_3pLead_3pi',
                'is_NotSignal_OptSBPi0_3pLead_3pipi0',
                'is_NotSignal_OptSBPi0_3pLead_3pi2pi0',
                'is_NotSignal_OptSBPi0_3pSub_3pi',
                'is_NotSignal_OptSBPi0_3pSub_3pipi0',
                'is_NotSignal_OptSBPi0_3pSub_3pi2pi0',
                'is_NotSignal_OptSBPi0_3pThird_3pi',
                'is_NotSignal_OptSBPi0_3pThird_3pipi0',
                'is_NotSignal_OptSBPi0_3pThird_3pi2pi0'
            ]
        
        if pi0_list == ["pi0pi0MVA"]:
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_pi0pi0MVASBPi0_3pLead_3pi',
                'is_Signal_pi0pi0MVASBPi0_3pLead_3pipi0',
                'is_Signal_pi0pi0MVASBPi0_3pLead_3pi2pi0',
                'is_Signal_pi0pi0MVASBPi0_3pSub_3pi',
                'is_Signal_pi0pi0MVASBPi0_3pSub_3pipi0',
                'is_Signal_pi0pi0MVASBPi0_3pSub_3pi2pi0',
                'is_Signal_pi0pi0MVASBPi0_3pThird_3pi',
                'is_Signal_pi0pi0MVASBPi0_3pThird_3pipi0',
                'is_Signal_pi0pi0MVASBPi0_3pThird_3pi2pi0',
                'is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi',
                'is_NotSignal_pi0pi0MVASBPi0_3pLead_3pipi0',
                'is_NotSignal_pi0pi0MVASBPi0_3pLead_3pi2pi0',
                'is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi',
                'is_NotSignal_pi0pi0MVASBPi0_3pSub_3pipi0',
                'is_NotSignal_pi0pi0MVASBPi0_3pSub_3pi2pi0',
                'is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi',
                'is_NotSignal_pi0pi0MVASBPi0_3pThird_3pipi0',
                'is_NotSignal_pi0pi0MVASBPi0_3pThird_3pi2pi0'
            ]

            
        
        if pi0_list == ["rhorhoMVA"]:
            df_analyze['is_Signal_rhorhoMVASBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pLead_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pLead_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pLead_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pSub_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pSub_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pSub_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pThird_3pi']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pThird_3pipi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_Signal_rhorhoMVASBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pThird_3pi2pi0']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_rhorhoMVASBPi0_3pLead_3pi',
                'is_Signal_rhorhoMVASBPi0_3pLead_3pipi0',
                'is_Signal_rhorhoMVASBPi0_3pLead_3pi2pi0',
                'is_Signal_rhorhoMVASBPi0_3pSub_3pi',
                'is_Signal_rhorhoMVASBPi0_3pSub_3pipi0',
                'is_Signal_rhorhoMVASBPi0_3pSub_3pi2pi0',
                'is_Signal_rhorhoMVASBPi0_3pThird_3pi',
                'is_Signal_rhorhoMVASBPi0_3pThird_3pipi0',
                'is_Signal_rhorhoMVASBPi0_3pThird_3pi2pi0',
                'is_NotSignal_rhorhoMVASBPi0_3pLead_3pi',
                'is_NotSignal_rhorhoMVASBPi0_3pLead_3pipi0',
                'is_NotSignal_rhorhoMVASBPi0_3pLead_3pi2pi0',
                'is_NotSignal_rhorhoMVASBPi0_3pSub_3pi',
                'is_NotSignal_rhorhoMVASBPi0_3pSub_3pipi0',
                'is_NotSignal_rhorhoMVASBPi0_3pSub_3pi2pi0',
                'is_NotSignal_rhorhoMVASBPi0_3pThird_3pi',
                'is_NotSignal_rhorhoMVASBPi0_3pThird_3pipi0',
                'is_NotSignal_rhorhoMVASBPi0_3pThird_3pi2pi0'
            ]


    elif is_Signal:   
        if pi0_list == ["Eff50"]:
            df_analyze['is_Signal_Eff50SBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_Eff50SBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_Eff50SBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff50SBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_Eff50SBPi0_3pLead', 'is_NotSignal_Eff50SBPi0_3pLead',
                'is_Signal_Eff50SBPi0_3pSub', 'is_NotSignal_Eff50SBPi0_3pSub',
                'is_Signal_Eff50SBPi0_3pThird', 'is_NotSignal_Eff50SBPi0_3pThird',
            ]
            
        elif pi0_list == ["Eff40"]:
            df_analyze['is_Signal_Eff40SBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_Eff40SBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_Eff40SBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff40SBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_Eff40SBPi0_3pLead', 'is_NotSignal_Eff40SBPi0_3pLead',
                'is_Signal_Eff40SBPi0_3pSub', 'is_NotSignal_Eff40SBPi0_3pSub',
                'is_Signal_Eff40SBPi0_3pThird', 'is_NotSignal_Eff40SBPi0_3pThird',
            ]
            
        elif pi0_list == ["Eff30"]:
            df_analyze['is_Signal_Eff30SBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_Eff30SBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_Eff30SBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_Eff30SBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_Eff30SBPi0_3pLead', 'is_NotSignal_Eff30SBPi0_3pLead',
                'is_Signal_Eff30SBPi0_3pSub', 'is_NotSignal_Eff30SBPi0_3pSub',
                'is_Signal_Eff30SBPi0_3pThird', 'is_NotSignal_Eff30SBPi0_3pThird',
            ]
            
        elif pi0_list == ["Nom"]:
            df_analyze['is_Signal_NomSBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_NomSBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_NomSBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_NomSBPi0_3pLead', 'is_NotSignal_NomSBPi0_3pLead',
                'is_Signal_NomSBPi0_3pSub', 'is_NotSignal_NomSBPi0_3pSub',
                'is_Signal_NomSBPi0_3pThird', 'is_NotSignal_NomSBPi0_3pThird',
            ]
        elif pi0_list == ["Opt"]:
            df_analyze['is_Signal_OptSBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_OptSBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_OptSBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_OptSBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_OptSBPi0_3pLead', 'is_NotSignal_OptSBPi0_3pLead',
                'is_Signal_OptSBPi0_3pSub', 'is_NotSignal_OptSBPi0_3pSub',
                'is_Signal_OptSBPi0_3pThird', 'is_NotSignal_OptSBPi0_3pThird',
            ]
            
        elif pi0_list == ["pi0pi0MVA"]:
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_pi0pi0MVASBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_pi0pi0MVASBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_pi0pi0MVASBPi0_3pLead', 'is_NotSignal_pi0pi0MVASBPi0_3pLead',
                'is_Signal_pi0pi0MVASBPi0_3pSub', 'is_NotSignal_pi0pi0MVASBPi0_3pSub',
                'is_Signal_pi0pi0MVASBPi0_3pThird', 'is_NotSignal_pi0pi0MVASBPi0_3pThird',
            ]
            
        elif pi0_list == ["rhorhoMVA"]:
            df_analyze['is_Signal_rhorhoMVASBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pLead']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_rhorhoMVASBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pSub']['sample_luminosity'] = 4*data_lumi
            
            df_analyze['is_Signal_rhorhoMVASBPi0_3pThird']['sample_luminosity'] = 4*data_lumi
            df_analyze['is_NotSignal_rhorhoMVASBPi0_3pThird']['sample_luminosity'] = 4*data_lumi

            processes = [
                'is_Signal_rhorhoMVASBPi0_3pLead', 'is_NotSignal_rhorhoMVASBPi0_3pLead',
                'is_Signal_rhorhoMVASBPi0_3pSub', 'is_NotSignal_rhorhoMVASBPi0_3pSub',
                'is_Signal_rhorhoMVASBPi0_3pThird', 'is_NotSignal_rhorhoMVASBPi0_3pThird',
            ]

if new_data and is_Signal == False:
    if prong_number == '1prong':
        '''
        qqbar_weight=(df_analyze['qqbar'][var_w]/mc_lumi)*data_lumi/df_analyze['qqbar'][n_cand]
        taupair_el_weight=(df_analyze['taupair_el_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_el_elmu'][n_cand]
        taupair_mu_weight=(df_analyze['taupair_mu_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_mu_elmu'][n_cand]
        taupair_pi_weight=(df_analyze['taupair_pi_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_pi_elmu'][n_cand]
        taupair_pipi0_weight=(df_analyze['taupair_pipi0_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_pipi0_elmu'][n_cand]
        taupair_bkg_weight=(df_analyze['taupair_bkg_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_bkg_elmu'][n_cand]
        '''

        processes = ['taupair_el_elmu', 'taupair_mu_elmu', 'taupair_pi_elmu',
                 'taupair_pipi0_elmu', 'taupair_bkg_elmu', 'qqbar',]


        
    elif prong_number == '3prong':
        '''
        qqbar_weight=(df_analyze['qqbar'][var_w]/mc_lumi)*data_lumi/df_analyze['qqbar'][n_cand]
        taupair_3pi_weight=(df_analyze['taupair_3pi'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_3pi'][n_cand]
        taupair_3pipi0_weight=(df_analyze['taupair_3pipi0'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_3pipi0'][n_cand]
        taupair_3pi2pi0_weight=(df_analyze['taupair_3pi2pi0'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_3pi2pi0'][n_cand]
        taupair_bkg_3prong_weight=(df_analyze['taupair_bkg_3prong'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_bkg_3prong'][n_cand]
        '''
        
        processes = ['taupair_3pi', 'taupair_3pipi0',
                 'taupair_3pi2pi0', 'taupair_bkg_3prong',
                 'qqbar']

    
elif new_data == False:
    if prong_number == '1prong':
        processes = ['taupair_el_elmu', 'taupair_mu_elmu', 'taupair_pi_elmu',
                 'taupair_pipi0_elmu', 'taupair_bkg_elmu', 'qqbar',
                 'ellellgamma', 'twoPhotons', 'eetautau']
        '''
        taupair_el_weight=(df_analyze['taupair_el_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_el_elmu'][n_cand]
        taupair_mu_weight=(df_analyze['taupair_mu_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_mu_elmu'][n_cand]
        taupair_pi_weight=(df_analyze['taupair_pi_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_pi_elmu'][n_cand]
        taupair_pipi0_weight=(df_analyze['taupair_pipi0_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_pipi0_elmu'][n_cand]
        taupair_bkg_weight=(df_analyze['taupair_bkg_elmu'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_bkg_elmu'][n_cand]
        qqbar_weight=(df_analyze['qqbar'][var_w]/mc_lumi)*data_lumi/df_analyze['qqbar'][n_cand]
        ellellgamma_weight=(df_analyze['ellellgamma'][var_w]/mc_lumi)*data_lumi/df_analyze['ellellgamma'][n_cand]
        twoPhotons_weight=(df_analyze['twoPhotons'][var_w]/mc_lumi)*data_lumi/df_analyze['twoPhotons'][n_cand]  
        eetautau_weight=(df_analyze['eetautau'][var_w]/mc_lumi)*data_lumi/df_analyze['eetautau'][n_cand] 

        weight_table = {'taupair_el_elmu': taupair_el_weight,
                        'taupair_mu_elmu': taupair_mu_weight,
                        'qqbar': qqbar_weight,
                        'ellellgamma': ellellgamma_weight,
                        'taupair_bkg_elmu':taupair_bkg_weight,
                        'taupair_pipi0_elmu': taupair_pipi0_weight,
                        'taupair_pi_elmu': taupair_pi_weight,                           
                        'eetautau': eetautau_weight,
                        'twoPhotons': twoPhotons_weight
        }
        '''
        
    elif prong_number == '3prong':
        '''
        qqbar_weight=(df_analyze['qqbar'][var_w]/mc_lumi)*data_lumi/df_analyze['qqbar'][n_cand]
        taupair_3pi_weight=(df_analyze['taupair_3pi'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_3pi'][n_cand]
        taupair_3pipi0_weight=(df_analyze['taupair_3pipi0'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_3pipi0'][n_cand]
        taupair_3pi2pi0_weight=(df_analyze['taupair_3pi2pi0'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_3pi2pi0'][n_cand]
        taupair_bkg_3prong_weight=(df_analyze['taupair_bkg_3prong'][var_w]/mc_lumi)*data_lumi/df_analyze['taupair_bkg_3prong'][n_cand]
        '''

        processes = ['taupair_3pi', 'taupair_3pipi0',
                 'taupair_3pi2pi0', 'taupair_bkg_3prong',
                 'ellellgamma', 'twoPhotons', 'eetautau', 'qqbar']


weight_table = {                                                                                   #creating weight tables
        proc: (df_analyze[proc][var_w] / mc_lumi) * data_lumi / df_analyze[proc][n_cand]
        for proc in processes
    }



# In[34]:




# # variables to plot, together with unit, number of bins, x-axis range
print('------------------------------------------------------------------------------------------')
print('preparing histograms')


var_prop={}
if pi0all == False and pi0cuts == False:
    if new_data:
        var_prop['thrust']={'unit': '', 'bin': 120, 'range': [0.9, 0.99]}
        var_prop['visibleEnergyOfEventCMS']={'unit': '[GeV]', 'bin': 120, 'range': [4, 9.1]}
        var_prop['M_3prong']={'unit': '[GeV]', 'bin': 120, 'range': [0, 2.5]}
    else:
        
        var_prop['thrust']={'unit': '', 'bin': 120, 'range': [0.5, 1]}
        var_prop['visibleEnergyOfEventCMS']={'unit': '[GeV]', 'bin': 120, 'range': [0, 25]}
        '''
        var_prop['thrust']={'unit': '', 'bin': 120, 'range': [0.9, 0.99]}
        var_prop['visibleEnergyOfEventCMS']={'unit': '[GeV]', 'bin': 120, 'range': [4, 9.1]}
        var_prop['M_3prong']={'unit': 'GeV', 'bin': 120, 'range': [0, 2.5]}
        '''
        
    
    # define plot data
    if new_data:
        if prong_number == '1prong':
            plot_data_thrust= {'taupair_el_elmu': df_analyze['taupair_el_elmu']['thrust'],
                               'taupair_mu_elmu': df_analyze['taupair_mu_elmu']['thrust'],
                               'taupair_pi_elmu': df_analyze['taupair_pi_elmu']['thrust'],
                               'taupair_pipi0_elmu': df_analyze['taupair_pipi0_elmu']['thrust'],
                               'taupair_bkg_elmu': df_analyze['taupair_bkg_elmu']['thrust'],
                               'qqbar': df_analyze['qqbar']['thrust']
            }
            
            plot_data_visibleEnergyOfEventCMS= {'taupair_el_elmu': df_analyze['taupair_el_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_mu_elmu': df_analyze['taupair_mu_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_pi_elmu': df_analyze['taupair_pi_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_pipi0_elmu': df_analyze['taupair_pipi0_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_bkg_elmu': df_analyze['taupair_bkg_elmu']['visibleEnergyOfEventCMS'],
                                                'qqbar': df_analyze['qqbar']['visibleEnergyOfEventCMS']
            }
        elif prong_number == '3prong':
            plot_data_thrust= {'taupair_3pipi0': df_analyze['taupair_3pipi0']['thrust'],
                               'taupair_3pi2pi0': df_analyze['taupair_3pi2pi0']['thrust'],
                               'taupair_3pi': df_analyze['taupair_3pi']['thrust'],
                               'taupair_bkg_3prong': df_analyze['taupair_bkg_3prong']['thrust'],
                               'qqbar': df_analyze['qqbar']['thrust']                      
            }
            
            plot_data_visibleEnergyOfEventCMS= {'taupair_3pipi0': df_analyze['taupair_3pipi0']['visibleEnergyOfEventCMS'],
                                                'taupair_3pi2pi0': df_analyze['taupair_3pi2pi0']['visibleEnergyOfEventCMS'],
                                                'taupair_3pi': df_analyze['taupair_3pi']['visibleEnergyOfEventCMS'],
                                                'taupair_bkg_3prong': df_analyze['taupair_bkg_3prong']['visibleEnergyOfEventCMS'],
                                                'qqbar': df_analyze['qqbar']['visibleEnergyOfEventCMS']
            }
            
            
    
    
    
    
    else:
        if prong_number == '1prong':
            plot_data_thrust= {'taupair_el_elmu': df_analyze['taupair_el_elmu']['thrust'],
                               'taupair_mu_elmu': df_analyze['taupair_mu_elmu']['thrust'],
                               'qqbar': df_analyze['qqbar']['thrust'],
                               'ellellgamma': df_analyze['ellellgamma']['thrust'],
                               'taupair_bkg_elmu': df_analyze['taupair_bkg_elmu']['thrust'],
                               'taupair_pipi0_elmu': df_analyze['taupair_pipi0_elmu']['thrust'],
                               'taupair_pi_elmu': df_analyze['taupair_pi_elmu']['thrust'],                           
                               'eetautau': df_analyze['eetautau']['thrust'],
                               'twoPhotons': df_analyze['twoPhotons']['thrust']
                              }
            
            plot_data_visibleEnergyOfEventCMS= {'taupair_el_elmu': df_analyze['taupair_el_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_mu_elmu': df_analyze['taupair_mu_elmu']['visibleEnergyOfEventCMS'],
                                                'qqbar': df_analyze['qqbar']['visibleEnergyOfEventCMS'],
                                                'ellellgamma': df_analyze['ellellgamma']['visibleEnergyOfEventCMS'],
                                                'taupair_bkg_elmu': df_analyze['taupair_bkg_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_pipi0_elmu': df_analyze['taupair_pipi0_elmu']['visibleEnergyOfEventCMS'],
                                                'taupair_pi_elmu': df_analyze['taupair_pi_elmu']['visibleEnergyOfEventCMS'],
                                                'eetautau': df_analyze['eetautau']['visibleEnergyOfEventCMS'],
                                                'twoPhotons': df_analyze['twoPhotons']['visibleEnergyOfEventCMS']
                                               }
        elif prong_number == '3prong':
            plot_data_thrust= {'taupair_3pipi0': df_analyze['taupair_3pipi0']['thrust'],
                               'taupair_3pi2pi0': df_analyze['taupair_3pi2pi0']['thrust'],
                               'taupair_3pi': df_analyze['taupair_3pi']['thrust'],
                               'taupair_bkg_3prong': df_analyze['taupair_bkg_3prong']['thrust'],
                               'ellellgamma': df_analyze['ellellgamma']['thrust'],
                               'qqbar': df_analyze['qqbar']['thrust'],
                               'eetautau': df_analyze['eetautau']['thrust'],
                               'twoPhotons': df_analyze['twoPhotons']['thrust']
            }
            
            plot_data_visibleEnergyOfEventCMS= {'taupair_3pipi0': df_analyze['taupair_3pipi0']['visibleEnergyOfEventCMS'],
                                                'taupair_3pi2pi0': df_analyze['taupair_3pi2pi0']['visibleEnergyOfEventCMS'],
                                                'taupair_3pi': df_analyze['taupair_3pi']['visibleEnergyOfEventCMS'],
                                                'taupair_bkg_3prong': df_analyze['taupair_bkg_3prong']['visibleEnergyOfEventCMS'],
                                                'ellellgamma': df_analyze['ellellgamma']['visibleEnergyOfEventCMS'],
                                                'qqbar': df_analyze['qqbar']['visibleEnergyOfEventCMS'],
                                                'eetautau': df_analyze['eetautau']['visibleEnergyOfEventCMS'],
                                                'twoPhotons': df_analyze['twoPhotons']['visibleEnergyOfEventCMS']
            }
            
    
    # sort the data by the number of elements in each category in descending order
    #sorted_data_thrust = dict(sorted(plot_data_thrust.items(), key=lambda item: len(item[1]), reverse=True))
    #sorted_data_visibleEnergyOfEventCMS = dict(sorted(plot_data_visibleEnergyOfEventCMS.items(), key=lambda item: len(item[1]), reverse=True))
    
    #manually sorted data
    sorted_data_thrust = plot_data_thrust
    sorted_data_visibleEnergyOfEventCMS = plot_data_visibleEnergyOfEventCMS
    
    # prepare the data for the histogram, reversed order for histogram stacking
    hist_data_thrust = [sorted_data_thrust[key] for key in reversed(sorted_data_thrust)]
    hist_data_visibleEnergyOfEventCMS = [sorted_data_visibleEnergyOfEventCMS[key] for key in reversed(sorted_data_visibleEnergyOfEventCMS)]

    
    # prepare weights for the histogram, reversed order for histogram stacking
    weights_thrust = [weight_table[key] for key in reversed(sorted_data_thrust)]
    weights_visibleEnergy = [weight_table[key] for key in reversed(sorted_data_visibleEnergyOfEventCMS)]
    

    
    # extract colors, reversed order for histogram stacking
    colors_thrust = [color_map[key] for key in reversed(sorted_data_thrust)]
    colors_visibleEnergy = [color_map[key] for key in reversed(sorted_data_visibleEnergyOfEventCMS)]
    
    # create legend handles with correct colors
    legend_labels = list(sorted_data_thrust.keys())  # Correct order for legend
    legend_handles = [mpatches.Patch(color=color_map[label], label=label) for label in legend_labels]
    
    print('done')
    
    
    
    
    # # plot histogram
    
    print('ploting')
    
    
    fig, ((hist0, hist1),(hist2, hist3)) = plt.subplots(nrows=2, ncols=2, figsize=(16, 8))
    fig.subplots_adjust(hspace=0.3, wspace=0.2)  # adjust vertical and horizontal spacing
    
    # create figure
    hist0.hist(hist_data_thrust, weights=weights_thrust, stacked=True, label=list(sorted_data_thrust.keys()), range=var_prop['thrust']['range'], bins=var_prop['thrust']['bin'], color=colors_thrust)
    
    hist1.hist(hist_data_thrust, weights=weights_thrust, stacked=True, label=list(sorted_data_thrust.keys()), range=var_prop['thrust']['range'], bins=var_prop['thrust']['bin'], color=colors_thrust, log=True)
    
    hist2.hist(hist_data_visibleEnergyOfEventCMS, weights=weights_visibleEnergy, stacked=True, label=list(sorted_data_visibleEnergyOfEventCMS.keys()), range=var_prop['visibleEnergyOfEventCMS']['range'], bins=var_prop['visibleEnergyOfEventCMS']['bin'], color=colors_visibleEnergy)
    
    hist3.hist(hist_data_visibleEnergyOfEventCMS, weights=weights_visibleEnergy, stacked=True, label=list(sorted_data_visibleEnergyOfEventCMS.keys()), range=var_prop['visibleEnergyOfEventCMS']['range'], bins=var_prop['visibleEnergyOfEventCMS']['bin'], color=colors_visibleEnergy, log=True)
    
    # add legend with correct colors
    for ax in [hist0, hist1, hist2, hist3]:
        ax.legend(handles=legend_handles, loc= 'best') 
    
    # add legend and labels
    hist0.set_xlabel('Thrust ' + var_prop['thrust']['unit'])
    hist0.set_ylabel('Events')
    #hist0.set_title()
    
    hist1.set_xlabel('Thrust ' + var_prop['thrust']['unit'])
    hist1.set_ylabel('Events')
    #hist1.set_title()
    
    hist2.set_xlabel('Visible energy of event CMS ' + var_prop['visibleEnergyOfEventCMS']['unit'])
    hist2.set_ylabel('Events')
    #hist2.set_title('Visible energy of event CMS')
    
    hist3.set_xlabel('Visible energy of event CMS ' + var_prop['visibleEnergyOfEventCMS']['unit'])
    hist3.set_ylabel('Events')
    #hist3.set_title('Energy of event CMS log scale')
    
    plt.show()
    
    
    plt.savefig(save_file_location+'pi0'+name_add+'.png')

if pi0all == False and pi0cuts == True:        #making different histograms for each cut
    if pi0cuts_sel == 1:
        list_LST = ['lead_3prong_pt', 'sub_3prong_pt', 'third_3prong_pt']
    elif pi0cuts_sel == 2:
        list_LST = ['thrust']
    elif pi0cuts_sel == 3:
        list_LST = ['visibleEnergyOfEventCMS']
    elif pi0cuts_sel == 4:
        list_LST = ['nPi0s_1prong_Nom', 'nPhotons_1prong_Nom']
    elif pi0cuts_sel == 5:
        list_LST = ['M_3prong']
    
    plot_data_pt = {}
    sorted_data_pi0 = {}
    hist_data_pi0 = {}
    weights_pi0 = {}
    colors_data_pi0 = {}
    legend_labels_pi0 = {}
    legend_handles_pi0 = {}
       
    
    
    fig2, axes = plt.subplots(nrows=1, ncols=len(list_LST), figsize=(8*len(list_LST), 4))  # Create subplots
    fig2.subplots_adjust(hspace=0.3, wspace=0.2)  # Adjust vertical and horizontal spacing

    if len(list_LST) == 1:
        histogram = [axes]
    elif len(list_LST) > 1:
        histogram = axes.flatten()  # Convert grid into a 1D list
    
    for i, element in enumerate(list_LST):
        if pi0cuts_sel == 1:
            var_prop[element]={'unit': '[GeV]', 'bin': 120, 'range': [0, 6]}
        elif pi0cuts_sel == 2:
            var_prop[element]={'unit': '', 'bin': 120, 'range': [0.5, 1]}
        elif pi0cuts_sel == 3:
            var_prop[element]={'unit': '[GeV]', 'bin': 120, 'range': [0, 25]}
        elif pi0cuts_sel == 4:
            var_prop[element]={'unit': '[N]', 'bin': 6, 'range': [-0.5, 5.5]}
        elif pi0cuts_sel == 5:
            var_prop[element]={'unit': '[GeV]', 'bin': 120, 'range': [0, 2.5]}
            
        if prong_number == '1prong':
            plot_data_pt[element]= {'taupair_el_elmu': df_analyze['taupair_el_elmu'][element],
                                    'taupair_mu_elmu': df_analyze['taupair_mu_elmu'][element],
                                    'qqbar': df_analyze['qqbar'][element],
                                    'ellellgamma': df_analyze['ellellgamma'][element],
                                    'taupair_bkg_elmu': df_analyze['taupair_bkg_elmu'][element],
                                    'taupair_pipi0_elmu': df_analyze['taupair_pipi0_elmu'][element],
                                    'taupair_pi_elmu': df_analyze['taupair_pi_elmu'][element],                           
                                    'eetautau': df_analyze['eetautau'][element],
                                    'twoPhotons': df_analyze['twoPhotons'][element]
                                   }
        elif prong_number == '3prong':
            plot_data_pt[element]={
                           'taupair_3pipi0': df_analyze['taupair_3pipi0'][element],
                           'taupair_3pi2pi0': df_analyze['taupair_3pi2pi0'][element],
                           'taupair_3pi': df_analyze['taupair_3pi'][element],
                           'taupair_bkg_3prong': df_analyze['taupair_bkg_3prong'][element],
                           'ellellgamma': df_analyze['ellellgamma'][element],
                           'qqbar': df_analyze['qqbar'][element],
                           'eetautau': df_analyze['eetautau'][element],
                           'twoPhotons': df_analyze['twoPhotons'][element]
            }
     
        
        # manually sorted data
        sorted_data_pi0[element] = plot_data_pt[element]
        
        # prepare the data for the histogram, reversed order for histogram stacking
        hist_data_pi0[element] = [sorted_data_pi0[element][key] for key in reversed(sorted_data_pi0[element])]

        # prepare weights for the histogram, reversed order for histogram stacking
        weights_pi0[element] = [weight_table[key] for key in reversed(sorted_data_pi0[element])]

        
        # extract colors, reversed order for histogram stacking
        colors_data_pi0[element] = [color_map[key] for key in reversed(sorted_data_pi0[element])]
        
        # create legend handles with correct colors
        legend_labels_pi0[element] = list(sorted_data_pi0[element].keys())  # Correct order for legend
        legend_handles_pi0[element] = [mpatches.Patch(color=color_map[label], label=label) for label in legend_labels_pi0[element]]

        #print(hist_data_pi0)
        
        # create figure
        histogram[i].hist(hist_data_pi0[element], weights=weights_pi0[element], stacked=True, label=list(sorted_data_pi0[element].keys()), range=var_prop[element]['range'], bins=var_prop[element]['bin'], color=colors_data_pi0[element])
        print("here12")
        histogram[i].legend(handles=legend_handles_pi0[element])

        histogram[i].set_xlabel(element + ' ' + var_prop[element]['unit'])
        histogram[i].set_ylabel('Events')
        #histogram[i].set_title(element)

    
    plt.show()
    plt.savefig(save_file_location+"pi0cut"+name_add+".png")
        
    

print('done')



if new_data and pi0all:
    print('Pi0 graphs')


    # defining of vairables        
    if SB:
        name_add += 'SB'
        pi0_list_all = []
        for pi0_sel in pi0_list:
            if npi0:
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi')

                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pipi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pipi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pipi0')

                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi2pi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi2pi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi2pi0')

                Npi0range = [-0.5, 40.5]
                NPi0bin = int(Npi0range[1] - Npi0range[0])

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead_3pipi0']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub_3pipi0']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird_3pipi0']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi2pi0']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi2pi0']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi2pi0']={'unit': nPi0_sel, 'bin': NPi0bin, 'range': Npi0range}
            elif is_Signal:
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird')

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead']={'unit': '[N]', 'bin': 120, 'range': [0, 0.5]}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub']={'unit': '[N]', 'bin': 120, 'range': [0, 0.5]}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird']={'unit': '[N]', 'bin': 120, 'range': [0, 0.5]}
            else:
                pi0_list_all.append('M_'+pi0_sel+'SBPi0_3pLead')
                pi0_list_all.append('M_'+pi0_sel+'SBPi0_3pSub')
                pi0_list_all.append('M_'+pi0_sel+'SBPi0_3pThird')
    
                var_prop['M_'+pi0_sel+'SBPi0_3pLead']={'unit': '[GeV]', 'bin': 120, 'range': [0, 0.5]}
                var_prop['M_'+pi0_sel+'SBPi0_3pSub']={'unit': '[GeV]', 'bin': 120, 'range': [0, 0.5]}
                var_prop['M_'+pi0_sel+'SBPi0_3pThird']={'unit': '[GeV]', 'bin': 120, 'range': [0, 0.5]}
    else:
        if npi0:
            pi0_list_all = []
            
            for pi0_sel in pi0_list:
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi')

                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pipi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pipi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pipi0')

                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi2pi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi2pi0')
                pi0_list_all.append('is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi2pi0')

                Npi0range = [-0.5, 40.5]
                NPi0bin = int(Npi0range[1] - Npi0range[0])

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead_3pipi0']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub_3pipi0']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird_3pipi0']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}

                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pLead_3pi2pi0']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pSub_3pi2pi0']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
                var_prop['is_Signal_'+pi0_sel+'SBPi0_3pThird_3pi2pi0']={'unit': nPi0_sel + ' [N]', 'bin': NPi0bin, 'range': Npi0range}
        else:
            for pi0_sel in pi0_list:
                var_prop['M_'+pi0_sel+'Pi0_3pLead']={'unit': 'GeV', 'bin': 120, 'range': [0.1, 0.15]}
                var_prop['M_'+pi0_sel+'Pi0_3pSub']={'unit': 'GeV', 'bin': 120, 'range': [0.1, 0.15]}
                var_prop['M_'+pi0_sel+'Pi0_3pThird']={'unit': 'GeV', 'bin': 120, 'range': [0.1, 0.15]}
            
        
        

    #print(pi0_list_all)
    if npi0:
        fig2, axes = plt.subplots(nrows=3*len(pi0_list), ncols=3, figsize=(24, 3*len(pi0_list)*4))  # Create subplots
    else:
        fig2, axes = plt.subplots(nrows=len(pi0_list), ncols=3, figsize=(24, len(pi0_list)*4))  # Create subplots
    fig2.subplots_adjust(hspace=0.3, wspace=0.2)  # Adjust vertical and horizontal spacing

    histogram = axes.flatten()  # Convert 9x3 grid into a 1D list


    plot_data_histogram={}    
    sorted_data_pi0={}
    hist_data_pi0={}
    weights_pi0={}
    colors_data_pi0={}
    legend_labels_pi0={}
    legend_handles_pi0={}
    
    
        
    
    j = 0
    sum_nrealpi0 = 0
    sum_nallpi0 = 0

    sumall_signal = 0
    sumall_all = 0
    
    for i, element in enumerate(pi0_list_all):
        if npi0:
            if i == 0:
                print(nPi0_sel + ":")
                print('------------------------------------------------------------')
            #print(element)
            #print('==============================================================================================================')
            #print(df_grouped[element].columns.values.tolist())
            #print('==============================================================================================================')
            plot_data_histogram[element]={
                           'isSignal':df_analyze[element][nPi0_sel],
                           'isNotSignal':df_analyze[element.replace('is_Signal_', 'is_NotSignal_')][nPi0_sel],
            }
            #print(element, ' is Signal:', len(df_analyze[element][nPi0_sel]), ', is Not Signal:', len(df_analyze[element.replace('is_Signal_', 'is_NotSignal_')][nPi0_sel]), 'sum:', len(df_analyze[element][nPi0_sel]) + len(df_analyze[element.replace('is_Signal_', 'is_NotSignal_')][nPi0_sel]))
            
            sum_nrealpi0 += len(df_analyze[element][nPi0_sel])
            sum_nallpi0 += len(df_analyze[element][nPi0_sel]) + len(df_analyze[element.replace('is_Signal_', 'is_NotSignal_')][nPi0_sel])

            if not pi0two:
                if (i+1) / 3 == 1:
                    print('------------------------------------------------------------')
                    print("3pi:")
                    print("N real:", sum_nrealpi0)
                    #sumall_signal += sum_nrealpi0
                    
                    print("N all:", sum_nallpi0)
                    #sumall_all += sum_nallpi0
                    
                    print("Efficiency:", sum_nrealpi0/(sum_nallpi0))
                    
                    sum_nrealpi0 = 0
                    sum_nallpi0 = 0
                    print('------------------------------------------------------------')
                    
                elif (i+1) / 3 == 2:
                    print('------------------------------------------------------------')
                    print("3pip0:")
                    print("N real:", sum_nrealpi0)
                    sumall_signal += sum_nrealpi0
                    
                    print("N all:", sum_nallpi0)
                    sumall_all += sum_nallpi0
                    
                    print("Efficiency:", sum_nrealpi0/(sum_nallpi0))
                    
                    sum_nrealpi0 = 0
                    sum_nallpi0 = 0
                    print('------------------------------------------------------------')
                    
                elif (i+1) / 3 == 3:
                    print('------------------------------------------------------------')
                    print("3pi2p0:")
                    print("N real:", sum_nrealpi0)
                    sumall_signal += sum_nrealpi0
                    
                    print("N all:", sum_nallpi0)
                    sumall_all += sum_nallpi0
                    
                    print("Efficiency:", sum_nrealpi0/(sum_nallpi0))
                    sum_nrealpi0 = 0
                    sum_nallpi0 = 0
    
                    print('------------------------------------------------------------')
                    print("N signal all:", sumall_signal)
                    print("N all all:", sumall_all)
                    print("Efficiency for the total sum of 1pi0 + 2pi0:", sumall_signal/sumall_all)
                    print('------------------------------------------------------------')
            else:
                if element == 'is_Signal_'+pi0_selection[0]+'SBPi0_3pLead_3pi2pi0':
                    print('------------------------------------------------------------')
                    print('N 1pi0 in 3pi2pi0:', len(df_analyze[element][nPi0_sel]))
                    print('N 2pi0 in 3pi2pi0:', len(df_analyze[element.replace('is_Signal_', 'is_NotSignal_')][nPi0_sel]))
                    print('------------------------------------------------------------')
                    
                elif element == 'is_Signal_'+pi0_selection[0]+'SBPi0_3pSub_3pi':
                    print('------------------------------------------------------------')
                    print('N 3pi0 in 3pi2pi0:', len(df_analyze[element][nPi0_sel]))
                    print('------------------------------------------------------------')

        
            
        elif is_Signal:
            #print('==============================================================================================================')
            #print(df_grouped[element].columns.values.tolist())
            #print('==============================================================================================================')
            plot_data_histogram[element]={
                           'isSignal':df_analyze[element][element.replace('is_Signal_', 'M_')],
                           'isNotSignal':df_analyze[element.replace('is_Signal_', 'is_NotSignal_')][element.replace('is_Signal_', 'M_')],
            }
            
        else:
            plot_data_histogram[element]={
                           'taupair_3pipi0': df_analyze['taupair_3pipi0'][element],
                           'taupair_3pi2pi0': df_analyze['taupair_3pi2pi0'][element],
                           'taupair_3pi': df_analyze['taupair_3pi'][element],
                           'taupair_bkg_3prong': df_analyze['taupair_bkg_3prong'][element],
                           'qqbar': df_analyze['qqbar'][element],
            }
            
        

        # sort the data by the number of elements in each category in descending order
        #sorted_data_pi0[element] = dict(sorted( plot_data_histogram[element].items(), key=lambda item: len(item[1]), reverse=True))

        # manually sorted data
        sorted_data_pi0[element] = plot_data_histogram[element]
        
        # prepare the data for the histogram, reversed order for histogram stacking
        hist_data_pi0[element] = [sorted_data_pi0[element][key] for key in reversed(sorted_data_pi0[element])]

        # prepare weights for the histogram, reversed order for histogram stacking
        if not is_Signal:
            weights_pi0[element] = [weight_table[key] for key in reversed(sorted_data_pi0[element])]
        else:
            weights_pi0[element]=[                
                weight_table[element.replace('is_Signal_', 'is_NotSignal_')],
                weight_table[element],           
            ]

        
        # extract colors, reversed order for histogram stacking
        colors_data_pi0[element] = [color_map[key] for key in reversed(sorted_data_pi0[element])]
        
        # create legend handles with correct colors
        legend_labels_pi0[element] = list(sorted_data_pi0[element].keys())  # Correct order for legend
        legend_handles_pi0[element] = [mpatches.Patch(color=color_map[label], label=label) for label in legend_labels_pi0[element]]

        #print(hist_data_pi0[element])
        #print(weights_pi0[element])

        # create figure
        histogram[i+3*j].hist(hist_data_pi0[element], weights=weights_pi0[element], stacked=True, label=list(sorted_data_pi0[element].keys()), range=var_prop[element]['range'], bins=var_prop[element]['bin'], color=colors_data_pi0[element])
        histogram[i+3*j].legend(handles=legend_handles_pi0[element])

        
        
        if SB:
            histogram[i+3*j].set_xlabel(element + ' ' +var_prop[element]['unit'])
            #histogram[i+3*j].set_title(element)
        else:
            histogram[i+3*j].set_xlabel(element.replace('SB','') + ' ' +var_prop[element]['unit'])       #without SB
            #histogram[i+3*j].set_title(element.replace('SB',''))  #without SB

        histogram[i+3*j].set_ylabel('Events')
        '''
        histogram[i+3*j+3].hist(hist_data_pi0[element], weights=weights_pi0[element], stacked=True, label=list(sorted_data_pi0[element].keys()), range=var_prop[element]['range'], bins=var_prop[element]['bin'], color=colors_data_pi0[element], log=True)
        histogram[i+3*j+3].legend(handles=legend_handles_pi0[element])

        histogram[i+3*j+3].set_xlabel(var_prop[element]['unit'])
        histogram[i+3*j+3].set_ylabel('N')
        histogram[i+3*j+3].set_title(element+' log scale')
        if (i+1) % 3 == 0:
            j += 1
        '''

    if is_Signal:
        name_add += '_isSignal' + pi0_selection[0]
    if npi0:
        name_add += '_' + nPi0_sel
    plt.show()
    plt.savefig(save_file_location+"pi0_all"+name_add+".png")

print("=================================================================================================================================")
usage = resource.getrusage(resource.RUSAGE_SELF)
max_memory_gb = usage.ru_maxrss / (1024 ** 2)  # ru_maxrss is in kilobytes on Linux
print(f"Peak memory usage: {max_memory_gb:.2f} GB")
end_time = time.time()
print('done, end. Time: ', end_time - start_time)



















