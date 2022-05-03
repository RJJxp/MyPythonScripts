import io
import os
import sys
import argparse

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# # s = pd.Series([1, 3, 5, np.nan, 6, 8])
    # # print(s)
    # dates = pd.date_range('20130101', periods=6)
    # print(dates)
    # df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    # print(df)
    # df2 = pd.DataFrame({'A': 1.,
    #                     'B': pd.Timestamp('20130102'),
    #                     'C': pd.Series(1, index=list(range(4)), dtype='float32'),
    #                     'D': np.array([3] * 4, dtype='int32'),
    #                     'E': pd.Categorical(["test", "train", "test", "train"]),
    #                     'F': 'foo'})
    # # print(df2)
    # # print(df2.dtypes)
    # # print(df.head)
    # # print(df.tail)
    # # print(df.index)
    # # print(df.describe())
    # # print(df.sort_index(axis=1, ascending=False)) 
    # # print(df.sort_values(by='B', ascending=True))
    # # print(df.sort_values(by='B', ascending=False))
    # # print(df["B"])
    # # print(df[0:3])
    # print(df)
    # print("=============")
    # print(df.loc[dates[0]])
    # df.iloc[1:3, 2:4] = 2
    # print(df)

    # df3 = pd.DataFrame({"id": [1, 2, 3, 4, 5, 6],
    #                     "raw_grade": ['a', 'b', 'b', 'a', 'a', 'e']})
    # df3["grade"] = df3["raw_grade"].astype("category")
    # df3["grade"].cat.categories = ["very good", "good", "very bad"]
    # df3["grade"].cat.set_categories(["very bad", "bad", "medium",
    #                                                "good", "very good"])

    # print(df3["grade"])
    # ts = pd.Series(np.random.randn(1000),
    #                index=pd.date_range('1/1/2000', periods=1000))
    # print(ts)
    
    # ts = ts.cumsum()
    # print("ts")
    # ts.plot()
    # plt.show()
    # print("ts2")

def drawDF(df, pic_name):
    print(df.shape)
    reason_liencense_sum = df.loc[:, "无叉车证"].value_counts().sum()
    reason_gaocha_sum = df.loc[:, "不做高叉"].value_counts().sum()
    reason_food_sum = df.loc[:, "不包吃住"].value_counts().sum()
    reason_salary_sum = df.loc[:, "薪资过低"].value_counts().sum()
    reason_commute_sum = df.loc[:, "距离过远"].value_counts().sum()
    reason_nightshift_sum = df.loc[:, "拒绝夜班"].value_counts().sum()
    reason_noncontact_sum = df.loc[:, "无法联系"].value_counts().sum()
    reason_occupied_sum = df.loc[:, "已找到工作"].value_counts().sum()
    reason_covid_sum = df.loc[:, "疫情"].value_counts().sum()
    reason_funds_sum = df.loc[:, "公积金"].value_counts().sum()
    reason_performance_sum = df.loc[:, "底薪计件"].value_counts().sum()
    reason_sarturday_sum = df.loc[:, "做六休一"].value_counts().sum()
    reason_website_sum = df.loc[:, "招聘网站错投或信息滞后"].value_counts().sum()

    print("无叉车证: %d" %reason_liencense_sum)
    print("不做高叉: %d" %reason_gaocha_sum)
    print("不包吃住: %d" %reason_food_sum)
    print("薪资过低: %d" %reason_salary_sum)
    print("距离过远: %d" %reason_commute_sum)
    print("拒绝夜班: %d" %reason_nightshift_sum)
    print("无法联系: %d" %reason_noncontact_sum)
    print("已找到工作: %d" %reason_occupied_sum)
    print("疫情: %d" %reason_covid_sum)
    print("公积金: %d" %reason_funds_sum)
    print("底薪计件: %d" %reason_performance_sum)
    print("做六休一: %d" %reason_sarturday_sum)
    print("招聘网站错投或信息滞后: %d" %reason_website_sum)
    reason_list = [reason_liencense_sum, reason_gaocha_sum, reason_food_sum,
                    reason_salary_sum, reason_commute_sum, reason_nightshift_sum,
                    reason_noncontact_sum, reason_occupied_sum, reason_covid_sum, 
                    reason_funds_sum, reason_performance_sum, reason_sarturday_sum, reason_website_sum]
    reason_index = ["无叉车证", "不做高叉", "不包吃住", "薪资过低", "距离过远", "拒绝夜班", "无法联系",
                    "已找到工作", "疫情", "公积金", "底薪计件", "做六休一", "招聘网站错投或信息滞后"]

    data1 = pd.Series(reason_list, index=reason_index, name="")
    data1.plot(kind = 'pie', # 选择图形类型
                autopct='%.1f%%', # 饼图中添加数值标签
                radius = 1, # 设置饼图的半径
                startangle = 90, # 设置饼图的初始角度
                counterclock = False, # 将饼图的顺序设置为顺时针方向
                title = pic_name, # 为饼图添加标题
                wedgeprops = {'linewidth': 1.5, 'edgecolor':'green'}, # 设置饼图内外边界的属性值
                textprops = {'fontsize':10, 'color':'black'} # 设置文本标签的属性值
    )
    plt.show()
    print("finished drawing.")

