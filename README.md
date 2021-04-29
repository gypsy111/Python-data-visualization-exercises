# Python-data-visualization-exercises
一个学习过程中的python数据可视化小练习

## 原理说明
- 数据请求

```python
def china_update_data():
    confirmAdd_data = {}
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare'
    res = requests.get(url).json()
    for k, v in res['data']['provinceCompare'].items():
        confirmAdd_data[k] = v['confirmAdd']
    return confirmAdd_data

def get_china_of_COVID():
    confirmAdd = china_update_data()
    china_of_CVOID = []
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    res = requests.get(url).json()
    data = json.loads(res['data'])
    for i in range(0, len(data['areaTree'][0]['children']) - 1):
        data_list = [data['areaTree'][0]['children'][i]['name'],
                     confirmAdd[data['areaTree'][0]['children'][i]['name']],
                     data['areaTree'][0]['children'][i]['total']['nowConfirm'],
                     # data['areaTree'][0]['children'][i]['total']['confirm'],
                     data['areaTree'][0]['children'][i]['total']['heal'],
                     data['areaTree'][0]['children'][i]['total']['dead'],
                     ]
        china_of_CVOID.append(data_list)
    return china_of_CVOID
```




使用request请求关于中国疫情的相关数据，使用简单的逻辑对数据进行初步的筛选（得到新增疫情的人数和现有疫情的人数数据）


-数据存储
请求得到的数据使用csv创建当天数据的csv文件，以日期为文件名存储到china目录当中

```python
def writer_csv_file():
    china_data = get_china_of_COVID()
    with open('./china/{}.csv'.format(datetime.date.today()), 'w', encoding='utf-8-sig') as csvchinafile:
        writer = csv.writer(csvchinafile)
        writer.writerow(['地区', '新增确诊', '现有确诊', '治愈', '死亡'])
        for i in china_data:
            writer.writerow(i)
```

- 数据可视化


使用pyecharts进行数据可视化的工作（个人觉得挺不错的一款工具，对JavaScript没学好的同学及其友好！！！）
具体实现查看 COVID_data_of_china.py
下面进行某一帧的可视化效果展示


## 可视化效果
![image](https://github.com/gypsy111/Python-data-visualization-exercises/blob/master/image/%E6%95%88%E6%9E%9C.png)
