#!/usr/bin/env python
# coding: utf-8

import csv
from math import log
import numpy as np
from sklearn.linear_model import LinearRegression
from genser import *
from copy import deepcopy

def notbad(x, mean_value = 0, level = 10):
    return abs(x-mean_value)/min(x,mean_value) < level
def bad_filter(datafile, header=1, level=10):
    dataset = np.genfromtxt(datafile, delimiter=',', dtype = None, skip_header = header)
    mean_value = sum(dataset[:,1])/len(dataset[:,1])
    vbad = np.vectorize(notbad)
    dataset = dataset[vbad(dataset[:,1],mean_value,level)]
    return dataset
def bucket_maker(data, bucket_size):
    datalen = int((data[-1][0]-data[0][0])/bucket_size)+1
    blist = [data[np.logical_and(data[:,0]>di*bucket_size+data[0][0], 
                                 data[:,0]<(di+1)*bucket_size+data[0][0])][:,1] 
             for di in range(datalen)]
    blist = list(map(lambda x: sum(x)/len(x) if x.size > 0 else 0,blist))
    return np.array(blist), data[0][0]
def hentropy(zdata):
    vdata = sorted(list(set(zdata)))
    if 0 in vdata:
        vdata.remove(0)
    lz = len(zdata)
    parray = np.array([len(zdata[zdata == v])/lz for v in vdata])
    larray = np.vectorize(lambda x: -x*log(x))(parray)
    return sum(larray)
def rounded(ar1,k):
    fr = np.vectorize(lambda x,c: round(x,c))
    return fr(ar1,k)
def integered(ar1, k):
    rbarray = rounded(ar1,k)
    zarray = np.vectorize(int)(rbarray*10**k)
    zm = min(zarray[zarray!=0])
    return np.vectorize(lambda x: x-zm+1 if x else 0)(zarray), zm
def intarray(ar1):
    H,k = 0,0
    while True:
        zdata = integered(ar1, k)[0]
        Hn = hentropy(zdata)
        if Hn-H < 1  and Hn > 1:
            rk = k-1
            break
        else:
            H,k = Hn,k+1
    return rk
def make_integer_dataset(dataset, bucket_size):
    bdata, timeshift = bucket_maker(dataset, bucket_size)
    k = intarray(bdata)
    zdata, zmin = integered(bdata, k)
    return zdata, zmin, k, timeshift # датасет, добавка (минимальное целое), число учтенных знаков, стартовое время
    # Внимание! При обратном преобразовании нужно прибавлять к z не zmin, а zmin-1 !
def unification(zdata_list):
    ml = len(zdata_list[0])
    common_data = np.array(range(ml))
    for zd in zdata_list:
        ml = min(ml,len(zd))
        common_data = common_data[:ml]
        zd = zd[:ml]
        common_data = np.vstack((common_data, zd))
    return common_data.T
def unitimeseries(common_data):
    clear_data = []
    for cd in common_data:
        if all(cd[1:]):
            clear_data.append(cd)
    clear_data = np.array(clear_data)
    lcd = [list(cd) for cd in clear_data[:,1:]]
    onedim_data, dict_to1 = transform_to(lcd,1)
    res_data = [[t]+d for t,d in zip(clear_data[:,0],onedim_data)]
    return np.array(res_data), dict_to1
def transform_with(data, xdicts):
    f = 0
    xdicts.reverse()
    rdata = deepcopy(data)
    for r in xdicts:
        k, n = tuple(r[1].keys())
        Pk, Pn = tuple(r[1].values())
        try:
            rdata = list(map(lambda x: x[:k] + [x[k]*Pn+x[n]] + x[k+1:-1], rdata))
        except:
            f = 1
    if f:
        return transform_with(data, xdicts)
    else:
        return rdata


def auto_data(xdata, window, tpred): # xdata - из unitimeseries, window - размер окна, tpred - номер предсказываемого периода
    X, y, T = [], [], []
    for i in range(len(xdata)-window-tpred):
        if xdata[i+window,0]+tpred > len(xdata)-window-tpred-1:
            break
        if xdata[i+window,0]-xdata[i,0] == window and xdata[xdata[i+window,0]+tpred,0] - xdata[xdata[i+window,0],0] == tpred:
            X.append(xdata[i:i+window,1])
            T.append(xdata[i:i+window,0])
            y.append(xdata[i+window+tpred,1])
    return X,y,T
def find_regression(signals, bucket_size, tpred, min_butches = 5, limit_window = 200): # signals - это список имен файлов с данными
    datasets = [np.genfromtxt(signal, delimiter=',', dtype = None, skip_header = 1) for signal in signals]
    zdata_data = [list(make_integer_dataset(dataset, bucket_size)) for dataset in datasets]
    zdata_list = [zd[0] for zd in zdata_data]
    com_data = unification(zdata_list)
    xdata, xdict = unitimeseries(com_data)
    window, R2 = 1, 0
    while True:
        window += 1
        try:
            adata = auto_data(xdata, window, tpred)
        except:
            break
        if len(adata[0]) > min_butches:
            X, y, T = adata
        else:
            break
        reg = LinearRegression().fit(X, y)
        R2_new = reg.score(X, y)
        if R2_new > R2:
            R2 = R2_new
            rwindow = window
            rcoeffs = reg.coef_
            rintersept = reg.intercept_
            #rX = np.copy(X)
            #rT = np.copy(T)
            #ry = np.copy(y)
        elif window > limit_window:
            break
    return R2, rwindow, rcoeffs, rintersept, xdict, [zd[1:] for zd in zdata_data]

def mpredict(testdatas, bucket_size, window, coeffs, intersept, zkt_list, xdict, tpred):
    # testdatas есть список из датасетов, содержащих сигналы - они должны быть отображены в целочисленные по данным zkt_list и унифицированы с помощью xdict
    zdata_list, timeshifts = [],[]
    for testdata,zkt in zip(testdatas,zkt_list):
        bdata, timeshift = bucket_maker(testdata, bucket_size)
        k, zm = zkt[1], zkt[0]
        zdata = np.vectorize(lambda x: int(x*10**k)-zm+1 if x else 0)(rounded(bdata,k))
        zdata_list.append(zdata)
        timeshifts.append(timeshift)
    common_test = unification(zdata_list)
    clear_data = []
    for cd in common_test:
        if all(cd[1:]):
            clear_data.append(cd)
    clear_data = np.array(clear_data)
    lcd = [list(cd) for cd in clear_data[:,1:]]
    onedim_data = transform_with(lcd,xdict)
    xdata = np.array([[t]+d for t,d in zip(clear_data[:,0],onedim_data)])
    if xdata[-1,0] > xdata[-1-window,0]+window:
        return 'тестовые данные бедны'
    else:
        X = xdata[-window:, 1]
        testy1 = round(np.dot(coeffs,X) + intersept) 
        atesty = np.array(transform_out_up([[testy1],[1]],xdict)[0])[0]
        rtesty = [(a + z[0] + 1)/10**z[1] for a,z in zip(atesty, zkt_list)]
        return rtesty