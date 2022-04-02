import sys

#時間のデータを読みやすい形にする
def time_decorator(time):
    return time[:4] + "/" + time[4:6] + "/" + time[6:8] + " " + time[8:10] + ":" + time[10:12] + ":" + time[12:]

#ファイル読み込み
with open(sys.argv[1]) as f:
    lines = f.readlines()

n = int(sys.argv[2])
m = int(sys.argv[3])
t = int(sys.argv[4])

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
failure_list=[]
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
            failure = False
            count = 0
        if count >= n:
            failure = True
    if failure == True:
        failure_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': ''})

#過負荷の確認
overload_list = []
for i in data_dict:
    overload = False
    for j in range(len(data_dict[i]) - (m - 1)):
        failure = False
        sum = 0
        list = data_dict[i][j:j + m]
        for k in list:
            if k['ping'] == "-":
                failure = True
                break
            sum += int(k['ping'])
        if failure == True:
            continue
        if (sum / m) > t and overload == False:
            overload = True
            start_time = time_decorator(list[0]['time'])
            end_time = time_decorator(list[m - 1]['time'])
        if (sum / m) > t and overload == True:
            end_time = time_decorator(list[m - 1]['time'])
        if (sum / m) <= t and overload == True:
            overload_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': end_time})
            overload = False
    if overload == True:
        overload_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': end_time})

#障害の出力
for i in failure_list:
    print("ipアドレス: " + i['ipaddr'])
    print("故障期間: " + i['start_time'] + "～" + i['end_time'] + "\n")

print("----------------------------------------------------\n")

#過負荷の出力
for i in overload_list:
    print("ipアドレス: " + i['ipaddr'])
    print("過負荷期間: " + i['start_time'] + "～" + i['end_time'] + "\n")
