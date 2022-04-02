# 概要
main1.py～main4.pyがそれぞれ設問1～設問4に対応しています

# 設問1
## 実行方法
```
$ python3 main1.py example_data(ログファイル)
```
## 解説
```
def time_decorator(time):
    return time[:4] + "/" + time[4:6] + "/" + time[6:8] + " " + time[8:10] + ":" + time[10:12] + ":" + time[12:]
```
上記部分でログファイルの日時のフォーマットから読みやすい形にしています
```
data_dict = {}
for item in lines:
    i = item.strip()
    list = i.split(',')
    if list[1] in data_dict.keys():
        data_dict[list[1]].append({'time': list[0], 'ping': list[2] })
    else:
        data_dict[list[1]] = [{'time': list[0], 'ping': list[2]}]
```
上記部分でdata_dictにipアドレスごとに時間とpingの応答時間をまとめています
```
failure_list=[]
for i in data_dict:
    failure = False
    for j in data_dict[i]:
        if j['ping'] == '-' and failure == False:
            start_time = time_decorator(j['time'])
            failure = True
        if j['ping'] != '-' and failure == True:
            end_time = time_decorator(j['time'])
            failure_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': end_time})
            failure = False
    if failure == True:
        failure_list.append({'ipaddr': i, 'start_time': start_time, 'end_time': ''})
```
上記部分でfailture_listに障害の発生しているipアドレスと時間を集約しています
```
for i in failure_list:
    print("ipアドレス: " + i['ipaddr'])
    print("故障期間: " + i['start_time'] + "～" + i['end_time'] + "\n")
```
上記部分で情報を出力しています



# 設問2
## 実行方法
```
$ python3 main1.py example_data(ログファイル) N(回数)
```
## 解説
```
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
```
main1.pyからの変更点として、countという変数でタイムアウトの連続回数をカウントし、コマンドライン引数nと比較して障害と判定するように変更しています


# 設問3
## 実行方法
```
$ python3 main1.py example_data(ログファイル) N(回数) m(回数) t(ミリ秒)
```
## 解説
```
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
```
上記部分で過負荷かどうかを判定しています。タイムアウトしている場合は除外しています。


# 設問4(作業中です)
## 実行方法
```
$ python3 main1.py example_data(ログファイル) N(回数)
```
