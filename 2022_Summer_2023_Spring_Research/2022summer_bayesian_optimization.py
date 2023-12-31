# -*- coding: utf-8 -*-
"""2022Summer_Bayesian_Optimization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZUjFoaUeoIG3Uktkz4dYuFwsS_TQolpd

STEP 1
"""

###################################
# --- Library Initialization  --- #
###################################
!pip install bayesian-optimization

"""STEP 2"""

#############################
# ---   import libary   --- #
#############################
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from bayes_opt import BayesianOptimization, UtilityFunction
import warnings
warnings.filterwarnings("ignore")

import math
from numpy import dot
from scipy import special

import time

#############################
# ---   analyst model   --- #
#############################

# This This function is an analysis function for communication networks.
# It has seven inputs and three outputs.
#
# ---> Inputs: gammap, k, lambdap, Nrp, W0, beita, Nf_value
# ---> Output: CBR, ED, PRP
#
# Among these seven input values, we only perform the optimization search for
# the first four parameters. The remaining parameters will be set to constants.

def qosGenerator(gammap, k, lambdap, Nrp, W0 = 1024, beita = 0.2, Nf_value = 1.2589e-13):

    def SubrSNRC_pi(M=None, re=None, T=None, W0=None, lambdap=None, DIFS=None, sigma=None, *args, **kwargs):

        R = re
        lambda_ = lambdap / 1000000.0
        Ntr = M
        Ncs = Ntr
        Nph = dot(2.0, Ntr) - Ncs
        rho = 1
        rho_old = 0
        pb = 1
        epsilon = 1e-06
        while (abs(rho_old - rho) > epsilon):
            pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)),
                                                                                                    (1 / lambda_ + DIFS)))
            Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
            pb1 = 1 - np.exp(dot(- Ntr, Pxmt))
            if (pb1 < 0):
                pb1 = 0
            while (abs(pb1 - pb) > epsilon):
                pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)), (
                        1 / lambda_ + DIFS)))
                Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
                pbb = 1 - np.exp(dot(- Ntr, Pxmt))
                if (pbb < 0):
                    pbb = 0
                pb1 = pb
                pb = pbb
            pb = pb1
            qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
            mu_tem = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
            rho_old = rho
            if (lambda_ < mu_tem):
                rho = lambda_ / mu_tem
            else:
                rho = 1
        qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
        mu = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
        # ==========================================================================
        var_PA = 0
        mean_service = 1 / mu / 1000000.0
        var_service = dot((dot(dot(dot((W0 - 1), (dot(2, W0) - 1)), (sigma + dot(pb, T)) ** 2),
                            (1 - dot((1 - qb), (1 - rho)))) / 6 + dot(
            dot((W0 - 1), (dot(var_PA, pb) + dot(dot(T ** 2, pb), (1 - pb)) + dot(dot(2, T), (sigma + dot(pb, T))))),
            (1 - dot((1 - qb), (1 - rho)))) / 2 + var_PA + T ** 2 - (
                                dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))),
                                    (W0 - 1)) / 2 + T) ** 2), (1 / 1000000.0) ** 2)
        # ==========================================================================
        EDq = dot(lambdap, (var_service + mean_service ** 2)) / (dot(2, (1 - rho)))
        ED = EDq + mean_service
        # ==========================================================================
        pi_XMT = dot(2, T) / (
                dot((rho + dot(qb, (1 - rho))), (dot((sigma + dot(pb, T)), W0) + (sigma - dot(pb, T)))) + dot(2,
                                                                                                            T) + dot(
            dot(2, (1 - rho)), (1 / lambda_ + DIFS)))
        P_XMT = dot(pi_XMT, (T - DIFS + dot(dot(2, sigma), W0))) / (dot(W0, T))
        # --------------------------------------------------------------------------
        pi_0 = dot(dot(pi_XMT, (rho + dot(qb, (1 - rho)))), sigma) / T
        # ==========================================================================
        pt = dot(dot(pi_XMT, 2), (T - DIFS)) / T
        return pt, pi_0, pi_XMT, ED


    if __name__ == '__main__':
        pass


    #initialization
    ds = 100      #change from 350
    R = 100
    #beita = 0.2
    M = 1
    gammap=gammap ##########NEW#ADD###############

    Band = 20
    PAn = 1600
    nds = 52
    cr = 5 / 6
    nhmac = 64
    tbdh = 4
    kb = Band / 5
    sigma = 21 / kb
    SIFS = 64 / kb
    AIFS = SIFS + dot(2, sigma)
    tsym = 16 / kb
    tpre = math.floor(160 / kb)
    nmimo = 1 ##### MIMO rate = 2在原来的代码里

    #Payload duration calculation
    Ts = tpre + AIFS + dot(tsym, np.ceil((dot(PAn, 8) + nhmac) / (dot(dot(k, nds), cr)))) + tbdh
    Ts = Ts / nmimo
    Tp = (Ts - tpre - AIFS - tbdh)
    T = Ts + dot(Tp, (Nrp))

    #Network parameter settingup
    d0 = 1
    dc = 102
    Pt = 0.28183815
    Rth = 1.3969e-15
    Pth = 1.3969e-15
    Inta = 1.63726e-05
    Nf = Nf_value          #dot(0.0001, 1.2589e-13)  ################NEW#ADD##################
    alfa1 = 2.56
    alfa2 = 6.34
    rE = dot((gammap) ** (1 / alfa2), R)
    sigma1 = 3.9
    sigma2 = 5.2

    M = round(dot(dot(2, rE), beita)) ################NEW#ADD##################
    #The Density of vehicles on the road
    #beta(M)=beita   #beta(M)=M/R/2 旧代码

    #Call the subroutine to derive pt, pi_0, and pi_{XMT} from Eq. (7)
    pt, pi_0, pi_XMT, ED = SubrSNRC_pi(M, rE, T, W0, lambdap, AIFS, sigma)
    #Calculate QoS metrics
    #256QAM with 8 dB Gain
    ed = ED
    pt = dot(pt, (1 + 1 / (Nrp + 1))) / 2
    B1 = Band ####################原来是B1=20
    Dr = 68.82
    Sr = np.arange(0, 1300, 0.5)
    EbNo = dot(dot(Sr, 10 ** 0.8), B1) / Dr
    MM = 2 ** k
    x3 = np.sqrt(dot(dot(3, k), EbNo) / (MM - 1))
    Pbg = dot(dot(dot((4 / k), (1 - 1 / np.sqrt(MM))), (1 / 2)), special.erfc(x3 / math.sqrt(2)))
    FER = 1 - (1 - Pbg) ** (dot(PAn, 8))

    if ds <= dc:
        sigma = sigma1
    else:
        sigma = sigma2
    theta = 0

    CSINR=np.ones(2600)
    dt=np.ones(2600)
    while theta < 1300:
        theta1 = int(1 + np.floor(dot(theta, 2))) - 1
        if ds <= dc:
            DImax = dot((theta) ** (1 / alfa1), ds)
            if DImax > dc:
                DImax = dot(dot((theta) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax = dot(dot((theta) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax > dc:
                DImax = dot((theta) ** (1 / alfa2), ds)
        if ds <= dc:
            DImax2 = dot((dot(2, theta)) ** (1 / alfa1), ds)
            if DImax2 > dc:
                DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax2 > dc:
                DImax2 = dot((dot(2, theta)) ** (1 / alfa2), ds)
        N_ht = max(DImax - rE + ds, 0) + max(DImax - rE - ds, 0)
        Psh = 1 - np.exp(dot(dot(- pt, N_ht), beita))
        N_ht21 = (max(DImax2 - max(DImax, rE + ds), 0))
        N_ht22 = (max(DImax2 - max(DImax, rE - ds), 0))
        Phc = dot((1 - np.exp(dot(dot(- pt, N_ht21), beita))), (1 - np.exp(dot(dot(- pt, N_ht22), beita))))
        Ncc = min(DImax, rE - ds) + min(DImax, rE + ds)
        Pcc = 1 - np.exp(dot(dot(- pi_0, Ncc), beita))
        Pt1=gammap*Pt ################NEW#ADD##################

        if ds <= dc:
            Pr = dot(dot(Pt1, Inta), (d0 / ds) ** alfa1)################NEW#ADD##################change Pt to Pt1
        else:
            Pr = dot(dot(dot(Pt1, Inta), (d0 / dc) ** alfa1), (dc / ds) ** alfa2)################NEW#ADD##################change Pt to Pt1
        Prdb = dot(10, np.log10(Pr))
        Fn = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(dot(Nf, theta)))) / 2 ** (1 / 2) / sigma)))

        Prth = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(Rth))) / 2 ** (1 / 2) / sigma)))
        CSINR[theta1] = 1 - dot(dot(dot((1 - Psh), (1 - Phc)), (1 - Pcc)), (1 - Fn))
        dt[theta1] = theta
        theta = theta + 0.5

    #Calculate the dFSINR
    dFSINR = np.diff(CSINR) / np.diff(dt)

    #Calculate the integral
    sum = 0
    for th in range(1, 2598 + 1):   # Might be arange(1, 2598+1, 1)
        num = dot(dot(FER[th - 1], dFSINR[th - 1]), 0.5)
        sum = sum + num


    Integration = sum
    tPRP = dot((1 - Integration), (1 - Prth))

    #Transmission capacity and throughput
    Pdc = 1 - np.exp(dot(dot(dot(- pi_0, 2), beita), rE))################NEW#ADD##################change R to rE
    Pdh = (1 - np.exp(dot(dot(- pt, rE), beita) / 2)) ** 2################NEW#ADD##################change R to rE
    TC = dot(dot(dot(dot(2, lambdap), rE), beita), (1 - Pdc / 2 - Pdh / 2))################NEW#ADD##################change R to rE
    CBR = dot(dot(TC, T), 1e-06)
    cbr = CBR
    Thruput = dot(CBR, (Nrp + 1))

    #PRP with repetitions
    ss = 0
    for i in range (1, int(Nrp) + 1 + 1):  #(1, Nrp.astype(np.int64) + 1 + 1):
        ss = ss + dot(dot(special.comb(Nrp + 1, i), tPRP ** i), (1 - tPRP) ** (Nrp + 1 - i))
    PRP = ss


    #print('prp:%f\n'% PRP)
    #print('ed:%f\n'% ed)
    #print('cbr:%f'% CBR)



    #########################
    # ---   constrain   --- #
    #########################

    #penalty = 1000000  #1000000
    #if (PRP >= 0.999) & (ed <= 0.01):
    #    return -CBR,PRP,ed
    #else:
    return -CBR

