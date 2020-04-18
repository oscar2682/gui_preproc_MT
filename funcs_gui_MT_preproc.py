from sys import exit
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
plt.style.use('bmh')

def plot_file(fn):
    f = open(fn)
    lines = f.readlines()
    ns = int(lines[1][-3:])
    ofn = fn.split("/")[-1].split(".")[0]
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
                volt.append(float(lines[idx+14+j].split()[3].replace(",", "")))
                err.append(float(lines[idx+14+j].split()[4].replace(",", "")))
            axs[cont].loglog(t,volt,'.-', label="Sounding %02d" % (cont+1))
            axs[cont].get_shared_x_axes().join(axs[cont], axs[cont-1])
            axs[cont].legend(loc=1)
            idx = idx + npts + 22
            cont += 1
        axs[cont-1].set_xlabel("Time, s")
        axs[cont-1].set_ylabel("Volt/Amp",fontsize=8)
    elif ns == 1 and ofn[0] == "R":
        idx = 10
        npts = int(lines[idx][-3:])
        t = []; volt = []; err = []
        for j in range(0,npts):
            t.append(float(lines[idx+14+j].split()[1].replace(",", "")))
            volt.append(float(lines[idx+14+j].split()[3].replace(",", "")))
            err.append(float(lines[idx+14+j].split()[4].replace(",", "")))
        plt.figure(figsize=(8,4))
        plt.title("Noise curve for: %s" % ofn,fontsize=18)
        plt.loglog(t,volt,'.-', label="Noise sounding")
        plt.xlabel("Time, s")
        plt.ylabel("Volt/Amp")
        plt.legend(loc=1)
    plt.tight_layout()
    plt.savefig(ofn + ".png",dpi=300)
    plt.show()
