from sys import exit
import os
from os import path
import matplotlib.pyplot as plt
import warnings
from numpy import absolute,where, array, logical_and
import stat
import subprocess as sp
warnings.filterwarnings("ignore")
plt.style.use('bmh')

def plot_file(fn):
    global all_surveys, all_times, all_errors, t_n, volt_n, err_n, ofn
    f = open(fn)
    lines = f.readlines()
    ns = int(lines[1][-3:])
    ofn = fn.split("/")[-1].split(".")[0]
    noisefn = fn.replace(ofn,"R" + ofn)
    all_surveys = []
    all_times = []
    all_errors = []
    flg1 = 0
    if path.isfile(noisefn):
        if ns > 0:
            idx = 10
            cont = 0
            fig = plt.subplots(1, 1,figsize=(18, 6),facecolor='w',edgecolor='k')
            plt.title("Ploting file: %s" % ofn,fontsize=18)
            for i in range(0,ns):
                npts = int(lines[idx][-3:])
                t = []; volt = []; err = []
                for j in range(0,npts):
                    t.append(float(lines[idx+14+j].split()[1].replace(",", "")))
                    volt.append(absolute(float(\
                            lines[idx+14+j].split()[3].replace(",", ""))))
                    err.append(float(lines[idx+14+j].split()[4].replace(",", "")))
                plt.loglog(t,volt,'.-', label="Sounding %02d" % (cont+1))
                idx = idx + npts + 22
                cont += 1
                all_surveys.append(volt)
                all_times.append(t)
                all_errors.append(err)
        f = open(noisefn)
        lines = f.readlines()
        idx = 10
        npts = int(lines[idx][-3:])
        t_n = []; volt_n = []; err_n = []
        for j in range(0,npts):
            t_n.append(float(lines[idx+14+j].split()[1].replace(",", "")))
            volt_n.append(absolute(float(\
                    lines[idx+14+j].split()[3].replace(",", ""))))
            err_n.append(float(lines[idx+14+j].split()[4].replace(",", "")))
        plt.loglog(t_n,volt_n,'.-', label="Noise sounding")
#        plt.errorbar(t_n, volt_n, yerr=err, ls='none',label="Error bar",elinewidth=0.5)
        plt.xlabel("Time, s")
        plt.ylabel("Volt/Amp",fontsize=8)
#        plt.ylim([1e-8,1e-3])
        plt.legend(loc=1)
        flg1 = 1
    else:
        if ns > 1:
            idx = 10
            cont = 0
            plt.figure(figsize=(18, 6),facecolor='w',edgecolor='k')
            plt.title("Ploting file: %s" % ofn,fontsize=18)
            for i in range(0,ns):
                npts = int(lines[idx][-3:])
                t = []; volt = []; err = []
                for j in range(0,npts):
                    t.append(float(lines[idx+14+j].split()[1].replace(",", "")))
                    volt.append(absolute(float(\
                            lines[idx+14+j].split()[3].replace(",", ""))))
                    err.append(float(lines[idx+14+j].split()[4].replace(",", "")))
                plt.loglog(t,volt,'.-', label="Sounding %02d" % (cont+1))
                plt.legend(loc=3)
                idx = idx + npts + 22
                cont += 1
                all_surveys.append(volt)
                all_times.append(t)
                all_errors.append(err)
            plt.xlabel("Time, s")
            plt.ylabel("Volt/Amp",fontsize=8)
            flg1 = 0
    plt.tight_layout()
    plt.savefig(ofn + ".png",dpi=300)
    plt.show()
    return flg1

def get_info_labels(fn):
    f = open(fn)
    lines = f.readlines()
    ns = int(lines[1][-3:])
    return ns

def clean_survey(svy_num):
    global f_t, f_volt, f_err
    volt = all_surveys[svy_num-1]
    t = all_times[svy_num-1]
    err = all_errors[svy_num-1]
    plt.figure(figsize=(18, 6),facecolor='w',edgecolor='k')
    plt.title("Survey Number: %02d" % int(svy_num),fontsize=18)
    plt.xlabel("Time, s")
    plt.ylabel("Volt/Amp",fontsize=8)
    plt.loglog(t,volt,'.-', label="Sounding %02d" % (svy_num))
    plt.loglog(t_n,volt_n,'.-', label="Noise")
    plt.errorbar(t, volt, yerr=err, ls='none',label="Error bar")
    plt.legend(loc=1)
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
    fig, axs = plt.subplots(2, 1,figsize=(18, 6),facecolor='w',edgecolor='k')
    axs[0].set_title("Survey Number: %02d" % int(svy_num),fontsize=18)
    axs[0].loglog(t,volt,'.-', label="Sounding %02d" % (svy_num))
    axs[0].errorbar(t, volt, yerr=err, ls='none',label="Error bar")
    axs[0].axvspan(t0,t1,alpha=0.15,color='red',label="Final cut")
    axs[0].legend(loc=3)
    axs[0].set_xlabel("Time, s")
    axs[0].set_ylabel("Volt/Amp",fontsize=8)
    axs[1].loglog(f_t,f_volt,'.-', label="Sounding %02d" % (svy_num))
    axs[1].errorbar(f_t, f_volt, yerr=f_err, ls='none',label="Error bar")
    axs[1].loglog(t_n,volt_n,'.-', label="Noise")
    axs[1].set_xlabel("Time, s")
    axs[1].set_ylabel("Volt/Amp",fontsize=8)
    axs[1].legend(loc=1)
    axs[1].get_shared_x_axes().join(axs[1], axs[0])
    plt.tight_layout()
    plt.show()