if __name__ == "__main__":
    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['axes.unicode_minus']=False
    
    with pd.ExcelFile(r"0916.xlsx") as xls:
        df = pd.read_excel(xls, "report")
        yesOrNot = df.loc[:, "是否推荐面试"]
        print(yesOrNot.value_counts())
        print(yesOrNot.value_counts().sum())
        location = df.loc[:, "所在地"]
        print(location.value_counts()) 
        print(location.value_counts().sum()) 
        datetime = df.loc[:, "Date"]
        print(datetime.value_counts())
        print(datetime.value_counts().sum())
        reasons = df.loc[:, "候选人来源(51, 58,智联,boss,wechat group,etc)"]
        print(reasons.value_counts())
        print(reasons.value_counts().sum())
        data1 = pd.Series([4, 16, 19, 371], index=["入职", "参加面试", "答应未到面试", "拒绝面试"], name="")
        data1.plot(kind = 'pie', # 选择图形类型
                   autopct='%.1f%%', # 饼图中添加数值标签
                   radius = 1, # 设置饼图的半径
                   startangle = 180, # 设置饼图的初始角度
                   counterclock = False, # 将饼图的顺序设置为顺时针方向
                   title = '招聘整体结果', # 为饼图添加标题
                   wedgeprops = {'linewidth': 1.5, 'edgecolor':'green'}, # 设置饼图内外边界的属性值
                   textprops = {'fontsize':10, 'color':'black'} # 设置文本标签的属性值
        )
        plt.show()

        data1 = pd.Series([143, 131, 49, 31, 26, 39, 16, 14], index=["51job", "boss", "58", "智联", "菁英", "嘉兴人才", "太仓人才", "朋友推荐"], name="")
        data1.plot(kind = 'pie', # 选择图形类型
                   autopct='%.1f%%', # 饼图中添加数值标签
                   radius = 1, # 设置饼图的半径
                   startangle = 90, # 设置饼图的初始角度
                   counterclock = False, # 将饼图的顺序设置为顺时针方向
                   title = '渠道占比分析', # 为饼图添加标题
                   wedgeprops = {'linewidth': 1.5, 'edgecolor':'green'}, # 设置饼图内外边界的属性值
                   textprops = {'fontsize':10, 'color':'black'} # 设置文本标签的属性值
        )
        plt.show()

        
        drawDF(df, "整体原因占比分析")
        df_jiaxing = df[df["所在地"].isin(["嘉兴叉车", "七星叉车", "新丰叉车"])]
        drawDF(df_jiaxing, "嘉兴仓库原因占比分析")
        df_taicang = df[df["所在地"].isin(["太仓叉车", "太仓客服"])]
        drawDF(df_taicang, "太仓仓库原因占比分析")
        df_shanghai = df[df["所在地"].isin(["闵行叉车"])]
        drawDF(df_shanghai, "上海仓库原因占比分析")
    print("finished main function.")
