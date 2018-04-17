
# coding: utf-8

# In[3]:


import pandas as pd
import datetime as dt
import matplotlib as m
import matplotlib.pyplot as plt
import numpy as np


# # Retrieving informtion for a particular account id

# In[4]:


#dataset['operation'] = dataset['operation'].replace(['CASH IN'], 0)
#dataset['operation'] = dataset['operation'].replace(['CASH WITHDRAWAL'], 1)
#dataset['operation'] = dataset['operation'].replace(['BANK TRANSFER'], 2)

#global l , accountCashOut, accountCashIngrp,sumOfGroup
#accountCashIn
#maxAccID = dataset['account_id'][len(dataset)-1]
listOfTransaction=[]
    
def heavyWithdrawal(dataset,accountlist,maxAccID):
    for index in accountlist:
        df=dataset.loc[dataset['account_id'] == index]
        accountCashIn= df.loc[df['operation'] == 0]
        accountCashOut = df.loc[df['operation'] == 1]
        accountBankTransfer = df.loc[df['operation'] == 2]
        mylist=list(accountCashIn['date1']) 
        l=set([dt.datetime.strptime(d,'%m/%y').date() for d in mylist])
        accountCashIngrp  = accountCashIn.groupby(['date1'])['amount']
        sumOfGroup = accountCashIn.groupby(['date1'])['amount'].sum()
        
        listOfTransaction=suspiciousTransaction(sumOfGroup,accountCashOut,accountCashIngrp,accountCashIn,accountBankTransfer)
        if(dataset['account_id'][0]==maxAccID):
            break
    return listOfTransaction


# In[5]:


#accountBankTransfer


# ## Deciding Threshold for Cash Withdrwal
# we ll take mean of amount deposit in account by cash or bank transfer

# In[6]:


#mean balance for a particular account  ----to be changed under RBI guidelines
def meanAndSD(accountCashIn,accountBankTransfer):
    bal_cash=np.sum(accountCashIn['amount'])
    bal_bank=np.sum(accountBankTransfer['amount'])
    std_bank= np.std(accountBankTransfer['amount'])
    std_cash= np.std(accountCashIn['amount']+accountBankTransfer['amount'])
    mean=(bal_cash+bal_bank)/(len(accountBankTransfer)+len(accountCashIn))
    mean
    std1=0
    accountBankTransfer_arr=np.array(accountBankTransfer)
    for i in range(len(accountBankTransfer_arr)):
        std1=std1+(mean-accountBankTransfer_arr[i][4])**2
    accountCashIn_arr=np.array(accountCashIn)
    for i in range(len(accountCashIn_arr)):
        std1+=(mean-accountCashIn_arr[i][4])**2
    
    std1=np.sqrt((std1)/(len(accountBankTransfer)+len(accountCashIn)))
    threshold=mean+2*(std1)
    return threshold


# In[7]:


#sumOfGroup.sort_values(ascending=False)
def groupByDates(accountCashIngrp):
    x=accountCashIngrp.groups.keys()
    x=sorted(x)
    return x


# In[8]:


def suspiciousTransaction(sumOfGroup,accountCashOut,accountCashIngrp,accountCashIn,accountBankTransfer):
    sumOfGroup=np.array(sumOfGroup)
    amount = accountCashOut['amount']
    accountCashOut_arr= np.array(accountCashOut)
    flag =1
    for i in range(len(sumOfGroup)):
        x = groupByDates(accountCashIngrp)
        if(sumOfGroup[i]>meanAndSD(accountCashIn,accountBankTransfer)):
            for j in range(len(accountCashOut_arr)):
                if(accountCashOut_arr[j][8]==x[i]):
                    listOfTransaction.append(accountCashOut_arr[j])
                    flag=0
                elif (flag==0):
                    break
    return listOfTransaction

