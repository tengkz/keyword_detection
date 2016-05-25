#coding:utf-8
import numpy as np
import pandas as pd
import re
from numpy import log,min

f = open("sanguo_utf8.txt",'r')
s = f.read().decode('utf-8')

drop_dict = [u'，', u'\n', u'。', u'、', u'：', u'(', u')', u'[', u']', u'.', u',', u' ', u'\u3000', u'”', u'“', u'？', u'?', u'！', u'‘', u'’', u'…']
for i in drop_dict:
    s = s.replace(i,'')

myre = {2:'(..)', 3:'(...)', 4:'(....)', 5:'(.....)', 6:'(......)', 7:'(.......)'}

min_count = 10
min_support = 30
min_s = 3
max_sep = 4
t = []

t.append(pd.Series(list(s)).value_counts())
tsum = t[0].sum()
rt = []

for m in range(2,max_sep+1):
    t.append([])
    for i in range(m):
        t[m-1] = t[m-1] + re.findall(myre[m],s[i:])

    t[m-1] = pd.Series(t[m-1]).value_counts()
    t[m-1] = t[m-1][t[m-1] > min_count]
    tt = t[m-1][:]
    for k in range(m-1):
        qq = np.array(list(map(lambda ms: tsum*t[m-1][ms]/t[m-2-k][ms[:m-1-k]]/t[k][ms[m-1-k:]], tt.index))) > min_support
        tt = tt[qq]
    rt.append(tt.index)

def cal_S(sl):
    return -((sl/sl.sum()).apply(log)*sl/sl.sum()).sum()

for i in range(2,max_sep+1):
    pp = []
    for j in range(i):
        pp = pp + re.findall('(.)%s(.)' % myre[i],s[j:])
    pp = pd.DataFrame(pp).set_index(1).sort_index()
    index = np.sort(np.intersect1d(rt[i-2],pp.index))
    index = index[np.array(list(map(lambda s: cal_S(pd.Series(pp[0][s]).value_counts()), index))) > min_s]
    rt[i-2] = index[np.array(list(map(lambda s: cal_S(pd.Series(pp[2][s]).value_counts()), index))) > min_s]

for i in range(len(rt)):
    t[i+1] = t[i+1][rt[i]]
    t[i+1].sort_values(inplace=True,ascending = False)

ret = pd.DataFrame(pd.concat(t[1:]))
for x,y in zip(ret.index,ret.values):
    print x,y[0]
