import requests, csv, json, datetime, os
import pandas as pd
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie


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


def writer_csv_file():
    china_data = get_china_of_COVID()
    with open('./china/{}.csv'.format(datetime.date.today()), 'w', encoding='utf-8-sig') as csvchinafile:
        writer = csv.writer(csvchinafile)
        writer.writerow(['地区', '新增确诊', '现有确诊', '治愈', '死亡'])
        for i in china_data:
            writer.writerow(i)


def get_year_chart(date):
    data = pd.read_csv('./china/{}.csv'.format(date))
    df_clear = data.drop(data[(data['地区'] == '香港')].index)
    df_clear1 = df_clear.drop(df_clear[df_clear['新增确诊'] == 0].index)
    df_clear2 = df_clear.drop(df_clear[df_clear['现有确诊'] == 0].index)
    name = list(df_clear['地区'])
    nowConfirm = list(df_clear1['新增确诊'])
    confirm = list(df_clear2['现有确诊'])
    heal = list(df_clear['治愈'])
    dead = list(df_clear['死亡'])
    map_chart = (
        Map()
            .add(
            series_name="",
            data_pair=[list(z) for z in zip(name, confirm)],
            label_opts=opts.LabelOpts(is_show=False),
            is_map_symbol_show=False,
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="现有疫情和新增疫情",
                subtitle="中国",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="center",
                range_text=["高风险地区", "低风险地区"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=0,
                max_=100,
            ),
        )
    )

    bar = (
        Bar()
            .add_xaxis(xaxis_data=name)
            .add_yaxis(
            series_name="",
            yaxis_index=1,
            y_axis=confirm,
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b}: {c}"
            ),
        )
            .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="center",
                range_text=["高风险地区", "低风险地区"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=0,
                max_=100,
            ),
            graphic_opts=[
                opts.GraphicGroup(
                    graphic_item=opts.GraphicItem(
                        bounding="raw",
                        right=110,
                        bottom=11,
                        z=100,
                    ),
                    children=[
                        opts.GraphicRect(
                            graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                            graphic_shape_opts=opts.GraphicShapeOpts(width=400, height=50),
                            graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                fill="rgba(0,0,0,0.3)"
                            ),
                        ),
                        opts.GraphicText(
                            graphic_item=opts.GraphicItem(left="center", top="center", z=100),
                            graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                text=date,
                                font="bold 26px Microsoft YaHei",
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(fill="#fff"),
                            ),
                        ),
                    ],
                )
            ],
        )
    )

    pie = (
        Pie()
            .add(
            series_name="",
            data_pair=[list(z) for z in zip(name, nowConfirm)],
            radius=["12%", "20%"],
            center=["75%", "85%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    grid_chart = (
        Grid()
            .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="70%", pos_bottom="5"
            ),
        )
            .add(pie, grid_opts=opts.GridOpts())
            .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart


def get_file_name(path_str):
    file_name_list = []
    for root, dirs, files in os.walk(path_str):
        for file in files:
            file_name_list.append(os.path.join(file)[:10])
    return file_name_list


writer_csv_file()
time_list = get_file_name('./china')
timeline = Timeline(
    init_opts=opts.InitOpts(width="1200px", height="800px", theme=ThemeType.DARK)
)
for y in time_list:
    g = get_year_chart(y)
    timeline.add(g, time_point=y)

timeline.add_schema(
    orient="vertical",
    is_auto_play=True,
    is_inverse=True,
    play_interval=5000,
    pos_left="null",
    pos_right="5",
    pos_top="20",
    pos_bottom="20",
    width="50",
    label_opts=opts.LabelOpts(is_show=True, color="#fff"),
)

timeline.render("COVID_data_of_china.html")
