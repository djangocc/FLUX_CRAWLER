from typing import Tuple
import time
from datetime import datetime
import requests
import json
import _thread
from subprocess import call

scale_threshold_forawrd = 0.018 #正换threadhold
scale_threshold_backward = 0.018 #反threadhold

drivers = []
total_count = 1

okt_price = 90

def notify(title="title", display="dispay"):
    cmd = 'display notification \"' + display + '\" with title \"' +title+ '\"'
    call(["osascript", "-e", cmd])

def parse_number(str):
    return float("".join(str.split(",")))

def alarm(scale_str,title):
    notify(title,scale_str)
    print('chance!!!!!!!')
    _thread.start_new_thread(do_alarm, ())

def do_alarm():
    for num in range(0,2):
        time.sleep(1)
        print("\7")

def getOKTPrice():
    url = "https://www.okex.com/api/v5/market/index-tickers?instId=OKT-USDT"
    payload={}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.text)
        if(resp['code'] == '0'):
            return float(resp['data'][0]['idxPx'])
        else:
            return -1
    except Exception as inst:
        print(inst)
        return -1

def getUsdtFluxPool():
    url = 'https://www.oklink.com/api/explorer/v1/okexchain/addresses/0x69fd660bdcd0f92716d7aaadd7111df95ca5d87e/holders?t=1622309227949&offset=0&limit=20&tokenType=OIP20'
    payload={}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.text)
        if(resp['code'] == 0):
            return resp['data']
        else:
            return None
    except Exception as inst:
        print(inst)
        return None
def getUsdtFluxAmountInPool():
    data = getUsdtFluxPool()
    if data['hits'][0]['symbol'] == "USDT":
        return (data['hits'][0]['value'],data['hits'][1]['value'])
    else:
        return (data['hits'][1]['value'],data['hits'][0]['value'])

def getFluxOktPool():
    url = 'https://www.oklink.com/api/explorer/v1/okexchain/addresses/0xb5a4f628d9342a5ff91da02e3083e0479f088f99/holders?t=1622308841831&offset=0&limit=20&tokenType=OIP20'
    payload={}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.text)
        if(resp['code'] == 0):
            return resp['data']
        else:
            return None
    except Exception as inst:
        print(inst)
        return None

def getFluxOktAmountInPool():
    data = getFluxOktPool()
    if data['hits'][0]['symbol'] == "FLUXK":
        return (data['hits'][0]['value'],data['hits'][1]['value'])
    else:
        return (data['hits'][1]['value'],data['hits'][0]['value'])

def setOKTprice():
    global okt_price
    cur_okt_price = getOKTPrice()
    if(cur_okt_price != -1):
        okt_price = cur_okt_price

def threadOktLoop():
    while True:
        setOKTprice()

def need_alarm(price_in_dex,price_in_cex,scale_forward,scale_backward):
    cur_scale = price_in_dex/price_in_cex
    if((cur_scale <= 1-scale_forward) | (cur_scale >= 1+scale_backward)):
        return True
    return False

setOKTprice()
_thread.start_new_thread(threadOktLoop,())

while True:
    try:
        (usdt_flux_usdt_num,usdt_flux_flux_num) = getUsdtFluxAmountInPool()
        (okt_flux_flux_num,okt_flux_okt_num) = getFluxOktAmountInPool()
        usdt_per_flux = usdt_flux_usdt_num/usdt_flux_flux_num
        flux_per_okt = okt_flux_flux_num/okt_flux_okt_num
        usdt_per_okt = usdt_per_flux*flux_per_okt
        print('%(time)s - okt_price_in_dex:%(okt_price_in_flux).3f | okt_price_in_cex:%(okt_price_in_cex).3f | cur_scale:%(dex_cex_scale).3f'%{
            'time':datetime.now(),
            'okt_price_in_flux':usdt_per_okt,
            'okt_price_in_cex':okt_price,
            'dex_cex_scale':usdt_per_okt/okt_price,
        })
        if(need_alarm(usdt_per_okt,okt_price,scale_threshold_forawrd,scale_threshold_backward)):
            alarm('{:.3f}'.format(usdt_per_okt/okt_price),'反换 dex卖okt' if usdt_per_okt/okt_price > 1 else '正换 cex卖okt')
        # driver.refresh()
    except Exception as ex:
        print(ex)