"""
Author: Filipe Azevedo
Title: Convergence Plot
Version: v1 
Created: 2024/02

Ansys version: 2021R2

Description:
Builds Convergence and Timestep plot from Ansys analysis and send it to an e-mail in an specific time interval.

"""

import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import time
import win32com.client

global FORCES, DISPLACEMENTS, SCRATCH

FORCES = True
DISPLACEMENTS = False
SCRATCH = '_ProjectScratch'


def joinPath(path1, path2):
    pathComb = os.path.join(path1,path2)
    return pathComb

def findAnalysis(analysis, analysis_folder, main_folder):
    # return (0,0): No .gst file in either folders - ProjectScratch or Analysis Folder
    # return (0,subPath): Analysis not finished yet, but ProjectScratch exist
    # return (1, analysis Folder): Analysis finished, plot final convergence plot and move to next simulation if exists

    if os.path.exists( joinPath(analysis_folder[analysis], 'file.gst') ):
        return 1, analysis_folder[analysis]
    if os.path.exists( joinPath(main_folder, SCRATCH)):
        list_subfolders_with_paths = [ f.path for f in os.scandir( joinPath(main_folder, SCRATCH) ) if f.is_dir() ] 
        for subPath in list_subfolders_with_paths:
            if os.path.exists( joinPath(subPath, 'file.gst') ):
                return 0, subPath
    return 0,0        

def plotConvergence(analysis_folder, plot_folder):
    os.chdir(analysis_folder)

    tree = ET.parse('file.gst')
    root = tree.getroot()
    f_crit = False
    u_crit = False

    # Collects all column Id fom XML file
    for child in root[0][0]:
        if str(child.text) == 'Cum Iter':
            cum_iter = int(child.attrib["ID"])
        elif str(child.text) == 'F   CRIT':
            f_crit = int(child.attrib["ID"])
        elif str(child.text) == 'F    L2 ':
            f_norm = int(child.attrib["ID"])
        elif str(child.text) == 'U   CRIT':
            u_crit = int(child.attrib["ID"])
        elif str(child.text) == 'U    INF':
            u_inf = int(child.attrib["ID"])
        elif str(child.text) == 'Time':
            time = int(child.attrib["ID"])
        elif str(child.text) == 'Bisection':
            b_sec = int(child.attrib["ID"])
        elif str(child.text) == 'Load Step':
            l_step = int(child.attrib["ID"])
        elif str(child.text) == 'Sub-step':
            s_step = int(child.attrib["ID"])   


    #FORCES = FORCES * f_crit
    #DISPLACEMENTS = DISPLACEMENTS * u_crit
    #print(DISPLACEMENTS)
    data_line = ''

    for ls in range(0,len(root[0:])):
        for child in root[ls:][0]:
            data_line = data_line + child.text #child.text extracts all information below ColData

    data_line = data_line.split('\n')
    cum_iter_counter = []
    load_step_counter = []
    sub_step_counter = []
    b_sec_counter = []
    force_criteria = []
    force_norm = []
    displacement_criteria = []
    displacement_norm = []
    time_counter = []

    for c in range(0,len(data_line)):
        if data_line[c] != '' and data_line[c] != ' ' :
            while '  ' in data_line[c]:
                data_line[c] = data_line[c].replace('  ', ' ')
            data_line_current = data_line[c].split(' ')
            cum_iter_counter.append(float(data_line_current[cum_iter]))
            load_step_counter.append(float(data_line_current[l_step]))
            sub_step_counter.append(float(data_line_current[s_step]))
            b_sec_counter.append(float(data_line_current[b_sec]))
            time_counter.append(float(data_line_current[time]))
            #print(cum_iter_counter)
            if FORCES:
                force_criteria.append(float(data_line_current[f_crit]))
                force_norm.append(float(data_line_current[f_norm]))
            if DISPLACEMENTS:
                displacement_criteria.append(float(data_line_current[u_crit]))
                displacement_norm.append(float(data_line_current[u_inf]))

    # Filtering position for Load step, sub-step and Bisection 
    for load_step in range(0,len(cum_iter_counter)-1):
        if load_step_counter[load_step] < load_step_counter[load_step+1]:
            load_step_counter[load_step] = cum_iter_counter[load_step]
        else:
            load_step_counter[load_step] = 0
    del load_step_counter[-1]              

    for sub_step in range(0,len(cum_iter_counter)-1):
        if sub_step_counter[sub_step] < sub_step_counter[sub_step+1]:
            sub_step_counter[sub_step] = cum_iter_counter[sub_step]
        else:
            sub_step_counter[sub_step] = 0
    del sub_step_counter[-1] 

    for bis in range(0,len(cum_iter_counter)-1):
        if b_sec_counter[bis] != 0:
            b_sec_counter[bis] = cum_iter_counter[bis]

    # deleting all zeros from np arrays (vertical lines only)
    load_step_counter = np.asanyarray(load_step_counter)
    load_step_counter = load_step_counter[load_step_counter != 0]
    sub_step_counter = np.asanyarray(sub_step_counter)
    sub_step_counter = sub_step_counter[sub_step_counter != 0]
    b_sec_counter = np.asanyarray(b_sec_counter)
    b_sec_counter = b_sec_counter[b_sec_counter != 0]

    # Converting to np array
    cum_iter_counter = np.asarray(cum_iter_counter)
    sub_step_counter = np.asanyarray(sub_step_counter)
    b_sec_counter = np.asanyarray(b_sec_counter)
    force_criteria = np.asarray(force_criteria)
    force_norm = np.asarray(force_norm)
    displacement_criteria = np.asarray(displacement_criteria)
    displacement_norm = np.asarray(displacement_norm)
    current_time = float(data_line_current[time])

    # Plotting convergence
    plt.cla()
    plt.title('Time = ' + str(current_time) + ' [sec]', loc = 'center')
    plt.xlabel('Cumulative Iteration')
    plt.ylabel('Force [N]')
    plt.yscale("log")
    if FORCES:
        plt.plot(cum_iter_counter, force_criteria, 'c', label = 'Force Crit')
        plt.plot(cum_iter_counter, force_norm, 'm', label = 'F Norm')
    if DISPLACEMENTS:
        plt.plot(cum_iter_counter, displacement_criteria, label = 'U Crit')
        plt.plot(cum_iter_counter, displacement_norm, label = 'U Norm')

    # vertical lines for Load-Step Converged, Sub-Step Converged and Bissection
    if len(load_step_counter != 0):
        plt.vlines(x = load_step_counter, ymin = 0, ymax = max(force_norm),
                colors = 'blue',
                label = 'Load step Converged',
                linestyles= 'dashed')
    if len(sub_step_counter != 0):
        plt.vlines(x = sub_step_counter, ymin = 0, ymax = max(force_norm),
                colors = 'lime',
                label = 'Sub-step Converged',
                linestyles= 'dashed')
    if len(b_sec_counter != 0):
        plt.vlines(x = b_sec_counter, ymin = 0, ymax = max(force_norm),
                colors = 'red',
                label = 'Bisection',
                linestyles= 'dashed')

    # Saving Plot
    plt.legend(loc = 'upper right')
    plt.grid()
    os.chdir(plot_folder)
    plt.savefig('PlotConvForce.png', bbox_inches='tight', dpi=199)

    # plotting timesteps
    plt.cla()
    plt.title('Time')
    plt.xlabel('Cumulative Iteration')
    plt.ylabel('Time [s]')
    plt.plot(cum_iter_counter, time_counter, 'r')
    plt.grid()
    plt.savefig('PlotTime.png', bbox_inches='tight', dpi=199)