# Prepare the data.

t1 = time.perf_counter()
# Create the optimizer. The black box function to optimize is not
# specified here, as we will call that function directly later on.
optimizer = BayesianOptimization(f = qosGenerator,
                                 pbounds = {'gammap': [1,10],
                                            'k': [6,10],
                                            'lambdap': [1, 20],
                                            'Nrp': [1, 10]},
                                 verbose = 2, random_state = 1234,
                                 allow_duplicate_points=True)
# let the init_points = 5
# let the iteration = 100

a = optimizer.maximize(init_points = 5, n_iter = 100)
t2 = time.perf_counter()
print("Best result: {}; f(x) = {}.".format(optimizer.max["params"], -1 * optimizer.max["target"]),'time taken to run:',t2-t1)

# 'Nrp': 5.434506633360701, 'gammap': 8.905423463802887, 'k': 6.971498676061573, 'lambdap': 2.7234252325602806
def qosGenerator_PRP(gammap, k, lambdap, Nrp, W0 = 1024, beita = 0.3, Nf_value = 1.2589e-13):

    def SubrSNRC_pi(M=None, re=None, T=None, W0=None, lambdap=None, DIFS=None, sigma=None, *args, **kwargs):

        R = re
        lambda_ = lambdap / 1000000.0
        Ntr = M
        Ncs = Ntr
        Nph = dot(2.0, Ntr) - Ncs
        rho = 1
        rho_old = 0
        pb = 1
        epsilon = 1e-06
        while (abs(rho_old - rho) > epsilon):
            pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)),
                                                                                                    (1 / lambda_ + DIFS)))
            Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
            pb1 = 1 - np.exp(dot(- Ntr, Pxmt))
            if (pb1 < 0):
                pb1 = 0
            while (abs(pb1 - pb) > epsilon):
                pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)), (
                        1 / lambda_ + DIFS)))
                Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
                pbb = 1 - np.exp(dot(- Ntr, Pxmt))
                if (pbb < 0):
                    pbb = 0
                pb1 = pb
                pb = pbb
            pb = pb1
            qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
            mu_tem = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
            rho_old = rho
            if (lambda_ < mu_tem):
                rho = lambda_ / mu_tem
            else:
                rho = 1
        qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
        mu = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
        # ==========================================================================
        var_PA = 0
        mean_service = 1 / mu / 1000000.0
        var_service = dot((dot(dot(dot((W0 - 1), (dot(2, W0) - 1)), (sigma + dot(pb, T)) ** 2),
                            (1 - dot((1 - qb), (1 - rho)))) / 6 + dot(
            dot((W0 - 1), (dot(var_PA, pb) + dot(dot(T ** 2, pb), (1 - pb)) + dot(dot(2, T), (sigma + dot(pb, T))))),
            (1 - dot((1 - qb), (1 - rho)))) / 2 + var_PA + T ** 2 - (
                                dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))),
                                    (W0 - 1)) / 2 + T) ** 2), (1 / 1000000.0) ** 2)
        # ==========================================================================
        EDq = dot(lambdap, (var_service + mean_service ** 2)) / (dot(2, (1 - rho)))
        ED = EDq + mean_service
        # ==========================================================================
        pi_XMT = dot(2, T) / (
                dot((rho + dot(qb, (1 - rho))), (dot((sigma + dot(pb, T)), W0) + (sigma - dot(pb, T)))) + dot(2,
                                                                                                            T) + dot(
            dot(2, (1 - rho)), (1 / lambda_ + DIFS)))
        P_XMT = dot(pi_XMT, (T - DIFS + dot(dot(2, sigma), W0))) / (dot(W0, T))
        # --------------------------------------------------------------------------
        pi_0 = dot(dot(pi_XMT, (rho + dot(qb, (1 - rho)))), sigma) / T
        # ==========================================================================
        pt = dot(dot(pi_XMT, 2), (T - DIFS)) / T
        return pt, pi_0, pi_XMT, ED


    if __name__ == '__main__':
        pass


    #initialization
    ds = 100      #change from 350
    R = 100
    #beita = 0.2
    M = 1
    gammap=gammap ##########NEW#ADD###############

    Band = 20
    PAn = 1600
    nds = 52
    cr = 5 / 6
    nhmac = 64
    tbdh = 4
    kb = Band / 5
    sigma = 21 / kb
    SIFS = 64 / kb
    AIFS = SIFS + dot(2, sigma)
    tsym = 16 / kb
    tpre = math.floor(160 / kb)
    nmimo = 1 ##### MIMO rate = 2在原来的代码里

    #Payload duration calculation
    Ts = tpre + AIFS + dot(tsym, np.ceil((dot(PAn, 8) + nhmac) / (dot(dot(k, nds), cr)))) + tbdh
    Ts = Ts / nmimo
    Tp = (Ts - tpre - AIFS - tbdh)
    T = Ts + dot(Tp, (Nrp))

    #Network parameter settingup
    d0 = 1
    dc = 102
    Pt = 0.28183815
    Rth = 1.3969e-15
    Pth = 1.3969e-15
    Inta = 1.63726e-05
    Nf = Nf_value          #dot(0.0001, 1.2589e-13)  ################NEW#ADD##################
    alfa1 = 2.56
    alfa2 = 6.34
    rE = dot((gammap) ** (1 / alfa2), R)
    sigma1 = 3.9
    sigma2 = 5.2

    M = round(dot(dot(2, rE), beita)) ################NEW#ADD##################
    #The Density of vehicles on the road
    #beta(M)=beita   #beta(M)=M/R/2 旧代码

    #Call the subroutine to derive pt, pi_0, and pi_{XMT} from Eq. (7)
    pt, pi_0, pi_XMT, ED = SubrSNRC_pi(M, rE, T, W0, lambdap, AIFS, sigma)
    #Calculate QoS metrics
    #256QAM with 8 dB Gain
    ed = ED
    pt = dot(pt, (1 + 1 / (Nrp + 1))) / 2
    B1 = Band ####################原来是B1=20
    Dr = 68.82
    Sr = np.arange(0, 1300, 0.5)
    EbNo = dot(dot(Sr, 10 ** 0.8), B1) / Dr
    MM = 2 ** k
    x3 = np.sqrt(dot(dot(3, k), EbNo) / (MM - 1))
    Pbg = dot(dot(dot((4 / k), (1 - 1 / np.sqrt(MM))), (1 / 2)), special.erfc(x3 / math.sqrt(2)))
    FER = 1 - (1 - Pbg) ** (dot(PAn, 8))

    if ds <= dc:
        sigma = sigma1
    else:
        sigma = sigma2
    theta = 0

    CSINR=np.ones(2600)
    dt=np.ones(2600)
    while theta < 1300:
        theta1 = int(1 + np.floor(dot(theta, 2))) - 1
        if ds <= dc:
            DImax = dot((theta) ** (1 / alfa1), ds)
            if DImax > dc:
                DImax = dot(dot((theta) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax = dot(dot((theta) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax > dc:
                DImax = dot((theta) ** (1 / alfa2), ds)
        if ds <= dc:
            DImax2 = dot((dot(2, theta)) ** (1 / alfa1), ds)
            if DImax2 > dc:
                DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax2 > dc:
                DImax2 = dot((dot(2, theta)) ** (1 / alfa2), ds)
        N_ht = max(DImax - rE + ds, 0) + max(DImax - rE - ds, 0)
        Psh = 1 - np.exp(dot(dot(- pt, N_ht), beita))
        N_ht21 = (max(DImax2 - max(DImax, rE + ds), 0))
        N_ht22 = (max(DImax2 - max(DImax, rE - ds), 0))
        Phc = dot((1 - np.exp(dot(dot(- pt, N_ht21), beita))), (1 - np.exp(dot(dot(- pt, N_ht22), beita))))
        Ncc = min(DImax, rE - ds) + min(DImax, rE + ds)
        Pcc = 1 - np.exp(dot(dot(- pi_0, Ncc), beita))
        Pt1=gammap*Pt ################NEW#ADD##################

        if ds <= dc:
            Pr = dot(dot(Pt1, Inta), (d0 / ds) ** alfa1)################NEW#ADD##################change Pt to Pt1
        else:
            Pr = dot(dot(dot(Pt1, Inta), (d0 / dc) ** alfa1), (dc / ds) ** alfa2)################NEW#ADD##################change Pt to Pt1
        Prdb = dot(10, np.log10(Pr))
        Fn = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(dot(Nf, theta)))) / 2 ** (1 / 2) / sigma)))

        Prth = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(Rth))) / 2 ** (1 / 2) / sigma)))
        CSINR[theta1] = 1 - dot(dot(dot((1 - Psh), (1 - Phc)), (1 - Pcc)), (1 - Fn))
        dt[theta1] = theta
        theta = theta + 0.5

    #Calculate the dFSINR
    dFSINR = np.diff(CSINR) / np.diff(dt)

    #Calculate the integral
    sum = 0
    for th in range(1, 2598 + 1):   # Might be arange(1, 2598+1, 1)
        num = dot(dot(FER[th - 1], dFSINR[th - 1]), 0.5)
        sum = sum + num


    Integration = sum
    tPRP = dot((1 - Integration), (1 - Prth))

    #Transmission capacity and throughput
    Pdc = 1 - np.exp(dot(dot(dot(- pi_0, 2), beita), rE))################NEW#ADD##################change R to rE
    Pdh = (1 - np.exp(dot(dot(- pt, rE), beita) / 2)) ** 2################NEW#ADD##################change R to rE
    TC = dot(dot(dot(dot(2, lambdap), rE), beita), (1 - Pdc / 2 - Pdh / 2))################NEW#ADD##################change R to rE
    CBR = dot(dot(TC, T), 1e-06)
    cbr = CBR
    Thruput = dot(CBR, (Nrp + 1))

    #PRP with repetitions
    ss = 0
    for i in range (1, int(Nrp) + 1 + 1):  #(1, Nrp.astype(np.int64) + 1 + 1):
        ss = ss + dot(dot(special.comb(Nrp + 1, i), tPRP ** i), (1 - tPRP) ** (Nrp + 1 - i))
    PRP = ss


    #print('prp:%f\n'% PRP)
    #print('ed:%f\n'% ed)
    #print('cbr:%f'% CBR)



    #########################
    # ---   constrain   --- #
    #########################

    #penalty = 1000000  #1000000
    #if (PRP >= 0.999) & (ed <= 0.01):
    #    return -CBR,PRP,ed
    #else:
    return -CBR,PRP,ed

