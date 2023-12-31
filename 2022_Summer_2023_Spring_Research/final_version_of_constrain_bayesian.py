# -*- coding: utf-8 -*-
"""“Final Version of Constrain Bayesian.ipynb”的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xCqWsc_hIB3ZbJPuVJkSDD6Obai5LwBM
"""

'''
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
'''

import math
from numpy import dot
from scipy import special
import numpy as np

def qosGenerator(gammap, k, lambdap, Nrp, W0 = 1024, beita = 0.2, Band = 20, Nf_value = 1.2589e-13):

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

    Band = Band #120
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
    nmimo = 1 ##### MIMO rate = 2

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
    #beta(M)=beita   #beta(M)=M/R/2 old code

    #Call the subroutine to derive pt, pi_0, and pi_{XMT} from Eq. (7)
    pt, pi_0, pi_XMT, ED = SubrSNRC_pi(M, rE, T, W0, lambdap, AIFS, sigma)
    #Calculate QoS metrics
    #256QAM with 8 dB Gain
    ed = ED
    pt = dot(pt, (1 + 1 / (Nrp + 1))) / 2
    B1 = Band ####################B1=20
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
    for i in range(1, Nrp.astype(np.int64) + 1 + 1):
    # for i in range(1, Nrp + 1 + 1):
        ss = ss + dot(dot(special.comb(Nrp + 1, i), tPRP ** i), (1 - tPRP) ** (Nrp + 1 - i))
    PRP = ss


    #print('prp:%f\n'% PRP)
    #print('ed:%f\n'% ed)
    #print('cbr:%f'% CBR)



    #########################
    # ---   constrain   --- #
    #########################
    if (PRP >= 0.999) & (ed <= 0.01):
        constrain = 1      #符合要求
    else:
        constrain = 0      #不符合要求

    return -CBR, constrain, PRP, ed

import warnings
warnings.filterwarnings('ignore')

# example of bayesian optimization for a 1d function from scratch
import numpy as np
from math import sin
from math import pi
from numpy import arange
from numpy import vstack
from numpy import argmax
from numpy import asarray
from numpy.random import normal
from numpy.random import random
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from warnings import catch_warnings
from warnings import simplefilter
from matplotlib import pyplot

# objective function
#完成
def mul_objective(paraSet):
    gammap  = paraSet[0]
    k       = paraSet[1]
    lambdap = paraSet[2]
    Nrp     = paraSet[3]
    return qosGenerator(gammap, k, lambdap, Nrp)[:2]


# surrogate or approximation for the objective function
#完成
def surrogate(model, X_mul):
    # catch any warning generated when making a prediction
    with catch_warnings():
        # ignore generated warnings
        simplefilter("ignore")
        return model.predict(X_mul, return_std=True)

# probability of improvement acquisition function
#完成
def acquisition(X_mul, Xsamples_mul, model_CBR, model_constrain):
    # calculate the best surrogate score found so far
    CBRHat, _       = surrogate(model_CBR, X_mul)
    constrainHat, _ = surrogate(model_constrain, X_mul)
    best = max(CBRHat * constrainHat)
    # calculate mean and stdev via surrogate function
    mu, std         = surrogate(model_CBR, Xsamples_mul)
    delt, delt_std  = surrogate(model_constrain, Xsamples_mul)
    mu   = mu
    delt_mu = delt
    # calculate the probability of improvement
    CBRprobs = norm.cdf((mu - best) / (std+1E-9))
    deltprob = norm.cdf((delt_mu - best) / (delt_std+1E-9))
    return CBRprobs*deltprob

# optimize the acquisition function
#完成 大概
def opt_acquisition(X_mul, y, model_CBR, model_constrain):
    # random search, generate random samples
    Xsamples_mul = [[]]
    for i in range(1000):
        gammap   = np.random.random()*10          #0-10      continue
        k        = np.random.randint(0,3)*2 + 6   #6, 8, 10  discrete
        lambdap  = np.random.randint(1, 20 + 1)   #1-20      discrete
        Nrp      = np.random.randint(1, 10 + 1)   #1-10      discrete
        setArray = [[gammap, k, lambdap, Nrp]]

        if i == 0:
            Xsamples_mul = setArray
        else:
            Xsamples_mul = np.r_[Xsamples_mul, setArray]
    Xsamples_mul = np.asarray(Xsamples_mul)
    ##Xsamples_mul = np.asarray([[np.random.random() for i in range(2)] for j in range(100)])
    ##Xsamples_mul = Xsamples_mul.reshape(len(X_mul[0]), len(X_mul))

    # calculate the acquisition function for each sample
    scores = acquisition(X_mul, Xsamples_mul, model_CBR, model_constrain)

    # locate the index of the largest scores
    ix = argmax(scores)
    return Xsamples_mul[ix]