def AnsysConvergencePlotter(main_folder, analysis_folder, timerInterval, email):
    
    # analysis counter
    analysis = 0 

    while True:
        if os.path.exists( os.path.join( main_folder,'plots' ) ) == False:
            os.mkdir( os.path.join( main_folder,'plots' ) )
            plot_folder = os.path.join( main_folder,'plots' )
        else:
            plot_folder = os.path.join( main_folder,'plots' )    
        
        # Puts sript to sleep
        print(f"Sleeping for {timerInterval}s\n")
        time.sleep(timerInterval)
        print("Going to find the folder for plots\n")
        
        # Search for folder with analysis, build plots
        typeAnalysis, analysis_path = findAnalysis(analysis, analysis_folder, main_folder)
        plotConvergence(analysis_path, plot_folder)
        # tracking analysis
        analysis = analysis + typeAnalysis                                                  
        print("Plots saved. Going to send it\n")

        # Sending plots to e-mail
        if analysis_path == 0:
            print("No .gst files yet created. Checking later.\n")
        elif typeAnalysis == 1:
            plot = joinPath(plot_folder,'PlotConvForce.png')
            time_plot = joinPath(plot_folder, 'PlotTime.png')
            o = win32com.client.Dispatch("Outlook.Application")
            mail = o.CreateItem(0)
            mail.To = email
            mail.Subject = "Ansys Convergence Report"
            mail.Body = "The simulation has finished."
            mail.Attachments.Add(plot)
            mail.Attachments.Add(time_plot)
            mail.Send()
        elif typeAnalysis == 0:
            plot = joinPath(plot_folder,'PlotConvForce.png')
            time_plot = joinPath(plot_folder, 'PlotTime.png')        
            o = win32com.client.Dispatch("Outlook.Application")
            mail = o.CreateItem(0)
            mail.To = email
            mail.Subject = "Ansys Convergence Report"
            mail.Body = "This is the current Status of the simulation."
            mail.Attachments.Add(plot)
            mail.Attachments.Add(time_plot)        
            mail.Send()
        if analysis > (len(analysis_folder)-1):
            print("all completed.")
            break