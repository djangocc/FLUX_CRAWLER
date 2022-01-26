# coding=UTF-8
import time
from datetime import datetime
import requests
import json
import pygame
import _thread
from subprocess import call
from concurrent import futures
from concurrent.futures._base import TimeoutError



music_file = "./alarm.mp3"
pygame.mixer.init()
track = pygame.mixer.music.load(music_file)

last_okt_price_in_dex = 0
last_okt_price_in_cex = 0


scale_threshold_forawrd = 0.03 #正换threadhold
scale_threshold_backward = 0.03 #反threadhold

drivers = []
total_count = 1

# for i in range(total_count):
#     drivers.append(Chrome())
#     drivers[i].get("https://flux.01.finance/stake?chain=okexchain")
# driver = Chrome()
# driver.get("https://flux.01.finance/okexchain/stake")
okt_price = 90

def notify(title="title", display="dispay"):
    cmd = 'display notification \"' + display + '\" with title \"' +title+ '\"'
    call(["osascript", "-e", cmd])


def parse_number(str):
    return float("".join(str.split(",")))

def alarm(scale_str,title):
    notify(title,scale_str)
    print('chance!!!!!!!')
    _thread.start_new_thread(doAlarm,())

def doAlarm():
    for num in range(0,2):
        time.sleep(1)
        pygame.mixer.music.play()

def getOKTPrice():
    global last_okt_price_in_cex,okt_price
    last_okt_price_in_cex = okt_price
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
    m = {}
    for item in data['hits']:
        m[item['symbol']] = item['value']
    return (m['USDT'],m['FLUXK'])

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
    m = {}
    for item in data['hits']:
        m[item['symbol']] = item['value']
    return (m['FLUXK'],m['WOKT'])

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

usdt_per_okt = 0
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    while True:
        try:
           futureUsdtFlux = executor.submit(getUsdtFluxAmountInPool)
           futureFluxOKT = executor.submit(getFluxOktAmountInPool)
           (usdt_flux_usdt_num,usdt_flux_flux_num) = futureUsdtFlux.result(2)
           (okt_flux_flux_num,okt_flux_okt_num) = futureFluxOKT.result(2)
           usdt_per_flux = usdt_flux_usdt_num/usdt_flux_flux_num
           flux_per_okt = okt_flux_flux_num/okt_flux_okt_num
           last_okt_price_in_dex = usdt_per_okt
           usdt_per_okt = usdt_per_flux*flux_per_okt
           print('%(time)s - okt_price_in_dex:%(okt_price_in_flux).3f | okt_price_in_cex:%(okt_price_in_cex).3f | cur_scale:%(dex_cex_scale).3f'%{
               'time':datetime.now(),
               'okt_price_in_flux':usdt_per_okt,
               'okt_price_in_cex':okt_price,
               'dex_cex_scale':usdt_per_okt/okt_price,
           })
           contrib_dex = abs(usdt_per_okt/last_okt_price_in_cex - last_okt_price_in_dex/last_okt_price_in_cex)
           contrib_cex = abs(last_okt_price_in_dex/okt_price - last_okt_price_in_dex/last_okt_price_in_cex)

           if(need_alarm(usdt_per_okt,okt_price,scale_threshold_forawrd,scale_threshold_backward)):
               alarm('{:.3f}'.format(usdt_per_okt/okt_price),('dex贡献{:.3f}'.format(abs(usdt_per_okt-last_okt_price_in_dex)) if contrib_dex > contrib_cex else '' )+ '反换 dex卖okt cex买okt' if usdt_per_okt/okt_price > 1 else '正换 dex买okt cex卖okt')
        except TimeoutError as ex:
            print('timeout')
        except Exception as ex:
            print(str(ex))