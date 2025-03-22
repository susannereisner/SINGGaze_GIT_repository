# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:58:10 2025

SING Gaze Project, Wieki, University of Vienna
Script author: Pierre Labendzki
June 2024, Revision March 2025

This script plots the permutation analyses of look-related changes
in audio features - for OFFSETS. 

"""

# import os
import matplotlib.pyplot as plt
import numpy as np
from random import randint
import scipy.stats

def cluster_test(ERCs_ORG,ERCs_SUR):
    nb_frames = len(ERCs_ORG[0])

    print('ERCs_ORG', np.shape(ERCs_ORG))
    print('ERCs_SUR', np.shape(ERCs_SUR))

    nb_look = np.shape(ERCs_ORG)[0]
    p_val_continous = np.zeros(nb_frames)
    t_val_continous = np.zeros(nb_frames)
    mean_ORG = np.nanmean(ERCs_ORG,axis = 0)
    mean_SUR = np.nanmean(ERCs_SUR,axis = 0)
    # Distance_to_ORG = np.zeros(nb_frames)
    # Distance_to_SUR = np.zeros(nb_frames)
    for frame in range(nb_frames):
        # print("\n frame = ", frame)
        # print("look = ", look)
        Distance_to_ORG = (ERCs_ORG[:,frame])
        Distance_to_SUR = (ERCs_SUR[:,frame])
        # print("np.shape(Distance_to_ORG)", np.shape(Distance_to_ORG))
        # print("np.shape(Distance_to_SUR)", np.shape(Distance_to_SUR))
            
        t,p = scipy.stats.ttest_ind(Distance_to_ORG, Distance_to_SUR, nan_policy='omit')
        # if (p < 0.05):
        #     print(p)
        #     plt.hist(Distance_to_ORG,alpha = 0.5)
        #     plt.hist(Distance_to_SUR,alpha = 0.5)
        #     plt.title('frame = ' + str(frame))
        #     plt.show()

        p_val_continous[frame] = p
        t_val_continous[frame] = t
    return t_val_continous,p_val_continous    



def cluster(ORG_CORR,SUR_CORR,n_perm):
    n_ORG = np.shape(ORG_CORR)[0]
    n_SUR = np.shape(SUR_CORR)[0]
    n_COL = n_ORG + n_SUR

    COL_CORR = np.vstack((ORG_CORR,SUR_CORR))
    COL_CORR_GROUND =COL_CORR
    random_p_distributions = np.zeros(np.shape(ORG_CORR)[1])
    
    for perm in range(n_perm):
        print("perm = ", perm)
        rdn_ORG = np.zeros(np.shape(ORG_CORR)[1])
        rdn_SUR = np.zeros(np.shape(SUR_CORR)[1])
        COL_CORR_temp = COL_CORR_GROUND
        for k in range(n_ORG):
            value = randint(0, n_COL-k-1)
            # print(value)
            COL_CORR_temp = np.delete(COL_CORR_temp, value, axis=0)
            rdn_SUR = COL_CORR_temp
            rdn_ORG = np.vstack((rdn_ORG,COL_CORR[value,:]))

            # print("rdn_ORG = ", np.shape(rdn_ORG))
            # print("rdn_SUR = ", np.shape(rdn_SUR))

        rdn_ORG = np.delete(rdn_ORG, (0), axis=0) 
        rdn_ORG = np.delete(rdn_ORG, (0), axis=0)  
            
        t_val_continous,p_val_continous = cluster_test(rdn_ORG,rdn_SUR)
        random_p_distributions = np.vstack((random_p_distributions,p_val_continous))
    random_p_distributions = np.delete(random_p_distributions, (0), axis=0)
    return random_p_distributions

def compare_real_to_cluster(real_p,RDN_CORR,threshold):
    # check if the real observed ORG p value is in the first 5th percentile of the permuted p_values
    N = len(real_p)
    is_significant = np.nan * np.zeros(N) 
    for k in range(N):
        if (real_p[k] < np.percentile(RDN_CORR[:,k], threshold)): ### threshold needs to be 5, NOT 0.05 !!!
            is_significant[k] = 1
    return is_significant




window_size = 5
padd = 0
frame_rate = 100 # frames a second
window_size_samples = window_size * frame_rate

big_path = 'W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_npy_BIG_offsets/'


#load files SF
BIG_ERCs_SF_LUL_OFF = np.load(big_path+'BIG_ERCs_SF_LUL_OFF.npy')
BIG_ERCs_SF_SUR_LUL_OFF = np.load(big_path+'BIG_ERCs_SF_SUR_LUL_OFF.npy')
BIG_ERCs_SF_PLA_OFF = np.load(big_path+'BIG_ERCs_SF_PLA_OFF.npy')
BIG_ERCs_SF_SUR_PLA_OFF = np.load(big_path+'BIG_ERCs_SF_SUR_PLA_OFF.npy')

BIG_ERCs_SF_PLA_OFF = np.delete(BIG_ERCs_SF_PLA_OFF, (0), axis=0)
BIG_ERCs_SF_SUR_PLA_OFF = np.delete(BIG_ERCs_SF_SUR_PLA_OFF, (0), axis=0)
BIG_ERCs_SF_LUL_OFF = np.delete(BIG_ERCs_SF_LUL_OFF, (0), axis=0)
BIG_ERCs_SF_SUR_LUL_OFF= np.delete(BIG_ERCs_SF_SUR_LUL_OFF, (0), axis=0)


#ENVELOPE
#load files ENV
BIG_ERCs_ENV_LUL_OFF = np.load(big_path+'BIG_ERCs_env_LUL_OFF.npy')
BIG_ERCs_ENV_SUR_LUL_OFF = np.load(big_path+'BIG_ERCs_env_SUR_LUL_OFF.npy')
BIG_ERCs_ENV_PLA_OFF = np.load(big_path+'BIG_ERCs_env_PLA_OFF.npy')
BIG_ERCs_ENV_SUR_PLA_OFF = np.load(big_path+'BIG_ERCs_env_SUR_PLA_OFF.npy')

BIG_ERCs_ENV_PLA_OFF = np.delete(BIG_ERCs_ENV_PLA_OFF, (0), axis=0)
BIG_ERCs_ENV_SUR_PLA_OFF = np.delete(BIG_ERCs_ENV_SUR_PLA_OFF, (0), axis=0)
BIG_ERCs_ENV_LUL_OFF = np.delete(BIG_ERCs_ENV_LUL_OFF, (0), axis=0)
BIG_ERCs_ENV_SUR_LUL_OFF = np.delete(BIG_ERCs_ENV_SUR_LUL_OFF, (0), axis=0)

#PITCH
#load files F0
BIG_ERCs_F0_LUL_OFF = np.load(big_path+'BIG_ERCs_F0_LUL_OFF.npy')
BIG_ERCs_F0_SUR_LUL_OFF = np.load(big_path+'BIG_ERCs_F0_SUR_LUL_OFF.npy')
BIG_ERCs_F0_PLA_OFF = np.load(big_path+'BIG_ERCs_F0_PLA_OFF.npy')
BIG_ERCs_F0_SUR_PLA_OFF = np.load(big_path+'BIG_ERCs_F0_SUR_PLA_OFF.npy')

BIG_ERCs_F0_PLA_OFF = np.delete(BIG_ERCs_F0_PLA_OFF, (0), axis=0)
BIG_ERCs_F0_SUR_PLA_OFF = np.delete(BIG_ERCs_F0_SUR_PLA_OFF, (0), axis=0)
BIG_ERCs_F0_LUL_OFF = np.delete(BIG_ERCs_F0_LUL_OFF, (0), axis=0)
BIG_ERCs_F0_SUR_LUL_OFF = np.delete(BIG_ERCs_F0_SUR_LUL_OFF, (0), axis=0)



### COMPUTE MEAN AND STD FOR ORG AND SUR
## SF PLA
mean_SF_PLA_OFF = np.nanmean(BIG_ERCs_SF_PLA_OFF,axis = 0)
sigma_SF_PLA_OFF = scipy.stats.sem(BIG_ERCs_SF_PLA_OFF,axis = 0)
mean_SF_SUR_PLA_OFF = np.nanmean(BIG_ERCs_SF_SUR_PLA_OFF,axis = 0)
sigma_SF_SUR_PLA_OFF = scipy.stats.sem(BIG_ERCs_SF_SUR_PLA_OFF,axis = 0)

## SF LUL
mean_SF_LUL_OFF = np.nanmean(BIG_ERCs_SF_LUL_OFF,axis = 0)
sigma_SF_LUL_OFF = scipy.stats.sem(BIG_ERCs_SF_LUL_OFF,axis = 0)
mean_SF_SUR_LUL_OFF = np.nanmean(BIG_ERCs_SF_SUR_LUL_OFF,axis = 0)
sigma_SF_SUR_LUL_OFF = scipy.stats.sem(BIG_ERCs_SF_SUR_LUL_OFF,axis = 0)


#### ENVELOPE
## ENV PLA
mean_ENV_PLA_OFF = np.nanmean(BIG_ERCs_ENV_PLA_OFF,axis = 0)
sigma_ENV_PLA_OFF = scipy.stats.sem(BIG_ERCs_ENV_PLA_OFF,axis = 0)
mean_ENV_SUR_PLA_OFF = np.nanmean(BIG_ERCs_ENV_SUR_PLA_OFF,axis = 0)
sigma_ENV_SUR_PLA_OFF = scipy.stats.sem(BIG_ERCs_ENV_SUR_PLA_OFF,axis = 0)

## ENV LUL
mean_ENV_LUL_OFF = np.nanmean(BIG_ERCs_ENV_LUL_OFF,axis = 0)
sigma_ENV_LUL_OFF = scipy.stats.sem(BIG_ERCs_ENV_LUL_OFF,axis = 0)
mean_ENV_SUR_LUL_OFF = np.nanmean(BIG_ERCs_ENV_SUR_LUL_OFF,axis = 0)
sigma_ENV_SUR_LUL_OFF = scipy.stats.sem(BIG_ERCs_ENV_SUR_LUL_OFF,axis = 0)


#### F0
## F0 PLA
mean_F0_PLA_OFF = np.nanmean(BIG_ERCs_F0_PLA_OFF,axis = 0)
sigma_F0_PLA_OFF = scipy.stats.sem(BIG_ERCs_F0_PLA_OFF,axis = 0)
mean_F0_SUR_PLA_OFF = np.nanmean(BIG_ERCs_F0_SUR_PLA_OFF,axis = 0)
sigma_F0_SUR_PLA_OFF = scipy.stats.sem(BIG_ERCs_F0_SUR_PLA_OFF,axis = 0)

## F0 LUL
mean_F0_LUL_OFF = np.nanmean(BIG_ERCs_F0_LUL_OFF,axis = 0)
sigma_F0_LUL_OFF = scipy.stats.sem(BIG_ERCs_F0_LUL_OFF,axis = 0)
mean_F0_SUR_LUL_OFF = np.nanmean(BIG_ERCs_F0_SUR_LUL_OFF,axis = 0)
sigma_F0_SUR_LUL_OFF = scipy.stats.sem(BIG_ERCs_F0_SUR_LUL_OFF,axis = 0)









### PLOTTING RESULTS

window_size = 5 # number of seconds to looks before and after the gaze onset
frame_rate = 100 # frames in a second
window_size_samples = window_size * frame_rate
rt = np.arange(-window_size,window_size,1/frame_rate)



path = 'W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_perm/'
savepath = 'W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_pvalues/'
figpath = 'W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_gaze_figs_sec/'

# percentile required by the observed pvalue to be below
p_to_test = 5/2


t_val_sf_pla_off, p_val_sf_pla_off = cluster_test(BIG_ERCs_SF_PLA_OFF,BIG_ERCs_SF_SUR_PLA_OFF)    # Compute ORG p value
RDN_CORR_pla_off = np.load(path+'RDN_p_SF_PLA_OFF.npy')    # Load 1000  permuted p values
plt.plot(np.transpose(RDN_CORR_pla_off)[:,1:8])
plt.show()
# np.save(savepath + "pvalue_SF_PLA_OFF.npy",p_val_sf_pla_off)
# np.save(savepath + "tvalue_SF_PLA_OFF.npy",t_val_sf_pla_off)
p_v_sf_pla_off = compare_real_to_cluster(p_val_sf_pla_off,RDN_CORR_pla_off,p_to_test)   # Check when p value is in 5th/2 percentile
plt.plot(p_v_sf_pla_off)
# np.save(savepath + "pv_SF_PLA_OFF.npy",p_v_sf_pla_off) 
p_v_sf_pla_off_times = np.hstack((p_v_sf_pla_off[:, np.newaxis], t_val_sf_pla_off[:, np.newaxis], p_val_sf_pla_off[:, np.newaxis]))
# np.save(savepath + "p_v_sf_times_PLA_OFF.npy", p_v_sf_pla_off_times)


t_val_sf_lul_off, p_val_sf_lul_off = cluster_test(BIG_ERCs_SF_LUL_OFF,BIG_ERCs_SF_SUR_LUL_OFF)
RDN_CORR_lul_off = np.load(path+'RDN_p_SF_LUL_OFF.npy')
# np.save(savepath + "pvalue_SF_LUL_OFF.npy",p_val_sf_lul_off)
# np.save(savepath + "tvalue_SF_LUL_OFF.npy",t_val_sf_lul_off)
p_v_sf_lul_off = compare_real_to_cluster(p_val_sf_lul_off,RDN_CORR_lul_off,p_to_test)
# np.save(savepath + "pv_SF_LUL_OFF.npy",p_v_sf_lul_off)
p_v_sf_lul_off_times = np.hstack((p_v_sf_lul_off[:, np.newaxis], t_val_sf_lul_off[:, np.newaxis], p_val_sf_lul_off[:, np.newaxis]))
# np.save(savepath + "p_v_sf_times_LUL_OFF.npy", p_v_sf_lul_off_times)



# ###### PLOTS PAPER
line_width = 4
line_height = 1

fig, axs = plt.subplots(1, 2, figsize=(20, 6))

# Plot Playsongs
axs[0].plot(rt, mean_SF_PLA_OFF, label='Social Gaze Data', color='#009e74', linewidth=3)
axs[0].fill_between(rt, mean_SF_PLA_OFF - sigma_SF_PLA_OFF, mean_SF_PLA_OFF + sigma_SF_PLA_OFF, alpha=0.1, color='#009e74')
axs[0].plot(rt, mean_SF_SUR_PLA_OFF, label='Surrogate Data', color='#56b4e9', linewidth=3)
axs[0].fill_between(rt, mean_SF_SUR_PLA_OFF - sigma_SF_SUR_PLA_OFF, mean_SF_SUR_PLA_OFF + sigma_SF_SUR_PLA_OFF, alpha=0.1, color='#56b4e9')
axs[0].axvline(x=0, color='black', linestyle='--')
# axs[0].plot(rt, line_height * np.mean(BIG_ERCs_SF_PLA_OFF) * p_v_sf_pla_off, linewidth=line_width, color='#d55e00')
axs[0].plot(rt, line_height * 750 * p_v_sf_pla_off, linewidth=line_width, color='#d55e00')
axs[0].set_xlabel("Time relative to Infant Gaze Offset (s)", fontsize=20)
axs[0].set_ylabel("Spectral Flux", fontsize=20)
axs[0].set_xlim(-5, 5)
axs[0].set_ylim(130, 850)
axs[0].text(0.05, 1.08, "(A)", transform=axs[0].transAxes, fontsize=18, verticalalignment='top')
axs[0].text(0.05, 0.96, "Playsongs", transform=axs[0].transAxes, fontsize=20, verticalalignment='top')

# Plot Lullabies
line1, = axs[1].plot(rt, mean_SF_LUL_OFF, label='Social Gaze Data', color='#009e74', linewidth=3)
axs[1].fill_between(rt, mean_SF_LUL_OFF - sigma_SF_LUL_OFF, mean_SF_LUL_OFF + sigma_SF_LUL_OFF, alpha=0.1, color='#009e74')
line2, = axs[1].plot(rt, mean_SF_SUR_LUL_OFF, label='Surrogate Data', color='#56b4e9', linewidth=3)
axs[1].fill_between(rt, mean_SF_SUR_LUL_OFF - sigma_SF_SUR_LUL_OFF, mean_SF_SUR_LUL_OFF + sigma_SF_SUR_LUL_OFF, alpha=0.1, color='#56b4e9')
axs[1].axvline(x=0, color='black', linestyle='--')
# line3, = axs[1].plot(rt, line_height * np.mean(BIG_ERCs_SF_LUL_OFF) * p_v_sf_lul_off, label='p<.05/2', linewidth=line_width, color='#d55e00')
line3, = axs[1].plot(rt, line_height * 400 * p_v_sf_lul_off, label='p < 5th/2 percentile', linewidth=line_width, color='#d55e00')

axs[1].set_xlabel("Time relative to Infant Gaze Offset (s)", fontsize=20)
axs[1].set_ylabel("Spectral Flux", fontsize=20)
axs[1].set_xlim(-5, 5)
axs[1].set_ylim(130, 850)
axs[1].text(0.05, 1.08, "(B)", transform=axs[1].transAxes, fontsize=18, verticalalignment='top')
axs[1].text(0.05, 0.96, "Lullabies", transform=axs[1].transAxes, fontsize=20, verticalalignment='top')

# Add legend to the right plot
axs[1].legend(handles=[line1, line2, line3], fontsize=14, loc='upper right')


# plt.tight_layout()
# plt.show()
# plt.savefig("W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/gaze_figs_sec/SF_pla_offlul_samescale.svg")
plt.savefig("W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_gaze_figs_sec/SF_pla_lul_OFF_samescale.svg")










### ENVELOPE
t_val_env_pla_off, p_val_env_pla_off = cluster_test(BIG_ERCs_ENV_PLA_OFF,BIG_ERCs_ENV_SUR_PLA_OFF)
RDN_CORR_env_PLA_off = np.load(path+'RDN_p_ENV_PLA_OFF.npy')
# np.save(savepath + "pvalue_ENV_PLA_OFF.npy",p_val_env_pla_off)
# np.save(savepath + "tvalue_ENV_PLA_OFF.npy",t_val_env_pla_off)
p_v_env_pla_off = compare_real_to_cluster(p_val_env_pla_off,RDN_CORR_env_PLA_off,p_to_test)
# np.save(savepath + "pv_ENV_PLA_OFF.npy",p_val_env_pla_off)
p_v_env_pla_off_times = np.hstack((p_v_env_pla_off[:, np.newaxis], t_val_env_pla_off[:, np.newaxis], p_val_env_pla_off[:, np.newaxis]))
# np.save(savepath + "p_v_times_PLA_OFF.npy", p_v_env_pla_off_times)

t_val_env_lul_off, p_val_env_lul_off = cluster_test(BIG_ERCs_ENV_LUL_OFF,BIG_ERCs_ENV_SUR_LUL_OFF)
RDN_CORR_env_lul_off = np.load(path+'RDN_p_ENV_LUL_OFF.npy')
# np.save("pvalue_ENV_LUL_OFF.npy",p_val_env_lul_off)
# np.save("tvalue_ENV_LUL_OFF.npy",t_val_env_lul_off)
p_v_env_lul_off = compare_real_to_cluster(p_val_env_lul_off,RDN_CORR_env_lul_off,p_to_test)
# np.save("pv_ENV_LUL_OFF.npy",p_val_env_lul_off)
p_v_env_lul_off_times = np.hstack((p_v_env_lul_off[:, np.newaxis], t_val_env_lul_off[:, np.newaxis], p_val_env_lul_off[:, np.newaxis]))
# np.save(savepath + "p_v_times_LUL_OFF.npy", p_v_env_lul_off_times)


#plots

line_width = 4
line_height = 1

fig, axs = plt.subplots(1, 2, figsize=(20, 6))

# Plot Playsongs
axs[0].plot(rt, mean_ENV_PLA_OFF, label='Social Gaze Data', color='#009e74', linewidth=3)
axs[0].fill_between(rt, mean_ENV_PLA_OFF - sigma_ENV_PLA_OFF, mean_ENV_PLA_OFF + sigma_ENV_PLA_OFF, alpha=0.1, color='#009e74')
axs[0].plot(rt, mean_ENV_SUR_PLA_OFF, label='Surrogate Data', color='#56b4e9', linewidth=3)
axs[0].fill_between(rt, mean_ENV_SUR_PLA_OFF - sigma_ENV_SUR_PLA_OFF, mean_ENV_SUR_PLA_OFF + sigma_ENV_SUR_PLA_OFF, alpha=0.1, color='#56b4e9')
axs[0].axvline(x=0, color='black', linestyle='--')
# axs[0].plot(rt, line_height * np.mean(BIG_ERCs_SF_PLA_OFF) * p_v_sf_pla_off, linewidth=line_width, color='#d55e00')
axs[0].plot(rt, line_height * 170 * p_v_env_pla_off, linewidth=line_width, color='#d55e00')
axs[0].set_xlabel("Time relative to Infant Gaze Offset (s)", fontsize=20)
axs[0].set_ylabel("Amplitude Envelope", fontsize=20)
axs[0].set_xlim(-5, 5)
axs[0].set_ylim(80, 190)
axs[0].text(0.05, 1.08, "(A)", transform=axs[0].transAxes, fontsize=18, verticalalignment='top')
axs[0].text(0.05, 0.96, "Playsongs", transform=axs[0].transAxes, fontsize=20, verticalalignment='top')

# Plot Lullabies
line1, = axs[1].plot(rt, mean_ENV_LUL_OFF, label='Social Gaze Data', color='#009e74', linewidth=3)
axs[1].fill_between(rt, mean_ENV_LUL_OFF - sigma_ENV_LUL_OFF, mean_ENV_LUL_OFF + sigma_ENV_LUL_OFF, alpha=0.1, color='#009e74')
line2, = axs[1].plot(rt, mean_ENV_SUR_LUL_OFF, label='Surrogate Data', color='#56b4e9', linewidth=3)
axs[1].fill_between(rt, mean_ENV_SUR_LUL_OFF - sigma_ENV_SUR_LUL_OFF, mean_ENV_SUR_LUL_OFF + sigma_ENV_SUR_LUL_OFF, alpha=0.1, color='#56b4e9')
axs[1].axvline(x=0, color='black', linestyle='--')
# line3, = axs[1].plot(rt, line_height * np.mean(BIG_ERCs_SF_LUL_OFF) * p_v_sf_lul_off, label='p<.05/2', linewidth=line_width, color='#d55e00')
line3, = axs[1].plot(rt, line_height * 160 * p_v_env_lul_off, label='p < 5th/2 percentile', linewidth=line_width, color='#d55e00')

axs[1].set_xlabel("Time relative to Infant Gaze Offset (s)", fontsize=20)
axs[1].set_ylabel("Amplitude Envelope", fontsize=20)
axs[1].set_xlim(-5, 5)
axs[1].set_ylim(80, 190)
axs[1].text(0.05, 1.08, "(B)", transform=axs[1].transAxes, fontsize=18, verticalalignment='top')
axs[1].text(0.05, 0.96, "Lullabies", transform=axs[1].transAxes, fontsize=20, verticalalignment='top')

# Add legend to the right plot
axs[1].legend(handles=[line1, line2, line3], fontsize=14, loc='upper right')


# plt.tight_layout()
# plt.show()
# plt.savefig("W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/gaze_figs_sec/SF_pla_offlul_samescale.svg")
plt.savefig("W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_gaze_figs_sec/ENV_pla_lul_OFF_samescale.svg")





### F0

t_val_f0_pla_off, p_val_f0_pla_off = cluster_test(BIG_ERCs_F0_PLA_OFF,BIG_ERCs_F0_SUR_PLA_OFF)
RDN_CORR_f0_pla_off = np.load(path+'RDN_p_F0_PLA_OFF.npy')
# np.save(savepath + "pvalue_F0_PLA_OFF.npy",p_val_f0_pla_off)
# np.save(savepath + "tvalue_F0_PLA_OFF.npy",t_val_f0_pla_off)
p_v_f0_pla_off = compare_real_to_cluster(p_val_f0_pla_off,RDN_CORR_f0_pla_off,p_to_test)
# np.save(savepath + "pv_F0_PLA_OFF.npy",p_val_f0_pla_off)
p_v_f0_pla_off_times = np.hstack((p_v_f0_pla_off[:, np.newaxis], t_val_f0_pla_off[:, np.newaxis], p_val_f0_pla_off[:, np.newaxis]))
# np.save(savepath + "p_v_times_PLA_OFF.npy", p_v_f0_pla_off_times)

t_val_f0_lul_off, p_val_f0_lul_off = cluster_test(BIG_ERCs_F0_LUL_OFF,BIG_ERCs_F0_SUR_LUL_OFF)
RDN_CORR_f0_lul_off = np.load(path+'RDN_p_F0_LUL_OFF.npy')
# np.save("pvalue_F0_LUL_OFF.npy",p_val_f0_lul_off)
# np.save("tvalue_F0_LUL_OFF.npy",t_val_f0_lul_off)
p_v_f0_lul_off = compare_real_to_cluster(p_val_f0_lul_off,RDN_CORR_f0_lul_off,p_to_test)
# np.save("pv_F0_LUL_OFF.npy",p_v_f0_lul_off)
p_v_f0_lul_off_times = np.hstack((p_v_f0_lul_off[:, np.newaxis], t_val_f0_lul_off[:, np.newaxis], p_val_f0_lul_off[:, np.newaxis]))
# np.save(savepath + "p_v_times_LUL_OFF.npy", p_v_f0_lul_off_times)


#plots
line_width = 4
line_height = 1

fig, axs = plt.subplots(1, 2, figsize=(20, 6))

# Plot Playsongs
axs[0].plot(rt, mean_F0_PLA_OFF, label='Social Gaze Data', color='#009e74', linewidth=3)
axs[0].fill_between(rt, mean_F0_PLA_OFF - sigma_F0_PLA_OFF, mean_F0_PLA_OFF + sigma_F0_PLA_OFF, alpha=0.1, color='#009e74')
axs[0].plot(rt, mean_F0_SUR_PLA_OFF, label='Surrogate Data', color='#56b4e9', linewidth=3)
axs[0].fill_between(rt, mean_F0_SUR_PLA_OFF - sigma_F0_SUR_PLA_OFF, mean_F0_SUR_PLA_OFF + sigma_F0_SUR_PLA_OFF, alpha=0.1, color='#56b4e9')
axs[0].axvline(x=0, color='black', linestyle='--')
# axs[0].plot(rt, line_height * np.mean(BIG_ERCs_SF_PLA_OFF) * p_v_sf_pla_OFF, linewidth=line_width, color='#d55e00')
axs[0].plot(rt, line_height * 260 * p_v_f0_pla_off, linewidth=line_width, color='#d55e00')
axs[0].set_xlabel("Time relative to Infant Gaze Offset (s)", fontsize=20)
axs[0].set_ylabel("Pitch (F0)", fontsize=20)
axs[0].set_xlim(-5, 5)
axs[0].set_ylim(230,270)
axs[0].text(0.05, 1.08, "(A)", transform=axs[0].transAxes, fontsize=18, verticalalignment='top')
axs[0].text(0.05, 0.96, "Playsongs", transform=axs[0].transAxes, fontsize=20, verticalalignment='top')


# Plot Lullabies
line1, = axs[1].plot(rt, mean_F0_LUL_OFF, label='Social Gaze Data', color='#009e74', linewidth=3)
axs[1].fill_between(rt, mean_F0_LUL_OFF - sigma_F0_LUL_OFF, mean_F0_LUL_OFF + sigma_F0_LUL_OFF, alpha=0.1, color='#009e74')
line2, = axs[1].plot(rt, mean_F0_SUR_LUL_OFF, label='Surrogate Data', color='#56b4e9', linewidth=3)
axs[1].fill_between(rt, mean_F0_SUR_LUL_OFF - sigma_F0_SUR_LUL_OFF, mean_F0_SUR_LUL_OFF + sigma_F0_SUR_LUL_OFF, alpha=0.1, color='#56b4e9')
axs[1].axvline(x=0, color='black', linestyle='--')
# line3, = axs[1].plot(rt, line_height * np.mean(BIG_ERCs_SF_LUL_OFF) * p_v_sf_lul_OFF, label='p<.05/2', linewidth=line_width, color='#d55e00')
line3, = axs[1].plot(rt, line_height * 260 * p_v_f0_lul_off, label='p < 5th/2 percentile', linewidth=line_width, color='#d55e00')

axs[1].set_xlabel("Time relative to Infant Gaze Offset (s)", fontsize=20)
axs[1].set_ylabel("Pitch (F0)", fontsize=20)
axs[1].set_xlim(-5, 5)
axs[1].set_ylim(230,270)
axs[1].text(0.05, 1.08, "(B)", transform=axs[1].transAxes, fontsize=18, verticalalignment='top')
axs[1].text(0.05, 0.96, "Lullabies", transform=axs[1].transAxes, fontsize=20, verticalalignment='top')

# Add legend to the right plot
axs[1].legend(handles=[line1, line2, line3], fontsize=14, loc='upper right')


# plt.tight_layout()
# plt.show()
plt.savefig("W:/hoehl/projects/sing/Acoustic_analysis_SRE/specflux_python/seconds/revision/revision_gaze_figs_sec/F0_pla_lul_OFF_samescale.svg")




