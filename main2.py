import sys

#時間のデータを読みやすい形にする
def time_decorator(time):
    return time[:4] + "/" + time[4:6] + "/" + time[6:8] + " " + time[8:10] + ":" + time[10:12] + ":" + time[12:]

#ファイル読み込み
with open(sys.argv[1]) as f:
    lines = f.readlines()

n = int(sys.argv[2])

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

#出力
for i in failure_list:
    print("ipアドレス: " + i['ipaddr'])
    print("故障期間: " + i['start_time'] + "～" + i['end_time'] + "\n")