qosGenerator_PRP(1, 7.01, 1.0, 1.0)

t1 = time.perf_counter()
# This is the shaking function
import random


inputs = (1.0, 10.0, 1.0, 1.0)

# stats = qosGenerator_PRP(inputs[0], inputs[1],inputs[2],inputs[3])
# new_second = (6,8,10)
# while stats[1] < 0.999:
#   new_inputs = (random.uniform(0,10), random.choice(new_second), inputs[2], inputs[3])
#   stats = qosGenerator_PRP(new_inputs[0],new_inputs[1],new_inputs[2],new_inputs[3])


def shaking(i,j,k,l):
  stats = qosGenerator_PRP(i, j,k,l)
  new_second = (6,8,10)
  while stats[1] < 0.999:
    new_inputs = (random.uniform(0,10), random.choice(new_second), k, l)
    stats = qosGenerator_PRP(new_inputs[0],new_inputs[1],new_inputs[2],new_inputs[3])
  return stats[0]

cbr = shaking(1, 10, 1, 1)
print(cbr)

qosGenerator_PRP(9,10,1,1)

x,y = shaking(1,10,1,1)
min = x

for p in range(1,11):
  x,y = shaking(1,10,1,1)
  if(x < min):
    min = x


print(min)

################################################
#
#     0.3 Density
#
################################################

