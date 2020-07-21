from sys import exit
import os
import matplotlib.pyplot as plt
import warnings
from numpy import absolute,where, array, logical_and
warnings.filterwarnings("ignore")
plt.style.use('bmh')

def plot_file(fn):
    global all_surveys, all_times, all_errors
    f = open(fn)
    lines = f.readlines()
    ns = int(lines[1][-3:])
    ofn = fn.split("/")[-1].split(".")[0]
    all_surveys = []
    all_times = []
    all_errors = []
    if ns > 1:
        idx = 10
        cont = 0
        fig, axs = plt.subplots(ns, 1,figsize=(8, 10),facecolor='w',edgecolor='k')
        axs[0].set_title("Ploting file: %s" % ofn,fontsize=18)
        for i in range(0,ns):
            npts = int(lines[idx][-3:])
            t = []; volt = []; err = []
            for j in range(0,npts):
                t.append(float(lines[idx+14+j].split()[1].replace(",", "")))
                volt.append(absolute(float(\
                        lines[idx+14+j].split()[3].replace(",", ""))))
                err.append(float(lines[idx+14+j].split()[4].replace(",", "")))
            axs[cont].loglog(t,volt,'.-', label="Sounding %02d" % (cont+1))
            axs[cont].errorbar(t, volt, yerr=err, ls='none',label="Error bar")
            axs[cont].get_shared_x_axes().join(axs[cont], axs[cont-1])
            axs[cont].legend(loc=3)
            idx = idx + npts + 22
            cont += 1
            all_surveys.append(volt)
            all_times.append(t)
            all_errors.append(err)
        axs[cont-1].set_xlabel("Time, s")
        axs[cont-1].set_ylabel("Volt/Amp",fontsize=8)
    elif ns == 1 and ofn[0] == "R":
        idx = 10
        npts = int(lines[idx][-3:])
        t = []; volt = []; err = []
        for j in range(0,npts):
            t.append(float(lines[idx+14+j].split()[1].replace(",", "")))
            volt.append(absolute(float(\
                    lines[idx+14+j].split()[3].replace(",", ""))))
            err.append(float(lines[idx+14+j].split()[4].replace(",", "")))
        plt.figure(figsize=(8,4))
        plt.title("Noise curve for: %s" % ofn,fontsize=18)
        plt.loglog(t,volt,'.-', label="Noise sounding")
        plt.errorbar(t, volt, yerr=err, ls='none',label="Error bar")
        plt.xlabel("Time, s")
        plt.ylabel("Volt/Amp")
        plt.legend(loc=3)
    plt.tight_layout()
    plt.savefig(ofn + ".png",dpi=300)
    plt.show()

def get_info_labels(fn):
    f = open(fn)
    lines = f.readlines()
    ns = int(lines[1][-3:])
    return ns

def clean_survey(svy_num):
    volt = all_surveys[svy_num-1]
    t = all_times[svy_num-1]
    err = all_errors[svy_num-1]
    plt.figure(figsize=(8, 3),facecolor='w',edgecolor='k')
    plt.title("Survey Number: %02d" % int(svy_num),fontsize=18)
    plt.xlabel("Time, s")
    plt.ylabel("Volt/Amp",fontsize=8)
    plt.loglog(t,volt,'.-', label="Sounding %02d" % (svy_num))
    plt.errorbar(t, volt, yerr=err, ls='none',label="Error bar")
    plt.tight_layout()
    lim_pts = plt.ginput(2)
    plt.close()
    t0 = lim_pts[0][0]
    t1 = lim_pts[1][0]
    idx = where( (t >= t0) & (t <= t1))[0]
    f_volt = []
    f_t = []
    f_err = []
    for i in idx:
        f_volt.append(volt[i])
        f_t.append(t[i])
        f_err.append(err[i])
    fig, axs = plt.subplots(2, 1,figsize=(8, 4),facecolor='w',edgecolor='k')
    axs[0].set_title("Survey Number: %02d" % int(svy_num),fontsize=18)
    axs[0].loglog(t,volt,'.-', label="Sounding %02d" % (svy_num))
    axs[0].errorbar(t, volt, yerr=err, ls='none',label="Error bar")
    axs[0].axvspan(t0,t1,alpha=0.15,color='red',label="Ventana cortada")
    axs[0].legend(loc=3)
    axs[0].set_xlabel("Time, s")
    axs[0].set_ylabel("Volt/Amp",fontsize=8)
    axs[1].loglog(f_t,f_volt,'.-', label="Sounding %02d" % (svy_num))
    axs[1].errorbar(f_t, f_volt, yerr=f_err, ls='none',label="Error bar")
    axs[1].set_xlabel("Time, s")
    axs[1].set_ylabel("Volt/Amp",fontsize=8)
    axs[1].legend(loc=3)
    axs[1].get_shared_x_axes().join(axs[1], axs[0])
    plt.tight_layout()
    plt.show()
