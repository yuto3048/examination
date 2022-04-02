import sys
import ipaddress

#時間のデータを読みやすい形にする
def time_decorator(time):
    return time[:4] + "/" + time[4:6] + "/" + time[6:8] + " " + time[8:10] + ":" + time[10:12] + ":" + time[12:]

#ファイル読み込み
with open(sys.argv[1]) as f:
    lines = f.readlines()

n = int(sys.argv[2])

#サブネットとipアドレスをリストにする
subnet_dict = {}
for i in lines:
    ip = ipaddress.ip_interface(i.split(',')[1])
    if str(ip.network) in subnet_dict.keys():
        if ip.with_prefixlen not in subnet_dict[str(ip.network)]:
            subnet_dict[str(ip.network)].append(ip.with_prefixlen)
    else:
        subnet_dict[str(ip.network)] = [ip.with_prefixlen]

#ipアドレスごとにデータ整形
data_dict = {}
for item in lines:
    i = item.strip()
    list = i.split(',')
    if list[1] in data_dict.keys():
        data_dict[list[1]].append({'time': list[0], 'ping': list[2] })
    else:
        data_dict[list[1]] = [{'time': list[0], 'ping': list[2]}]

#障害を確認
failure_list = []
failure_ip_list = []
for i in data_dict:
    failure = False
    count = 0
    for j in data_dict[i]:
        if j['ping'] == '-' and failure == False:
            if count == 0:
                start_time = time_decorator(j['time'])
            count += 1
        if j['ping'] != '-' and failure == True:
            end_time = time_decorator(j['time'])
            failure_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': end_time})
            failure_ip_list.append(i)
            failure = False
            count = 0
        if count >= n:
            failure = True
    if failure == True:
        failure_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': ''})
        failure_ip_list.append(i)
        
for i in subnet_dict:
    print(i)
    bool = True
    for j in subnet_dict[i]:
        print(j)
        if j not in failure_ip_list:
            bool = False
    print(bool)

#出力
for i in failure_list:
    print(i)
    #print("ipアドレス: " + i['ipaddr'])
    #print("故障期間: " + i['start_time'] + "～" + i['end_time'] + "\n")