def qosGenerator_0_point_3(gammap, k, lambdap, Nrp, W0 = 1024, beita = 0.3, Nf_value = 1.2589e-13):

    def SubrSNRC_pi(M=None, re=None, T=None, W0=None, lambdap=None, DIFS=None, sigma=None, *args, **kwargs):

        R = re
        lambda_ = lambdap / 1000000.0
        Ntr = M
        Ncs = Ntr
        Nph = dot(2.0, Ntr) - Ncs
        rho = 1
        rho_old = 0
        pb = 1
        epsilon = 1e-06
        while (abs(rho_old - rho) > epsilon):
            pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)),
                                                                                                    (1 / lambda_ + DIFS)))
            Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
            pb1 = 1 - np.exp(dot(- Ntr, Pxmt))
            if (pb1 < 0):
                pb1 = 0
            while (abs(pb1 - pb) > epsilon):
                pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)), (
                        1 / lambda_ + DIFS)))
                Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
                pbb = 1 - np.exp(dot(- Ntr, Pxmt))
                if (pbb < 0):
                    pbb = 0
                pb1 = pb
                pb = pbb
            pb = pb1
            qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
            mu_tem = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
            rho_old = rho
            if (lambda_ < mu_tem):
                rho = lambda_ / mu_tem
            else:
                rho = 1
        qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
        mu = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
        # ==========================================================================
        var_PA = 0
        mean_service = 1 / mu / 1000000.0
        var_service = dot((dot(dot(dot((W0 - 1), (dot(2, W0) - 1)), (sigma + dot(pb, T)) ** 2),
                            (1 - dot((1 - qb), (1 - rho)))) / 6 + dot(
            dot((W0 - 1), (dot(var_PA, pb) + dot(dot(T ** 2, pb), (1 - pb)) + dot(dot(2, T), (sigma + dot(pb, T))))),
            (1 - dot((1 - qb), (1 - rho)))) / 2 + var_PA + T ** 2 - (
                                dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))),
                                    (W0 - 1)) / 2 + T) ** 2), (1 / 1000000.0) ** 2)
        # ==========================================================================
        EDq = dot(lambdap, (var_service + mean_service ** 2)) / (dot(2, (1 - rho)))
        ED = EDq + mean_service
        # ==========================================================================
        pi_XMT = dot(2, T) / (
                dot((rho + dot(qb, (1 - rho))), (dot((sigma + dot(pb, T)), W0) + (sigma - dot(pb, T)))) + dot(2,
                                                                                                            T) + dot(
            dot(2, (1 - rho)), (1 / lambda_ + DIFS)))
        P_XMT = dot(pi_XMT, (T - DIFS + dot(dot(2, sigma), W0))) / (dot(W0, T))
        # --------------------------------------------------------------------------
        pi_0 = dot(dot(pi_XMT, (rho + dot(qb, (1 - rho)))), sigma) / T
        # ==========================================================================
        pt = dot(dot(pi_XMT, 2), (T - DIFS)) / T
        return pt, pi_0, pi_XMT, ED


    if __name__ == '__main__':
        pass


    #initialization
    ds = 100      #change from 350
    R = 100
    #beita = 0.2
    M = 1
    gammap=gammap ##########NEW#ADD###############

    Band = 20
    PAn = 1600
    nds = 52
    cr = 5 / 6
    nhmac = 64
    tbdh = 4
    kb = Band / 5
    sigma = 21 / kb
    SIFS = 64 / kb
    AIFS = SIFS + dot(2, sigma)
    tsym = 16 / kb
    tpre = math.floor(160 / kb)
    nmimo = 1 ##### MIMO rate = 2在原来的代码里

    #Payload duration calculation
    Ts = tpre + AIFS + dot(tsym, np.ceil((dot(PAn, 8) + nhmac) / (dot(dot(k, nds), cr)))) + tbdh
    Ts = Ts / nmimo
    Tp = (Ts - tpre - AIFS - tbdh)
    T = Ts + dot(Tp, (Nrp))

    #Network parameter settingup
    d0 = 1
    dc = 102
    Pt = 0.28183815
    Rth = 1.3969e-15
    Pth = 1.3969e-15
    Inta = 1.63726e-05
    Nf = Nf_value          #dot(0.0001, 1.2589e-13)  ################NEW#ADD##################
    alfa1 = 2.56
    alfa2 = 6.34
    rE = dot((gammap) ** (1 / alfa2), R)
    sigma1 = 3.9
    sigma2 = 5.2

    M = round(dot(dot(2, rE), beita)) ################NEW#ADD##################
    #The Density of vehicles on the road
    #beta(M)=beita   #beta(M)=M/R/2 旧代码

    #Call the subroutine to derive pt, pi_0, and pi_{XMT} from Eq. (7)
    pt, pi_0, pi_XMT, ED = SubrSNRC_pi(M, rE, T, W0, lambdap, AIFS, sigma)
    #Calculate QoS metrics
    #256QAM with 8 dB Gain
    ed = ED
    pt = dot(pt, (1 + 1 / (Nrp + 1))) / 2
    B1 = Band ####################原来是B1=20
    Dr = 68.82
    Sr = np.arange(0, 1300, 0.5)
    EbNo = dot(dot(Sr, 10 ** 0.8), B1) / Dr
    MM = 2 ** k
    x3 = np.sqrt(dot(dot(3, k), EbNo) / (MM - 1))
    Pbg = dot(dot(dot((4 / k), (1 - 1 / np.sqrt(MM))), (1 / 2)), special.erfc(x3 / math.sqrt(2)))
    FER = 1 - (1 - Pbg) ** (dot(PAn, 8))

    if ds <= dc:
        sigma = sigma1
    else:
        sigma = sigma2
    theta = 0

    CSINR=np.ones(2600)
    dt=np.ones(2600)
    while theta < 1300:
        theta1 = int(1 + np.floor(dot(theta, 2))) - 1
        if ds <= dc:
            DImax = dot((theta) ** (1 / alfa1), ds)
            if DImax > dc:
                DImax = dot(dot((theta) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax = dot(dot((theta) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax > dc:
                DImax = dot((theta) ** (1 / alfa2), ds)
        if ds <= dc:
            DImax2 = dot((dot(2, theta)) ** (1 / alfa1), ds)
            if DImax2 > dc:
                DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax2 > dc:
                DImax2 = dot((dot(2, theta)) ** (1 / alfa2), ds)
        N_ht = max(DImax - rE + ds, 0) + max(DImax - rE - ds, 0)
        Psh = 1 - np.exp(dot(dot(- pt, N_ht), beita))
        N_ht21 = (max(DImax2 - max(DImax, rE + ds), 0))
        N_ht22 = (max(DImax2 - max(DImax, rE - ds), 0))
        Phc = dot((1 - np.exp(dot(dot(- pt, N_ht21), beita))), (1 - np.exp(dot(dot(- pt, N_ht22), beita))))
        Ncc = min(DImax, rE - ds) + min(DImax, rE + ds)
        Pcc = 1 - np.exp(dot(dot(- pi_0, Ncc), beita))
        Pt1=gammap*Pt ################NEW#ADD##################

        if ds <= dc:
            Pr = dot(dot(Pt1, Inta), (d0 / ds) ** alfa1)################NEW#ADD##################change Pt to Pt1
        else:
            Pr = dot(dot(dot(Pt1, Inta), (d0 / dc) ** alfa1), (dc / ds) ** alfa2)################NEW#ADD##################change Pt to Pt1
        Prdb = dot(10, np.log10(Pr))
        Fn = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(dot(Nf, theta)))) / 2 ** (1 / 2) / sigma)))

        Prth = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(Rth))) / 2 ** (1 / 2) / sigma)))
        CSINR[theta1] = 1 - dot(dot(dot((1 - Psh), (1 - Phc)), (1 - Pcc)), (1 - Fn))
        dt[theta1] = theta
        theta = theta + 0.5

    #Calculate the dFSINR
    dFSINR = np.diff(CSINR) / np.diff(dt)

    #Calculate the integral
    sum = 0
    for th in range(1, 2598 + 1):   # Might be arange(1, 2598+1, 1)
        num = dot(dot(FER[th - 1], dFSINR[th - 1]), 0.5)
        sum = sum + num


    Integration = sum
    tPRP = dot((1 - Integration), (1 - Prth))

    #Transmission capacity and throughput
    Pdc = 1 - np.exp(dot(dot(dot(- pi_0, 2), beita), rE))################NEW#ADD##################change R to rE
    Pdh = (1 - np.exp(dot(dot(- pt, rE), beita) / 2)) ** 2################NEW#ADD##################change R to rE
    TC = dot(dot(dot(dot(2, lambdap), rE), beita), (1 - Pdc / 2 - Pdh / 2))################NEW#ADD##################change R to rE
    CBR = dot(dot(TC, T), 1e-06)
    cbr = CBR
    Thruput = dot(CBR, (Nrp + 1))

    #PRP with repetitions
    ss = 0
    for i in range (1, int(Nrp) + 1 + 1):  #(1, Nrp.astype(np.int64) + 1 + 1):
        ss = ss + dot(dot(special.comb(Nrp + 1, i), tPRP ** i), (1 - tPRP) ** (Nrp + 1 - i))
    PRP = ss


    #print('prp:%f\n'% PRP)
    #print('ed:%f\n'% ed)
    #print('cbr:%f'% CBR)



    #########################
    # ---   constrain   --- #
    #########################

    #penalty = 1000000  #1000000
    #if (PRP >= 0.999) & (ed <= 0.01):
    #    return -CBR,PRP,ed
    #else:
    return -CBR,PRP,ed