def write_data_all_datafile(clen,rlen,val=[]):
    global datafilename
    f_err1 = []
    if val:
        for i in range(len(f_t)):
            f_err1.append(val)
    else:
        for i in range(len(f_t)):
            f_err1.append(f_err[i])

    datafilename  = "%s.inv" % ofn
    dfn = open(datafilename, 'w')
    dfn.write("TEM\n")
    dfn.write(" %s\n" % ofn)
    dfn.write("   0.0000000000000000        0.0000000000000000        %20.15f        %20.15f\n" % (clen,clen))
    dfn.write("   1.0000000000000000\n")
    dfn.write(" %20.15f\n" % (rlen*-1.0))
    dfn.write("%d\n" % (len(f_t)))
    for i in range(len(f_t)):
        dfn.write("%14.12f  %14.12f  %14.12f\n" % (f_t[i], f_volt[i], f_err1[i]))
    dfn.close()

def write_inv_occ1(invtype,numlay,tcklay,deplay,reslay,maxite):
    if invtype == "occ1":
        invfn = open("emufood_occ_r1", 'w')
        invfn.write("!rm -r tem_occr1.epl\n")
    elif invtype == "occ2":
        invfn = open("emufood_occ_r2", 'w')
        invfn.write("!rm -r tem_occr2.epl\n")
    invfn.write("\n")
    invfn.write("modl\n")
    invfn.write("%d\n" % numlay)
    invfn.write("yes\n")
    invfn.write("%d\n" % tcklay)
    invfn.write("%d\n" % deplay)
    invfn.write("yes\n")
    invfn.write("%d\n" % reslay)
    invfn.write("yes\n")
    invfn.write("m0_occam\n")
    invfn.write("\n")
    invfn.write("load\n")
    invfn.write("TLHZ\n")
    invfn.write("no\n")
    invfn.write("no\n")
    invfn.write("no\n")
    invfn.write("yes\n")
    invfn.write("%s\n" % datafilename)
    invfn.write("setu\n")
    invfn.write("invm\n")
    invfn.write("2\n")
    invfn.write("invp\n")
    invfn.write("0.8\n")
    invfn.write("10\n")
    invfn.write("%d\n" % maxite)
    if invtype == "occ1":
        invfn.write("1\n")
    elif invtype == "occ2":
        invfn.write("2\n")
    invfn.write("2\n")
    invfn.write("0.901\n")
    invfn.write("no\n")
    invfn.write("1\n")
    invfn.write("erro\n")
    invfn.write("yes\n")
    invfn.write("no\n")
    invfn.write("1.6\n")
    invfn.write("5\n")
    invfn.write("yes\n")
    invfn.write("no\n")
    invfn.write("exit\n")
    invfn.write("\n")
    invfn.write("fix\n")
    invfn.write("c\n")
    invfn.write("e\n")
    invfn.write("auto\n")
    invfn.write("savd\n")
    invfn.write("%s.dat\n" % ofn)
    invfn.write("xypl\n")
    invfn.write("no\n")
    if invtype == "occ1":
        invfn.write("tem_occr1\n")
    elif invtype == "occ2":
        invfn.write("tem_occr2\n")
    invfn.write("\n")
    invfn.write("!mv synth* tem_occr1.epl\n")
    invfn.write("!mv *.olo tem_occr1.epl\n")
    invfn.write("!mv *.mod tem_occr1.epl\n")
    invfn.write("!mv *.ps tem_occr1.epl\n")
    invfn.write("!mv *.dat tem_occr1.epl\n")
    invfn.write("!mv *.mod tem_occr1.epl\n")
    invfn.write("\n")
    invfn.write("exit\n")
    invfn.close()

def run_inversion(invtype):
    if invtype == "occ1":
        inv_infile = "emufood_occ_r1"
    elif invtype == "occ2":
        inv_infile = "emufood_occ_r2"
    fn = open("shinv",'w')
    fn.write("inversion/emuplus < %s" %inv_infile)
    fn.close()
    st = os.stat('shinv')
    os.chmod('shinv', st.st_mode | stat.S_IEXEC)
    sp.call('shinv', shell=True)
