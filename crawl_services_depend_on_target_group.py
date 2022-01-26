import requests
import json
import _thread

from requests.api import head



# cookies = {
#     'session':".eJw1z0FOxDAMheG7ZD0LO3Edey5T2Y4jEEMHtZ0V4u5UQhzgf_red1nnnsdbuZ_7K29lfR_lXuqsldBgDGwofRH1RaZwziWopwcSQ2_Bo7J28NmMpkhPBiNh9eTFWSwcolOrUpuKVNdoyDB8uhmh8qCWGTSspXUkYFEJxygX5Cv3T9tyO_9pcexzPZ8fuV3CRZANG6BqZwadU6lDrU4CSTbQeFZ3uJYez7BHXs0V3srryP3vJKKClJ9fLSpJag.YQEMAA.FeyreWo25nk6gokISHkKC6svDfQ; auth_proxy=j%3A%7B%22data%22%3A%7B%22userData%22%3A%7B%22uid%22%3A%5B%22chentao_jiang%22%5D%2C%22mail%22%3A%5B%22chentao.jiang%40airbnb.com%22%5D%2C%22memberOf%22%3A%5B%22cn%3Dgithub_musta%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dprodartifactory_cn%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Ddashboards%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dfireball%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dkibana%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dincidents%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Djitney%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dupshot_pivot%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dsitar_portal%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dsinopia%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dnerds%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dhadoop_user%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DOffice-CHN-Beijing%2Cou%3Dlocations%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dactive_employees%2Cou%3Dsearches%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DCC22_Engineering%2Cou%3DcostCenters%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DCC22-01_Engineering%2Ccn%3DCC22_Engineering%2Cou%3DcostCenters%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DEngineering%2Cou%3Dteams%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DEngineering_Fullstack%2Ccn%3DEngineering%2Cou%3Dteams%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DRegion-APAC%2Cou%3Dlocations%2Cdc%3Dairbnb%2Cdc%3Dcom%22%5D%7D%2C%22expiration%22%3A1627593771182%2C%22authMethod%22%3A%22ldap-duo%22%7D%2C%22signature%22%3A%229ea5733a4884613375f7fb7236bdaf048e6a5d9cba90aa67282c673c302c317d%22%7D",
# }

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Accept': 'application/json, text/javascript, */*; q=0.01' ,
    'X-CSRF-Token': 'e7JF+Rgh8Nfu/qbi7YGMmKCiNSC29Bwn8ezBfx7wWwE=' ,
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36' ,
    'X-Requested-With': 'XMLHttpRequest' ,
    'Sec-Fetch-Site': 'same-origin' ,
    'Referer': 'https://sitar-portal.d.musta.ch/prod' ,
    'Cookie': '_ga=GA1.2.1845517950.1626085675; GCP_IAP_UID=107125644620228675119; _gid=GA1.2.2003646308.1627365415; _airconfig-portal_session=BAh7CEkiD3Nlc3Npb25faWQGOgZFVEkiJWIxZTVkNThiNGI4ZjJjNjRjZjJmZDY3OTNmMmQ0OWI1BjsAVEkiDHVzZXJfaWQGOwBGIhJjaGVudGFvX2ppYW5nSSIQX2NzcmZfdG9rZW4GOwBGSSIxZTdKRitSZ2g4TmZ1L3FiaTdZR01tS0NpTlNDMjlCd244ZXpCZng3d1d3RT0GOwBG--c90f59ef4f2558d03c8e3c92cbf436e27ce8c564; session=.eJw1z0FOxDAMheG7ZD0LO3Edey5T2Y4jEEMHtZ0V4u5UQhzgf_red1nnnsdbuZ_7K29lfR_lXuqsldBgDGwofRH1RaZwziWopwcSQ2_Bo7J28NmMpkhPBiNh9eTFWSwcolOrUpuKVNdoyDB8uhmh8qCWGTSspXUkYFEJxygX5Cv3T9tyO_9pcexzPZ8fuV3CRZANG6BqZwadU6lDrU4CSTbQeFZ3uJYez7BHXs0V3srryP3vJKKClJ9fLSpJag.YQEMAA.FeyreWo25nk6gokISHkKC6svDfQ; auth_proxy=j%3A%7B%22data%22%3A%7B%22userData%22%3A%7B%22uid%22%3A%5B%22chentao_jiang%22%5D%2C%22mail%22%3A%5B%22chentao.jiang%40airbnb.com%22%5D%2C%22memberOf%22%3A%5B%22cn%3Dgithub_musta%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dprodartifactory_cn%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Ddashboards%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dfireball%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dkibana%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dincidents%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Djitney%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dupshot_pivot%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dsitar_portal%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dsinopia%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dnerds%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dhadoop_user%2Cou%3Dengineering%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DOffice-CHN-Beijing%2Cou%3Dlocations%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3Dactive_employees%2Cou%3Dsearches%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DCC22_Engineering%2Cou%3DcostCenters%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DCC22-01_Engineering%2Ccn%3DCC22_Engineering%2Cou%3DcostCenters%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DEngineering%2Cou%3Dteams%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DEngineering_Fullstack%2Ccn%3DEngineering%2Cou%3Dteams%2Cou%3Ddepartments%2Cdc%3Dairbnb%2Cdc%3Dcom%22%2C%22cn%3DRegion-APAC%2Cou%3Dlocations%2Cdc%3Dairbnb%2Cdc%3Dcom%22%5D%7D%2C%22expiration%22%3A1627593771182%2C%22authMethod%22%3A%22ldap-duo%22%7D%2C%22signature%22%3A%229ea5733a4884613375f7fb7236bdaf048e6a5d9cba90aa67282c673c302c317d%22%7D' ,
    'If-None-Match': 'W/"6a71f9f11f3821edbd1f511d5bed400d"',
}


def get_groups_from_services(service_name):
    global headers 
    url = "https://sitar-portal.d.musta.ch/prod/backend?method=get&args[]=sitar&args[]={0}&options[archived_config_ok]=true".format(service_name)
    response = requests.get(url,headers=headers)
    # response = requests.get(url,headers=headers,cookies=cookies)
    respjson = json.loads(response.text)
    payload_json = json.loads(respjson['content']['subscriptions']['payload'])
    groups = payload_json['groups']
    return groups

# response = requests.get('https://sitar-portal.d.musta.ch/prod/groups_ajax/sitar', headers=headers, cookies=cookies)
response = requests.get('https://sitar-portal.d.musta.ch/prod/groups_ajax/sitar', headers=headers)
respjson = json.loads(response.text)
list = respjson['configs_by_group']['sitar']
fToWrite = open('/Users/chentao_jiang/service.list','a+')
fToWrite.write('aaa\n')

totalSize = len(list)
threadCnt = 30
def work(threadId,start,end,list):
    last_stage  = 0
    for index in range(start,end):
        curPct = (100*(index-start))/(end-start)
        curStage = curPct//10
        if curStage != last_stage:
            print(("thread_id:{0} stage:{1}/10").format(threadId,curStage))
            last_stage = curStage
        name = list[index]
        try:
            a = name.index('service')
            all_group_list = get_groups_from_services(name)
            if('china_host' in all_group_list):
                fToWrite.write(name+"\n")
        except Exception as inst:
            pass
            # print(inst)

namelist = []
for name in list:
    namelist.append(name)

for i in range(threadCnt):
    threadId = i
    size = totalSize//threadCnt if i !=threadCnt-1 else totalSize - (threadCnt-1)*(totalSize//threadCnt)
    startIdx = i*(totalSize//threadCnt)
    endIdx = startIdx+size
    _thread.start_new_thread(work,(i,startIdx,endIdx,namelist))

while True:
    pass



# response = requests.get('https://sitar-portal.d.musta.ch/prod/groups_ajax/sitar', headers=headers, cookies=cookies)
# respjson = json.loads(response.text)
# list = respjson['configs_by_group']['sitar']
# print(list)