# sample the domain sparsely with noise
# reshape into rows and cols

initial = 5
X_mul = [[]]
for i in range(initial - 1):
    gammap   = np.random.random()*10          #0-10      continue
    k        = np.random.randint(0,3)*2 + 6   #6, 8, 10  discrete
    lambdap  = np.random.randint(1, 20 + 1)   #1-20      discrete
    Nrp      = np.random.randint(1, 10 + 1)   #1-10      discrete

    setArray = [[gammap, k, lambdap, Nrp]]

    if i == 0:
        X_mul = setArray
    else:
        X_mul = np.r_[X_mul, setArray]
X_mul = np.asarray(X_mul)

CBR_list        = []
constrain_list  = []
for paraSet in X_mul:
    CBR, constrain  = mul_objective(paraSet)
    CBR_list        = np.r_[CBR_list, CBR]
    constrain_list  = np.r_[constrain_list, constrain]

CBR_list        = np.asarray(CBR_list)
constrain_list  = np.asarray(constrain_list)
CBR_list = CBR_list.reshape(len(CBR_list), 1)
constrain_list = constrain_list.reshape(len(constrain_list), 1)

# define the model

model_constrain = GaussianProcessRegressor()
model_CBR       = GaussianProcessRegressor()

# fit the model
model_constrain.fit(X_mul, constrain_list)
model_CBR.fit(X_mul, CBR_list)
# plot before hand
# plot(X_mul, y, model)


# perform the optimization process
CBR_min = 999

myCBR = []
trueCBR = []
falseCBR = []
myminCBR = []

for i in range(100):
    # select the next point to sample

    x_single_mul = opt_acquisition(X_mul, CBR_list, model_CBR, model_constrain)
    # sample the point
    actual_CBR, actual_constrain = mul_objective(x_single_mul)
    # summarize the finding
    est_CBR, _       = surrogate(model_CBR, [x_single_mul]) ##[[x]]
    est_constrain, _ = surrogate(model_constrain, [x_single_mul]) ##[[x]]
    #print('>>>  x = %s, f()=%3f, actual=%.3f' % (x_single_mul, est, actual))

    # add the data to the dataset
    X_mul = vstack((X_mul, x_single_mul))
    CBR_list = vstack((CBR_list, [[actual_CBR]]))
    constrain_list = vstack((constrain_list, [[actual_constrain]]))
    # update the model
    #model.fit(X_mul, CBR_list)
    model_constrain.fit(X_mul, constrain_list)
    model_CBR.fit(X_mul, CBR_list)

    if actual_constrain == 1:
        myCBR.append(-actual_CBR)
        trueCBR.append(-actual_CBR)
        falseCBR.append(None)
    else:
        myCBR.append(999)
        trueCBR.append(None)
        falseCBR.append(-actual_CBR)

    if (-actual_CBR < CBR_min):
        CBR_min = -actual_CBR
        print('\033[0;33;46m#{:<4d}gamma = {:^10.6f}  k = {:^10.1f}  lambda = {:^10.1f}  Nrp = {:^10.1f}, f()={:^10.3f}, actual CBR={:^10.5f}, est_constrain={:^10.1f}, actual_constrain={:^10d}'.format( i,
                                                                                                                                                                                                        x_single_mul[0],
                                                                                                                                                                                                        x_single_mul[1],
                                                                                                                                                                                                        x_single_mul[2],
                                                                                                                                                                                                        x_single_mul[3],
                                                                                                                                                                                                        -est_CBR[0],
                                                                                                                                                                                                        -actual_CBR,
                                                                                                                                                                                                        est_constrain[0],
                                                                                                                                                                                                        actual_constrain)
                )
    else:
        print('\033[0;30m#{:<4d}gamma = {:^10.6f}  k = {:^10.1f}  lambda = {:^10.1f}  Nrp = {:^10.1f}, f()={:^10.3f}, actual CBR={:^10.5f}, est_constrain={:^10.1f}, actual_constrain={:^10d}'.format(i,
                                                                                                                                            x_single_mul[0],
                                                                                                                                            x_single_mul[1],
                                                                                                                                            x_single_mul[2],
                                                                                                                                            x_single_mul[3],
                                                                                                                                            -est_CBR[0],
                                                                                                                                            -actual_CBR,
                                                                                                                                            est_constrain[0],
                                                                                                                                            actual_constrain)
                )
    #print('>>>  x = %s, f()=%3f, actual=%.3f' % (x_single_mul, est, actual))