###################################
#
#        120 Mega Hertz
#
###################################

def qosGenerator_120_MHz(gammap, k, lambdap, Nrp, W0 = 1024, beita = 0.2, Nf_value = 1.2589e-13):

    def SubrSNRC_pi(M=None, re=None, T=None, W0=None, lambdap=None, DIFS=None, sigma=None, *args, **kwargs):

        R = re
        lambda_ = lambdap / 1000000.0
        Ntr = M
        Ncs = Ntr
        Nph = dot(2.0, Ntr) - Ncs
        rho = 1
        rho_old = 0
        pb = 1
        epsilon = 1e-06
        while (abs(rho_old - rho) > epsilon):
            pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)),
                                                                                                    (1 / lambda_ + DIFS)))
            Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
            pb1 = 1 - np.exp(dot(- Ntr, Pxmt))
            if (pb1 < 0):
                pb1 = 0
            while (abs(pb1 - pb) > epsilon):
                pix = dot(2, T) / (dot(W0, (sigma + dot(pb, T))) + sigma - dot(pb, T) + dot(2, T) + dot(dot(2, (1 - rho)), (
                        1 / lambda_ + DIFS)))
                Pxmt = dot((T - DIFS - dot(2, sigma)), pix) / W0 / T + dot(dot(dot((1 - 1 / W0), 2), sigma), pix) / T
                pbb = 1 - np.exp(dot(- Ntr, Pxmt))
                if (pbb < 0):
                    pbb = 0
                pb1 = pb
                pb = pbb
            pb = pb1
            qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
            mu_tem = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
            rho_old = rho
            if (lambda_ < mu_tem):
                rho = lambda_ / mu_tem
            else:
                rho = 1
        qb = 1 - (1 - pb) ** (dot((T + DIFS), W0) / (T - DIFS + dot(dot(2, sigma), W0)))
        mu = 2 / (dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))), (W0 - 1)) + dot(2, T))
        # ==========================================================================
        var_PA = 0
        mean_service = 1 / mu / 1000000.0
        var_service = dot((dot(dot(dot((W0 - 1), (dot(2, W0) - 1)), (sigma + dot(pb, T)) ** 2),
                            (1 - dot((1 - qb), (1 - rho)))) / 6 + dot(
            dot((W0 - 1), (dot(var_PA, pb) + dot(dot(T ** 2, pb), (1 - pb)) + dot(dot(2, T), (sigma + dot(pb, T))))),
            (1 - dot((1 - qb), (1 - rho)))) / 2 + var_PA + T ** 2 - (
                                dot(dot((sigma + dot(pb, T)), (1 - dot((1 - qb), (1 - rho)))),
                                    (W0 - 1)) / 2 + T) ** 2), (1 / 1000000.0) ** 2)
        # ==========================================================================
        EDq = dot(lambdap, (var_service + mean_service ** 2)) / (dot(2, (1 - rho)))
        ED = EDq + mean_service
        # ==========================================================================
        pi_XMT = dot(2, T) / (
                dot((rho + dot(qb, (1 - rho))), (dot((sigma + dot(pb, T)), W0) + (sigma - dot(pb, T)))) + dot(2,
                                                                                                            T) + dot(
            dot(2, (1 - rho)), (1 / lambda_ + DIFS)))
        P_XMT = dot(pi_XMT, (T - DIFS + dot(dot(2, sigma), W0))) / (dot(W0, T))
        # --------------------------------------------------------------------------
        pi_0 = dot(dot(pi_XMT, (rho + dot(qb, (1 - rho)))), sigma) / T
        # ==========================================================================
        pt = dot(dot(pi_XMT, 2), (T - DIFS)) / T
        return pt, pi_0, pi_XMT, ED


    if __name__ == '__main__':
        pass


    #initialization
    ds = 100      #change from 350
    R = 100
    #beita = 0.2
    M = 1
    gammap=gammap ##########NEW#ADD###############

    Band = 120
    PAn = 1600
    nds = 52
    cr = 5 / 6
    nhmac = 64
    tbdh = 4
    kb = Band / 5
    sigma = 21 / kb
    SIFS = 64 / kb
    AIFS = SIFS + dot(2, sigma)
    tsym = 16 / kb
    tpre = math.floor(160 / kb)
    nmimo = 1 ##### MIMO rate = 2在原来的代码里

    #Payload duration calculation
    Ts = tpre + AIFS + dot(tsym, np.ceil((dot(PAn, 8) + nhmac) / (dot(dot(k, nds), cr)))) + tbdh
    Ts = Ts / nmimo
    Tp = (Ts - tpre - AIFS - tbdh)
    T = Ts + dot(Tp, (Nrp))

    #Network parameter settingup
    d0 = 1
    dc = 102
    Pt = 0.28183815
    Rth = 1.3969e-15
    Pth = 1.3969e-15
    Inta = 1.63726e-05
    Nf = Nf_value          #dot(0.0001, 1.2589e-13)  ################NEW#ADD##################
    alfa1 = 2.56
    alfa2 = 6.34
    rE = dot((gammap) ** (1 / alfa2), R)
    sigma1 = 3.9
    sigma2 = 5.2

    M = round(dot(dot(2, rE), beita)) ################NEW#ADD##################
    #The Density of vehicles on the road
    #beta(M)=beita   #beta(M)=M/R/2 旧代码

    #Call the subroutine to derive pt, pi_0, and pi_{XMT} from Eq. (7)
    pt, pi_0, pi_XMT, ED = SubrSNRC_pi(M, rE, T, W0, lambdap, AIFS, sigma)
    #Calculate QoS metrics
    #256QAM with 8 dB Gain
    ed = ED
    pt = dot(pt, (1 + 1 / (Nrp + 1))) / 2
    B1 = Band ####################原来是B1=20
    Dr = 68.82
    Sr = np.arange(0, 1300, 0.5)
    EbNo = dot(dot(Sr, 10 ** 0.8), B1) / Dr
    MM = 2 ** k
    x3 = np.sqrt(dot(dot(3, k), EbNo) / (MM - 1))
    Pbg = dot(dot(dot((4 / k), (1 - 1 / np.sqrt(MM))), (1 / 2)), special.erfc(x3 / math.sqrt(2)))
    FER = 1 - (1 - Pbg) ** (dot(PAn, 8))

    if ds <= dc:
        sigma = sigma1
    else:
        sigma = sigma2
    theta = 0

    CSINR=np.ones(2600)
    dt=np.ones(2600)
    while theta < 1300:
        theta1 = int(1 + np.floor(dot(theta, 2))) - 1
        if ds <= dc:
            DImax = dot((theta) ** (1 / alfa1), ds)
            if DImax > dc:
                DImax = dot(dot((theta) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax = dot(dot((theta) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax > dc:
                DImax = dot((theta) ** (1 / alfa2), ds)
        if ds <= dc:
            DImax2 = dot((dot(2, theta)) ** (1 / alfa1), ds)
            if DImax2 > dc:
                DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa2), (ds / dc) ** (alfa1 / alfa2)), dc)
        else:
            DImax2 = dot(dot((dot(2, theta)) ** (1 / alfa1), (ds / dc) ** (alfa2 / alfa1)), dc)
            if DImax2 > dc:
                DImax2 = dot((dot(2, theta)) ** (1 / alfa2), ds)
        N_ht = max(DImax - rE + ds, 0) + max(DImax - rE - ds, 0)
        Psh = 1 - np.exp(dot(dot(- pt, N_ht), beita))
        N_ht21 = (max(DImax2 - max(DImax, rE + ds), 0))
        N_ht22 = (max(DImax2 - max(DImax, rE - ds), 0))
        Phc = dot((1 - np.exp(dot(dot(- pt, N_ht21), beita))), (1 - np.exp(dot(dot(- pt, N_ht22), beita))))
        Ncc = min(DImax, rE - ds) + min(DImax, rE + ds)
        Pcc = 1 - np.exp(dot(dot(- pi_0, Ncc), beita))
        Pt1=gammap*Pt ################NEW#ADD##################

        if ds <= dc:
            Pr = dot(dot(Pt1, Inta), (d0 / ds) ** alfa1)################NEW#ADD##################change Pt to Pt1
        else:
            Pr = dot(dot(dot(Pt1, Inta), (d0 / dc) ** alfa1), (dc / ds) ** alfa2)################NEW#ADD##################change Pt to Pt1
        Prdb = dot(10, np.log10(Pr))
        Fn = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(dot(Nf, theta)))) / 2 ** (1 / 2) / sigma)))

        Prth = dot(1 / 2, (1 - special.erf((Prdb - dot(10, np.log10(Rth))) / 2 ** (1 / 2) / sigma)))
        CSINR[theta1] = 1 - dot(dot(dot((1 - Psh), (1 - Phc)), (1 - Pcc)), (1 - Fn))
        dt[theta1] = theta
        theta = theta + 0.5

    #Calculate the dFSINR
    dFSINR = np.diff(CSINR) / np.diff(dt)

    #Calculate the integral
    sum = 0
    for th in range(1, 2598 + 1):   # Might be arange(1, 2598+1, 1)
        num = dot(dot(FER[th - 1], dFSINR[th - 1]), 0.5)
        sum = sum + num


    Integration = sum
    tPRP = dot((1 - Integration), (1 - Prth))

    #Transmission capacity and throughput
    Pdc = 1 - np.exp(dot(dot(dot(- pi_0, 2), beita), rE))################NEW#ADD##################change R to rE
    Pdh = (1 - np.exp(dot(dot(- pt, rE), beita) / 2)) ** 2################NEW#ADD##################change R to rE
    TC = dot(dot(dot(dot(2, lambdap), rE), beita), (1 - Pdc / 2 - Pdh / 2))################NEW#ADD##################change R to rE
    CBR = dot(dot(TC, T), 1e-06)
    cbr = CBR
    Thruput = dot(CBR, (Nrp + 1))

    #PRP with repetitions
    ss = 0
    for i in range (1, int(Nrp) + 1 + 1):  #(1, Nrp.astype(np.int64) + 1 + 1):
        ss = ss + dot(dot(special.comb(Nrp + 1, i), tPRP ** i), (1 - tPRP) ** (Nrp + 1 - i))
    PRP = ss


    #print('prp:%f\n'% PRP)
    #print('ed:%f\n'% ed)
    #print('cbr:%f'% CBR)



    #########################
    # ---   constrain   --- #
    #########################

    #penalty = 1000000  #1000000
    #if (PRP >= 0.999) & (ed <= 0.01):
    #    return -CBR,PRP,ed
    #else:
    return -CBR,PRP,ed

# First Run Through
qosGenerator_120_MHz(1, 6.8677, 1.0, 1.0)

# Second Run Through
qosGenerator_120_MHz(1, 8.8677, 1.0, 1.0)