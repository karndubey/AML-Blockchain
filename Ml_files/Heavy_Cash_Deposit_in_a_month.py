
# coding: utf-8

# In[7]:


import pandas as pd
import datetime as dt
import matplotlib as m
import matplotlib.pyplot as plt
import numpy as np


# # Retrieving informtion for a particular account id

# In[8]:


listofTransaction=[]
def heavyDeposit(dataset,accountlist,maxAccID):
    for index in accountlist:
        df=dataset.loc[dataset['account_id'] == index]
        accountCashIn= df.loc[df['operation'] == 0]
        accountCashOut = df.loc[df['operation'] == 1]
        accountBankTransfer = df.loc[df['operation'] == 2]
        mylist=list(accountCashIn['date1']) 
        l=set([dt.datetime.strptime(d,'%m/%y').date() for d in mylist])
        accountCashIngrp  = accountCashIn.groupby(['date1'])['amount']
        sumOfGroup = accountCashIn.groupby(['date1'])['amount'].sum()
        
        suspiciousTransaction(sumOfGroup,accountCashIn,accountCashIngrp)
        if(dataset['account_id'][0]==maxAccID):
            break
    return listofTransaction


# In[1]:


#mean balance for a particular account  ----to be changed under RBI guidelines
def meanAndSD(accountCashIn):
    #meanAmount=float(accountCashIn['amount'])/len(accountCashIn['amount'])
    meanAmount=np.mean(accountCashIn['amount'])
    #meanAmount
    sigma=np.std(accountCashIn['amount'])
    sigma
    threshold=2.5*sigma+meanAmount
    return threshold

def groupBydates(accountCashIngrp):
    x= accountCashIngrp.groups.keys()
    x=sorted(x)
    return x


# In[10]:


# threshold to generate alert for large deposit in month
# parameter 
def suspiciousTransaction(sumOfGroup,accountCashIn,accountCashIngrp):
    
    sumOfGroup=np.array(sumOfGroup)
    #amount = accountCashOut['amount']
    accountCashIn_arr= np.array(accountCashIn)
    flag =1
    x= groupBydates(accountCashIngrp)
    #print("sumofgrop ",len(sumOfGroup)," X: ",len(x),"account_cash_arr: ",len(accountCashIn_arr))
        
    for i in range(len(sumOfGroup)):
       
        if(sumOfGroup[i]>meanAndSD(accountCashIn)):
            for j in range(len(accountCashIn_arr)):
                #print(accountCashIn_arr[j][8],x[i])
                if(accountCashIn_arr[j][8]==x[i]):
                    listofTransaction.append(accountCashIn_arr[j])
                    flag=0
    