# plot all samples and the final surrogate function
#plot(X, y, model)
# best result
ix = argmax(CBR_list)
for i in range(np.size(myCBR)):
    myminCBR.append(None)
myminCBR[ix] = CBR_min
print(CBR_min)

################
# --- Plot --- #
################

'''
trueCBR = []
falseCBR = []
myminCBR = []
'''

import numpy as np
import matplotlib.pyplot as plt

def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

y = smooth_curve(-CBR_list[-np.size(myminCBR):])

ingore_first = 0

#mooth_loss_history = smooth_curve(loss[ingore_first:])
#mooth_val_loss_history = smooth_curve(val_loss[ingore_first:])
epochs = range(ingore_first + 1, len(y) + 1)

#plt.figure(dpi=100)
plt.figure(figsize=(10,8),dpi=130)
#plt.plot(epochs, mooth_loss_history, '-y', label='Training loss')
plt.plot(epochs, y, 'y', linewidth = 5.0, label='CBR')
plt.plot(epochs, trueCBR, 'b.', markersize = 10.0, label='true CBR')
plt.plot(epochs, falseCBR, 'bx', markersize = 10.0, label='false CBR')
plt.plot(epochs, myminCBR, 'rD', markersize = 10.0, label='minCBR')
plt.ylim(0,0.2)
plt.title('Band = 120, \u03B2 = 0.2', fontsize = 20)
plt.xlabel('Epochs', fontsize = 18)
plt.ylabel('CBR', fontsize = 18)
plt.legend(fontsize = 18)

"""下面是算不同初始点下的寻优结果比较。更改第二个代码块中88行的（initial = 5）。"""

y5 = -CBR_list[-np.size(myminCBR):]  # initial = 5

y20 = -CBR_list[-np.size(myminCBR):]  # initial = 20

y50 = -CBR_list[-np.size(myminCBR):]  # initial = 50

y150 = -CBR_list[-np.size(myminCBR):]

################
# --- Plot Comparison --- #
################

'''
trueCBR = []
falseCBR = []
myminCBR = []
'''

import numpy as np
import matplotlib.pyplot as plt

def smooth_curve(points, factor=0.8):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

line5 = smooth_curve(y5)
line20 = smooth_curve(y20)
line50 = smooth_curve(y50)
line150 = smooth_curve(y150)

ingore_first = 0

#mooth_loss_history = smooth_curve(loss[ingore_first:])
#mooth_val_loss_history = smooth_curve(val_loss[ingore_first:])
epochs = range(ingore_first + 1, len(line5) + 1)

#plt.figure(dpi=100)
plt.figure(figsize=(10,8),dpi=130)
#plt.plot(epochs, mooth_loss_history, '-y', label='Training loss')
plt.plot(epochs, line5, 'y', linewidth = 3.0, label='Initial sampling number = 5')
plt.plot(epochs, line20, 'b', linewidth = 3.0, label='Initial sampling number = 20')
plt.plot(epochs, line50, 'r', linewidth = 3.0, label='Initial sampling number = 50')
plt.plot(epochs, line150, 'g', linewidth = 3.0, label='Initial sampling number = 150')
plt.ylim(0,0.5)
#plt.title('', fontsize = 20)
plt.xlabel('Epochs', fontsize = 18)
plt.ylabel('CBR', fontsize = 18)
plt.legend(fontsize = 18)