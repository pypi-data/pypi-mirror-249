_B='total_count'
_A='summary'
import os,json
try:import requests
except ModuleNotFoundError:os.system('pip install requests');import requests
get=requests.get
post=requests.post
session=requests.session
def Scrape_Year(uid):
  D='20??';E='2023';C='2009';B=uid
  if len(B)==15:
    if str(B)[:10]in['1000000000']:A=C
    elif str(B)[:9]in['100000000']:A=C
    elif str(B)[:8]in['10000000']:A=C
    elif str(B)[:7]in['1000000','1000001','1000002','1000003','1000004','1000005']:A=C
    elif str(B)[:7]in['1000006','1000007','1000008','1000009']:A='2010'
    elif str(B)[:6]in['100001']:A='2010-2011'
    elif str(B)[:6]in['100002','100003']:A='2011-2012'
    elif str(B)[:6]in['100004']:A='2012-2013'
    elif str(B)[:6]in['100005','100006']:A='2013-2014'
    elif str(B)[:6]in['100007','100008']:A='2014-2015'
    elif str(B)[:6]in['100009']:A='2015'
    elif str(B)[:5]in['10001']:A='2015-2016'
    elif str(B)[:5]in['10002']:A='2016-2017'
    elif str(B)[:5]in['10003']:A='2018-2019'
    elif str(B)[:5]in['10004']:A='2019-2020'
    elif str(B)[:5]in['10005']:A='2020'
    elif str(B)[:5]in['10006','10007']:A='2021'
    elif str(B)[:5]in['10008']:A='2022'
    elif str(B)[:5]in['10009']:A=E
    else:A=D
  elif len(B)==14:A=E
  elif len(B)in[9,10]:A=' 2008-2009 '
  elif len(B)==8:A=' 2007-2008 '
  elif len(B)==7:A=' 2006-2007 '
  else:A=D
  return A
def Scrape_Followers(token):
  try:A=get(f"https://graph.facebook.com/me/subscribers?limit=1000&access_token={token}").json()[_A][_B];return A
  except:return
def Scrape_Friends(token):
  try:A=get(f"https://graph.facebook.com/me/friends?limit=5000&access_token={token}").json()[_A][_B];return A
  except:return
def Scrape_Name(token):A=get(f"https://graph.facebook.com/me?fields=name&access_token={token}").json()['name'];return A


# sintacs ao #facebook.com/sintxcs