#!/usr/bin/env python
# coding: utf-8

# 第一部分：程序说明###################################################################################
# coding=utf-8
# 药械不良事件工作平台
# 开发人：蔡权周
import tkinter as Tk #line:11
import os #line:12
import traceback #line:13
import ast #line:14
import re #line:15
import xlrd #line:16
import xlwt #line:17
import openpyxl #line:18
import pandas as pd #line:19
import numpy as np #line:20
import math #line:21
import scipy .stats as st #line:22
from tkinter import ttk ,Menu ,Frame ,Canvas ,StringVar ,LEFT ,RIGHT ,TOP ,BOTTOM ,BOTH ,Y ,X ,YES ,NO ,DISABLED ,END ,Button ,LabelFrame ,GROOVE ,Toplevel ,Label ,Entry ,Scrollbar ,Text ,filedialog ,dialog ,PhotoImage #line:23
import tkinter .font as tkFont #line:24
from tkinter .messagebox import showinfo #line:25
from tkinter .scrolledtext import ScrolledText #line:26
import matplotlib as plt #line:27
from matplotlib .backends .backend_tkagg import FigureCanvasTkAgg #line:28
from matplotlib .figure import Figure #line:29
from matplotlib .backends .backend_tkagg import NavigationToolbar2Tk #line:30
import collections #line:31
from collections import Counter #line:32
import datetime #line:33
from datetime import datetime ,timedelta #line:34
import xlsxwriter #line:35
import time #line:36
import threading #line:37
import warnings #line:38
from matplotlib .ticker import PercentFormatter #line:39
import sqlite3 #line:40
from sqlalchemy import create_engine #line:41
from sqlalchemy import text as sqltext #line:42
import random #line:43
import requests #line:44
import webbrowser #line:45
global ori #line:48
ori =0 #line:49
global auto_guize #line:50
global biaozhun #line:53
global dishi #line:54
biaozhun =""#line:55
dishi =""#line:56
global ini #line:60
ini ={}#line:61
ini ["四个品种"]=1 #line:62
global version_now #line:66
global usergroup #line:67
global setting_cfg #line:68
global csdir #line:69
global peizhidir #line:70
version_now ="0.1.2"#line:71
usergroup ="用户组=0"#line:72
setting_cfg =""#line:73
csdir =str (os .path .abspath (__file__ )).replace (str (__file__ ),"")#line:74
if csdir =="":#line:75
    csdir =str (os .path .dirname (__file__ ))#line:76
    csdir =csdir +csdir .split ("adrmdr")[0 ][-1 ]#line:77
title_all ="药械妆不良反应报表统计分析工作站 V"+version_now #line:80
title_all2 ="药械妆不良反应报表统计分析工作站 V"+version_now #line:81
def extract_zip_file (O0O00000O00000000 ,OO0O000O0OO0O0000 ):#line:88
    import zipfile #line:90
    if OO0O000O0OO0O0000 =="":#line:91
        return 0 #line:92
    with zipfile .ZipFile (O0O00000O00000000 ,'r')as O00OO00000O00O00O :#line:93
        for O0OOOO000OOOO0O0O in O00OO00000O00O00O .infolist ():#line:94
            O0OOOO000OOOO0O0O .filename =O0OOOO000OOOO0O0O .filename .encode ('cp437').decode ('gbk')#line:96
            O00OO00000O00O00O .extract (O0OOOO000OOOO0O0O ,OO0O000O0OO0O0000 )#line:97
def get_directory_path (OO0O0OOOOOO000O0O ):#line:103
    global csdir #line:105
    if not (os .path .isfile (os .path .join (OO0O0OOOOOO000O0O ,'0（范例）比例失衡关键字库.xls'))):#line:107
        extract_zip_file (csdir +"def.py",OO0O0OOOOOO000O0O )#line:112
    if OO0O0OOOOOO000O0O =="":#line:114
        quit ()#line:115
    return OO0O0OOOOOO000O0O #line:116
def convert_and_compare_dates (OOOOO00O00OOO000O ):#line:120
    import datetime #line:121
    OO000O0OOO0OO000O =datetime .datetime .now ()#line:122
    try :#line:124
       O0O0O0OOO0O0OOOO0 =datetime .datetime .strptime (str (int (int (OOOOO00O00OOO000O )/4 )),"%Y%m%d")#line:125
    except :#line:126
        print ("fail")#line:127
        return "已过期"#line:128
    if O0O0O0OOO0O0OOOO0 >OO000O0OOO0OO000O :#line:130
        return "未过期"#line:132
    else :#line:133
        return "已过期"#line:134
def read_setting_cfg ():#line:136
    global csdir #line:137
    if os .path .exists (csdir +'setting.cfg'):#line:139
        text .insert (END ,"已完成初始化\n")#line:140
        with open (csdir +'setting.cfg','r')as O0O000O00OO0OO0O0 :#line:141
            OO00000OO0OO0O0OO =eval (O0O000O00OO0OO0O0 .read ())#line:142
    else :#line:143
        OO0OOOOOOOO0OO0O0 =csdir +'setting.cfg'#line:145
        with open (OO0OOOOOOOO0OO0O0 ,'w')as O0O000O00OO0OO0O0 :#line:146
            O0O000O00OO0OO0O0 .write ('{"settingdir": 0, "sidori": 0, "sidfinal": "11111180000808"}')#line:147
        text .insert (END ,"未初始化，正在初始化...\n")#line:148
        OO00000OO0OO0O0OO =read_setting_cfg ()#line:149
    return OO00000OO0OO0O0OO #line:150
def open_setting_cfg ():#line:153
    global csdir #line:154
    with open (csdir +"setting.cfg","r")as OOOO000O0O000O0O0 :#line:156
        OO0O0O0OO0O0O00OO =eval (OOOO000O0O000O0O0 .read ())#line:158
    return OO0O0O0OO0O0O00OO #line:159
def update_setting_cfg (OO0O00O0OOO0OO0O0 ,OO000OO00OO00OO00 ):#line:161
    global csdir #line:162
    with open (csdir +"setting.cfg","r")as O0O0000OO0OO0OO00 :#line:164
        O0O00OOO0OOO00O0O =eval (O0O0000OO0OO0OO00 .read ())#line:166
    if O0O00OOO0OOO00O0O [OO0O00O0OOO0OO0O0 ]==0 or O0O00OOO0OOO00O0O [OO0O00O0OOO0OO0O0 ]=="11111180000808":#line:168
        O0O00OOO0OOO00O0O [OO0O00O0OOO0OO0O0 ]=OO000OO00OO00OO00 #line:169
        with open (csdir +"setting.cfg","w")as O0O0000OO0OO0OO00 :#line:171
            O0O0000OO0OO0OO00 .write (str (O0O00OOO0OOO00O0O ))#line:172
def generate_random_file ():#line:175
    OOOOOO0OOOOO00OOO =random .randint (200000 ,299999 )#line:177
    update_setting_cfg ("sidori",OOOOOO0OOOOO00OOO )#line:179
def display_random_number ():#line:181
    global csdir #line:182
    OOO0OOO0OOOO0O0O0 =Toplevel ()#line:183
    OOO0OOO0OOOO0O0O0 .title ("ID")#line:184
    O000O000O00O00OOO =OOO0OOO0OOOO0O0O0 .winfo_screenwidth ()#line:186
    OOOOO0OOO0OOOOO00 =OOO0OOO0OOOO0O0O0 .winfo_screenheight ()#line:187
    OOO000O0O00OO0O0O =80 #line:189
    O0OOO000OOOOO00O0 =70 #line:190
    O0OOO0OO00OO00O0O =(O000O000O00O00OOO -OOO000O0O00OO0O0O )/2 #line:192
    O0O000O000O0OO0OO =(OOOOO0OOO0OOOOO00 -O0OOO000OOOOO00O0 )/2 #line:193
    OOO0OOO0OOOO0O0O0 .geometry ("%dx%d+%d+%d"%(OOO000O0O00OO0O0O ,O0OOO000OOOOO00O0 ,O0OOO0OO00OO00O0O ,O0O000O000O0OO0OO ))#line:194
    with open (csdir +"setting.cfg","r")as O0O00OO0OO0O00OOO :#line:197
        OOOO000O0O00O0OO0 =eval (O0O00OO0OO0O00OOO .read ())#line:199
    OO0OO0O00OO0000O0 =int (OOOO000O0O00O0OO0 ["sidori"])#line:200
    OO000O00O00OO0O0O =OO0OO0O00OO0000O0 *2 +183576 #line:201
    print (OO000O00O00OO0O0O )#line:203
    O0O0O0OOOOOO000OO =ttk .Label (OOO0OOO0OOOO0O0O0 ,text =f"机器码: {OO0OO0O00OO0000O0}")#line:205
    OO0OOOO0OO000O0O0 =ttk .Entry (OOO0OOO0OOOO0O0O0 )#line:206
    O0O0O0OOOOOO000OO .pack ()#line:209
    OO0OOOO0OO000O0O0 .pack ()#line:210
    ttk .Button (OOO0OOO0OOOO0O0O0 ,text ="验证",command =lambda :check_input (OO0OOOO0OO000O0O0 .get (),OO000O00O00OO0O0O )).pack ()#line:214
def check_input (OOO000OOOO0000O00 ,O0OOOO000O000O000 ):#line:216
    try :#line:220
        OOO0O000OO00OO000 =int (str (OOO000OOOO0000O00 )[0 :6 ])#line:221
        OOO0000000000O000 =convert_and_compare_dates (str (OOO000OOOO0000O00 )[6 :14 ])#line:222
    except :#line:223
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:224
        return 0 #line:225
    if OOO0O000OO00OO000 ==O0OOOO000O000O000 and OOO0000000000O000 =="未过期":#line:227
        update_setting_cfg ("sidfinal",OOO000OOOO0000O00 )#line:228
        showinfo (title ="提示",message ="注册成功,请重新启动程序。")#line:229
        quit ()#line:230
    else :#line:231
        showinfo (title ="提示",message ="不匹配，注册失败。")#line:232
def update_software (O000OO000O0OOO0O0 ):#line:237
    global version_now #line:239
    text .insert (END ,"当前版本为："+version_now +",正在检查更新...(您可以同时执行分析任务)")#line:240
    try :#line:241
        O0OO0O0OO0O000OO0 =requests .get (f"https://pypi.org/pypi/{O000OO000O0OOO0O0}/json",timeout =2 ).json ()["info"]["version"]#line:242
    except :#line:243
        return "...更新失败。"#line:244
    if O0OO0O0OO0O000OO0 >version_now :#line:245
        text .insert (END ,"\n最新版本为："+O0OO0O0OO0O000OO0 +",正在尝试自动更新....")#line:246
        pip .main (['install',O000OO000O0OOO0O0 ,'--upgrade'])#line:248
        text .insert (END ,"\n您可以开展工作。")#line:249
        return "...更新成功。"#line:250
def TOOLS_ror_mode1 (O0O0OOOO0O00OOOOO ,O0OOO0OOOO00O000O ):#line:267
	O0OO0OOOOOOO000O0 =[]#line:268
	for OOO00O000O000OO0O in ("事件发生年份","性别","年龄段","报告类型-严重程度","停药减药后反应是否减轻或消失","再次使用可疑药是否出现同样反应","对原患疾病影响","不良反应结果","关联性评价"):#line:269
		O0O0OOOO0O00OOOOO [OOO00O000O000OO0O ]=O0O0OOOO0O00OOOOO [OOO00O000O000OO0O ].astype (str )#line:270
		O0O0OOOO0O00OOOOO [OOO00O000O000OO0O ]=O0O0OOOO0O00OOOOO [OOO00O000O000OO0O ].fillna ("不详")#line:271
		O00O00O0OO00OO0O0 =0 #line:273
		for OOO0000O00000OOO0 in O0O0OOOO0O00OOOOO [O0OOO0OOOO00O000O ].drop_duplicates ():#line:274
			O00O00O0OO00OO0O0 =O00O00O0OO00OO0O0 +1 #line:275
			OO0OOOOO0O0000O00 =O0O0OOOO0O00OOOOO [(O0O0OOOO0O00OOOOO [O0OOO0OOOO00O000O ]==OOO0000O00000OOO0 )].copy ()#line:276
			O0000O00000000000 =str (OOO0000O00000OOO0 )+"计数"#line:278
			O00OO000O00OO0O0O =str (OOO0000O00000OOO0 )+"构成比(%)"#line:279
			OOO000OOOO0000OOO =OO0OOOOO0O0000O00 .groupby (OOO00O000O000OO0O ).agg (计数 =("报告编码","nunique")).sort_values (by =OOO00O000O000OO0O ,ascending =[True ],na_position ="last").reset_index ()#line:280
			OOO000OOOO0000OOO [O00OO000O00OO0O0O ]=round (100 *OOO000OOOO0000OOO ["计数"]/OOO000OOOO0000OOO ["计数"].sum (),2 )#line:281
			OOO000OOOO0000OOO =OOO000OOOO0000OOO .rename (columns ={OOO00O000O000OO0O :"项目"})#line:282
			OOO000OOOO0000OOO =OOO000OOOO0000OOO .rename (columns ={"计数":O0000O00000000000 })#line:283
			if O00O00O0OO00OO0O0 >1 :#line:284
				O0O0OOO0OO000OO00 =pd .merge (O0O0OOO0OO000OO00 ,OOO000OOOO0000OOO ,on =["项目"],how ="outer")#line:285
			else :#line:286
				O0O0OOO0OO000OO00 =OOO000OOOO0000OOO .copy ()#line:287
		O0O0OOO0OO000OO00 ["类别"]=OOO00O000O000OO0O #line:289
		O0OO0OOOOOOO000O0 .append (O0O0OOO0OO000OO00 .copy ().reset_index (drop =True ))#line:290
	O0OO00O0O0O0O00OO =pd .concat (O0OO0OOOOOOO000O0 ,ignore_index =True ).fillna (0 )#line:293
	O0OO00O0O0O0O00OO ["报表类型"]="KETI"#line:294
	TABLE_tree_Level_2 (O0OO00O0O0O0O00OO ,1 ,O0OO00O0O0O0O00OO )#line:295
def TOOLS_ror_mode2 (O0O000OO0OOO0O00O ,OOOOO0O00000O0O0O ):#line:297
	O0O0O00OO00000OO0 =Countall (O0O000OO0OOO0O00O ).df_ror (["产品类别",OOOOO0O00000O0O0O ]).reset_index ()#line:298
	O0O0O00OO00000OO0 ["四分表"]=O0O0O00OO00000OO0 ["四分表"].str .replace ("(","")#line:299
	O0O0O00OO00000OO0 ["四分表"]=O0O0O00OO00000OO0 ["四分表"].str .replace (")","")#line:300
	O0O0O00OO00000OO0 ["ROR信号（0-否，1-是）"]=0 #line:301
	O0O0O00OO00000OO0 ["PRR信号（0-否，1-是）"]=0 #line:302
	O0O0O00OO00000OO0 ["分母核验"]=0 #line:303
	for O0OO00OO000000OO0 ,OO0OO0OO0OOO0O000 in O0O0O00OO00000OO0 .iterrows ():#line:304
		OO0O00O0OO00000OO =tuple (OO0OO0OO0OOO0O000 ["四分表"].split (","))#line:305
		O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"a"]=int (OO0O00O0OO00000OO [0 ])#line:306
		O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"b"]=int (OO0O00O0OO00000OO [1 ])#line:307
		O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"c"]=int (OO0O00O0OO00000OO [2 ])#line:308
		O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"d"]=int (OO0O00O0OO00000OO [3 ])#line:309
		if int (OO0O00O0OO00000OO [1 ])*int (OO0O00O0OO00000OO [2 ])*int (OO0O00O0OO00000OO [3 ])*int (OO0O00O0OO00000OO [0 ])==0 :#line:310
			O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"分母核验"]=1 #line:311
		if OO0OO0OO0OOO0O000 ['ROR值的95%CI下限']>1 and OO0OO0OO0OOO0O000 ['出现频次']>=3 :#line:312
			O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"ROR信号（0-否，1-是）"]=1 #line:313
		if OO0OO0OO0OOO0O000 ['PRR值的95%CI下限']>1 and OO0OO0OO0OOO0O000 ['出现频次']>=3 :#line:314
			O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"PRR信号（0-否，1-是）"]=1 #line:315
		O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"事件分类"]=str (TOOLS_get_list (O0O0O00OO00000OO0 .loc [O0OO00OO000000OO0 ,"特定关键字"])[0 ])#line:316
	O0O0O00OO00000OO0 =pd .pivot_table (O0O0O00OO00000OO0 ,values =["出现频次",'ROR值',"ROR值的95%CI下限","ROR信号（0-否，1-是）",'PRR值',"PRR值的95%CI下限","PRR信号（0-否，1-是）","a","b","c","d","分母核验","风险评分"],index ='事件分类',columns =OOOOO0O00000O0O0O ,aggfunc ='sum').reset_index ().fillna (0 )#line:318
	try :#line:321
		OO00O000O0OOOO0O0 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:322
		if "报告类型-新的"in O0O000OO0OOO0O00O .columns :#line:323
			O00O00OO00OO0OOO0 ="药品"#line:324
		else :#line:325
			O00O00OO00OO0OOO0 ="器械"#line:326
		O00000OO00O0000OO =pd .read_excel (OO00O000O0OOOO0O0 ,header =0 ,sheet_name =O00O00OO00OO0OOO0 ).reset_index (drop =True )#line:327
	except :#line:328
		pass #line:329
	for O0OO00OO000000OO0 ,OO0OO0OO0OOO0O000 in O00000OO00O0000OO .iterrows ():#line:331
		O0O0O00OO00000OO0 .loc [O0O0O00OO00000OO0 ["事件分类"].str .contains (OO0OO0OO0OOO0O000 ["值"],na =False ),"器官系统损害"]=TOOLS_get_list (OO0OO0OO0OOO0O000 ["值"])[0 ]#line:332
	try :#line:335
		OO0OO0O0O0000OOOO =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:336
		try :#line:337
			O00O00O00000OOO00 =pd .read_excel (OO0OO0O0O0000OOOO ,sheet_name ="onept",header =0 ,index_col =0 ).reset_index ()#line:338
		except :#line:339
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:340
		try :#line:342
			O0O0000O0OO0OO000 =pd .read_excel (OO0OO0O0O0000OOOO ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:343
		except :#line:344
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:345
		O00O00O00000OOO00 =pd .concat ([O0O0000O0OO0OO000 ,O00O00O00000OOO00 ],ignore_index =True ).drop_duplicates ("code")#line:347
		O00O00O00000OOO00 ["code"]=O00O00O00000OOO00 ["code"].astype (str )#line:348
		O0O0O00OO00000OO0 ["事件分类"]=O0O0O00OO00000OO0 ["事件分类"].astype (str )#line:349
		O00O00O00000OOO00 ["事件分类"]=O00O00O00000OOO00 ["PT"]#line:350
		O0OO00OO0O0000000 =pd .merge (O0O0O00OO00000OO0 ,O00O00O00000OOO00 ,on =["事件分类"],how ="left")#line:351
		for O0OO00OO000000OO0 ,OO0OO0OO0OOO0O000 in O0OO00OO0O0000000 .iterrows ():#line:352
			O0O0O00OO00000OO0 .loc [O0O0O00OO00000OO0 ["事件分类"]==OO0OO0OO0OOO0O000 ["事件分类"],"Chinese"]=OO0OO0OO0OOO0O000 ["Chinese"]#line:353
			O0O0O00OO00000OO0 .loc [O0O0O00OO00000OO0 ["事件分类"]==OO0OO0OO0OOO0O000 ["事件分类"],"PT"]=OO0OO0OO0OOO0O000 ["PT"]#line:354
			O0O0O00OO00000OO0 .loc [O0O0O00OO00000OO0 ["事件分类"]==OO0OO0OO0OOO0O000 ["事件分类"],"HLT"]=OO0OO0OO0OOO0O000 ["HLT"]#line:355
			O0O0O00OO00000OO0 .loc [O0O0O00OO00000OO0 ["事件分类"]==OO0OO0OO0OOO0O000 ["事件分类"],"HLGT"]=OO0OO0OO0OOO0O000 ["HLGT"]#line:356
			O0O0O00OO00000OO0 .loc [O0O0O00OO00000OO0 ["事件分类"]==OO0OO0OO0OOO0O000 ["事件分类"],"SOC"]=OO0OO0OO0OOO0O000 ["SOC"]#line:357
	except :#line:358
		pass #line:359
	O0O0O00OO00000OO0 ["报表类型"]="KETI"#line:362
	TABLE_tree_Level_2 (O0O0O00OO00000OO0 ,1 ,O0O0O00OO00000OO0 )#line:363
def TOOLS_ror_mode3 (OO0OO0OO00000OOOO ,OOOOO00OO0000O0O0 ):#line:365
	OO0OO0OO00000OOOO ["css"]=0 #line:366
	TOOLS_ror_mode2 (OO0OO0OO00000OOOO ,OOOOO00OO0000O0O0 )#line:367
def TOOLS_ror_mode4 (OOO0000OOOOOOOOO0 ,OOO000O00O00O0000 ):#line:369
	O0OO0OOO0OOOOO00O =[]#line:370
	for O0O000OO0OO0O00OO ,O0O0O00O000OOOOOO in data .drop_duplicates (OOO000O00O00O0000 ).iterrows ():#line:371
		O000O00O00OO0O0O0 =data [(OOO0000OOOOOOOOO0 [OOO000O00O00O0000 ]==O0O0O00O000OOOOOO [OOO000O00O00O0000 ])]#line:372
		O0OOOO0OO0O00O0OO =Countall (O000O00O00OO0O0O0 ).df_psur ()#line:373
		O0OOOO0OO0O00O0OO [OOO000O00O00O0000 ]=O0O0O00O000OOOOOO [OOO000O00O00O0000 ]#line:374
		if len (O0OOOO0OO0O00O0OO )>0 :#line:375
			O0OO0OOO0OOOOO00O .append (O0OOOO0OO0O00O0OO )#line:376
	O00OO0O00OO00O000 =pd .concat (O0OO0OOO0OOOOO00O ,ignore_index =True ).sort_values (by ="关键字标记",ascending =[False ],na_position ="last").reset_index ()#line:378
	O00OO0O00OO00O000 ["报表类型"]="KETI"#line:379
	TABLE_tree_Level_2 (O00OO0O00OO00O000 ,1 ,O00OO0O00OO00O000 )#line:380
def STAT_pinzhong (O0O0OOOOOO0O0OOO0 ,OOO0O00OO00O00000 ,OO0O0OOOOOO0000OO ):#line:382
	OOOOO00O000O0O000 =[OOO0O00OO00O00000 ]#line:384
	if OO0O0OOOOOO0000OO ==-1 :#line:385
		OOOO00OOOO00O0000 =O0O0OOOOOO0O0OOO0 .drop_duplicates ("报告编码").copy ()#line:386
		OOOOO00O0O0000O00 =OOOO00OOOO00O0000 .groupby ([OOO0O00OO00O00000 ]).agg (计数 =("报告编码","nunique")).sort_values (by =OOO0O00OO00O00000 ,ascending =[True ],na_position ="last").reset_index ()#line:387
		OOOOO00O0O0000O00 ["构成比(%)"]=round (100 *OOOOO00O0O0000O00 ["计数"]/OOOOO00O0O0000O00 ["计数"].sum (),2 )#line:388
		OOOOO00O0O0000O00 [OOO0O00OO00O00000 ]=OOOOO00O0O0000O00 [OOO0O00OO00O00000 ].astype (str )#line:389
		OOOOO00O0O0000O00 ["报表类型"]="dfx_deepview"+"_"+str (OOOOO00O000O0O000 )#line:390
		TABLE_tree_Level_2 (OOOOO00O0O0000O00 ,1 ,OOOO00OOOO00O0000 )#line:391
	if OO0O0OOOOOO0000OO ==1 :#line:393
		OOOO00OOOO00O0000 =O0O0OOOOOO0O0OOO0 .copy ()#line:394
		OOOOO00O0O0000O00 =OOOO00OOOO00O0000 .groupby ([OOO0O00OO00O00000 ]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:395
		OOOOO00O0O0000O00 ["构成比(%)"]=round (100 *OOOOO00O0O0000O00 ["计数"]/OOOOO00O0O0000O00 ["计数"].sum (),2 )#line:396
		OOOOO00O0O0000O00 ["报表类型"]="dfx_deepview"+"_"+str (OOOOO00O000O0O000 )#line:397
		TABLE_tree_Level_2 (OOOOO00O0O0000O00 ,1 ,OOOO00OOOO00O0000 )#line:398
	if OO0O0OOOOOO0000OO ==4 :#line:400
		OOOO00OOOO00O0000 =O0O0OOOOOO0O0OOO0 .copy ()#line:401
		OOOO00OOOO00O0000 .loc [OOOO00OOOO00O0000 ["不良反应结果"].str .contains ("好转",na =False ),"不良反应结果2"]="好转"#line:402
		OOOO00OOOO00O0000 .loc [OOOO00OOOO00O0000 ["不良反应结果"].str .contains ("痊愈",na =False ),"不良反应结果2"]="痊愈"#line:403
		OOOO00OOOO00O0000 .loc [OOOO00OOOO00O0000 ["不良反应结果"].str .contains ("无进展",na =False ),"不良反应结果2"]="无进展"#line:404
		OOOO00OOOO00O0000 .loc [OOOO00OOOO00O0000 ["不良反应结果"].str .contains ("死亡",na =False ),"不良反应结果2"]="死亡"#line:405
		OOOO00OOOO00O0000 .loc [OOOO00OOOO00O0000 ["不良反应结果"].str .contains ("不详",na =False ),"不良反应结果2"]="不详"#line:406
		OOOO00OOOO00O0000 .loc [OOOO00OOOO00O0000 ["不良反应结果"].str .contains ("未好转",na =False ),"不良反应结果2"]="未好转"#line:407
		OOOOO00O0O0000O00 =OOOO00OOOO00O0000 .groupby (["不良反应结果2"]).agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:408
		OOOOO00O0O0000O00 ["构成比(%)"]=round (100 *OOOOO00O0O0000O00 ["计数"]/OOOOO00O0O0000O00 ["计数"].sum (),2 )#line:409
		OOOOO00O0O0000O00 ["报表类型"]="dfx_deepview"+"_"+str (["不良反应结果2"])#line:410
		TABLE_tree_Level_2 (OOOOO00O0O0000O00 ,1 ,OOOO00OOOO00O0000 )#line:411
	if OO0O0OOOOOO0000OO ==5 :#line:413
		OOOO00OOOO00O0000 =O0O0OOOOOO0O0OOO0 .copy ()#line:414
		OOOO00OOOO00O0000 ["关联性评价汇总"]="("+OOOO00OOOO00O0000 ["评价状态"].astype (str )+"("+OOOO00OOOO00O0000 ["县评价"].astype (str )+"("+OOOO00OOOO00O0000 ["市评价"].astype (str )+"("+OOOO00OOOO00O0000 ["省评价"].astype (str )+"("+OOOO00OOOO00O0000 ["国家评价"].astype (str )+")"#line:416
		OOOO00OOOO00O0000 ["关联性评价汇总"]=OOOO00OOOO00O0000 ["关联性评价汇总"].str .replace ("(nan","",regex =False )#line:417
		OOOO00OOOO00O0000 ["关联性评价汇总"]=OOOO00OOOO00O0000 ["关联性评价汇总"].str .replace ("nan)","",regex =False )#line:418
		OOOO00OOOO00O0000 ["关联性评价汇总"]=OOOO00OOOO00O0000 ["关联性评价汇总"].str .replace ("nan","",regex =False )#line:419
		OOOO00OOOO00O0000 ['最终的关联性评价']=OOOO00OOOO00O0000 ["关联性评价汇总"].str .extract ('.*\((.*)\).*',expand =False )#line:420
		OOOOO00O0O0000O00 =OOOO00OOOO00O0000 .groupby ('最终的关联性评价').agg (计数 =("报告编码","nunique")).sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index ()#line:421
		OOOOO00O0O0000O00 ["构成比(%)"]=round (100 *OOOOO00O0O0000O00 ["计数"]/OOOOO00O0O0000O00 ["计数"].sum (),2 )#line:422
		OOOOO00O0O0000O00 ["报表类型"]="dfx_deepview"+"_"+str (['最终的关联性评价'])#line:423
		TABLE_tree_Level_2 (OOOOO00O0O0000O00 ,1 ,OOOO00OOOO00O0000 )#line:424
	if OO0O0OOOOOO0000OO ==0 :#line:426
		O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ]=O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ].fillna ("未填写")#line:427
		O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ]=O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ].str .replace ("*","",regex =False )#line:428
		OOOOO000O0OO0000O ="use("+str (OOO0O00OO00O00000 )+").file"#line:429
		O0000O0OOOOOO0OOO =str (Counter (TOOLS_get_list0 (OOOOO000O0OO0000O ,O0O0OOOOOO0O0OOO0 ,1000 ))).replace ("Counter({","{")#line:430
		O0000O0OOOOOO0OOO =O0000O0OOOOOO0OOO .replace ("})","}")#line:431
		O0000O0OOOOOO0OOO =ast .literal_eval (O0000O0OOOOOO0OOO )#line:432
		OOOOO00O0O0000O00 =pd .DataFrame .from_dict (O0000O0OOOOOO0OOO ,orient ="index",columns =["计数"]).reset_index ()#line:433
		OOOOO00O0O0000O00 ["构成比(%)"]=round (100 *OOOOO00O0O0000O00 ["计数"]/OOOOO00O0O0000O00 ["计数"].sum (),2 )#line:435
		OOOOO00O0O0000O00 ["报表类型"]="dfx_deepvie2"+"_"+str (OOOOO00O000O0O000 )#line:436
		TABLE_tree_Level_2 (OOOOO00O0O0000O00 ,1 ,O0O0OOOOOO0O0OOO0 )#line:437
		return OOOOO00O0O0000O00 #line:438
	if OO0O0OOOOOO0000OO ==2 or OO0O0OOOOOO0000OO ==3 :#line:442
		O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ]=O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ].astype (str )#line:443
		O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ]=O0O0OOOOOO0O0OOO0 [OOO0O00OO00O00000 ].fillna ("未填写")#line:444
		OOOOO000O0OO0000O ="use("+str (OOO0O00OO00O00000 )+").file"#line:446
		O0000O0OOOOOO0OOO =str (Counter (TOOLS_get_list0 (OOOOO000O0OO0000O ,O0O0OOOOOO0O0OOO0 ,1000 ))).replace ("Counter({","{")#line:447
		O0000O0OOOOOO0OOO =O0000O0OOOOOO0OOO .replace ("})","}")#line:448
		O0000O0OOOOOO0OOO =ast .literal_eval (O0000O0OOOOOO0OOO )#line:449
		OOOOO00O0O0000O00 =pd .DataFrame .from_dict (O0000O0OOOOOO0OOO ,orient ="index",columns =["计数"]).reset_index ()#line:450
		print ("正在统计，请稍后...")#line:451
		O0OO0O00O00OOOO00 =peizhidir +""+"0（范例）标准术语"+".xlsx"#line:452
		try :#line:453
			O00O00O0O00O0000O =pd .read_excel (O0OO0O00O00OOOO00 ,sheet_name ="simple",header =0 ,index_col =0 ).reset_index ()#line:454
		except :#line:455
			showinfo (title ="错误信息",message ="标准术语集无法加载。")#line:456
			return 0 #line:457
		try :#line:458
			OOOO00OO0O0OO0OO0 =pd .read_excel (O0OO0O00O00OOOO00 ,sheet_name ="my",header =0 ,index_col =0 ).reset_index ()#line:459
		except :#line:460
			showinfo (title ="错误信息",message ="自定义术语集无法加载。")#line:461
			return 0 #line:462
		O00O00O0O00O0000O =pd .concat ([OOOO00OO0O0OO0OO0 ,O00O00O0O00O0000O ],ignore_index =True ).drop_duplicates ("code")#line:463
		O00O00O0O00O0000O ["code"]=O00O00O0O00O0000O ["code"].astype (str )#line:464
		OOOOO00O0O0000O00 ["index"]=OOOOO00O0O0000O00 ["index"].astype (str )#line:465
		OOOOO00O0O0000O00 =OOOOO00O0O0000O00 .rename (columns ={"index":"code"})#line:467
		OOOOO00O0O0000O00 =pd .merge (OOOOO00O0O0000O00 ,O00O00O0O00O0000O ,on =["code"],how ="left")#line:468
		OOOOO00O0O0000O00 ["code构成比(%)"]=round (100 *OOOOO00O0O0000O00 ["计数"]/OOOOO00O0O0000O00 ["计数"].sum (),2 )#line:469
		OOO0O0O0OO000OOOO =OOOOO00O0O0000O00 .groupby ("SOC").agg (SOC计数 =("计数","sum")).sort_values (by ="SOC计数",ascending =[False ],na_position ="last").reset_index ()#line:470
		OOO0O0O0OO000OOOO ["soc构成比(%)"]=round (100 *OOO0O0O0OO000OOOO ["SOC计数"]/OOO0O0O0OO000OOOO ["SOC计数"].sum (),2 )#line:471
		OOO0O0O0OO000OOOO ["SOC计数"]=OOO0O0O0OO000OOOO ["SOC计数"].astype (int )#line:472
		OOOOO00O0O0000O00 =pd .merge (OOOOO00O0O0000O00 ,OOO0O0O0OO000OOOO ,on =["SOC"],how ="left")#line:473
		if OO0O0OOOOOO0000OO ==3 :#line:475
			OOO0O0O0OO000OOOO ["具体名称"]=""#line:476
			for O0OO0O0O0OO0O0000 ,OOOOO0O0OO00000O0 in OOO0O0O0OO000OOOO .iterrows ():#line:477
				O00O0OOOOOOO0000O =""#line:478
				O0OOOO000OO00OOOO =OOOOO00O0O0000O00 .loc [OOOOO00O0O0000O00 ["SOC"].str .contains (OOOOO0O0OO00000O0 ["SOC"],na =False )].copy ()#line:479
				for O0O00O0O000OOOO00 ,O0O000OO0O0OO0000 in O0OOOO000OO00OOOO .iterrows ():#line:480
					O00O0OOOOOOO0000O =O00O0OOOOOOO0000O +str (O0O000OO0O0OO0000 ["PT"])+"("+str (O0O000OO0O0OO0000 ["计数"])+")、"#line:481
				OOO0O0O0OO000OOOO .loc [O0OO0O0O0OO0O0000 ,"具体名称"]=O00O0OOOOOOO0000O #line:482
			OOO0O0O0OO000OOOO ["报表类型"]="dfx_deepvie2"+"_"+str (["SOC"])#line:483
			TABLE_tree_Level_2 (OOO0O0O0OO000OOOO ,1 ,OOOOO00O0O0000O00 )#line:484
		if OO0O0OOOOOO0000OO ==2 :#line:486
			OOOOO00O0O0000O00 ["报表类型"]="dfx_deepvie2"+"_"+str (OOOOO00O000O0O000 )#line:487
			TABLE_tree_Level_2 (OOOOO00O0O0000O00 ,1 ,O0O0OOOOOO0O0OOO0 )#line:488
	pass #line:491
def DRAW_pre (OO00OOO0O000OOO0O ):#line:493
	""#line:494
	OOOOOO0OOOOO0OO0O =list (OO00OOO0O000OOO0O ["报表类型"])[0 ].replace ("1","")#line:502
	if "dfx_org监测机构"in OOOOOO0OOOOO0OO0O :#line:504
		OO00OOO0O000OOO0O =OO00OOO0O000OOO0O [:-1 ]#line:505
		DRAW_make_one (OO00OOO0O000OOO0O ,"报告图","监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:506
	elif "dfx_org市级监测机构"in OOOOOO0OOOOO0OO0O :#line:507
		OO00OOO0O000OOO0O =OO00OOO0O000OOO0O [:-1 ]#line:508
		DRAW_make_one (OO00OOO0O000OOO0O ,"报告图","市级监测机构","报告数量","超级托帕斯图(严重伤害数)")#line:509
	elif "dfx_user"in OOOOOO0OOOOO0OO0O :#line:510
		OO00OOO0O000OOO0O =OO00OOO0O000OOO0O [:-1 ]#line:511
		DRAW_make_one (OO00OOO0O000OOO0O ,"报告单位图","单位名称","报告数量","超级托帕斯图(严重伤害数)")#line:512
	elif "dfx_deepview"in OOOOOO0OOOOO0OO0O :#line:515
		DRAW_make_one (OO00OOO0O000OOO0O ,"柱状图",OO00OOO0O000OOO0O .columns [0 ],"计数","柱状图")#line:516
	elif "dfx_chiyouren"in OOOOOO0OOOOO0OO0O :#line:518
		OO00OOO0O000OOO0O =OO00OOO0O000OOO0O [:-1 ]#line:519
		DRAW_make_one (OO00OOO0O000OOO0O ,"涉及持有人图","上市许可持有人名称","总报告数","超级托帕斯图(总待评价数量)")#line:520
	elif "dfx_zhenghao"in OOOOOO0OOOOO0OO0O :#line:522
		OO00OOO0O000OOO0O ["产品"]=OO00OOO0O000OOO0O ["产品名称"]+"("+OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"]+")"#line:523
		DRAW_make_one (OO00OOO0O000OOO0O ,"涉及产品图","产品","证号计数","超级托帕斯图(严重伤害数)")#line:524
	elif "dfx_pihao"in OOOOOO0OOOOO0OO0O :#line:526
		if len (OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:527
			OO00OOO0O000OOO0O ["产品"]=OO00OOO0O000OOO0O ["产品名称"]+"("+OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"]+"--"+OO00OOO0O000OOO0O ["产品批号"]+")"#line:528
			DRAW_make_one (OO00OOO0O000OOO0O ,"涉及批号图","产品","批号计数","超级托帕斯图(严重伤害数)")#line:529
		else :#line:530
			DRAW_make_one (OO00OOO0O000OOO0O ,"涉及批号图","产品批号","批号计数","超级托帕斯图(严重伤害数)")#line:531
	elif "dfx_xinghao"in OOOOOO0OOOOO0OO0O :#line:533
		if len (OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:534
			OO00OOO0O000OOO0O ["产品"]=OO00OOO0O000OOO0O ["产品名称"]+"("+OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"]+"--"+OO00OOO0O000OOO0O ["型号"]+")"#line:535
			DRAW_make_one (OO00OOO0O000OOO0O ,"涉及型号图","产品","型号计数","超级托帕斯图(严重伤害数)")#line:536
		else :#line:537
			DRAW_make_one (OO00OOO0O000OOO0O ,"涉及型号图","型号","型号计数","超级托帕斯图(严重伤害数)")#line:538
	elif "dfx_guige"in OOOOOO0OOOOO0OO0O :#line:540
		if len (OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"].drop_duplicates ())>1 :#line:541
			OO00OOO0O000OOO0O ["产品"]=OO00OOO0O000OOO0O ["产品名称"]+"("+OO00OOO0O000OOO0O ["注册证编号/曾用注册证编号"]+"--"+OO00OOO0O000OOO0O ["规格"]+")"#line:542
			DRAW_make_one (OO00OOO0O000OOO0O ,"涉及规格图","产品","规格计数","超级托帕斯图(严重伤害数)")#line:543
		else :#line:544
			DRAW_make_one (OO00OOO0O000OOO0O ,"涉及规格图","规格","规格计数","超级托帕斯图(严重伤害数)")#line:545
	elif "PSUR"in OOOOOO0OOOOO0OO0O :#line:547
		DRAW_make_mutibar (OO00OOO0O000OOO0O ,"总数量","严重","事件分类","总数量","严重","表现分类统计图")#line:548
	elif "keyword_findrisk"in OOOOOO0OOOOO0OO0O :#line:550
		OOOO0O0OO00O000O0 =OO00OOO0O000OOO0O .columns .to_list ()#line:552
		OOO0O00OO0O00000O =OOOO0O0OO00O000O0 [OOOO0O0OO00O000O0 .index ("关键字")+1 ]#line:553
		O0OOOOO000OO0O000 =pd .pivot_table (OO00OOO0O000OOO0O ,index =OOO0O00OO0O00000O ,columns ="关键字",values =["计数"],aggfunc ={"计数":"sum"},fill_value ="0",margins =True ,dropna =False ,)#line:564
		O0OOOOO000OO0O000 .columns =O0OOOOO000OO0O000 .columns .droplevel (0 )#line:565
		O0OOOOO000OO0O000 =O0OOOOO000OO0O000 [:-1 ].reset_index ()#line:566
		O0OOOOO000OO0O000 =pd .merge (O0OOOOO000OO0O000 ,OO00OOO0O000OOO0O [[OOO0O00OO0O00000O ,"该元素总数量"]].drop_duplicates (OOO0O00OO0O00000O ),on =[OOO0O00OO0O00000O ],how ="left")#line:568
		del O0OOOOO000OO0O000 ["All"]#line:570
		DRAW_make_risk_plot (O0OOOOO000OO0O000 ,OOO0O00OO0O00000O ,[O0OO00O00000000OO for O0OO00O00000000OO in O0OOOOO000OO0O000 .columns if O0OO00O00000000OO !=OOO0O00OO0O00000O ],"关键字趋势图",100 )#line:575
def DRAW_make_risk_plot (O0O0O00O00OO00OOO ,O000O0O0000OO0000 ,OOOOOO0O000O0OO00 ,OO0OO0O0OO0O0OO00 ,OO000O000000O000O ,*O0O00O00O00O00OOO ):#line:580
    ""#line:581
    O0000OOOO0O0OOO0O =Toplevel ()#line:584
    O0000OOOO0O0OOO0O .title (OO0OO0O0OO0O0OO00 )#line:585
    O000000O00000O000 =ttk .Frame (O0000OOOO0O0OOO0O ,height =20 )#line:586
    O000000O00000O000 .pack (side =TOP )#line:587
    O0OOOO0O00O0OO0OO =Figure (figsize =(12 ,6 ),dpi =100 )#line:589
    O00OOO0O00O00O0O0 =FigureCanvasTkAgg (O0OOOO0O00O0OO0OO ,master =O0000OOOO0O0OOO0O )#line:590
    O00OOO0O00O00O0O0 .draw ()#line:591
    O00OOO0O00O00O0O0 .get_tk_widget ().pack (expand =1 )#line:592
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:594
    plt .rcParams ['axes.unicode_minus']=False #line:595
    OO0OO0O0OOOOOOO0O =NavigationToolbar2Tk (O00OOO0O00O00O0O0 ,O0000OOOO0O0OOO0O )#line:597
    OO0OO0O0OOOOOOO0O .update ()#line:598
    O00OOO0O00O00O0O0 .get_tk_widget ().pack ()#line:599
    OOO0OOOOO0O0O0O00 =O0OOOO0O00O0OO0OO .add_subplot (111 )#line:601
    OOO0OOOOO0O0O0O00 .set_title (OO0OO0O0OO0O0OO00 )#line:603
    OO0OOO0OOO0O0OOOO =O0O0O00O00OO00OOO [O000O0O0000OO0000 ]#line:604
    if OO000O000000O000O !=999 :#line:607
        OOO0OOOOO0O0O0O00 .set_xticklabels (OO0OOO0OOO0O0OOOO ,rotation =-90 ,fontsize =8 )#line:608
    O000OO000O0OOO0OO =range (0 ,len (OO0OOO0OOO0O0OOOO ),1 )#line:611
    try :#line:616
        OOO0OOOOO0O0O0O00 .bar (OO0OOO0OOO0O0OOOO ,O0O0O00O00OO00OOO ["报告总数"],color ='skyblue',label ="报告总数")#line:617
        OOO0OOOOO0O0O0O00 .bar (OO0OOO0OOO0O0OOOO ,height =O0O0O00O00OO00OOO ["严重伤害数"],color ="orangered",label ="严重伤害数")#line:618
    except :#line:619
        pass #line:620
    for OOOO0OO000OOO00OO in OOOOOO0O000O0OO00 :#line:623
        O0OO0OOO0O0OO0O0O =O0O0O00O00OO00OOO [OOOO0OO000OOO00OO ].astype (float )#line:624
        if OOOO0OO000OOO00OO =="关注区域":#line:626
            OOO0OOOOO0O0O0O00 .plot (list (OO0OOO0OOO0O0OOOO ),list (O0OO0OOO0O0OO0O0O ),label =str (OOOO0OO000OOO00OO ),color ="red")#line:627
        else :#line:628
            OOO0OOOOO0O0O0O00 .plot (list (OO0OOO0OOO0O0OOOO ),list (O0OO0OOO0O0OO0O0O ),label =str (OOOO0OO000OOO00OO ))#line:629
        if OO000O000000O000O ==100 :#line:632
            for O00O00O0000OO00O0 ,O0000OO0OOO00O0O0 in zip (OO0OOO0OOO0O0OOOO ,O0OO0OOO0O0OO0O0O ):#line:633
                if O0000OO0OOO00O0O0 ==max (O0OO0OOO0O0OO0O0O )and O0000OO0OOO00O0O0 >=3 :#line:634
                     OOO0OOOOO0O0O0O00 .text (O00O00O0000OO00O0 ,O0000OO0OOO00O0O0 ,(str (OOOO0OO000OOO00OO )+":"+str (int (O0000OO0OOO00O0O0 ))),color ='black',size =8 )#line:635
    try :#line:645
        if O0O00O00O00O00OOO [0 ]:#line:646
            OOOOOOO0O0O00O000 =O0O00O00O00O00OOO [0 ]#line:647
    except :#line:648
        OOOOOOO0O0O00O000 ="ucl"#line:649
    if len (OOOOOO0O000O0OO00 )==1 :#line:651
        if OOOOOOO0O0O00O000 =="更多控制线分位数":#line:653
            O000O0O0OOOOO00O0 =O0O0O00O00OO00OOO [OOOOOO0O000O0OO00 ].astype (float ).values #line:654
            O0O0000OOO0O0O0O0 =np .where (O000O0O0OOOOO00O0 >0 ,1 ,0 )#line:655
            O0O0O0OO000000000 =np .nonzero (O0O0000OOO0O0O0O0 )#line:656
            O000O0O0OOOOO00O0 =O000O0O0OOOOO00O0 [O0O0O0OO000000000 ]#line:657
            O0OOO000O0O0OOO0O =np .median (O000O0O0OOOOO00O0 )#line:658
            OO0OOO0O0000OO0OO =np .percentile (O000O0O0OOOOO00O0 ,25 )#line:659
            O0OO00000OO0OOOOO =np .percentile (O000O0O0OOOOO00O0 ,75 )#line:660
            O0OOO0OOOOO0O0000 =O0OO00000OO0OOOOO -OO0OOO0O0000OO0OO #line:661
            O0O0O0O0000O0OO00 =O0OO00000OO0OOOOO +1.5 *O0OOO0OOOOO0O0000 #line:662
            OOO000O000OOO0O0O =OO0OOO0O0000OO0OO -1.5 *O0OOO0OOOOO0O0000 #line:663
            OOO0OOOOO0O0O0O00 .axhline (OOO000O000OOO0O0O ,color ='c',linestyle ='--',label ='异常下限')#line:666
            OOO0OOOOO0O0O0O00 .axhline (OO0OOO0O0000OO0OO ,color ='r',linestyle ='--',label ='第25百分位数')#line:668
            OOO0OOOOO0O0O0O00 .axhline (O0OOO000O0O0OOO0O ,color ='g',linestyle ='--',label ='中位数')#line:669
            OOO0OOOOO0O0O0O00 .axhline (O0OO00000OO0OOOOO ,color ='r',linestyle ='--',label ='第75百分位数')#line:670
            OOO0OOOOO0O0O0O00 .axhline (O0O0O0O0000O0OO00 ,color ='c',linestyle ='--',label ='异常上限')#line:672
            O0O0OOO00000OOO00 =ttk .Label (O0000OOOO0O0OOO0O ,text ="中位数="+str (O0OOO000O0O0OOO0O )+"; 第25百分位数="+str (OO0OOO0O0000OO0OO )+"; 第75百分位数="+str (O0OO00000OO0OOOOO )+"; 异常上限(第75百分位数+1.5IQR)="+str (O0O0O0O0000O0OO00 )+"; IQR="+str (O0OOO0OOOOO0O0000 ))#line:673
            O0O0OOO00000OOO00 .pack ()#line:674
        elif OOOOOOO0O0O00O000 =="更多控制线STD":#line:676
            O000O0O0OOOOO00O0 =O0O0O00O00OO00OOO [OOOOOO0O000O0OO00 ].astype (float ).values #line:677
            O0O0000OOO0O0O0O0 =np .where (O000O0O0OOOOO00O0 >0 ,1 ,0 )#line:678
            O0O0O0OO000000000 =np .nonzero (O0O0000OOO0O0O0O0 )#line:679
            O000O0O0OOOOO00O0 =O000O0O0OOOOO00O0 [O0O0O0OO000000000 ]#line:680
            OOO0O0OOOO0000000 =O000O0O0OOOOO00O0 .mean ()#line:682
            O000OOOO00OOO0O0O =O000O0O0OOOOO00O0 .std (ddof =1 )#line:683
            O0OO0O0OO00000O00 =OOO0O0OOOO0000000 +3 *O000OOOO00OOO0O0O #line:684
            OOO000O0000000O00 =O000OOOO00OOO0O0O -3 *O000OOOO00OOO0O0O #line:685
            if len (O000O0O0OOOOO00O0 )<30 :#line:687
                O0OO0OO00O0O0O000 =st .t .interval (0.95 ,df =len (O000O0O0OOOOO00O0 )-1 ,loc =np .mean (O000O0O0OOOOO00O0 ),scale =st .sem (O000O0O0OOOOO00O0 ))#line:688
            else :#line:689
                O0OO0OO00O0O0O000 =st .norm .interval (0.95 ,loc =np .mean (O000O0O0OOOOO00O0 ),scale =st .sem (O000O0O0OOOOO00O0 ))#line:690
            O0OO0OO00O0O0O000 =O0OO0OO00O0O0O000 [1 ]#line:691
            OOO0OOOOO0O0O0O00 .axhline (O0OO0O0OO00000O00 ,color ='r',linestyle ='--',label ='UCL')#line:692
            OOO0OOOOO0O0O0O00 .axhline (OOO0O0OOOO0000000 +2 *O000OOOO00OOO0O0O ,color ='m',linestyle ='--',label ='μ+2σ')#line:693
            OOO0OOOOO0O0O0O00 .axhline (OOO0O0OOOO0000000 +O000OOOO00OOO0O0O ,color ='m',linestyle ='--',label ='μ+σ')#line:694
            OOO0OOOOO0O0O0O00 .axhline (OOO0O0OOOO0000000 ,color ='g',linestyle ='--',label ='CL')#line:695
            OOO0OOOOO0O0O0O00 .axhline (OOO0O0OOOO0000000 -O000OOOO00OOO0O0O ,color ='m',linestyle ='--',label ='μ-σ')#line:696
            OOO0OOOOO0O0O0O00 .axhline (OOO0O0OOOO0000000 -2 *O000OOOO00OOO0O0O ,color ='m',linestyle ='--',label ='μ-2σ')#line:697
            OOO0OOOOO0O0O0O00 .axhline (OOO000O0000000O00 ,color ='r',linestyle ='--',label ='LCL')#line:698
            OOO0OOOOO0O0O0O00 .axhline (O0OO0OO00O0O0O000 ,color ='g',linestyle ='-',label ='95CI')#line:699
            O0OO0O00000OOOO0O =ttk .Label (O0000OOOO0O0OOO0O ,text ="mean="+str (OOO0O0OOOO0000000 )+"; std="+str (O000OOOO00OOO0O0O )+"; 99.73%:UCL(μ+3σ)="+str (O0OO0O0OO00000O00 )+"; LCL(μ-3σ)="+str (OOO000O0000000O00 )+"; 95%CI="+str (O0OO0OO00O0O0O000 ))#line:700
            O0OO0O00000OOOO0O .pack ()#line:701
            O0O0OOO00000OOO00 =ttk .Label (O0000OOOO0O0OOO0O ,text ="68.26%:μ+σ="+str (OOO0O0OOOO0000000 +O000OOOO00OOO0O0O )+"; 95.45%:μ+2σ="+str (OOO0O0OOOO0000000 +2 *O000OOOO00OOO0O0O ))#line:703
            O0O0OOO00000OOO00 .pack ()#line:704
        else :#line:706
            O000O0O0OOOOO00O0 =O0O0O00O00OO00OOO [OOOOOO0O000O0OO00 ].astype (float ).values #line:707
            O0O0000OOO0O0O0O0 =np .where (O000O0O0OOOOO00O0 >0 ,1 ,0 )#line:708
            O0O0O0OO000000000 =np .nonzero (O0O0000OOO0O0O0O0 )#line:709
            O000O0O0OOOOO00O0 =O000O0O0OOOOO00O0 [O0O0O0OO000000000 ]#line:710
            OOO0O0OOOO0000000 =O000O0O0OOOOO00O0 .mean ()#line:711
            O000OOOO00OOO0O0O =O000O0O0OOOOO00O0 .std (ddof =1 )#line:712
            O0OO0O0OO00000O00 =OOO0O0OOOO0000000 +3 *O000OOOO00OOO0O0O #line:713
            OOO000O0000000O00 =O000OOOO00OOO0O0O -3 *O000OOOO00OOO0O0O #line:714
            OOO0OOOOO0O0O0O00 .axhline (O0OO0O0OO00000O00 ,color ='r',linestyle ='--',label ='UCL')#line:715
            OOO0OOOOO0O0O0O00 .axhline (OOO0O0OOOO0000000 ,color ='g',linestyle ='--',label ='CL')#line:716
            OOO0OOOOO0O0O0O00 .axhline (OOO000O0000000O00 ,color ='r',linestyle ='--',label ='LCL')#line:717
            O0OO0O00000OOOO0O =ttk .Label (O0000OOOO0O0OOO0O ,text ="mean="+str (OOO0O0OOOO0000000 )+"; std="+str (O000OOOO00OOO0O0O )+"; UCL(μ+3σ)="+str (O0OO0O0OO00000O00 )+"; LCL(μ-3σ)="+str (OOO000O0000000O00 ))#line:718
            O0OO0O00000OOOO0O .pack ()#line:719
    OOO0OOOOO0O0O0O00 .set_title ("控制图")#line:722
    OOO0OOOOO0O0O0O00 .set_xlabel ("项")#line:723
    O0OOOO0O00O0OO0OO .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:724
    OOO0O0O0OO00OO000 =OOO0OOOOO0O0O0O00 .get_position ()#line:725
    OOO0OOOOO0O0O0O00 .set_position ([OOO0O0O0OO00OO000 .x0 ,OOO0O0O0OO00OO000 .y0 ,OOO0O0O0OO00OO000 .width *0.7 ,OOO0O0O0OO00OO000 .height ])#line:726
    OOO0OOOOO0O0O0O00 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:727
    O00O00O0000OO0000 =StringVar ()#line:730
    O00OO0OOOO000O0OO =ttk .Combobox (O000000O00000O000 ,width =15 ,textvariable =O00O00O0000OO0000 ,state ='readonly')#line:731
    O00OO0OOOO000O0OO ['values']=OOOOOO0O000O0OO00 #line:732
    O00OO0OOOO000O0OO .pack (side =LEFT )#line:733
    O00OO0OOOO000O0OO .current (0 )#line:734
    OOOO0OO0000OOOOOO =Button (O000000O00000O000 ,text ="控制图（单项-UCL(μ+3σ)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0O0O00O00OO00OOO ,O000O0O0000OO0000 ,[OOOO00000OOOOO00O for OOOO00000OOOOO00O in OOOOOO0O000O0OO00 if O00O00O0000OO0000 .get ()in OOOO00000OOOOO00O ],OO0OO0O0OO0O0OO00 ,OO000O000000O000O ))#line:744
    OOOO0OO0000OOOOOO .pack (side =LEFT ,anchor ="ne")#line:745
    OO0O0OO00000O00O0 =Button (O000000O00000O000 ,text ="控制图（单项-UCL(标准差法)）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0O0O00O00OO00OOO ,O000O0O0000OO0000 ,[OOO000O0OOO000OO0 for OOO000O0OOO000OO0 in OOOOOO0O000O0OO00 if O00O00O0000OO0000 .get ()in OOO000O0OOO000OO0 ],OO0OO0O0OO0O0OO00 ,OO000O000000O000O ,"更多控制线STD"))#line:753
    OO0O0OO00000O00O0 .pack (side =LEFT ,anchor ="ne")#line:754
    OO0O0OO00000O00O0 =Button (O000000O00000O000 ,text ="控制图（单项-分位数）",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0O0O00O00OO00OOO ,O000O0O0000OO0000 ,[O0O00OOOO00O0O0OO for O0O00OOOO00O0O0OO in OOOOOO0O000O0OO00 if O00O00O0000OO0000 .get ()in O0O00OOOO00O0O0OO ],OO0OO0O0OO0O0OO00 ,OO000O000000O000O ,"更多控制线分位数"))#line:762
    OO0O0OO00000O00O0 .pack (side =LEFT ,anchor ="ne")#line:763
    O0OO000O00O000OO0 =Button (O000000O00000O000 ,text ="去除标记",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_risk_plot (O0O0O00O00OO00OOO ,O000O0O0000OO0000 ,OOOOOO0O000O0OO00 ,OO0OO0O0OO0O0OO00 ,0 ))#line:772
    O0OO000O00O000OO0 .pack (side =LEFT ,anchor ="ne")#line:774
    O00OOO0O00O00O0O0 .draw ()#line:775
def DRAW_make_one (OOO0OO0000000000O ,O0O000OO0O0O0O000 ,OO000O000O0000000 ,OOO000O000OOO0OO0 ,OO00O0OO00O00OOOO ):#line:779
    ""#line:780
    warnings .filterwarnings ("ignore")#line:781
    OO000OOOOO0OOOO0O =Toplevel ()#line:782
    OO000OOOOO0OOOO0O .title (O0O000OO0O0O0O000 )#line:783
    O0OO0OO0O0O0OOO0O =ttk .Frame (OO000OOOOO0OOOO0O ,height =20 )#line:784
    O0OO0OO0O0O0OOO0O .pack (side =TOP )#line:785
    OOO00000O0OO0OO00 =Figure (figsize =(12 ,6 ),dpi =100 )#line:787
    O00OO0OO0O0OO0OOO =FigureCanvasTkAgg (OOO00000O0OO0OO00 ,master =OO000OOOOO0OOOO0O )#line:788
    O00OO0OO0O0OO0OOO .draw ()#line:789
    O00OO0OO0O0OO0OOO .get_tk_widget ().pack (expand =1 )#line:790
    OOOO0OO0O0O0OO00O =OOO00000O0OO0OO00 .add_subplot (111 )#line:791
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:793
    plt .rcParams ['axes.unicode_minus']=False #line:794
    O00OOOOO0O0OOO000 =NavigationToolbar2Tk (O00OO0OO0O0OO0OOO ,OO000OOOOO0OOOO0O )#line:796
    O00OOOOO0O0OOO000 .update ()#line:797
    O00OO0OO0O0OO0OOO .get_tk_widget ().pack ()#line:799
    try :#line:802
        OO00O0OOO0OO0O000 =OOO0OO0000000000O .columns #line:803
    except :#line:805
        O0OOOOOO0000O0000 =eval (OOO0OO0000000000O )#line:806
        O0OOOOOO0000O0000 =pd .DataFrame .from_dict (O0OOOOOO0000O0000 ,orient =OO000O000O0000000 ,columns =[OOO000O000OOO0OO0 ]).reset_index ()#line:809
        OOO0OO0000000000O =O0OOOOOO0000O0000 .sort_values (by =OOO000O000OOO0OO0 ,ascending =[False ],na_position ="last")#line:810
    if ("日期"in O0O000OO0O0O0O000 or "时间"in O0O000OO0O0O0O000 or "季度"in O0O000OO0O0O0O000 )and "饼图"not in OO00O0OO00O00OOOO :#line:814
        OOO0OO0000000000O [OO000O000O0000000 ]=pd .to_datetime (OOO0OO0000000000O [OO000O000O0000000 ],format ="%Y/%m/%d").dt .date #line:815
        OOO0OO0000000000O =OOO0OO0000000000O .sort_values (by =OO000O000O0000000 ,ascending =[True ],na_position ="last")#line:816
    elif "批号"in O0O000OO0O0O0O000 :#line:817
        OOO0OO0000000000O [OO000O000O0000000 ]=OOO0OO0000000000O [OO000O000O0000000 ].astype (str )#line:818
        OOO0OO0000000000O =OOO0OO0000000000O .sort_values (by =OO000O000O0000000 ,ascending =[True ],na_position ="last")#line:819
        OOOO0OO0O0O0OO00O .set_xticklabels (OOO0OO0000000000O [OO000O000O0000000 ],rotation =-90 ,fontsize =8 )#line:820
    else :#line:821
        OOO0OO0000000000O [OO000O000O0000000 ]=OOO0OO0000000000O [OO000O000O0000000 ].astype (str )#line:822
        OOOO0OO0O0O0OO00O .set_xticklabels (OOO0OO0000000000O [OO000O000O0000000 ],rotation =-90 ,fontsize =8 )#line:823
    OOO0OOOO00O0000O0 =OOO0OO0000000000O [OOO000O000OOO0OO0 ]#line:825
    OOO0OOOO0OO00OO0O =range (0 ,len (OOO0OOOO00O0000O0 ),1 )#line:826
    OOOO0OO0O0O0OO00O .set_title (O0O000OO0O0O0O000 )#line:828
    if OO00O0OO00O00OOOO =="柱状图":#line:832
        OOOO0OO0O0O0OO00O .bar (x =OOO0OO0000000000O [OO000O000O0000000 ],height =OOO0OOOO00O0000O0 ,width =0.2 ,color ="#87CEFA")#line:833
    elif OO00O0OO00O00OOOO =="饼图":#line:834
        OOOO0OO0O0O0OO00O .pie (x =OOO0OOOO00O0000O0 ,labels =OOO0OO0000000000O [OO000O000O0000000 ],autopct ="%0.2f%%")#line:835
    elif OO00O0OO00O00OOOO =="折线图":#line:836
        OOOO0OO0O0O0OO00O .plot (OOO0OO0000000000O [OO000O000O0000000 ],OOO0OOOO00O0000O0 ,lw =0.5 ,ls ='-',c ="r",alpha =0.5 )#line:837
    elif "托帕斯图"in str (OO00O0OO00O00OOOO ):#line:839
        O0OOO00OO000O00O0 =OOO0OO0000000000O [OOO000O000OOO0OO0 ].fillna (0 )#line:840
        OOOO00OOOOO00OO0O =O0OOO00OO000O00O0 .cumsum ()/O0OOO00OO000O00O0 .sum ()*100 #line:844
        OOOO0OO0O0O0O000O =OOOO00OOOOO00OO0O [OOOO00OOOOO00OO0O >0.8 ].index [0 ]#line:846
        OO000OO0OOOO000OO =O0OOO00OO000O00O0 .index .tolist ().index (OOOO0OO0O0O0O000O )#line:847
        OOOO0OO0O0O0OO00O .bar (x =OOO0OO0000000000O [OO000O000O0000000 ],height =O0OOO00OO000O00O0 ,color ="C0",label =OOO000O000OOO0OO0 )#line:851
        OO00OOO0OO000O00O =OOOO0OO0O0O0OO00O .twinx ()#line:852
        OO00OOO0OO000O00O .plot (OOO0OO0000000000O [OO000O000O0000000 ],OOOO00OOOOO00OO0O ,color ="C1",alpha =0.6 ,label ="累计比例")#line:853
        OO00OOO0OO000O00O .yaxis .set_major_formatter (PercentFormatter ())#line:854
        OOOO0OO0O0O0OO00O .tick_params (axis ="y",colors ="C0")#line:859
        OO00OOO0OO000O00O .tick_params (axis ="y",colors ="C1")#line:860
        if "超级托帕斯图"in str (OO00O0OO00O00OOOO ):#line:863
            OO0OO0OO000000OO0 =re .compile (r'[(](.*?)[)]',re .S )#line:864
            O0OO00OOO0O0O0O00 =re .findall (OO0OO0OO000000OO0 ,OO00O0OO00O00OOOO )[0 ]#line:865
            OOOO0OO0O0O0OO00O .bar (x =OOO0OO0000000000O [OO000O000O0000000 ],height =OOO0OO0000000000O [O0OO00OOO0O0O0O00 ],color ="orangered",label =O0OO00OOO0O0O0O00 )#line:866
    OOO00000O0OO0OO00 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:868
    O000O0OOO0OO00000 =OOOO0OO0O0O0OO00O .get_position ()#line:869
    OOOO0OO0O0O0OO00O .set_position ([O000O0OOO0OO00000 .x0 ,O000O0OOO0OO00000 .y0 ,O000O0OOO0OO00000 .width *0.7 ,O000O0OOO0OO00000 .height ])#line:870
    OOOO0OO0O0O0OO00O .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:871
    O00OO0OO0O0OO0OOO .draw ()#line:874
    if len (OOO0OOOO00O0000O0 )<=20 and OO00O0OO00O00OOOO !="饼图":#line:877
        for O0OOOOOOO0O000O00 ,OO0OOO00O0O0O0O00 in zip (OOO0OOOO0OO00OO0O ,OOO0OOOO00O0000O0 ):#line:878
            OOO0OO0OOO00O0OO0 =str (OO0OOO00O0O0O0O00 )#line:879
            O00OOOOOO00O0O000 =(O0OOOOOOO0O000O00 ,OO0OOO00O0O0O0O00 +0.3 )#line:880
            OOOO0OO0O0O0OO00O .annotate (OOO0OO0OOO00O0OO0 ,xy =O00OOOOOO00O0O000 ,fontsize =8 ,color ="black",ha ="center",va ="baseline")#line:881
    O00OOO0O00O0O000O =Button (O0OO0OO0O0O0OOO0O ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OOO0OO0000000000O ),)#line:891
    O00OOO0O00O0O000O .pack (side =RIGHT )#line:892
    O0O00OOO0O00O0O00 =Button (O0OO0OO0O0O0OOO0O ,relief =GROOVE ,text ="查看原始数据",command =lambda :TOOLS_view_dict (OOO0OO0000000000O ,0 ))#line:896
    O0O00OOO0O00O0O00 .pack (side =RIGHT )#line:897
    OOOO00000O000O00O =Button (O0OO0OO0O0O0OOO0O ,relief =GROOVE ,text ="饼图",command =lambda :DRAW_make_one (OOO0OO0000000000O ,O0O000OO0O0O0O000 ,OO000O000O0000000 ,OOO000O000OOO0OO0 ,"饼图"),)#line:905
    OOOO00000O000O00O .pack (side =LEFT )#line:906
    OOOO00000O000O00O =Button (O0OO0OO0O0O0OOO0O ,relief =GROOVE ,text ="柱状图",command =lambda :DRAW_make_one (OOO0OO0000000000O ,O0O000OO0O0O0O000 ,OO000O000O0000000 ,OOO000O000OOO0OO0 ,"柱状图"),)#line:913
    OOOO00000O000O00O .pack (side =LEFT )#line:914
    OOOO00000O000O00O =Button (O0OO0OO0O0O0OOO0O ,relief =GROOVE ,text ="折线图",command =lambda :DRAW_make_one (OOO0OO0000000000O ,O0O000OO0O0O0O000 ,OO000O000O0000000 ,OOO000O000OOO0OO0 ,"折线图"),)#line:920
    OOOO00000O000O00O .pack (side =LEFT )#line:921
    OOOO00000O000O00O =Button (O0OO0OO0O0O0OOO0O ,relief =GROOVE ,text ="托帕斯图",command =lambda :DRAW_make_one (OOO0OO0000000000O ,O0O000OO0O0O0O000 ,OO000O000O0000000 ,OOO000O000OOO0OO0 ,"托帕斯图"),)#line:928
    OOOO00000O000O00O .pack (side =LEFT )#line:929
def DRAW_make_mutibar (OO0O00OO000OOOOOO ,O000O0000OOOO00OO ,O00OO0OOOO0OOO0OO ,OOOOO000OO00000OO ,O0OOOOOOOOOO0OO00 ,OOO0OO0000O0OOO00 ,OO0O000000O0OO00O ):#line:930
    ""#line:931
    O0OOO0OO0000O000O =Toplevel ()#line:932
    O0OOO0OO0000O000O .title (OO0O000000O0OO00O )#line:933
    O00OOOO00O00O0O0O =ttk .Frame (O0OOO0OO0000O000O ,height =20 )#line:934
    O00OOOO00O00O0O0O .pack (side =TOP )#line:935
    O0OO00O000O00OOO0 =0.2 #line:937
    O0O0O0O00O0OOO0O0 =Figure (figsize =(12 ,6 ),dpi =100 )#line:938
    OO00O0O000OOOO00O =FigureCanvasTkAgg (O0O0O0O00O0OOO0O0 ,master =O0OOO0OO0000O000O )#line:939
    OO00O0O000OOOO00O .draw ()#line:940
    OO00O0O000OOOO00O .get_tk_widget ().pack (expand =1 )#line:941
    O000OOO0OO0O0OOO0 =O0O0O0O00O0OOO0O0 .add_subplot (111 )#line:942
    plt .rcParams ["font.sans-serif"]=["SimHei"]#line:944
    plt .rcParams ['axes.unicode_minus']=False #line:945
    O0O0OO000000OOO00 =NavigationToolbar2Tk (OO00O0O000OOOO00O ,O0OOO0OO0000O000O )#line:947
    O0O0OO000000OOO00 .update ()#line:948
    OO00O0O000OOOO00O .get_tk_widget ().pack ()#line:950
    O000O0000OOOO00OO =OO0O00OO000OOOOOO [O000O0000OOOO00OO ]#line:951
    O00OO0OOOO0OOO0OO =OO0O00OO000OOOOOO [O00OO0OOOO0OOO0OO ]#line:952
    OOOOO000OO00000OO =OO0O00OO000OOOOOO [OOOOO000OO00000OO ]#line:953
    O0OO0OOO0000O0OO0 =range (0 ,len (O000O0000OOOO00OO ),1 )#line:955
    O000OOO0OO0O0OOO0 .set_xticklabels (OOOOO000OO00000OO ,rotation =-90 ,fontsize =8 )#line:956
    O000OOO0OO0O0OOO0 .bar (O0OO0OOO0000O0OO0 ,O000O0000OOOO00OO ,align ="center",tick_label =OOOOO000OO00000OO ,label =O0OOOOOOOOOO0OO00 )#line:959
    O000OOO0OO0O0OOO0 .bar (O0OO0OOO0000O0OO0 ,O00OO0OOOO0OOO0OO ,align ="center",label =OOO0OO0000O0OOO00 )#line:962
    O000OOO0OO0O0OOO0 .set_title (OO0O000000O0OO00O )#line:963
    O000OOO0OO0O0OOO0 .set_xlabel ("项")#line:964
    O000OOO0OO0O0OOO0 .set_ylabel ("数量")#line:965
    O0O0O0O00O0OOO0O0 .tight_layout (pad =0.4 ,w_pad =3.0 ,h_pad =3.0 )#line:967
    O00OO0OOO0O0O0O00 =O000OOO0OO0O0OOO0 .get_position ()#line:968
    O000OOO0OO0O0OOO0 .set_position ([O00OO0OOO0O0O0O00 .x0 ,O00OO0OOO0O0O0O00 .y0 ,O00OO0OOO0O0O0O00 .width *0.7 ,O00OO0OOO0O0O0O00 .height ])#line:969
    O000OOO0OO0O0OOO0 .legend (loc =2 ,bbox_to_anchor =(1.05 ,1.0 ),fontsize =10 ,borderaxespad =0.0 )#line:970
    OO00O0O000OOOO00O .draw ()#line:972
    OOOO00OO00O0OOO00 =Button (O00OOOO00O00O0O0O ,relief =GROOVE ,activebackground ="green",text ="保存原始数据",command =lambda :TOOLS_save_dict (OO0O00OO000OOOOOO ),)#line:979
    OOOO00OO00O0OOO00 .pack (side =RIGHT )#line:980
def SMALL_last_non_null_value (O00OOOO00OO0OOOOO ,OOO0000OOOOO0O000 ,OOO0O0OOO00OOO0O0 ):#line:985
    ""#line:996
    def OOO0000OOOO0000O0 (OOO0000O000000000 ):#line:999
        for OO00OO0O0OO000000 in reversed (OOO0000OOOOO0O000 ):#line:1000
            if pd .notna (OOO0000O000000000 [OO00OO0O0OO000000 ]):#line:1001
                return OOO0000O000000000 [OO00OO0O0OO000000 ]#line:1002
        return np .nan #line:1003
    O00OOOO00OO0OOOOO [OOO0O0OOO00OOO0O0 ]=O00OOOO00OO0OOOOO .apply (OOO0000OOOO0000O0 ,axis =1 )#line:1006
    return O00OOOO00OO0OOOOO #line:1008
def CLEAN_hzp (O0O00O0O00O0OO00O ):#line:1010
    ""#line:1011
    if "报告编码"not in O0O00O0O00O0OO00O .columns :#line:1012
            O0O00O0O00O0OO00O ["特殊化妆品注册证书编号/普通化妆品备案编号"]=O0O00O0O00O0OO00O ["特殊化妆品注册证书编号/普通化妆品备案编号"].fillna ("-未填写-")#line:1013
            O0O00O0O00O0OO00O ["省级评价结果"]=O0O00O0O00O0OO00O ["省级评价结果"].fillna ("-未填写-")#line:1014
            O0O00O0O00O0OO00O ["生产企业"]=O0O00O0O00O0OO00O ["生产企业"].fillna ("-未填写-")#line:1015
            O0O00O0O00O0OO00O ["提交人"]="不适用"#line:1016
            O0O00O0O00O0OO00O ["医疗机构类别"]="不适用"#line:1017
            O0O00O0O00O0OO00O ["经营企业或使用单位"]="不适用"#line:1018
            O0O00O0O00O0OO00O ["报告状态"]="报告单位评价"#line:1019
            O0O00O0O00O0OO00O ["所属地区"]="不适用"#line:1020
            O0O00O0O00O0OO00O ["医院名称"]="不适用"#line:1021
            O0O00O0O00O0OO00O ["报告地区名称"]="不适用"#line:1022
            O0O00O0O00O0OO00O ["提交人"]="不适用"#line:1023
            O0O00O0O00O0OO00O ["型号"]=O0O00O0O00O0OO00O ["化妆品分类"]#line:1024
            O0O00O0O00O0OO00O ["关联性评价"]=O0O00O0O00O0OO00O ["上报单位评价结果"]#line:1025
            O0O00O0O00O0OO00O ["规格"]="不适用"#line:1026
            O0O00O0O00O0OO00O ["器械故障表现"]=O0O00O0O00O0OO00O ["初步判断"]#line:1027
            O0O00O0O00O0OO00O ["伤害表现"]=O0O00O0O00O0OO00O ["自觉症状"]+O0O00O0O00O0OO00O ["皮损部位"]+O0O00O0O00O0OO00O ["皮损形态"]#line:1028
            O0O00O0O00O0OO00O ["事件原因分析"]="不适用"#line:1029
            O0O00O0O00O0OO00O ["事件原因分析描述"]="不适用"#line:1030
            O0O00O0O00O0OO00O ["调查情况"]="不适用"#line:1031
            O0O00O0O00O0OO00O ["具体控制措施"]="不适用"#line:1032
            O0O00O0O00O0OO00O ["未采取控制措施原因"]="不适用"#line:1033
            O0O00O0O00O0OO00O ["报告地区名称"]="不适用"#line:1034
            O0O00O0O00O0OO00O ["上报单位所属地区"]="不适用"#line:1035
            O0O00O0O00O0OO00O ["持有人报告状态"]="不适用"#line:1036
            O0O00O0O00O0OO00O ["年龄类型"]="岁"#line:1037
            O0O00O0O00O0OO00O ["经营企业使用单位报告状态"]="不适用"#line:1038
            O0O00O0O00O0OO00O ["产品归属"]="化妆品"#line:1039
            O0O00O0O00O0OO00O ["管理类别"]="不适用"#line:1040
            O0O00O0O00O0OO00O ["超时标记"]="不适用"#line:1041
            O0O00O0O00O0OO00O =O0O00O0O00O0OO00O .rename (columns ={"报告表编号":"报告编码","报告类型":"伤害","报告地区":"监测机构","报告单位名称":"单位名称","患者/消费者姓名":"姓名","不良反应发生日期":"事件发生日期","过程描述补充说明":"使用过程","化妆品名称":"产品名称","化妆品分类":"产品类别","生产企业":"上市许可持有人名称","生产批号":"产品批号","特殊化妆品注册证书编号/普通化妆品备案编号":"注册证编号/曾用注册证编号",})#line:1060
            O0O00O0O00O0OO00O ["时隔"]=pd .to_datetime (O0O00O0O00O0OO00O ["事件发生日期"])-pd .to_datetime (O0O00O0O00O0OO00O ["开始使用日期"])#line:1061
            O0O00O0O00O0OO00O ["时隔"]=O0O00O0O00O0OO00O ["时隔"].astype (str )#line:1062
            O0O00O0O00O0OO00O .loc [(O0O00O0O00O0OO00O ["省级评价结果"]!="-未填写-"),"有效报告"]=1 #line:1063
            O0O00O0O00O0OO00O ["伤害"]=O0O00O0O00O0OO00O ["伤害"].str .replace ("严重","严重伤害",regex =False )#line:1064
            try :#line:1065
	            O0O00O0O00O0OO00O =TOOL_guizheng (O0O00O0O00O0OO00O ,4 ,True )#line:1066
            except :#line:1067
                pass #line:1068
            return O0O00O0O00O0OO00O #line:1069
def CLEAN_yp (O0OOO0OOO0OO00OO0 ):#line:1074
    ""#line:1075
    if "报告编码"not in O0OOO0OOO0OO00OO0 .columns :#line:1076
        if "反馈码"in O0OOO0OOO0OO00OO0 .columns and "报告表编码"not in O0OOO0OOO0OO00OO0 .columns :#line:1078
            O0OOO0OOO0OO00OO0 ["提交人"]="不适用"#line:1080
            O0OOO0OOO0OO00OO0 ["经营企业或使用单位"]="不适用"#line:1081
            O0OOO0OOO0OO00OO0 ["报告状态"]="报告单位评价"#line:1082
            O0OOO0OOO0OO00OO0 ["所属地区"]="不适用"#line:1083
            O0OOO0OOO0OO00OO0 ["产品类别"]="无源"#line:1084
            O0OOO0OOO0OO00OO0 ["医院名称"]="不适用"#line:1085
            O0OOO0OOO0OO00OO0 ["报告地区名称"]="不适用"#line:1086
            O0OOO0OOO0OO00OO0 ["提交人"]="不适用"#line:1087
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"反馈码":"报告表编码","序号":"药品序号","新的":"报告类型-新的","报告类型":"报告类型-严重程度","用药-日数":"用法-日","用药-次数":"用法-次",})#line:1100
        if "唯一标识"not in O0OOO0OOO0OO00OO0 .columns :#line:1105
            O0OOO0OOO0OO00OO0 ["报告编码"]=O0OOO0OOO0OO00OO0 ["报告表编码"].astype (str )+O0OOO0OOO0OO00OO0 ["患者姓名"].astype (str )#line:1106
        if "唯一标识"in O0OOO0OOO0OO00OO0 .columns :#line:1107
            O0OOO0OOO0OO00OO0 ["唯一标识"]=O0OOO0OOO0OO00OO0 ["唯一标识"].astype (str )#line:1108
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"唯一标识":"报告编码"})#line:1109
        if "医疗机构类别"not in O0OOO0OOO0OO00OO0 .columns :#line:1110
            O0OOO0OOO0OO00OO0 ["医疗机构类别"]="医疗机构"#line:1111
            O0OOO0OOO0OO00OO0 ["经营企业使用单位报告状态"]="已提交"#line:1112
        try :#line:1113
            O0OOO0OOO0OO00OO0 ["年龄和单位"]=O0OOO0OOO0OO00OO0 ["年龄"].astype (str )+O0OOO0OOO0OO00OO0 ["年龄单位"]#line:1114
        except :#line:1115
            O0OOO0OOO0OO00OO0 ["年龄和单位"]=O0OOO0OOO0OO00OO0 ["年龄"].astype (str )+O0OOO0OOO0OO00OO0 ["年龄类型"]#line:1116
        O0OOO0OOO0OO00OO0 .loc [(O0OOO0OOO0OO00OO0 ["报告类型-新的"]=="新的"),"管理类别"]="Ⅲ类"#line:1117
        O0OOO0OOO0OO00OO0 .loc [(O0OOO0OOO0OO00OO0 ["报告类型-严重程度"]=="严重"),"管理类别"]="Ⅲ类"#line:1118
        text .insert (END ,"剔除已删除报告和重复报告...")#line:1119
        if "删除标识"in O0OOO0OOO0OO00OO0 .columns :#line:1120
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 [(O0OOO0OOO0OO00OO0 ["删除标识"]!="删除")]#line:1121
        if "重复报告"in O0OOO0OOO0OO00OO0 .columns :#line:1122
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 [(O0OOO0OOO0OO00OO0 ["重复报告"]!="重复报告")]#line:1123
        O0OOO0OOO0OO00OO0 ["报告类型-新的"]=O0OOO0OOO0OO00OO0 ["报告类型-新的"].fillna (" ")#line:1126
        O0OOO0OOO0OO00OO0 .loc [(O0OOO0OOO0OO00OO0 ["报告类型-严重程度"]=="严重"),"伤害"]="严重伤害"#line:1127
        O0OOO0OOO0OO00OO0 ["伤害"]=O0OOO0OOO0OO00OO0 ["伤害"].fillna ("所有一般")#line:1128
        O0OOO0OOO0OO00OO0 ["伤害PSUR"]=O0OOO0OOO0OO00OO0 ["报告类型-新的"].astype (str )+O0OOO0OOO0OO00OO0 ["报告类型-严重程度"].astype (str )#line:1129
        O0OOO0OOO0OO00OO0 ["用量用量单位"]=O0OOO0OOO0OO00OO0 ["用量"].astype (str )+O0OOO0OOO0OO00OO0 ["用量单位"].astype (str )#line:1130
        O0OOO0OOO0OO00OO0 ["规格"]="不适用"#line:1132
        O0OOO0OOO0OO00OO0 ["事件原因分析"]="不适用"#line:1133
        O0OOO0OOO0OO00OO0 ["事件原因分析描述"]="不适用"#line:1134
        O0OOO0OOO0OO00OO0 ["初步处置情况"]="不适用"#line:1135
        O0OOO0OOO0OO00OO0 ["伤害表现"]=O0OOO0OOO0OO00OO0 ["不良反应名称"]#line:1136
        O0OOO0OOO0OO00OO0 ["产品类别"]="无源"#line:1137
        O0OOO0OOO0OO00OO0 ["调查情况"]="不适用"#line:1138
        O0OOO0OOO0OO00OO0 ["具体控制措施"]="不适用"#line:1139
        O0OOO0OOO0OO00OO0 ["上报单位所属地区"]=O0OOO0OOO0OO00OO0 ["报告地区名称"]#line:1140
        O0OOO0OOO0OO00OO0 ["注册证编号/曾用注册证编号"]=O0OOO0OOO0OO00OO0 ["批准文号"]#line:1143
        O0OOO0OOO0OO00OO0 ["器械故障表现"]=O0OOO0OOO0OO00OO0 ["不良反应名称"]#line:1144
        O0OOO0OOO0OO00OO0 ["型号"]=O0OOO0OOO0OO00OO0 ["剂型"]#line:1145
        O0OOO0OOO0OO00OO0 ["未采取控制措施原因"]="不适用"#line:1148
        O0OOO0OOO0OO00OO0 ["报告单位评价"]=O0OOO0OOO0OO00OO0 ["报告类型-新的"].astype (str )+O0OOO0OOO0OO00OO0 ["报告类型-严重程度"].astype (str )#line:1149
        O0OOO0OOO0OO00OO0 .loc [(O0OOO0OOO0OO00OO0 ["报告类型-新的"]=="新的"),"持有人报告状态"]="待评价"#line:1150
        O0OOO0OOO0OO00OO0 ["用法temp日"]="日"#line:1151
        O0OOO0OOO0OO00OO0 ["用法temp次"]="次"#line:1152
        O0OOO0OOO0OO00OO0 ["用药频率"]=(O0OOO0OOO0OO00OO0 ["用法-日"].astype (str )+O0OOO0OOO0OO00OO0 ["用法temp日"]+O0OOO0OOO0OO00OO0 ["用法-次"].astype (str )+O0OOO0OOO0OO00OO0 ["用法temp次"])#line:1158
        try :#line:1159
            O0OOO0OOO0OO00OO0 ["相关疾病信息[疾病名称]-术语"]=O0OOO0OOO0OO00OO0 ["原患疾病"]#line:1160
            O0OOO0OOO0OO00OO0 ["治疗适应症-术语"]=O0OOO0OOO0OO00OO0 ["用药原因"]#line:1161
        except :#line:1162
            pass #line:1163
        try :#line:1165
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"提交日期":"报告日期"})#line:1166
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"提交人":"报告人"})#line:1167
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"报告状态":"持有人报告状态"})#line:1168
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"所属地区":"使用单位、经营企业所属监测机构"})#line:1169
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"医院名称":"单位名称"})#line:1170
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"通用名称":"产品名称"})#line:1172
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"生产厂家":"上市许可持有人名称"})#line:1173
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"不良反应发生时间":"事件发生日期"})#line:1174
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"不良反应过程描述":"使用过程"})#line:1176
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"生产批号":"产品批号"})#line:1177
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"报告地区名称":"使用单位、经营企业所属监测机构"})#line:1178
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"报告人评价":"关联性评价"})#line:1180
            O0OOO0OOO0OO00OO0 =O0OOO0OOO0OO00OO0 .rename (columns ={"年龄单位":"年龄类型"})#line:1181
        except :#line:1182
            text .insert (END ,"数据规整失败。")#line:1183
            return 0 #line:1184
        O0OOO0OOO0OO00OO0 ['报告日期']=O0OOO0OOO0OO00OO0 ['报告日期'].str .strip ()#line:1187
        O0OOO0OOO0OO00OO0 ['事件发生日期']=O0OOO0OOO0OO00OO0 ['事件发生日期'].str .strip ()#line:1188
        O0OOO0OOO0OO00OO0 ['用药开始时间']=O0OOO0OOO0OO00OO0 ['用药开始时间'].str .strip ()#line:1189
        return O0OOO0OOO0OO00OO0 #line:1191
    if "报告编码"in O0OOO0OOO0OO00OO0 .columns :#line:1192
        return O0OOO0OOO0OO00OO0 #line:1193
def CLEAN_qx (OOO0OOO00000O0OOO ):#line:1195
		""#line:1196
		if "使用单位、经营企业所属监测机构"not in OOO0OOO00000O0OOO .columns and "监测机构"not in OOO0OOO00000O0OOO .columns :#line:1198
			OOO0OOO00000O0OOO ["使用单位、经营企业所属监测机构"]="本地"#line:1199
		if "上市许可持有人名称"not in OOO0OOO00000O0OOO .columns :#line:1200
			OOO0OOO00000O0OOO ["上市许可持有人名称"]=OOO0OOO00000O0OOO ["单位名称"]#line:1201
		if "注册证编号/曾用注册证编号"not in OOO0OOO00000O0OOO .columns :#line:1202
			OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号"]#line:1203
		if "事件原因分析描述"not in OOO0OOO00000O0OOO .columns :#line:1204
			OOO0OOO00000O0OOO ["事件原因分析描述"]="  "#line:1205
		if "初步处置情况"not in OOO0OOO00000O0OOO .columns :#line:1206
			OOO0OOO00000O0OOO ["初步处置情况"]="  "#line:1207
		text .insert (END ,"\n正在执行格式规整和增加有关时间、年龄、性别等统计列...")#line:1210
		OOO0OOO00000O0OOO =OOO0OOO00000O0OOO .rename (columns ={"使用单位、经营企业所属监测机构":"监测机构"})#line:1211
		OOO0OOO00000O0OOO ["报告编码"]=OOO0OOO00000O0OOO ["报告编码"].astype ("str")#line:1212
		OOO0OOO00000O0OOO ["产品批号"]=OOO0OOO00000O0OOO ["产品批号"].astype ("str")#line:1213
		OOO0OOO00000O0OOO ["型号"]=OOO0OOO00000O0OOO ["型号"].astype ("str")#line:1214
		OOO0OOO00000O0OOO ["规格"]=OOO0OOO00000O0OOO ["规格"].astype ("str")#line:1215
		OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"].str .replace ("(","（",regex =False )#line:1216
		OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"].str .replace (")","）",regex =False )#line:1217
		OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"].str .replace ("*","※",regex =False )#line:1218
		OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1219
		OOO0OOO00000O0OOO ["产品名称"]=OOO0OOO00000O0OOO ["产品名称"].str .replace ("*","※",regex =False )#line:1220
		OOO0OOO00000O0OOO ["产品批号"]=OOO0OOO00000O0OOO ["产品批号"].str .replace ("(","（",regex =False )#line:1221
		OOO0OOO00000O0OOO ["产品批号"]=OOO0OOO00000O0OOO ["产品批号"].str .replace (")","）",regex =False )#line:1222
		OOO0OOO00000O0OOO ["产品批号"]=OOO0OOO00000O0OOO ["产品批号"].str .replace ("*","※",regex =False )#line:1223
		OOO0OOO00000O0OOO ["上市许可持有人名称"]=OOO0OOO00000O0OOO ["上市许可持有人名称"].fillna ("-未填写-")#line:1227
		OOO0OOO00000O0OOO ["产品类别"]=OOO0OOO00000O0OOO ["产品类别"].fillna ("-未填写-")#line:1228
		OOO0OOO00000O0OOO ["产品名称"]=OOO0OOO00000O0OOO ["产品名称"].fillna ("-未填写-")#line:1229
		OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"].fillna ("-未填写-")#line:1230
		OOO0OOO00000O0OOO ["产品批号"]=OOO0OOO00000O0OOO ["产品批号"].fillna ("-未填写-")#line:1231
		OOO0OOO00000O0OOO ["型号"]=OOO0OOO00000O0OOO ["型号"].fillna ("-未填写-")#line:1232
		OOO0OOO00000O0OOO ["规格"]=OOO0OOO00000O0OOO ["规格"].fillna ("-未填写-")#line:1233
		OOO0OOO00000O0OOO ["伤害与评价"]=OOO0OOO00000O0OOO ["伤害"]+OOO0OOO00000O0OOO ["持有人报告状态"]#line:1236
		OOO0OOO00000O0OOO ["注册证备份"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]#line:1237
		OOO0OOO00000O0OOO ['报告日期']=pd .to_datetime (OOO0OOO00000O0OOO ['报告日期'],format ='%Y-%m-%d',errors ='coerce')#line:1240
		OOO0OOO00000O0OOO ['事件发生日期']=pd .to_datetime (OOO0OOO00000O0OOO ['事件发生日期'],format ='%Y-%m-%d',errors ='coerce')#line:1241
		OOO0OOO00000O0OOO ["报告月份"]=OOO0OOO00000O0OOO ["报告日期"].dt .to_period ("M").astype (str )#line:1243
		OOO0OOO00000O0OOO ["报告季度"]=OOO0OOO00000O0OOO ["报告日期"].dt .to_period ("Q").astype (str )#line:1244
		OOO0OOO00000O0OOO ["报告年份"]=OOO0OOO00000O0OOO ["报告日期"].dt .to_period ("Y").astype (str )#line:1245
		OOO0OOO00000O0OOO ["事件发生月份"]=OOO0OOO00000O0OOO ["事件发生日期"].dt .to_period ("M").astype (str )#line:1246
		OOO0OOO00000O0OOO ["事件发生季度"]=OOO0OOO00000O0OOO ["事件发生日期"].dt .to_period ("Q").astype (str )#line:1247
		OOO0OOO00000O0OOO ["事件发生年份"]=OOO0OOO00000O0OOO ["事件发生日期"].dt .to_period ("Y").astype (str )#line:1248
		if ini ["模式"]=="器械":#line:1252
			OOO0OOO00000O0OOO ['发现或获知日期']=pd .to_datetime (OOO0OOO00000O0OOO ['发现或获知日期'],format ='%Y-%m-%d',errors ='coerce')#line:1253
			OOO0OOO00000O0OOO ["时隔"]=pd .to_datetime (OOO0OOO00000O0OOO ["发现或获知日期"])-pd .to_datetime (OOO0OOO00000O0OOO ["事件发生日期"])#line:1254
			OOO0OOO00000O0OOO ["时隔"]=OOO0OOO00000O0OOO ["时隔"].astype (str )#line:1255
			OOO0OOO00000O0OOO ["报告时限"]=pd .to_datetime (OOO0OOO00000O0OOO ["报告日期"])-pd .to_datetime (OOO0OOO00000O0OOO ["发现或获知日期"])#line:1256
			OOO0OOO00000O0OOO ["报告时限"]=OOO0OOO00000O0OOO ["报告时限"].dt .days #line:1257
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>20 )&(OOO0OOO00000O0OOO ["伤害"]=="严重伤害"),"超时标记"]=1 #line:1258
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>30 )&(OOO0OOO00000O0OOO ["伤害"]=="其他"),"超时标记"]=0 #line:1259
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>7 )&(OOO0OOO00000O0OOO ["伤害"]=="死亡"),"超时标记"]=1 #line:1260
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["经营企业使用单位报告状态"]=="审核通过"),"有效报告"]=1 #line:1262
		if ini ["模式"]=="药品":#line:1265
			OOO0OOO00000O0OOO ['用药开始时间']=pd .to_datetime (OOO0OOO00000O0OOO ['用药开始时间'],format ='%Y-%m-%d',errors ='coerce')#line:1266
			OOO0OOO00000O0OOO ["时隔"]=pd .to_datetime (OOO0OOO00000O0OOO ["事件发生日期"])-pd .to_datetime (OOO0OOO00000O0OOO ["用药开始时间"])#line:1267
			OOO0OOO00000O0OOO ["时隔"]=OOO0OOO00000O0OOO ["时隔"].astype (str )#line:1268
			OOO0OOO00000O0OOO ["报告时限"]=pd .to_datetime (OOO0OOO00000O0OOO ["报告日期"])-pd .to_datetime (OOO0OOO00000O0OOO ["事件发生日期"])#line:1269
			OOO0OOO00000O0OOO ["报告时限"]=OOO0OOO00000O0OOO ["报告时限"].dt .days #line:1270
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>15 )&(OOO0OOO00000O0OOO ["报告类型-严重程度"]=="严重"),"超时标记"]=1 #line:1271
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>30 )&(OOO0OOO00000O0OOO ["报告类型-严重程度"]=="一般"),"超时标记"]=1 #line:1272
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>15 )&(OOO0OOO00000O0OOO ["报告类型-新的"]=="新的"),"超时标记"]=1 #line:1273
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["报告时限"]>1 )&(OOO0OOO00000O0OOO ["报告类型-严重程度"]=="死亡"),"超时标记"]=1 #line:1274
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["评价状态"]!="未评价"),"有效报告"]=1 #line:1276
		OOO0OOO00000O0OOO .loc [((OOO0OOO00000O0OOO ["年龄"]=="未填写")|OOO0OOO00000O0OOO ["年龄"].isnull ()),"年龄"]=-1 #line:1278
		OOO0OOO00000O0OOO ["年龄"]=OOO0OOO00000O0OOO ["年龄"].astype (float )#line:1279
		OOO0OOO00000O0OOO ["年龄"]=OOO0OOO00000O0OOO ["年龄"].fillna (-1 )#line:1280
		OOO0OOO00000O0OOO ["性别"]=OOO0OOO00000O0OOO ["性别"].fillna ("未填写")#line:1281
		OOO0OOO00000O0OOO ["年龄段"]="未填写"#line:1282
		try :#line:1283
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄类型"]=="月"),"年龄"]=OOO0OOO00000O0OOO ["年龄"].values /12 #line:1284
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄类型"]=="月"),"年龄类型"]="岁"#line:1285
		except :#line:1286
			pass #line:1287
		try :#line:1288
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄类型"]=="天"),"年龄"]=OOO0OOO00000O0OOO ["年龄"].values /365 #line:1289
			OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄类型"]=="天"),"年龄类型"]="岁"#line:1290
		except :#line:1291
			pass #line:1292
		OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄"].values <=4 ),"年龄段"]="0-婴幼儿（0-4）"#line:1293
		OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄"].values >=5 ),"年龄段"]="1-少儿（5-14）"#line:1294
		OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄"].values >=15 ),"年龄段"]="2-青壮年（15-44）"#line:1295
		OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄"].values >=45 ),"年龄段"]="3-中年期（45-64）"#line:1296
		OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄"].values >=65 ),"年龄段"]="4-老年期（≥65）"#line:1297
		OOO0OOO00000O0OOO .loc [(OOO0OOO00000O0OOO ["年龄"].values ==-1 ),"年龄段"]="未填写"#line:1298
		try :#line:1300
			OOO0OOO00000O0OOO =SMALL_last_non_null_value (OOO0OOO00000O0OOO ,["伤害","伤害.1"],"综合伤害")#line:1301
			OOO0OOO00000O0OOO =OOO0OOO00000O0OOO .rename (columns ={"伤害":"伤害（医院上报）"})#line:1302
			OOO0OOO00000O0OOO =OOO0OOO00000O0OOO .rename (columns ={"综合伤害":"伤害"})#line:1303
		except :#line:1304
			pass #line:1305
		OOO0OOO00000O0OOO ["规整后品类"]="N"#line:1307
		OOO0OOO00000O0OOO =TOOL_guizheng (OOO0OOO00000O0OOO ,2 ,True )#line:1308
		if ini ['模式']in ["器械"]:#line:1311
			OOO0OOO00000O0OOO =TOOL_guizheng (OOO0OOO00000O0OOO ,3 ,True )#line:1312
		OOO0OOO00000O0OOO =TOOL_guizheng (OOO0OOO00000O0OOO ,"课题",True )#line:1316
		try :#line:1318
			OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"]=OOO0OOO00000O0OOO ["注册证编号/曾用注册证编号"].fillna ("未填写")#line:1319
		except :#line:1320
			pass #line:1321
		OOO0OOO00000O0OOO ["数据清洗完成标记"]="是"#line:1323
		O0O000O00O0OO0O00 =OOO0OOO00000O0OOO .loc [:]#line:1324
		return OOO0OOO00000O0OOO #line:1325
def TOOLS_fileopen ():#line:1331
    ""#line:1332
    warnings .filterwarnings ('ignore')#line:1333
    O0OOOO0O0OOO0OOO0 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1334
    O0O0OO0O00O0O0OO0 =Useful_tools_openfiles (O0OOOO0O0OOO0OOO0 ,0 )#line:1335
    try :#line:1336
        O0O0OO0O00O0O0OO0 =O0O0OO0O00O0O0OO0 .loc [:,~O0O0OO0O00O0O0OO0 .columns .str .contains ("^Unnamed")]#line:1337
    except :#line:1338
        pass #line:1339
    ini ["模式"]="其他"#line:1341
    OO0OO00O00000O00O =O0O0OO0O00O0O0OO0 #line:1342
    TABLE_tree_Level_2 (OO0OO00O00000O00O ,0 ,OO0OO00O00000O00O )#line:1343
def TOOLS_pinzhong (O0000000OOO0O0O0O ):#line:1346
    ""#line:1347
    O0000000OOO0O0O0O ["患者姓名"]=O0000000OOO0O0O0O ["报告表编码"]#line:1348
    O0000000OOO0O0O0O ["用量"]=O0000000OOO0O0O0O ["用法用量"]#line:1349
    O0000000OOO0O0O0O ["评价状态"]=O0000000OOO0O0O0O ["报告单位评价"]#line:1350
    O0000000OOO0O0O0O ["用量单位"]=""#line:1351
    O0000000OOO0O0O0O ["单位名称"]="不适用"#line:1352
    O0000000OOO0O0O0O ["报告地区名称"]="不适用"#line:1353
    O0000000OOO0O0O0O ["用法-日"]="不适用"#line:1354
    O0000000OOO0O0O0O ["用法-次"]="不适用"#line:1355
    O0000000OOO0O0O0O ["不良反应发生时间"]=O0000000OOO0O0O0O ["不良反应发生时间"].str [0 :10 ]#line:1356
    O0000000OOO0O0O0O ["持有人报告状态"]="待评价"#line:1358
    O0000000OOO0O0O0O =O0000000OOO0O0O0O .rename (columns ={"是否非预期":"报告类型-新的","不良反应-术语":"不良反应名称","持有人/生产厂家":"上市许可持有人名称"})#line:1363
    return O0000000OOO0O0O0O #line:1364
def Useful_tools_openfiles (O0OO00OO00000000O ,OO00O00O0OOOOO0OO ):#line:1369
    ""#line:1370
    OO0O0O0O000OOO00O =[pd .read_excel (OO0OO0OO0O0000000 ,header =0 ,sheet_name =OO00O00O0OOOOO0OO )for OO0OO0OO0O0000000 in O0OO00OO00000000O ]#line:1371
    OOOO0OOOOO0OOOO0O =pd .concat (OO0O0O0O000OOO00O ,ignore_index =True ).drop_duplicates ()#line:1372
    return OOOO0OOOOO0OOOO0O #line:1373
def TOOLS_allfileopen ():#line:1375
    ""#line:1376
    global ori #line:1377
    global ini #line:1378
    global data #line:1379
    ini ["原始模式"]="否"#line:1380
    warnings .filterwarnings ('ignore')#line:1381
    O0OOOO0O00OO0O0OO =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:1383
    ori =Useful_tools_openfiles (O0OOOO0O00OO0O0OO ,0 )#line:1384
    try :#line:1388
        O000O0O00000OO0O0 =Useful_tools_openfiles (O0OOOO0O00OO0O0OO ,"报告信息")#line:1389
        if "是否非预期"in O000O0O00000OO0O0 .columns :#line:1390
            ori =TOOLS_pinzhong (O000O0O00000OO0O0 )#line:1391
    except :#line:1392
        pass #line:1393
    ini ["模式"]="其他"#line:1395
    try :#line:1397
        ori =Useful_tools_openfiles (O0OOOO0O00OO0O0OO ,"字典数据")#line:1398
        ini ["原始模式"]="是"#line:1399
        if "UDI"in ori .columns :#line:1400
            ini ["模式"]="器械"#line:1401
            data =ori #line:1402
        if "报告类型-新的"in ori .columns :#line:1403
            ini ["模式"]="药品"#line:1404
            data =ori #line:1405
        else :#line:1406
            ini ["模式"]="其他"#line:1407
    except :#line:1408
        pass #line:1409
    try :#line:1412
        ori =ori .loc [:,~ori .columns .str .contains ("^Unnamed")]#line:1413
    except :#line:1414
        pass #line:1415
    if "UDI"in ori .columns and ini ["原始模式"]!="是":#line:1419
        text .insert (END ,"识别出为器械报表,正在进行数据规整...")#line:1420
        ini ["模式"]="器械"#line:1421
        ori =CLEAN_qx (ori )#line:1422
        data =ori #line:1423
    if "报告类型-新的"in ori .columns and ini ["原始模式"]!="是":#line:1424
        text .insert (END ,"识别出为药品报表,正在进行数据规整...")#line:1425
        ini ["模式"]="药品"#line:1426
        ori =CLEAN_yp (ori )#line:1427
        ori =CLEAN_qx (ori )#line:1428
        data =ori #line:1429
    if "光斑贴试验"in ori .columns and ini ["原始模式"]!="是":#line:1430
        text .insert (END ,"识别出为化妆品报表,正在进行数据规整...")#line:1431
        ini ["模式"]="化妆品"#line:1432
        ori =CLEAN_hzp (ori )#line:1433
        ori =CLEAN_qx (ori )#line:1434
        data =ori #line:1435
    if ini ["模式"]=="其他":#line:1438
        text .insert (END ,"\n数据读取成功，行数："+str (len (ori )))#line:1439
        data =ori #line:1440
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1441
        try :#line:1442
            ini ["button"][0 ].pack_forget ()#line:1443
            ini ["button"][1 ].pack_forget ()#line:1444
            ini ["button"][2 ].pack_forget ()#line:1445
            ini ["button"][3 ].pack_forget ()#line:1446
            ini ["button"][4 ].pack_forget ()#line:1447
        except :#line:1448
            pass #line:1449
    else :#line:1451
        ini ["清洗后的文件"]=data #line:1452
        ini ["证号"]=Countall (data ).df_zhenghao ()#line:1453
        text .insert (END ,"\n数据读取成功，行数："+str (len (data )))#line:1454
        PROGRAM_Menubar (root ,data ,0 ,data )#line:1455
        try :#line:1456
            ini ["button"][0 ].pack_forget ()#line:1457
            ini ["button"][1 ].pack_forget ()#line:1458
            ini ["button"][2 ].pack_forget ()#line:1459
            ini ["button"][3 ].pack_forget ()#line:1460
            ini ["button"][4 ].pack_forget ()#line:1461
        except :#line:1462
            pass #line:1463
        O00O0O00O00OOOOOO =Button (frame0 ,text ="地市统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("市级监测机构"),1 ,ori ),)#line:1474
        O00O0O00O00OOOOOO .pack ()#line:1475
        OOO0O00000OO00000 =Button (frame0 ,text ="县区统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_org ("监测机构"),1 ,ori ),)#line:1488
        OOO0O00000OO00000 .pack ()#line:1489
        O0000O00000O00O0O =Button (frame0 ,text ="上报单位",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_user (),1 ,ori ),)#line:1502
        O0000O00000O00O0O .pack ()#line:1503
        OOOOO0000OOOOO0O0 =Button (frame0 ,text ="生产企业",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (data ).df_chiyouren (),1 ,ori ),)#line:1514
        OOOOO0000OOOOO0O0 .pack ()#line:1515
        OOOOO0O0OO00O0OO0 =Button (frame0 ,text ="产品统计",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ini ["证号"],1 ,ori ,ori ,"dfx_zhenghao"),)#line:1526
        OOOOO0O0OO00O0OO0 .pack ()#line:1527
        ini ["button"]=[O00O0O00O00OOOOOO ,OOO0O00000OO00000 ,O0000O00000O00O0O ,OOOOO0000OOOOO0O0 ,OOOOO0O0OO00O0OO0 ]#line:1528
    text .insert (END ,"\n")#line:1530
def TOOLS_sql (OO0O00O0OOOO0O00O ):#line:1532
    ""#line:1533
    warnings .filterwarnings ("ignore")#line:1534
    try :#line:1535
        OOOOOOOOO0O00OOOO =OO0O00O0OOOO0O00O .columns #line:1536
    except :#line:1537
        return 0 #line:1538
    def O0O00OO0OO0O0OO0O (OO0O0OO0OOOO0OOOO ):#line:1540
        try :#line:1541
            O0O0O0O0OO0OO0O0O =pd .read_sql_query (sqltext (OO0O0OO0OOOO0OOOO ),con =O00O000OO00OOOO00 )#line:1542
        except :#line:1543
            showinfo (title ="提示",message ="SQL语句有误。")#line:1544
            return 0 #line:1545
        try :#line:1546
            del O0O0O0O0OO0OO0O0O ["level_0"]#line:1547
        except :#line:1548
            pass #line:1549
        TABLE_tree_Level_2 (O0O0O0O0OO0OO0O0O ,1 ,OO0O00O0OOOO0O00O )#line:1550
    OO00O0O0O0OOO000O ='sqlite://'#line:1554
    OO00OOO00O000000O =create_engine (OO00O0O0O0OOO000O )#line:1555
    try :#line:1556
        OO0O00O0OOOO0O00O .to_sql ('data',con =OO00OOO00O000000O ,chunksize =10000 ,if_exists ='replace',index =True )#line:1557
    except :#line:1558
        showinfo (title ="提示",message ="不支持该表格。")#line:1559
        return 0 #line:1560
    O00O000OO00OOOO00 =OO00OOO00O000000O .connect ()#line:1562
    O0O0000O0O0OO00OO ="select * from data"#line:1563
    O000OOO0O0OO00O0O =Toplevel ()#line:1566
    O000OOO0O0OO00O0O .title ("SQL查询")#line:1567
    O000OOO0O0OO00O0O .geometry ("700x500")#line:1568
    O0OOOO0O00O0OO000 =ttk .Frame (O000OOO0O0OO00O0O ,width =700 ,height =20 )#line:1570
    O0OOOO0O00O0OO000 .pack (side =TOP )#line:1571
    O000OO0OOO000OOOO =ttk .Frame (O000OOO0O0OO00O0O ,width =700 ,height =20 )#line:1572
    O000OO0OOO000OOOO .pack (side =BOTTOM )#line:1573
    try :#line:1576
        O0OOOO0O00000O0OO =StringVar ()#line:1577
        O0OOOO0O00000O0OO .set ("select * from data WHERE 单位名称='佛山市第一人民医院'")#line:1578
        O0O00000000OOOO0O =Label (O0OOOO0O00O0OO000 ,text ="SQL查询",anchor ='w')#line:1580
        O0O00000000OOOO0O .pack (side =LEFT )#line:1581
        O00OO00O0O00OO00O =Label (O0OOOO0O00O0OO000 ,text ="检索：")#line:1582
        O0OO00OOOOOO000O0 =Button (O000OO0OOO000OOOO ,text ="执行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",width =700 ,command =lambda :O0O00OO0OO0O0OO0O (OO0O00000O000OOO0 .get ("1.0","end")),)#line:1596
        O0OO00OOOOOO000O0 .pack (side =LEFT )#line:1597
    except EE :#line:1600
        pass #line:1601
    OO00OOO0000OO00O0 =Scrollbar (O000OOO0O0OO00O0O )#line:1603
    OO0O00000O000OOO0 =Text (O000OOO0O0OO00O0O ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:1604
    OO00OOO0000OO00O0 .pack (side =RIGHT ,fill =Y )#line:1605
    OO0O00000O000OOO0 .pack ()#line:1606
    OO00OOO0000OO00O0 .config (command =OO0O00000O000OOO0 .yview )#line:1607
    OO0O00000O000OOO0 .config (yscrollcommand =OO00OOO0000OO00O0 .set )#line:1608
    def O0OO0OO0OO00O0O0O (event =None ):#line:1609
        OO0O00000O000OOO0 .event_generate ('<<Copy>>')#line:1610
    def OOO0OO00OO00OO0OO (event =None ):#line:1611
        OO0O00000O000OOO0 .event_generate ('<<Paste>>')#line:1612
    def OO00O0O0O00OO0O0O (OO0OOO0O0O0OOOO0O ,OOOO0O0OO0OOO000O ):#line:1613
         TOOLS_savetxt (OO0OOO0O0O0OOOO0O ,OOOO0O0OO0OOO000O ,1 )#line:1614
    OOO0O0OO0OO0OO000 =Menu (OO0O00000O000OOO0 ,tearoff =False ,)#line:1615
    OOO0O0OO0OO0OO000 .add_command (label ="复制",command =O0OO0OO0OO00O0O0O )#line:1616
    OOO0O0OO0OO0OO000 .add_command (label ="粘贴",command =OOO0OO00OO00OO0OO )#line:1617
    OOO0O0OO0OO0OO000 .add_command (label ="源文件列",command =lambda :PROGRAM_helper (OO0O00O0OOOO0O00O .columns .to_list ()))#line:1618
    def OO0OO000OOOO00OO0 (OO00O000000O0000O ):#line:1619
         OOO0O0OO0OO0OO000 .post (OO00O000000O0000O .x_root ,OO00O000000O0000O .y_root )#line:1620
    OO0O00000O000OOO0 .bind ("<Button-3>",OO0OO000OOOO00OO0 )#line:1621
    OO0O00000O000OOO0 .insert (END ,O0O0000O0O0OO00OO )#line:1625
def TOOLS_view_dict (OOOOOO00O0OO0O000 ,OOOOOO00O0O0000OO ):#line:1629
    ""#line:1630
    O0OO00O00OOO00O0O =Toplevel ()#line:1631
    O0OO00O00OOO00O0O .title ("查看数据")#line:1632
    O0OO00O00OOO00O0O .geometry ("700x500")#line:1633
    O0O00O00O00O0OO0O =Scrollbar (O0OO00O00OOO00O0O )#line:1635
    O0O0OOO0O0O00O0O0 =Text (O0OO00O00OOO00O0O ,height =100 ,width =150 )#line:1636
    O0O00O00O00O0OO0O .pack (side =RIGHT ,fill =Y )#line:1637
    O0O0OOO0O0O00O0O0 .pack ()#line:1638
    O0O00O00O00O0OO0O .config (command =O0O0OOO0O0O00O0O0 .yview )#line:1639
    O0O0OOO0O0O00O0O0 .config (yscrollcommand =O0O00O00O00O0OO0O .set )#line:1640
    if OOOOOO00O0O0000OO ==1 :#line:1641
        O0O0OOO0O0O00O0O0 .insert (END ,OOOOOO00O0OO0O000 )#line:1643
        O0O0OOO0O0O00O0O0 .insert (END ,"\n\n")#line:1644
        return 0 #line:1645
    for OO000OOOO0O0O0O0O in range (len (OOOOOO00O0OO0O000 )):#line:1646
        O0O0OOO0O0O00O0O0 .insert (END ,OOOOOO00O0OO0O000 .iloc [OO000OOOO0O0O0O0O ,0 ])#line:1647
        O0O0OOO0O0O00O0O0 .insert (END ,":")#line:1648
        O0O0OOO0O0O00O0O0 .insert (END ,OOOOOO00O0OO0O000 .iloc [OO000OOOO0O0O0O0O ,1 ])#line:1649
        O0O0OOO0O0O00O0O0 .insert (END ,"\n\n")#line:1650
def TOOLS_save_dict (OO0OO0O0OO000O0O0 ):#line:1652
    ""#line:1653
    O0OOO0O0OOO0O00O0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile ="排序后的原始数据",defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:1659
    try :#line:1660
        OO0OO0O0OO000O0O0 ["详细描述T"]=OO0OO0O0OO000O0O0 ["详细描述T"].astype (str )#line:1661
    except :#line:1662
        pass #line:1663
    try :#line:1664
        OO0OO0O0OO000O0O0 ["报告编码"]=OO0OO0O0OO000O0O0 ["报告编码"].astype (str )#line:1665
    except :#line:1666
        pass #line:1667
    OO00O0OOOO00OO00O =pd .ExcelWriter (O0OOO0O0OOO0O00O0 ,engine ="xlsxwriter")#line:1669
    OO0OO0O0OO000O0O0 .to_excel (OO00O0OOOO00OO00O ,sheet_name ="字典数据")#line:1670
    OO00O0OOOO00OO00O .close ()#line:1671
    showinfo (title ="提示",message ="文件写入成功。")#line:1672
def TOOLS_savetxt (OOOOOO0O0O000OOO0 ,OO000O0O000OO0000 ,OO0OO0000000O0000 ):#line:1674
	""#line:1675
	O0O000OOOO0O00O00 =open (OO000O0O000OO0000 ,"w",encoding ='utf-8')#line:1676
	O0O000OOOO0O00O00 .write (OOOOOO0O0O000OOO0 )#line:1677
	O0O000OOOO0O00O00 .flush ()#line:1679
	if OO0OO0000000O0000 ==1 :#line:1680
		showinfo (title ="提示信息",message ="保存成功。")#line:1681
def TOOLS_deep_view (OO00OO000O0O00O0O ,OO0O00OO0OO00OOO0 ,OOOO0000O00O00000 ,OO000O0OO00OOO0OO ):#line:1684
    ""#line:1685
    if OO000O0OO00OOO0OO ==0 :#line:1686
        try :#line:1687
            OO00OO000O0O00O0O [OO0O00OO0OO00OOO0 ]=OO00OO000O0O00O0O [OO0O00OO0OO00OOO0 ].fillna ("这个没有填写")#line:1688
        except :#line:1689
            pass #line:1690
        OOO0OOO000O0000O0 =OO00OO000O0O00O0O .groupby (OO0O00OO0OO00OOO0 ).agg (计数 =(OOOO0000O00O00000 [0 ],OOOO0000O00O00000 [1 ]))#line:1691
    if OO000O0OO00OOO0OO ==1 :#line:1692
            OOO0OOO000O0000O0 =pd .pivot_table (OO00OO000O0O00O0O ,index =OO0O00OO0OO00OOO0 [:-1 ],columns =OO0O00OO0OO00OOO0 [-1 ],values =[OOOO0000O00O00000 [0 ]],aggfunc ={OOOO0000O00O00000 [0 ]:OOOO0000O00O00000 [1 ]},fill_value ="0",margins =True ,dropna =False ,)#line:1703
            OOO0OOO000O0000O0 .columns =OOO0OOO000O0000O0 .columns .droplevel (0 )#line:1704
            OOO0OOO000O0000O0 =OOO0OOO000O0000O0 .rename (columns ={"All":"计数"})#line:1705
    if "日期"in OO0O00OO0OO00OOO0 or "时间"in OO0O00OO0OO00OOO0 or "季度"in OO0O00OO0OO00OOO0 :#line:1708
        OOO0OOO000O0000O0 =OOO0OOO000O0000O0 .sort_values ([OO0O00OO0OO00OOO0 ],ascending =False ,na_position ="last")#line:1711
    else :#line:1712
        OOO0OOO000O0000O0 =OOO0OOO000O0000O0 .sort_values (by =["计数"],ascending =False ,na_position ="last")#line:1716
    OOO0OOO000O0000O0 =OOO0OOO000O0000O0 .reset_index ()#line:1717
    OOO0OOO000O0000O0 ["构成比(%)"]=round (100 *OOO0OOO000O0000O0 ["计数"]/OOO0OOO000O0000O0 ["计数"].sum (),2 )#line:1718
    if "计数"in OOO0OOO000O0000O0 .columns and OO000O0OO00OOO0OO ==1 :#line:1719
        OOO0OOO000O0000O0 ["构成比(%)"]=OOO0OOO000O0000O0 ["构成比(%)"]*2 #line:1720
    if OO000O0OO00OOO0OO ==0 :#line:1721
        OOO0OOO000O0000O0 ["报表类型"]="dfx_deepview"+"_"+str (OO0O00OO0OO00OOO0 )#line:1722
    if OO000O0OO00OOO0OO ==1 :#line:1723
        OOO0OOO000O0000O0 ["报表类型"]="dfx_deepview"+"_"+str (OO0O00OO0OO00OOO0 [:-1 ])#line:1724
    return OOO0OOO000O0000O0 #line:1725
def TOOLS_easyreadT (O000000O0O0OO0OOO ):#line:1729
    ""#line:1730
    O000000O0O0OO0OOO ["#####分隔符#########"]="######################################################################"#line:1733
    O0O000O0O0OOOOO00 =O000000O0O0OO0OOO .stack (dropna =False )#line:1734
    O0O000O0O0OOOOO00 =pd .DataFrame (O0O000O0O0OOOOO00 ).reset_index ()#line:1735
    O0O000O0O0OOOOO00 .columns =["序号","条目","详细描述T"]#line:1736
    O0O000O0O0OOOOO00 ["逐条查看"]="逐条查看"#line:1737
    O0O000O0O0OOOOO00 ["报表类型"]="逐条查看"#line:1738
    return O0O000O0O0OOOOO00 #line:1739
def TOOLS_data_masking (O000O00OOO00OO00O ):#line:1741
    ""#line:1742
    from random import choices #line:1743
    from string import ascii_letters ,digits #line:1744
    O000O00OOO00OO00O =O000O00OOO00OO00O .reset_index (drop =True )#line:1746
    if "单位名称.1"in O000O00OOO00OO00O .columns :#line:1747
        O0O0O00OOOOOO0OOO ="器械"#line:1748
    else :#line:1749
        O0O0O00OOOOOO0OOO ="药品"#line:1750
    O0OOO0OOOOO0OO0OO =peizhidir +""+"0（范例）数据脱敏"+".xls"#line:1751
    try :#line:1752
        O00O0O0OOO0OO0O00 =pd .read_excel (O0OOO0OOOOO0OO0OO ,sheet_name =O0O0O00OOOOOO0OOO ,header =0 ,index_col =0 ).reset_index ()#line:1755
    except :#line:1756
        showinfo (title ="错误信息",message ="该功能需要配置文件才能使用！")#line:1757
        return 0 #line:1758
    OO0OOO00OO0O00O0O =0 #line:1759
    O00OOOOOOO0OOOOOO =len (O000O00OOO00OO00O )#line:1760
    O000O00OOO00OO00O ["abcd"]="□"#line:1761
    for O0000000OOOOOOO00 in O00O0O0OOO0OO0O00 ["要脱敏的列"]:#line:1762
        OO0OOO00OO0O00O0O =OO0OOO00OO0O00O0O +1 #line:1763
        PROGRAM_change_schedule (OO0OOO00OO0O00O0O ,O00OOOOOOO0OOOOOO )#line:1764
        text .insert (END ,"\n正在对以下列进行脱敏处理：")#line:1765
        text .see (END )#line:1766
        text .insert (END ,O0000000OOOOOOO00 )#line:1767
        try :#line:1768
            OO0O0O0O0OOO00OO0 =set (O000O00OOO00OO00O [O0000000OOOOOOO00 ])#line:1769
        except :#line:1770
            showinfo (title ="提示",message ="脱敏文件配置错误，请修改配置表。")#line:1771
            return 0 #line:1772
        O0OO00OO0OOOO0000 ={O0O00000O000O0O00 :"".join (choices (digits ,k =10 ))for O0O00000O000O0O00 in OO0O0O0O0OOO00OO0 }#line:1773
        O000O00OOO00OO00O [O0000000OOOOOOO00 ]=O000O00OOO00OO00O [O0000000OOOOOOO00 ].map (O0OO00OO0OOOO0000 )#line:1774
        O000O00OOO00OO00O [O0000000OOOOOOO00 ]=O000O00OOO00OO00O ["abcd"]+O000O00OOO00OO00O [O0000000OOOOOOO00 ].astype (str )#line:1775
    try :#line:1776
        PROGRAM_change_schedule (10 ,10 )#line:1777
        del O000O00OOO00OO00O ["abcd"]#line:1778
        OO0000OOOO0O000O0 =filedialog .asksaveasfilename (title =u"保存脱敏后的文件",initialfile ="脱敏后的文件",defaultextension ="xlsx",filetypes =[("Excel 工作簿","*.xlsx"),("Excel 97-2003 工作簿","*.xls")],)#line:1784
        OO0OO000000OOO0OO =pd .ExcelWriter (OO0000OOOO0O000O0 ,engine ="xlsxwriter")#line:1785
        O000O00OOO00OO00O .to_excel (OO0OO000000OOO0OO ,sheet_name ="sheet0")#line:1786
        OO0OO000000OOO0OO .close ()#line:1787
    except :#line:1788
        text .insert (END ,"\n文件未保存，但导入的数据已按要求脱敏。")#line:1789
    text .insert (END ,"\n脱敏操作完成。")#line:1790
    text .see (END )#line:1791
    return O000O00OOO00OO00O #line:1792
def TOOLS_get_new (OO0O0O0O00O000OO0 ,OO000OOO0000OO0O0 ):#line:1794
	""#line:1795
	def OOOOO000O000O00O0 (O0OO00OO00O0OO0O0 ):#line:1796
		""#line:1797
		O0OO00OO00O0OO0O0 =O0OO00OO00O0OO0O0 .drop_duplicates ("报告编码")#line:1798
		OOOOOOOO00000OO00 =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",O0OO00OO00O0OO0O0 ,1000 ))).replace ("Counter({","{")#line:1799
		OOOOOOOO00000OO00 =OOOOOOOO00000OO00 .replace ("})","}")#line:1800
		import ast #line:1801
		O0OO0OOOO0OO0OO0O =ast .literal_eval (OOOOOOOO00000OO00 )#line:1802
		O00OOOOO0000OO000 =TOOLS_easyreadT (pd .DataFrame ([O0OO0OOOO0OO0OO0O ]))#line:1803
		O00OOOOO0000OO000 =O00OOOOO0000OO000 .rename (columns ={"逐条查看":"ADR名称规整"})#line:1804
		return O00OOOOO0000OO000 #line:1805
	if OO000OOO0000OO0O0 =="证号":#line:1806
		root .attributes ("-topmost",True )#line:1807
		root .attributes ("-topmost",False )#line:1808
		O0OOO0O0O000O0000 =OO0O0O0O00O000OO0 .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1809
		O0OOO0OOO0OOOO00O =O0OOO0O0O000O0000 .drop_duplicates ("注册证编号/曾用注册证编号").copy ()#line:1810
		O0OOO0OOO0OOOO00O ["所有不良反应"]=""#line:1811
		O0OOO0OOO0OOOO00O ["关注建议"]=""#line:1812
		O0OOO0OOO0OOOO00O ["疑似新的"]=""#line:1813
		O0OOO0OOO0OOOO00O ["疑似旧的"]=""#line:1814
		O0OOO0OOO0OOOO00O ["疑似新的（高敏）"]=""#line:1815
		O0OOO0OOO0OOOO00O ["疑似旧的（高敏）"]=""#line:1816
		OOOO0000O00OOO000 =1 #line:1817
		O0O00OOO0000O00OO =int (len (O0OOO0OOO0OOOO00O ))#line:1818
		for OOO0OOOO0000O0O0O ,O0000O0O00O00OO00 in O0OOO0OOO0OOOO00O .iterrows ():#line:1819
			OOOO0O00O0OO0O0OO =OO0O0O0O00O000OO0 [(OO0O0O0O00O000OO0 ["注册证编号/曾用注册证编号"]==O0000O0O00O00OO00 ["注册证编号/曾用注册证编号"])]#line:1820
			O000O0OOOO0O0OOO0 =OOOO0O00O0OO0O0OO .loc [OOOO0O00O0OO0O0OO ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1821
			OOOOO0O00O000OOO0 =OOOO0O00O0OO0O0OO .loc [~OOOO0O00O0OO0O0OO ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1822
			OOOO0O0OO0O0O0OOO =OOOOO000O000O00O0 (O000O0OOOO0O0OOO0 )#line:1823
			O0000OOO00OOO0O0O =OOOOO000O000O00O0 (OOOOO0O00O000OOO0 )#line:1824
			OO000O00OOO00OO0O =OOOOO000O000O00O0 (OOOO0O00O0OO0O0OO )#line:1825
			PROGRAM_change_schedule (OOOO0000O00OOO000 ,O0O00OOO0000O00OO )#line:1826
			OOOO0000O00OOO000 =OOOO0000O00OOO000 +1 #line:1827
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in OO000O00OOO00OO0O .iterrows ():#line:1829
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]:#line:1830
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1831
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"所有不良反应"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"所有不良反应"]+O0OOOO0O0O00OOO0O #line:1832
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in O0000OOO00OOO0O0O .iterrows ():#line:1834
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]:#line:1835
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1836
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的"]+O0OOOO0O0O00OOO0O #line:1837
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]and int (OOO000O0OOO0OO000 ["详细描述T"])>=2 :#line:1839
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1840
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的（高敏）"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的（高敏）"]+O0OOOO0O0O00OOO0O #line:1841
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in OOOO0O0OO0O0O0OOO .iterrows ():#line:1843
				if str (OOO000O0OOO0OO000 ["条目"]).strip ()not in str (O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的"])and "分隔符"not in str (OOO000O0OOO0OO000 ["条目"]):#line:1844
					O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1845
					O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的"]+O0OOOO0O0O00OOO0O #line:1846
					if int (OOO000O0OOO0OO000 ["详细描述T"])>=3 :#line:1847
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]+"！"#line:1848
					if int (OOO000O0OOO0OO000 ["详细描述T"])>=5 :#line:1849
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]+"●"#line:1850
				if str (OOO000O0OOO0OO000 ["条目"]).strip ()not in str (O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的（高敏）"])and "分隔符"not in str (OOO000O0OOO0OO000 ["条目"])and int (OOO000O0OOO0OO000 ["详细描述T"])>=2 :#line:1852
					O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1853
					O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的（高敏）"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的（高敏）"]+O0OOOO0O0O00OOO0O #line:1854
		O0OOO0OOO0OOOO00O ["疑似新的"]="{"+O0OOO0OOO0OOOO00O ["疑似新的"]+"}"#line:1856
		O0OOO0OOO0OOOO00O ["疑似旧的"]="{"+O0OOO0OOO0OOOO00O ["疑似旧的"]+"}"#line:1857
		O0OOO0OOO0OOOO00O ["所有不良反应"]="{"+O0OOO0OOO0OOOO00O ["所有不良反应"]+"}"#line:1858
		O0OOO0OOO0OOOO00O ["疑似新的（高敏）"]="{"+O0OOO0OOO0OOOO00O ["疑似新的（高敏）"]+"}"#line:1859
		O0OOO0OOO0OOOO00O ["疑似旧的（高敏）"]="{"+O0OOO0OOO0OOOO00O ["疑似旧的（高敏）"]+"}"#line:1860
		O0OOO0OOO0OOOO00O =O0OOO0OOO0OOOO00O .rename (columns ={"器械待评价(药品新的报告比例)":"新的报告比例"})#line:1862
		O0OOO0OOO0OOOO00O =O0OOO0OOO0OOOO00O .rename (columns ={"严重伤害待评价比例(药品严重中新的比例)":"严重报告中新的比例"})#line:1863
		O0OOO0OOO0OOOO00O ["报表类型"]="dfx_zhenghao"#line:1864
		OOO0OO0O00OO0000O =pd .pivot_table (OO0O0O0O00O000OO0 ,values =["报告编码"],index =["注册证编号/曾用注册证编号"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1866
		OOO0OO0O00OO0000O .columns =OOO0OO0O00OO0000O .columns .droplevel (0 )#line:1867
		O0OOO0OOO0OOOO00O =pd .merge (O0OOO0OOO0OOOO00O ,OOO0OO0O00OO0000O .reset_index (),on =["注册证编号/曾用注册证编号"],how ="left")#line:1868
		TABLE_tree_Level_2 (O0OOO0OOO0OOOO00O .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,OO0O0O0O00O000OO0 )#line:1872
	if OO000OOO0000OO0O0 =="品种":#line:1873
		root .attributes ("-topmost",True )#line:1874
		root .attributes ("-topmost",False )#line:1875
		O0OOO0O0O000O0000 =OO0O0O0O00O000OO0 .groupby (["产品类别","产品名称"]).agg (计数 =("报告编码","nunique")).reset_index ()#line:1876
		O0OOO0OOO0OOOO00O =O0OOO0O0O000O0000 .drop_duplicates ("产品名称").copy ()#line:1877
		O0OOO0OOO0OOOO00O ["产品名称"]=O0OOO0OOO0OOOO00O ["产品名称"].str .replace ("*","",regex =False )#line:1878
		O0OOO0OOO0OOOO00O ["所有不良反应"]=""#line:1879
		O0OOO0OOO0OOOO00O ["关注建议"]=""#line:1880
		O0OOO0OOO0OOOO00O ["疑似新的"]=""#line:1881
		O0OOO0OOO0OOOO00O ["疑似旧的"]=""#line:1882
		O0OOO0OOO0OOOO00O ["疑似新的（高敏）"]=""#line:1883
		O0OOO0OOO0OOOO00O ["疑似旧的（高敏）"]=""#line:1884
		OOOO0000O00OOO000 =1 #line:1885
		O0O00OOO0000O00OO =int (len (O0OOO0OOO0OOOO00O ))#line:1886
		for OOO0OOOO0000O0O0O ,O0000O0O00O00OO00 in O0OOO0OOO0OOOO00O .iterrows ():#line:1889
			OOOO0O00O0OO0O0OO =OO0O0O0O00O000OO0 [(OO0O0O0O00O000OO0 ["产品名称"]==O0000O0O00O00OO00 ["产品名称"])]#line:1891
			O000O0OOOO0O0OOO0 =OOOO0O00O0OO0O0OO .loc [OOOO0O00O0OO0O0OO ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1893
			OOOOO0O00O000OOO0 =OOOO0O00O0OO0O0OO .loc [~OOOO0O00O0OO0O0OO ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1894
			OO000O00OOO00OO0O =OOOOO000O000O00O0 (OOOO0O00O0OO0O0OO )#line:1895
			OOOO0O0OO0O0O0OOO =OOOOO000O000O00O0 (O000O0OOOO0O0OOO0 )#line:1896
			O0000OOO00OOO0O0O =OOOOO000O000O00O0 (OOOOO0O00O000OOO0 )#line:1897
			PROGRAM_change_schedule (OOOO0000O00OOO000 ,O0O00OOO0000O00OO )#line:1898
			OOOO0000O00OOO000 =OOOO0000O00OOO000 +1 #line:1899
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in OO000O00OOO00OO0O .iterrows ():#line:1901
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]:#line:1902
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1903
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"所有不良反应"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"所有不良反应"]+O0OOOO0O0O00OOO0O #line:1904
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in O0000OOO00OOO0O0O .iterrows ():#line:1907
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]:#line:1908
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1909
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的"]+O0OOOO0O0O00OOO0O #line:1910
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]and int (OOO000O0OOO0OO000 ["详细描述T"])>=2 :#line:1912
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1913
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的（高敏）"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的（高敏）"]+O0OOOO0O0O00OOO0O #line:1914
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in OOOO0O0OO0O0O0OOO .iterrows ():#line:1916
				if str (OOO000O0OOO0OO000 ["条目"]).strip ()not in str (O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的"])and "分隔符"not in str (OOO000O0OOO0OO000 ["条目"]):#line:1917
					O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1918
					O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的"]+O0OOOO0O0O00OOO0O #line:1919
					if int (OOO000O0OOO0OO000 ["详细描述T"])>=3 :#line:1920
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]+"！"#line:1921
					if int (OOO000O0OOO0OO000 ["详细描述T"])>=5 :#line:1922
						O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"关注建议"]+"●"#line:1923
				if str (OOO000O0OOO0OO000 ["条目"]).strip ()not in str (O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似旧的（高敏）"])and "分隔符"not in str (OOO000O0OOO0OO000 ["条目"])and int (OOO000O0OOO0OO000 ["详细描述T"])>=2 :#line:1925
					O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1926
					O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的（高敏）"]=O0OOO0OOO0OOOO00O .loc [OOO0OOOO0000O0O0O ,"疑似新的（高敏）"]+O0OOOO0O0O00OOO0O #line:1927
		O0OOO0OOO0OOOO00O ["疑似新的"]="{"+O0OOO0OOO0OOOO00O ["疑似新的"]+"}"#line:1929
		O0OOO0OOO0OOOO00O ["疑似旧的"]="{"+O0OOO0OOO0OOOO00O ["疑似旧的"]+"}"#line:1930
		O0OOO0OOO0OOOO00O ["所有不良反应"]="{"+O0OOO0OOO0OOOO00O ["所有不良反应"]+"}"#line:1931
		O0OOO0OOO0OOOO00O ["疑似新的（高敏）"]="{"+O0OOO0OOO0OOOO00O ["疑似新的（高敏）"]+"}"#line:1932
		O0OOO0OOO0OOOO00O ["疑似旧的（高敏）"]="{"+O0OOO0OOO0OOOO00O ["疑似旧的（高敏）"]+"}"#line:1933
		O0OOO0OOO0OOOO00O ["报表类型"]="dfx_chanpin"#line:1934
		OOO0OO0O00OO0000O =pd .pivot_table (OO0O0O0O00O000OO0 ,values =["报告编码"],index =["产品名称"],columns ="报告单位评价",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"})#line:1936
		OOO0OO0O00OO0000O .columns =OOO0OO0O00OO0000O .columns .droplevel (0 )#line:1937
		O0OOO0OOO0OOOO00O =pd .merge (O0OOO0OOO0OOOO00O ,OOO0OO0O00OO0000O .reset_index (),on =["产品名称"],how ="left")#line:1938
		TABLE_tree_Level_2 (O0OOO0OOO0OOOO00O .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,OO0O0O0O00O000OO0 )#line:1939
	if OO000OOO0000OO0O0 =="页面":#line:1941
		OOO0OO00O00O00OOO =""#line:1942
		OO0000000O0OO0OOO =""#line:1943
		O000O0OOOO0O0OOO0 =OO0O0O0O00O000OO0 .loc [OO0O0O0O00O000OO0 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1944
		OOOOO0O00O000OOO0 =OO0O0O0O00O000OO0 .loc [~OO0O0O0O00O000OO0 ["报告类型-新的"].str .contains ("新",na =False )].copy ()#line:1945
		OOOO0O0OO0O0O0OOO =OOOOO000O000O00O0 (O000O0OOOO0O0OOO0 )#line:1946
		O0000OOO00OOO0O0O =OOOOO000O000O00O0 (OOOOO0O00O000OOO0 )#line:1947
		if 1 ==1 :#line:1948
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in O0000OOO00OOO0O0O .iterrows ():#line:1949
					if "分隔符"not in OOO000O0OOO0OO000 ["条目"]:#line:1950
						O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1951
						OO0000000O0OO0OOO =OO0000000O0OO0OOO +O0OOOO0O0O00OOO0O #line:1952
			for OOOO00000OOO0000O ,OOO000O0OOO0OO000 in OOOO0O0OO0O0O0OOO .iterrows ():#line:1953
				if str (OOO000O0OOO0OO000 ["条目"]).strip ()not in OO0000000O0OO0OOO and "分隔符"not in str (OOO000O0OOO0OO000 ["条目"]):#line:1954
					O0OOOO0O0O00OOO0O ="'"+str (OOO000O0OOO0OO000 ["条目"])+"':"+str (OOO000O0OOO0OO000 ["详细描述T"])+","#line:1955
					OOO0OO00O00O00OOO =OOO0OO00O00O00OOO +O0OOOO0O0O00OOO0O #line:1956
		OO0000000O0OO0OOO ="{"+OO0000000O0OO0OOO +"}"#line:1957
		OOO0OO00O00O00OOO ="{"+OOO0OO00O00O00OOO +"}"#line:1958
		OO0OO0000OOOO0OO0 ="\n可能是新的不良反应：\n\n"+OOO0OO00O00O00OOO +"\n\n\n可能不是新的不良反应：\n\n"+OO0000000O0OO0OOO #line:1959
		TOOLS_view_dict (OO0OO0000OOOO0OO0 ,1 )#line:1960
def TOOLS_strdict_to_pd (OOO0O000OO00O0000 ):#line:1962
	""#line:1963
	return pd .DataFrame .from_dict (eval (OOO0O000OO00O0000 ),orient ="index",columns =["content"]).reset_index ()#line:1964
def TOOLS_xuanze (O00OO000OO0OOOOO0 ,OO00O000O0OOO00O0 ):#line:1966
    ""#line:1967
    if OO00O000O0OOO00O0 ==0 :#line:1968
        O00OO0OOOO0OO0OO0 =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLS",".xls")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1969
    else :#line:1970
        O00OO0OOOO0OO0OO0 =pd .read_excel (peizhidir +"0（范例）批量筛选.xls",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:1971
    O00OO000OO0OOOOO0 ["temppr"]=""#line:1972
    for O0OOOO0OOOO000OO0 in O00OO0OOOO0OO0OO0 .columns .tolist ():#line:1973
        O00OO000OO0OOOOO0 ["temppr"]=O00OO000OO0OOOOO0 ["temppr"]+"----"+O00OO000OO0OOOOO0 [O0OOOO0OOOO000OO0 ]#line:1974
    OOO000O0O000OO000 ="测试字段MMMMM"#line:1975
    for O0OOOO0OOOO000OO0 in O00OO0OOOO0OO0OO0 .columns .tolist ():#line:1976
        for O0O00O0O00O00O00O in O00OO0OOOO0OO0OO0 [O0OOOO0OOOO000OO0 ].drop_duplicates ():#line:1978
            if O0O00O0O00O00O00O :#line:1979
                OOO000O0O000OO000 =OOO000O0O000OO000 +"|"+str (O0O00O0O00O00O00O )#line:1980
    O00OO000OO0OOOOO0 =O00OO000OO0OOOOO0 .loc [O00OO000OO0OOOOO0 ["temppr"].str .contains (OOO000O0O000OO000 ,na =False )].copy ()#line:1981
    del O00OO000OO0OOOOO0 ["temppr"]#line:1982
    O00OO000OO0OOOOO0 =O00OO000OO0OOOOO0 .reset_index (drop =True )#line:1983
    TABLE_tree_Level_2 (O00OO000OO0OOOOO0 ,0 ,O00OO000OO0OOOOO0 )#line:1985
def TOOLS_add_c (OOO00000OOOOO00OO ,O0O00000O000OOO0O ):#line:1987
			OOO00000OOOOO00OO ["关键字查找列o"]=""#line:1988
			for O00OOOO0O0O0O0OOO in TOOLS_get_list (O0O00000O000OOO0O ["查找列"]):#line:1989
				OOO00000OOOOO00OO ["关键字查找列o"]=OOO00000OOOOO00OO ["关键字查找列o"]+OOO00000OOOOO00OO [O00OOOO0O0O0O0OOO ].astype ("str")#line:1990
			if O0O00000O000OOO0O ["条件"]=="等于":#line:1991
				OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO [O0O00000O000OOO0O ["查找列"]].astype (str )==str (O0O00000O000OOO0O ["条件值"])),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:1992
			if O0O00000O000OOO0O ["条件"]=="大于":#line:1993
				OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO [O0O00000O000OOO0O ["查找列"]].astype (float )>O0O00000O000OOO0O ["条件值"]),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:1994
			if O0O00000O000OOO0O ["条件"]=="小于":#line:1995
				OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO [O0O00000O000OOO0O ["查找列"]].astype (float )<O0O00000O000OOO0O ["条件值"]),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:1996
			if O0O00000O000OOO0O ["条件"]=="介于":#line:1997
				OO0O00OOOOOO000OO =TOOLS_get_list (O0O00000O000OOO0O ["条件值"])#line:1998
				OOO00000OOOOO00OO .loc [((OOO00000OOOOO00OO [O0O00000O000OOO0O ["查找列"]].astype (float )<float (OO0O00OOOOOO000OO [1 ]))&(OOO00000OOOOO00OO [O0O00000O000OOO0O ["查找列"]].astype (float )>float (OO0O00OOOOOO000OO [0 ]))),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:1999
			if O0O00000O000OOO0O ["条件"]=="不含":#line:2000
				OOO00000OOOOO00OO .loc [(~OOO00000OOOOO00OO ["关键字查找列o"].str .contains (O0O00000O000OOO0O ["条件值"])),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2001
			if O0O00000O000OOO0O ["条件"]=="包含":#line:2002
				OOO00000OOOOO00OO .loc [OOO00000OOOOO00OO ["关键字查找列o"].str .contains (O0O00000O000OOO0O ["条件值"],na =False ),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2003
			if O0O00000O000OOO0O ["条件"]=="同时包含":#line:2004
				OOOOO00000OOO00OO =TOOLS_get_list0 (O0O00000O000OOO0O ["条件值"],0 )#line:2005
				if len (OOOOO00000OOO00OO )==1 :#line:2006
				    OOO00000OOOOO00OO .loc [OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [0 ],na =False ),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2007
				if len (OOOOO00000OOO00OO )==2 :#line:2008
				    OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [0 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [1 ],na =False )),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2009
				if len (OOOOO00000OOO00OO )==3 :#line:2010
				    OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [0 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [1 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [2 ],na =False )),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2011
				if len (OOOOO00000OOO00OO )==4 :#line:2012
				    OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [0 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [1 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [2 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [3 ],na =False )),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2013
				if len (OOOOO00000OOO00OO )==5 :#line:2014
				    OOO00000OOOOO00OO .loc [(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [0 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [1 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [2 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [3 ],na =False ))&(OOO00000OOOOO00OO ["关键字查找列o"].str .contains (OOOOO00000OOO00OO [4 ],na =False )),O0O00000O000OOO0O ["赋值列名"]]=O0O00000O000OOO0O ["赋值"]#line:2015
			return OOO00000OOOOO00OO #line:2016
def TOOL_guizheng (OO0OO0O0O0O0OOO0O ,O000O0OOO000O00OO ,O0O00000OO0OOO0OO ):#line:2019
	""#line:2020
	if O000O0OOO000O00OO ==0 :#line:2021
		O0OOOOO0OOOOOO0O0 =pd .read_excel (filedialog .askopenfilename (filetypes =[("XLSX",".xlsx")]),sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:2022
		O0OOOOO0OOOOOO0O0 =O0OOOOO0OOOOOO0O0 [(O0OOOOO0OOOOOO0O0 ["执行标记"]=="是")].reset_index ()#line:2023
		for O00OOO00OO0OOOO00 ,O0O00O0O0OOO0000O in O0OOOOO0OOOOOO0O0 .iterrows ():#line:2024
			OO0OO0O0O0O0OOO0O =TOOLS_add_c (OO0OO0O0O0O0OOO0O ,O0O00O0O0OOO0000O )#line:2025
		del OO0OO0O0O0O0OOO0O ["关键字查找列o"]#line:2026
	elif O000O0OOO000O00OO ==1 :#line:2028
		O0OOOOO0OOOOOO0O0 =pd .read_excel (peizhidir +"0（范例）数据规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:2029
		O0OOOOO0OOOOOO0O0 =O0OOOOO0OOOOOO0O0 [(O0OOOOO0OOOOOO0O0 ["执行标记"]=="是")].reset_index ()#line:2030
		for O00OOO00OO0OOOO00 ,O0O00O0O0OOO0000O in O0OOOOO0OOOOOO0O0 .iterrows ():#line:2031
			OO0OO0O0O0O0OOO0O =TOOLS_add_c (OO0OO0O0O0O0OOO0O ,O0O00O0O0OOO0000O )#line:2032
		del OO0OO0O0O0O0OOO0O ["关键字查找列o"]#line:2033
	elif O000O0OOO000O00OO =="课题":#line:2035
		O0OOOOO0OOOOOO0O0 =pd .read_excel (peizhidir +"0（范例）品类规整.xlsx",sheet_name =0 ,header =0 ,index_col =0 ,).reset_index ()#line:2036
		O0OOOOO0OOOOOO0O0 =O0OOOOO0OOOOOO0O0 [(O0OOOOO0OOOOOO0O0 ["执行标记"]=="是")].reset_index ()#line:2037
		for O00OOO00OO0OOOO00 ,O0O00O0O0OOO0000O in O0OOOOO0OOOOOO0O0 .iterrows ():#line:2038
			OO0OO0O0O0O0OOO0O =TOOLS_add_c (OO0OO0O0O0O0OOO0O ,O0O00O0O0OOO0000O )#line:2039
		del OO0OO0O0O0O0OOO0O ["关键字查找列o"]#line:2040
	elif O000O0OOO000O00OO ==2 :#line:2042
		text .insert (END ,"\n开展报告单位和监测机构名称规整...")#line:2043
		O000OOO000O0OOO00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2044
		O0O0O00O000O0OOOO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2045
		O0O0000OO00O0OO00 =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="地市清单",header =0 ,index_col =0 ,).fillna ("没有定义好X").reset_index ()#line:2046
		for O00OOO00OO0OOOO00 ,O0O00O0O0OOO0000O in O000OOO000O0OOO00 .iterrows ():#line:2047
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["曾用名1"]),"单位名称"]=O0O00O0O0OOO0000O ["单位名称"]#line:2048
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["曾用名2"]),"单位名称"]=O0O00O0O0OOO0000O ["单位名称"]#line:2049
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["曾用名3"]),"单位名称"]=O0O00O0O0OOO0000O ["单位名称"]#line:2050
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["曾用名4"]),"单位名称"]=O0O00O0O0OOO0000O ["单位名称"]#line:2051
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["曾用名5"]),"单位名称"]=O0O00O0O0OOO0000O ["单位名称"]#line:2052
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["单位名称"]),"医疗机构类别"]=O0O00O0O0OOO0000O ["医疗机构类别"]#line:2054
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["单位名称"]),"监测机构"]=O0O00O0O0OOO0000O ["监测机构"]#line:2055
		for O00OOO00OO0OOOO00 ,O0O00O0O0OOO0000O in O0O0O00O000O0OOOO .iterrows ():#line:2057
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["监测机构"]==O0O00O0O0OOO0000O ["曾用名1"]),"监测机构"]=O0O00O0O0OOO0000O ["监测机构"]#line:2058
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["监测机构"]==O0O00O0O0OOO0000O ["曾用名2"]),"监测机构"]=O0O00O0O0OOO0000O ["监测机构"]#line:2059
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["监测机构"]==O0O00O0O0OOO0000O ["曾用名3"]),"监测机构"]=O0O00O0O0OOO0000O ["监测机构"]#line:2060
		for OO0OOO00OO0O0OO00 in O0O0000OO00O0OO00 ["地市列表"]:#line:2062
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["上报单位所属地区"].str .contains (OO0OOO00OO0O0OO00 ,na =False )),"市级监测机构"]=OO0OOO00OO0O0OO00 #line:2063
		OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["上报单位所属地区"].str .contains ("顺德",na =False )),"市级监测机构"]="佛山"#line:2066
		OO0OO0O0O0O0OOO0O ["市级监测机构"]=OO0OO0O0O0O0OOO0O ["市级监测机构"].fillna ("-未规整的-")#line:2067
	elif O000O0OOO000O00OO ==3 :#line:2069
			O0OOOOO0O00O00000 =(OO0OO0O0O0O0OOO0O .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]).aggregate ({"报告编码":"count"}).reset_index ())#line:2074
			O0OOOOO0O00O00000 =O0OOOOO0O00O00000 .sort_values (by =["注册证编号/曾用注册证编号","报告编码"],ascending =[False ,False ],na_position ="last").reset_index ()#line:2077
			text .insert (END ,"\n开展产品名称规整..")#line:2078
			del O0OOOOO0O00O00000 ["报告编码"]#line:2079
			O0OOOOO0O00O00000 =O0OOOOO0O00O00000 .drop_duplicates (["注册证编号/曾用注册证编号"])#line:2080
			OO0OO0O0O0O0OOO0O =OO0OO0O0O0O0OOO0O .rename (columns ={"上市许可持有人名称":"上市许可持有人名称（规整前）","产品类别":"产品类别（规整前）","产品名称":"产品名称（规整前）"})#line:2082
			OO0OO0O0O0O0OOO0O =pd .merge (OO0OO0O0O0O0OOO0O ,O0OOOOO0O00O00000 ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2083
	elif O000O0OOO000O00OO ==4 :#line:2085
		text .insert (END ,"\n正在开展化妆品注册单位规整...")#line:2086
		O0O0O00O000O0OOOO =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="机构列表",header =0 ,index_col =0 ,).reset_index ()#line:2087
		for O00OOO00OO0OOOO00 ,O0O00O0O0OOO0000O in O0O0O00O000O0OOOO .iterrows ():#line:2089
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["中文全称"]),"监测机构"]=O0O00O0O0OOO0000O ["归属地区"]#line:2090
			OO0OO0O0O0O0OOO0O .loc [(OO0OO0O0O0O0OOO0O ["单位名称"]==O0O00O0O0OOO0000O ["中文全称"]),"市级监测机构"]=O0O00O0O0OOO0000O ["地市"]#line:2091
		OO0OO0O0O0O0OOO0O ["监测机构"]=OO0OO0O0O0O0OOO0O ["监测机构"].fillna ("未规整")#line:2092
		OO0OO0O0O0O0OOO0O ["市级监测机构"]=OO0OO0O0O0O0OOO0O ["市级监测机构"].fillna ("未规整")#line:2093
	if O0O00000OO0OOO0OO ==True :#line:2094
		return OO0OO0O0O0O0OOO0O #line:2095
	else :#line:2096
		TABLE_tree_Level_2 (OO0OO0O0O0O0OOO0O ,0 ,OO0OO0O0O0O0OOO0O )#line:2097
def TOOL_person (OO00O000O0OO0O0OO ):#line:2099
	""#line:2100
	O0O0O0O0O0OO0000O =pd .read_excel (peizhidir +"0（范例）注册单位.xlsx",sheet_name ="专家列表",header =0 ,index_col =0 ,).reset_index ()#line:2101
	for O0O00O0000O0O0000 ,O00O00O0OO0OO0000 in O0O0O0O0O0OO0000O .iterrows ():#line:2102
		OO00O000O0OO0O0OO .loc [(OO00O000O0OO0O0OO ["市级监测机构"]==O00O00O0OO0OO0000 ["市级监测机构"]),"评表人员"]=O00O00O0OO0OO0000 ["评表人员"]#line:2103
		OO00O000O0OO0O0OO ["评表人员"]=OO00O000O0OO0O0OO ["评表人员"].fillna ("未规整")#line:2104
		OOOO000O000OO0O00 =OO00O000O0OO0O0OO .groupby (["评表人员"]).agg (报告数量 =("报告编码","nunique"),地市 =("市级监测机构",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:2108
	TABLE_tree_Level_2 (OOOO000O000OO0O00 ,0 ,OOOO000O000OO0O00 )#line:2109
def TOOLS_get_list (O0OO000OO00O00OOO ):#line:2111
    ""#line:2112
    O0OO000OO00O00OOO =str (O0OO000OO00O00OOO )#line:2113
    O00OOO00O0O000OO0 =[]#line:2114
    O00OOO00O0O000OO0 .append (O0OO000OO00O00OOO )#line:2115
    O00OOO00O0O000OO0 =",".join (O00OOO00O0O000OO0 )#line:2116
    O00OOO00O0O000OO0 =O00OOO00O0O000OO0 .split ("|")#line:2117
    O00OOO0O000OOO000 =O00OOO00O0O000OO0 [:]#line:2118
    O00OOO00O0O000OO0 =list (set (O00OOO00O0O000OO0 ))#line:2119
    O00OOO00O0O000OO0 .sort (key =O00OOO0O000OOO000 .index )#line:2120
    return O00OOO00O0O000OO0 #line:2121
def TOOLS_get_list_m (O00OOOOOOO00O000O ,O00OO00OOOO00OO0O ):#line:2123
    ""#line:2124
    O00OOOOOOO00O000O =str (O00OOOOOOO00O000O )#line:2125
    if O00OO00OOOO00OO0O :#line:2128
        O000O0OO0OO000OOO =re .split (O00OO00OOOO00OO0O ,O00OOOOOOO00O000O )#line:2129
    else :#line:2130
         O000O0OO0OO000OOO =re .split ("/||,|，|;|；|┋|、",O00OOOOOOO00O000O )#line:2131
    return O000O0OO0OO000OOO #line:2132
def TOOLS_get_list0 (OO0O00OO0OO0OOOOO ,O0O0OOOO00OO00O00 ,*O0O0O0OOOO0O0OO0O ):#line:2134
    ""#line:2135
    OO0O00OO0OO0OOOOO =str (OO0O00OO0OO0OOOOO )#line:2136
    if pd .notnull (OO0O00OO0OO0OOOOO ):#line:2138
        try :#line:2139
            if "use("in str (OO0O00OO0OO0OOOOO ):#line:2140
                O00O00O00O0OO000O =OO0O00OO0OO0OOOOO #line:2141
                O0O000OO0OOOO000O =re .compile (r"[(](.*?)[)]",re .S )#line:2142
                OOOO0OOOO000OOO0O =re .findall (O0O000OO0OOOO000O ,O00O00O00O0OO000O )#line:2143
                O0OOO0000O000O000 =[]#line:2144
                if ").list"in OO0O00OO0OO0OOOOO :#line:2145
                    OOO0OOOOO000O0000 =peizhidir +""+str (OOOO0OOOO000OOO0O [0 ])+".xls"#line:2146
                    OOO0O0OO0OOO00000 =pd .read_excel (OOO0OOOOO000O0000 ,sheet_name =OOOO0OOOO000OOO0O [0 ],header =0 ,index_col =0 ).reset_index ()#line:2149
                    OOO0O0OO0OOO00000 ["检索关键字"]=OOO0O0OO0OOO00000 ["检索关键字"].astype (str )#line:2150
                    O0OOO0000O000O000 =OOO0O0OO0OOO00000 ["检索关键字"].tolist ()+O0OOO0000O000O000 #line:2151
                if ").file"in OO0O00OO0OO0OOOOO :#line:2152
                    O0OOO0000O000O000 =O0O0OOOO00OO00O00 [OOOO0OOOO000OOO0O [0 ]].astype (str ).tolist ()+O0OOO0000O000O000 #line:2154
                try :#line:2157
                    if "报告类型-新的"in O0O0OOOO00OO00O00 .columns :#line:2158
                        O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2159
                        O0OOO0000O000O000 =O0OOO0000O000O000 .split (";")#line:2160
                        O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2161
                        O0OOO0000O000O000 =O0OOO0000O000O000 .split ("；")#line:2162
                        O0OOO0000O000O000 =[O0O00O00OO000O000 .replace ("（严重）","")for O0O00O00OO000O000 in O0OOO0000O000O000 ]#line:2163
                        O0OOO0000O000O000 =[OO00O0OO0OOO00O0O .replace ("（一般）","")for OO00O0OO0OOO00O0O in O0OOO0000O000O000 ]#line:2164
                except :#line:2165
                    pass #line:2166
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2168
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("┋")#line:2169
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2170
                O0OOO0000O000O000 =O0OOO0000O000O000 .split (";")#line:2171
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2172
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("；")#line:2173
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2174
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("、")#line:2175
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2176
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("，")#line:2177
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2178
                O0OOO0000O000O000 =O0OOO0000O000O000 .split (",")#line:2179
                OOOO0OO0OOO0OOOOO =O0OOO0000O000O000 [:]#line:2182
                try :#line:2183
                    if O0O0O0OOOO0O0OO0O [0 ]==1000 :#line:2184
                      pass #line:2185
                except :#line:2186
                      O0OOO0000O000O000 =list (set (O0OOO0000O000O000 ))#line:2187
                O0OOO0000O000O000 .sort (key =OOOO0OO0OOO0OOOOO .index )#line:2188
            else :#line:2190
                OO0O00OO0OO0OOOOO =str (OO0O00OO0OO0OOOOO )#line:2191
                O0OOO0000O000O000 =[]#line:2192
                O0OOO0000O000O000 .append (OO0O00OO0OO0OOOOO )#line:2193
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2194
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("┋")#line:2195
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2196
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("、")#line:2197
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2198
                O0OOO0000O000O000 =O0OOO0000O000O000 .split ("，")#line:2199
                O0OOO0000O000O000 =",".join (O0OOO0000O000O000 )#line:2200
                O0OOO0000O000O000 =O0OOO0000O000O000 .split (",")#line:2201
                OOOO0OO0OOO0OOOOO =O0OOO0000O000O000 [:]#line:2203
                try :#line:2204
                    if O0O0O0OOOO0O0OO0O [0 ]==1000 :#line:2205
                      O0OOO0000O000O000 =list (set (O0OOO0000O000O000 ))#line:2206
                except :#line:2207
                      pass #line:2208
                O0OOO0000O000O000 .sort (key =OOOO0OO0OOO0OOOOO .index )#line:2209
                O0OOO0000O000O000 .sort (key =OOOO0OO0OOO0OOOOO .index )#line:2210
        except ValueError2 :#line:2212
            showinfo (title ="提示信息",message ="创建单元格支持多个甚至表单（文件）传入的方法，返回一个经过整理的清单出错，任务终止。")#line:2213
            return False #line:2214
    return O0OOO0000O000O000 #line:2216
def TOOLS_easyread2 (OO0O0OOOOO0O0O0OO ):#line:2218
    ""#line:2219
    OO0O0OOOOO0O0O0OO ["分隔符"]="●"#line:2221
    OO0O0OOOOO0O0O0OO ["上报机构描述"]=(OO0O0OOOOO0O0O0OO ["使用过程"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["事件原因分析"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["事件原因分析描述"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["初步处置情况"].astype ("str"))#line:2230
    OO0O0OOOOO0O0O0OO ["持有人处理描述"]=(OO0O0OOOOO0O0O0OO ["关联性评价"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["调查情况"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["事件原因分析"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["具体控制措施"].astype ("str")+OO0O0OOOOO0O0O0OO ["分隔符"]+OO0O0OOOOO0O0O0OO ["未采取控制措施原因"].astype ("str"))#line:2241
    O0OO00O00OOOOOO0O =OO0O0OOOOO0O0O0OO [["报告编码","事件发生日期","报告日期","单位名称","产品名称","注册证编号/曾用注册证编号","产品批号","型号","规格","上市许可持有人名称","管理类别","伤害","伤害表现","器械故障表现","上报机构描述","持有人处理描述","经营企业使用单位报告状态","监测机构","产品类别","医疗机构类别","年龄","年龄类型","性别"]]#line:2268
    O0OO00O00OOOOOO0O =O0OO00O00OOOOOO0O .sort_values (by =["事件发生日期"],ascending =[False ],na_position ="last",)#line:2273
    O0OO00O00OOOOOO0O =O0OO00O00OOOOOO0O .rename (columns ={"报告编码":"规整编码"})#line:2274
    return O0OO00O00OOOOOO0O #line:2275
def fenci0 (O00O000000000OO00 ):#line:2278
	""#line:2279
	O0O0OO0000O000O0O =Toplevel ()#line:2280
	O0O0OO0000O000O0O .title ('词频统计')#line:2281
	OO00000OOO0OO00OO =O0O0OO0000O000O0O .winfo_screenwidth ()#line:2282
	OO0O0OO0O0OOO00O0 =O0O0OO0000O000O0O .winfo_screenheight ()#line:2284
	O00O00OOOO00O0OO0 =400 #line:2286
	OO00O0OO0OO000O0O =120 #line:2287
	O0OO0O00OO0O00OO0 =(OO00000OOO0OO00OO -O00O00OOOO00O0OO0 )/2 #line:2289
	OO0OOOOO0OO000O0O =(OO0O0OO0O0OOO00O0 -OO00O0OO0OO000O0O )/2 #line:2290
	O0O0OO0000O000O0O .geometry ("%dx%d+%d+%d"%(O00O00OOOO00O0OO0 ,OO00O0OO0OO000O0O ,O0OO0O00OO0O00OO0 ,OO0OOOOO0OO000O0O ))#line:2291
	O00000OO0OOO0OO0O =Label (O0O0OO0000O000O0O ,text ="配置文件：")#line:2292
	O00000OO0OOO0OO0O .pack ()#line:2293
	O0OO00O0OOO00OO0O =Label (O0O0OO0000O000O0O ,text ="需要分词的列：")#line:2294
	OO0O00000O000O00O =Entry (O0O0OO0000O000O0O ,width =80 )#line:2296
	OO0O00000O000O00O .insert (0 ,peizhidir +"0（范例）中文分词工作文件.xls")#line:2297
	OO000O000OOOOOOO0 =Entry (O0O0OO0000O000O0O ,width =80 )#line:2298
	OO000O000OOOOOOO0 .insert (0 ,"器械故障表现，伤害表现")#line:2299
	OO0O00000O000O00O .pack ()#line:2300
	O0OO00O0OOO00OO0O .pack ()#line:2301
	OO000O000OOOOOOO0 .pack ()#line:2302
	O00000OO000O0O00O =LabelFrame (O0O0OO0000O000O0O )#line:2303
	OOO00000000O00OOO =Button (O00000OO000O0O00O ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (tree_Level_2 ,fenci (OO0O00000O000O00O .get (),OO000O000OOOOOOO0 .get (),O00O000000000OO00 ),1 ,0 ))#line:2304
	OOO00000000O00OOO .pack (side =LEFT ,padx =1 ,pady =1 )#line:2305
	O00000OO000O0O00O .pack ()#line:2306
def fenci (OO00O00O00O000O00 ,O000O0OO000OOO0O0 ,O0O0O000000O00OO0 ):#line:2308
    ""#line:2309
    import glob #line:2310
    import jieba #line:2311
    import random #line:2312
    try :#line:2314
        O0O0O000000O00OO0 =O0O0O000000O00OO0 .drop_duplicates (["报告编码"])#line:2315
    except :#line:2316
        pass #line:2317
    def O000O000OO0000000 (OO0OOO0O0000000O0 ,O0OO0O0O0O0O00OOO ):#line:2318
        OOO0O0O0OO00O00O0 ={}#line:2319
        for OOOO0O0O0O0OO00O0 in OO0OOO0O0000000O0 :#line:2320
            OOO0O0O0OO00O00O0 [OOOO0O0O0O0OO00O0 ]=OOO0O0O0OO00O00O0 .get (OOOO0O0O0O0OO00O0 ,0 )+1 #line:2321
        return sorted (OOO0O0O0OO00O00O0 .items (),key =lambda OOOOO00OOOO0O0000 :OOOOO00OOOO0O0000 [1 ],reverse =True )[:O0OO0O0O0O0O00OOO ]#line:2322
    OO00O00OO00O0000O =pd .read_excel (OO00O00O00O000O00 ,sheet_name ="初始化",header =0 ,index_col =0 ).reset_index ()#line:2326
    OO0O0OO0OOOOO0000 =OO00O00OO00O0000O .iloc [0 ,2 ]#line:2328
    O0O0OO00OOO00OOOO =pd .read_excel (OO00O00O00O000O00 ,sheet_name ="停用词",header =0 ,index_col =0 ).reset_index ()#line:2331
    O0O0OO00OOO00OOOO ["停用词"]=O0O0OO00OOO00OOOO ["停用词"].astype (str )#line:2333
    OOO000OO00O0O0O00 =[O000OO00OO0O0O0O0 .strip ()for O000OO00OO0O0O0O0 in O0O0OO00OOO00OOOO ["停用词"]]#line:2334
    O0O0OOOO0O000OO00 =pd .read_excel (OO00O00O00O000O00 ,sheet_name ="本地词库",header =0 ,index_col =0 ).reset_index ()#line:2337
    O000OO000000O0000 =O0O0OOOO0O000OO00 ["本地词库"]#line:2338
    jieba .load_userdict (O000OO000000O0000 )#line:2339
    OO0O0O0O0OOO0OOOO =""#line:2342
    O000OOOO00O0OOOO0 =get_list0 (O000O0OO000OOO0O0 ,O0O0O000000O00OO0 )#line:2345
    try :#line:2346
        for OO0OO00OO00OOO0O0 in O000OOOO00O0OOOO0 :#line:2347
            for O000OO0O00O0OO0O0 in O0O0O000000O00OO0 [OO0OO00OO00OOO0O0 ]:#line:2348
                OO0O0O0O0OOO0OOOO =OO0O0O0O0OOO0OOOO +str (O000OO0O00O0OO0O0 )#line:2349
    except :#line:2350
        text .insert (END ,"分词配置文件未正确设置，将对整个表格进行分词。")#line:2351
        for OO0OO00OO00OOO0O0 in O0O0O000000O00OO0 .columns .tolist ():#line:2352
            for O000OO0O00O0OO0O0 in O0O0O000000O00OO0 [OO0OO00OO00OOO0O0 ]:#line:2353
                OO0O0O0O0OOO0OOOO =OO0O0O0O0OOO0OOOO +str (O000OO0O00O0OO0O0 )#line:2354
    O0OOO0OOOOO0OOO00 =[]#line:2355
    O0OOO0OOOOO0OOO00 =O0OOO0OOOOO0OOO00 +[OOOO0OOO000O0000O for OOOO0OOO000O0000O in jieba .cut (OO0O0O0O0OOO0OOOO )if OOOO0OOO000O0000O not in OOO000OO00O0O0O00 ]#line:2356
    O0O000OOO00OO0O0O =dict (O000O000OO0000000 (O0OOO0OOOOO0OOO00 ,OO0O0OO0OOOOO0000 ))#line:2357
    OOOOOOO0O0OO0OOO0 =pd .DataFrame ([O0O000OOO00OO0O0O ]).T #line:2358
    OOOOOOO0O0OO0OOO0 =OOOOOOO0O0OO0OOO0 .reset_index ()#line:2359
    return OOOOOOO0O0OO0OOO0 #line:2360
def TOOLS_time (O0000OO000O0OOOOO ,O000O00OO0O0O0000 ,OO0000OOOO000OOOO ):#line:2362
	""#line:2363
	O0OOO00O0O0OOO000 =O0000OO000O0OOOOO .drop_duplicates (["报告编码"]).groupby ([O000O00OO0O0O0000 ]).agg (报告总数 =("报告编码","nunique"),).sort_values (by =O000O00OO0O0O0000 ,ascending =[True ],na_position ="last").reset_index ()#line:2366
	O0OOO00O0O0OOO000 =O0OOO00O0O0OOO000 .set_index (O000O00OO0O0O0000 )#line:2368
	O0OOO00O0O0OOO000 =O0OOO00O0O0OOO000 .resample ('D').asfreq (fill_value =0 )#line:2370
	O0OOO00O0O0OOO000 ["time"]=O0OOO00O0O0OOO000 .index .values #line:2372
	O0OOO00O0O0OOO000 ["time"]=pd .to_datetime (O0OOO00O0O0OOO000 ["time"],format ="%Y/%m/%d").dt .date #line:2373
	OOO0O0000O00OO0OO =30 #line:2378
	O00OO00O000OO00OO =30 #line:2379
	O0OOO00O0O0OOO000 ["30日移动平均数"]=round (O0OOO00O0O0OOO000 ["报告总数"].rolling (OOO0O0000O00OO0OO ,min_periods =1 ).mean (),2 )#line:2381
	O0OOO00O0O0OOO000 ["目标值"]=round (O0OOO00O0O0OOO000 ["30日移动平均数"].rolling (O00OO00O000OO00OO ,min_periods =1 ).mean (),2 )#line:2383
	O0OOO00O0O0OOO000 ["均值"]=round (O0OOO00O0O0OOO000 ["目标值"].rolling (O00OO00O000OO00OO ,min_periods =1 ).mean (),2 )#line:2385
	O0OOO00O0O0OOO000 ["标准差"]=round (O0OOO00O0O0OOO000 ["目标值"].rolling (O00OO00O000OO00OO ,min_periods =1 ).std (ddof =1 ),2 )#line:2387
	O0OOO00O0O0OOO000 ["1STD"]=round ((O0OOO00O0O0OOO000 ["均值"]+O0OOO00O0O0OOO000 ["标准差"]),2 )#line:2388
	O0OOO00O0O0OOO000 ["2STD"]=round ((O0OOO00O0O0OOO000 ["均值"]+O0OOO00O0O0OOO000 ["标准差"]*2 ),2 )#line:2389
	O0OOO00O0O0OOO000 ["UCL_3STD"]=round ((O0OOO00O0O0OOO000 ["均值"]+O0OOO00O0O0OOO000 ["标准差"]*3 ),2 )#line:2390
	DRAW_make_risk_plot (O0OOO00O0O0OOO000 ,"time",["30日移动平均数","UCL_3STD"],"折线图",999 )#line:2412
def TOOLS_time_bak (OO00OOO0OO0O00O00 ,OOO0O0O0OOOOOOO00 ,O0O0OOOOO00OOOOO0 ):#line:2415
	""#line:2416
	O00000O0OO0OOO0O0 =OO00OOO0OO0O00O00 .drop_duplicates (["报告编码"]).groupby ([OOO0O0O0OOOOOOO00 ]).agg (报告总数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda OO0OO0OO0O000OO00 :STAT_countpx (OO0OO0OO0O000OO00 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00000O00OO0OO00O :STAT_countpx (O00000O00OO0OO00O .values ,"死亡")),).sort_values (by =OOO0O0O0OOOOOOO00 ,ascending =[True ],na_position ="last").reset_index ()#line:2421
	O00000O0OO0OOO0O0 =O00000O0OO0OOO0O0 .set_index (OOO0O0O0OOOOOOO00 )#line:2425
	O00000O0OO0OOO0O0 =O00000O0OO0OOO0O0 .resample ('D').asfreq (fill_value =0 )#line:2427
	O00000O0OO0OOO0O0 ["time"]=O00000O0OO0OOO0O0 .index .values #line:2429
	O00000O0OO0OOO0O0 ["time"]=pd .to_datetime (O00000O0OO0OOO0O0 ["time"],format ="%Y/%m/%d").dt .date #line:2430
	if O0O0OOOOO00OOOOO0 ==1 :#line:2432
		return O00000O0OO0OOO0O0 .reset_index (drop =True )#line:2434
	O00000O0OO0OOO0O0 ["30天累计数"]=O00000O0OO0OOO0O0 ["报告总数"].rolling (30 ,min_periods =1 ).agg (lambda O0O000O0OOO0O0OOO :sum (O0O000O0OOO0O0OOO )).astype (int )#line:2436
	O00000O0OO0OOO0O0 ["30天严重伤害累计数"]=O00000O0OO0OOO0O0 ["严重伤害数"].rolling (30 ,min_periods =1 ).agg (lambda OO0OO00OO00OOOO0O :sum (OO0OO00OO00OOOO0O )).astype (int )#line:2437
	O00000O0OO0OOO0O0 ["30天死亡累计数"]=O00000O0OO0OOO0O0 ["死亡数量"].rolling (30 ,min_periods =1 ).agg (lambda O000O0O0O00OOOO0O :sum (O000O0O0O00OOOO0O )).astype (int )#line:2438
	O00000O0OO0OOO0O0 .loc [(((O00000O0OO0OOO0O0 ["30天累计数"]>=3 )&(O00000O0OO0OOO0O0 ["30天严重伤害累计数"]>=1 ))|(O00000O0OO0OOO0O0 ["30天累计数"]>=5 )|(O00000O0OO0OOO0O0 ["30天死亡累计数"]>=1 )),"关注区域"]=O00000O0OO0OOO0O0 ["30天累计数"]#line:2459
	DRAW_make_risk_plot (O00000O0OO0OOO0O0 ,"time",["30天累计数","30天严重伤害累计数","关注区域"],"折线图",999 )#line:2464
def TOOLS_keti (OO0OO000O0000O00O ):#line:2468
	""#line:2469
	import datetime #line:2470
	def OOO0O00O00OOOO000 (O0OO0000O00O000O0 ,OOOO0O0OO00OOO00O ):#line:2472
		if ini ["模式"]=="药品":#line:2473
			OOOO000O00O0O0OOO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:2474
		if ini ["模式"]=="器械":#line:2475
			OOOO000O00O0O0OOO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:2476
		if ini ["模式"]=="化妆品":#line:2477
			OOOO000O00O0O0OOO =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:2478
		O00OOO0OOO0OOOOOO =OOOO000O00O0O0OOO ["权重"][0 ]#line:2479
		O00O00O0O0OOO0000 =OOOO000O00O0O0OOO ["权重"][1 ]#line:2480
		O0OOO00O00000OO00 =OOOO000O00O0O0OOO ["权重"][2 ]#line:2481
		O000O0OO0000O0OO0 =OOOO000O00O0O0OOO ["权重"][3 ]#line:2482
		OO000O00O0OOO0O0O =OOOO000O00O0O0OOO ["值"][3 ]#line:2483
		OOOO00OO0OO0OO0OO =OOOO000O00O0O0OOO ["权重"][4 ]#line:2485
		O0000O0OO00000000 =OOOO000O00O0O0OOO ["值"][4 ]#line:2486
		OOOOOOOOO0O00O0O0 =OOOO000O00O0O0OOO ["权重"][5 ]#line:2488
		OO0000OOOOO000O0O =OOOO000O00O0O0OOO ["值"][5 ]#line:2489
		OOO000OOO0OO0O00O =OOOO000O00O0O0OOO ["权重"][6 ]#line:2491
		O0O00OO0O0000O000 =OOOO000O00O0O0OOO ["值"][6 ]#line:2492
		O00O00000OO0O00O0 =pd .to_datetime (O0OO0000O00O000O0 )#line:2494
		OOO0O00OO000O000O =OOOO0O0OO00OOO00O .copy ().set_index ('报告日期')#line:2495
		OOO0O00OO000O000O =OOO0O00OO000O000O .sort_index ()#line:2496
		if ini ["模式"]=="器械":#line:2497
			OOO0O00OO000O000O ["关键字查找列"]=OOO0O00OO000O000O ["器械故障表现"].astype (str )+OOO0O00OO000O000O ["伤害表现"].astype (str )+OOO0O00OO000O000O ["使用过程"].astype (str )+OOO0O00OO000O000O ["事件原因分析描述"].astype (str )+OOO0O00OO000O000O ["初步处置情况"].astype (str )#line:2498
		else :#line:2499
			OOO0O00OO000O000O ["关键字查找列"]=OOO0O00OO000O000O ["器械故障表现"].astype (str )#line:2500
		OOO0O00OO000O000O .loc [OOO0O00OO000O000O ["关键字查找列"].str .contains (OO000O00O0OOO0O0O ,na =False ),"高度关注关键字"]=1 #line:2501
		OOO0O00OO000O000O .loc [OOO0O00OO000O000O ["关键字查找列"].str .contains (O0000O0OO00000000 ,na =False ),"二级敏感词"]=1 #line:2502
		OOO0O00OO000O000O .loc [OOO0O00OO000O000O ["关键字查找列"].str .contains (OO0000OOOOO000O0O ,na =False ),"减分项"]=1 #line:2503
		OO0O00O00OOOO00OO =OOO0O00OO000O000O .loc [O00O00000OO0O00O0 -pd .Timedelta (days =30 ):O00O00000OO0O00O0 ].reset_index ()#line:2505
		OO0000O00000O0000 =OOO0O00OO000O000O .loc [O00O00000OO0O00O0 -pd .Timedelta (days =365 ):O00O00000OO0O00O0 ].reset_index ()#line:2506
		OOO0O0000OOO0OOO0 =OO0O00O00OOOO00OO .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:2519
		O0O000OOO0OO00000 =OO0O00O00OOOO00OO .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda OO00O00O0O00O0000 :STAT_countpx (OO00O00O0O00O0000 .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0000OOOOO0O00OO :STAT_countpx (OO0000OOOOO0O00OO .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OO0OOOO00O00000O0 :STAT_countpx (OO0OOOO00O00000O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO0OOO0OOOO00O000 :STAT_countpx (OO0OOO0OOOO00O000 .values ,"严重伤害待评价")),高度关注关键字 =("高度关注关键字","sum"),二级敏感词 =("二级敏感词","sum"),减分项 =("减分项","sum"),).reset_index ()#line:2531
		O000OO0O00O0O00OO =pd .merge (OOO0O0000OOO0OOO0 ,O0O000OOO0OO00000 ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2533
		O00OOO00OO000OO00 =OO0O00O00OOOO00OO .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:2540
		O00OOO00OO000OO00 =O00OOO00OO000OO00 .drop_duplicates ("注册证编号/曾用注册证编号")#line:2541
		O0000O00OOOOOO00O =OO0O00O00OOOO00OO .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),严重伤害数 =("伤害",lambda O0O0O00000OO0000O :STAT_countpx (O0O0O00000OO0000O .values ,"严重伤害")),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:2546
		O0000O00OOOOOO00O ["风险评分-影响"]=0 #line:2550
		O0000O00OOOOOO00O ["评分说明"]=""#line:2551
		O0000O00OOOOOO00O .loc [((O0000O00OOOOOO00O ["批号计数"]>=3 )&(O0000O00OOOOOO00O ["严重伤害数"]>=1 )&(O0000O00OOOOOO00O ["产品类别"]!="有源"))|((O0000O00OOOOOO00O ["批号计数"]>=5 )&(O0000O00OOOOOO00O ["产品类别"]!="有源")),"风险评分-影响"]=O0000O00OOOOOO00O ["风险评分-影响"]+3 #line:2552
		O0000O00OOOOOO00O .loc [(O0000O00OOOOOO00O ["风险评分-影响"]>=3 ),"评分说明"]=O0000O00OOOOOO00O ["评分说明"]+"●符合省中心无源规则+3;"#line:2553
		O0000O00OOOOOO00O =O0000O00OOOOOO00O .sort_values (by ="风险评分-影响",ascending =[False ],na_position ="last").reset_index (drop =True )#line:2557
		O0000O00OOOOOO00O =O0000O00OOOOOO00O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2558
		O00OOO00OO000OO00 =O00OOO00OO000OO00 [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号","型号计数"]]#line:2559
		O0000O00OOOOOO00O =O0000O00OOOOOO00O [["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号","批号计数","风险评分-影响","评分说明"]]#line:2560
		O000OO0O00O0O00OO =pd .merge (O000OO0O00O0O00OO ,O00OOO00OO000OO00 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2561
		O000OO0O00O0O00OO =pd .merge (O000OO0O00O0O00OO ,O0000O00OOOOOO00O ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:2563
		O000OO0O00O0O00OO .loc [((O000OO0O00O0O00OO ["证号计数"]>=3 )&(O000OO0O00O0O00OO ["严重伤害数"]>=1 )&(O000OO0O00O0O00OO ["产品类别"]=="有源"))|((O000OO0O00O0O00OO ["证号计数"]>=5 )&(O000OO0O00O0O00OO ["产品类别"]=="有源")),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+3 #line:2567
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-影响"]>=3 )&(O000OO0O00O0O00OO ["产品类别"]=="有源"),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"●符合省中心有源规则+3;"#line:2568
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["死亡数量"]>=1 ),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+10 #line:2573
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-影响"]>=10 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"存在死亡报告;"#line:2574
		O0O0OO000OOO00O0O =round (O00OOO0OOO0OOOOOO *(O000OO0O00O0O00OO ["严重伤害数"]/O000OO0O00O0O00OO ["证号计数"]),2 )#line:2577
		O000OO0O00O0O00OO ["风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+O0O0OO000OOO00O0O #line:2578
		O000OO0O00O0O00OO ["评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"严重比评分"+O0O0OO000OOO00O0O .astype (str )+";"#line:2579
		O000O00000O00O000 =round (O00O00O0O0OOO0000 *(np .log (O000OO0O00O0O00OO ["单位个数"])),2 )#line:2582
		O000OO0O00O0O00OO ["风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+O000O00000O00O000 #line:2583
		O000OO0O00O0O00OO ["评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"报告单位评分"+O000O00000O00O000 .astype (str )+";"#line:2584
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["产品类别"]=="有源")&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+O0OOO00O00000OO00 *O000OO0O00O0O00OO ["型号计数"]/O000OO0O00O0O00OO ["证号计数"]#line:2587
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["产品类别"]=="有源")&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"型号集中度评分"+(round (O0OOO00O00000OO00 *O000OO0O00O0O00OO ["型号计数"]/O000OO0O00O0O00OO ["证号计数"],2 )).astype (str )+";"#line:2588
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["产品类别"]!="有源")&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+O0OOO00O00000OO00 *O000OO0O00O0O00OO ["批号计数"]/O000OO0O00O0O00OO ["证号计数"]#line:2589
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["产品类别"]!="有源")&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"批号集中度评分"+(round (O0OOO00O00000OO00 *O000OO0O00O0O00OO ["批号计数"]/O000OO0O00O0O00OO ["证号计数"],2 )).astype (str )+";"#line:2590
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["高度关注关键字"]>=1 ),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+O000O0OO0000O0OO0 #line:2593
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["高度关注关键字"]>=1 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"●含有高度关注关键字评分"+str (O000O0OO0000O0OO0 )+"；"#line:2594
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["二级敏感词"]>=1 ),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+OOOO00OO0OO0OO0OO #line:2597
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["二级敏感词"]>=1 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"含有二级敏感词评分"+str (OOOO00OO0OO0OO0OO )+"；"#line:2598
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["减分项"]>=1 ),"风险评分-影响"]=O000OO0O00O0O00OO ["风险评分-影响"]+OOOOOOOOO0O00O0O0 #line:2601
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["减分项"]>=1 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"减分项评分"+str (OOOOOOOOO0O00O0O0 )+"；"#line:2602
		O0OOOOO0O00OOO00O =Countall (OO0000O00000O0000 ).df_findrisk ("事件发生月份")#line:2605
		O0OOOOO0O00OOO00O =O0OOOOO0O00OOO00O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2606
		O0OOOOO0O00OOO00O =O0OOOOO0O00OOO00O [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2607
		O000OO0O00O0O00OO =pd .merge (O000OO0O00O0O00OO ,O0OOOOO0O00OOO00O ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2608
		O000OO0O00O0O00OO ["风险评分-月份"]=1 #line:2610
		O000OO0O00O0O00OO ["mfc"]=""#line:2611
		O000OO0O00O0O00OO .loc [((O000OO0O00O0O00OO ["证号计数"]>O000OO0O00O0O00OO ["均值"])&(O000OO0O00O0O00OO ["标准差"].astype (str )=="nan")),"风险评分-月份"]=O000OO0O00O0O00OO ["风险评分-月份"]+1 #line:2612
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>O000OO0O00O0O00OO ["均值"]),"mfc"]="月份计数超过历史均值"+O000OO0O00O0O00OO ["均值"].astype (str )+"；"#line:2613
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=(O000OO0O00O0O00OO ["均值"]+O000OO0O00O0O00OO ["标准差"]))&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"风险评分-月份"]=O000OO0O00O0O00OO ["风险评分-月份"]+1 #line:2615
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=(O000OO0O00O0O00OO ["均值"]+O000OO0O00O0O00OO ["标准差"]))&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"mfc"]="月份计数超过3例超过历史均值一个标准差("+O000OO0O00O0O00OO ["标准差"].astype (str )+")；"#line:2616
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"风险评分-月份"]=O000OO0O00O0O00OO ["风险评分-月份"]+2 #line:2618
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=3 ),"mfc"]="月份计数超过3例且超过历史95%CI上限("+O000OO0O00O0O00OO ["CI上限"].astype (str )+")；"#line:2619
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=5 ),"风险评分-月份"]=O000OO0O00O0O00OO ["风险评分-月份"]+1 #line:2621
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=5 ),"mfc"]="月份计数超过5例且超过历史95%CI上限("+O000OO0O00O0O00OO ["CI上限"].astype (str )+")；"#line:2622
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=7 ),"风险评分-月份"]=O000OO0O00O0O00OO ["风险评分-月份"]+1 #line:2624
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=7 ),"mfc"]="月份计数超过7例且超过历史95%CI上限("+O000OO0O00O0O00OO ["CI上限"].astype (str )+")；"#line:2625
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=9 ),"风险评分-月份"]=O000OO0O00O0O00OO ["风险评分-月份"]+1 #line:2627
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["证号计数"]>=9 ),"mfc"]="月份计数超过9例且超过历史95%CI上限("+O000OO0O00O0O00OO ["CI上限"].astype (str )+")；"#line:2628
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=3 )&(O000OO0O00O0O00OO ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2632
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["证号计数"]>=3 )&(O000OO0O00O0O00OO ["标准差"].astype (str )=="nan"),"mfc"]="无历史数据但数量超过3例；"#line:2633
		O000OO0O00O0O00OO ["评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"●●证号数量："+O000OO0O00O0O00OO ["证号计数"].astype (str )+";"+O000OO0O00O0O00OO ["mfc"]#line:2636
		del O000OO0O00O0O00OO ["mfc"]#line:2637
		O000OO0O00O0O00OO =O000OO0O00O0O00OO .rename (columns ={"均值":"月份均值","标准差":"月份标准差","CI上限":"月份CI上限"})#line:2638
		O0OOOOO0O00OOO00O =Countall (OO0000O00000O0000 ).df_findrisk ("产品批号")#line:2642
		O0OOOOO0O00OOO00O =O0OOOOO0O00OOO00O .drop_duplicates ("注册证编号/曾用注册证编号")#line:2643
		O0OOOOO0O00OOO00O =O0OOOOO0O00OOO00O [["注册证编号/曾用注册证编号","均值","标准差","CI上限"]]#line:2644
		O000OO0O00O0O00OO =pd .merge (O000OO0O00O0O00OO ,O0OOOOO0O00OOO00O ,on =["注册证编号/曾用注册证编号"],how ="left")#line:2645
		O000OO0O00O0O00OO ["风险评分-批号"]=1 #line:2647
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["产品类别"]!="有源"),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"●●高峰批号数量："+O000OO0O00O0O00OO ["批号计数"].astype (str )+";"#line:2648
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>O000OO0O00O0O00OO ["均值"]),"风险评分-批号"]=O000OO0O00O0O00OO ["风险评分-批号"]+1 #line:2650
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>O000OO0O00O0O00OO ["均值"]),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"高峰批号计数超过历史均值"+O000OO0O00O0O00OO ["均值"].astype (str )+"；"#line:2651
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>(O000OO0O00O0O00OO ["均值"]+O000OO0O00O0O00OO ["标准差"]))&(O000OO0O00O0O00OO ["批号计数"]>=3 ),"风险评分-批号"]=O000OO0O00O0O00OO ["风险评分-批号"]+1 #line:2652
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>(O000OO0O00O0O00OO ["均值"]+O000OO0O00O0O00OO ["标准差"]))&(O000OO0O00O0O00OO ["批号计数"]>=3 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"高峰批号计数超过3例超过历史均值一个标准差("+O000OO0O00O0O00OO ["标准差"].astype (str )+")；"#line:2653
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["批号计数"]>=3 ),"风险评分-批号"]=O000OO0O00O0O00OO ["风险评分-批号"]+1 #line:2654
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>O000OO0O00O0O00OO ["CI上限"])&(O000OO0O00O0O00OO ["批号计数"]>=3 ),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"高峰批号计数超过3例且超过历史95%CI上限("+O000OO0O00O0O00OO ["CI上限"].astype (str )+")；"#line:2655
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>=3 )&(O000OO0O00O0O00OO ["标准差"].astype (str )=="nan"),"风险评分-月份"]=3 #line:2657
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["批号计数"]>=3 )&(O000OO0O00O0O00OO ["标准差"].astype (str )=="nan"),"评分说明"]=O000OO0O00O0O00OO ["评分说明"]+"无历史数据但数量超过3例；"#line:2658
		O000OO0O00O0O00OO =O000OO0O00O0O00OO .rename (columns ={"均值":"高峰批号均值","标准差":"高峰批号标准差","CI上限":"高峰批号CI上限"})#line:2659
		O000OO0O00O0O00OO ["风险评分-影响"]=round (O000OO0O00O0O00OO ["风险评分-影响"],2 )#line:2662
		O000OO0O00O0O00OO ["风险评分-月份"]=round (O000OO0O00O0O00OO ["风险评分-月份"],2 )#line:2663
		O000OO0O00O0O00OO ["风险评分-批号"]=round (O000OO0O00O0O00OO ["风险评分-批号"],2 )#line:2664
		O000OO0O00O0O00OO ["总体评分"]=O000OO0O00O0O00OO ["风险评分-影响"].copy ()#line:2666
		O000OO0O00O0O00OO ["关注建议"]=""#line:2667
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-影响"]>=3 ),"关注建议"]=O000OO0O00O0O00OO ["关注建议"]+"●建议关注(影响范围)；"#line:2668
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-月份"]>=3 ),"关注建议"]=O000OO0O00O0O00OO ["关注建议"]+"●建议关注(当月数量异常)；"#line:2669
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-批号"]>=3 ),"关注建议"]=O000OO0O00O0O00OO ["关注建议"]+"●建议关注(高峰批号数量异常)。"#line:2670
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-月份"]>=O000OO0O00O0O00OO ["风险评分-批号"]),"总体评分"]=O000OO0O00O0O00OO ["风险评分-影响"]*O000OO0O00O0O00OO ["风险评分-月份"]#line:2674
		O000OO0O00O0O00OO .loc [(O000OO0O00O0O00OO ["风险评分-月份"]<O000OO0O00O0O00OO ["风险评分-批号"]),"总体评分"]=O000OO0O00O0O00OO ["风险评分-影响"]*O000OO0O00O0O00OO ["风险评分-批号"]#line:2675
		O000OO0O00O0O00OO ["总体评分"]=round (O000OO0O00O0O00OO ["总体评分"],2 )#line:2677
		O000OO0O00O0O00OO ["评分说明"]=O000OO0O00O0O00OO ["关注建议"]+O000OO0O00O0O00OO ["评分说明"]#line:2678
		O000OO0O00O0O00OO =O000OO0O00O0O00OO .sort_values (by =["总体评分","风险评分-影响"],ascending =[False ,False ],na_position ="last").reset_index (drop =True )#line:2679
		O000OO0O00O0O00OO ["主要故障分类"]=""#line:2682
		for OO0OOO0OO0000OOO0 ,O00O000OOO00O0O00 in O000OO0O00O0O00OO .iterrows ():#line:2683
			O0OOO000OOO0O0OO0 =OO0O00O00OOOO00OO [(OO0O00O00OOOO00OO ["注册证编号/曾用注册证编号"]==O00O000OOO00O0O00 ["注册证编号/曾用注册证编号"])].copy ()#line:2684
			if O00O000OOO00O0O00 ["总体评分"]>=float (OOO000OOO0OO0O00O ):#line:2685
				if O00O000OOO00O0O00 ["规整后品类"]!="N":#line:2686
					O0OO0OO0OOO00000O =Countall (O0OOO000OOO0O0OO0 ).df_psur ("特定品种",O00O000OOO00O0O00 ["规整后品类"])#line:2687
				elif O00O000OOO00O0O00 ["产品类别"]=="无源":#line:2688
					O0OO0OO0OOO00000O =Countall (O0OOO000OOO0O0OO0 ).df_psur ("通用无源")#line:2689
				elif O00O000OOO00O0O00 ["产品类别"]=="有源":#line:2690
					O0OO0OO0OOO00000O =Countall (O0OOO000OOO0O0OO0 ).df_psur ("通用有源")#line:2691
				elif O00O000OOO00O0O00 ["产品类别"]=="体外诊断试剂":#line:2692
					O0OO0OO0OOO00000O =Countall (O0OOO000OOO0O0OO0 ).df_psur ("体外诊断试剂")#line:2693
				OO0O00OO0OOO0O0O0 =O0OO0OO0OOO00000O [["事件分类","总数量"]].copy ()#line:2695
				O0OO00OOO0000O0O0 =""#line:2696
				for OOOO00000OOOO000O ,O0O0OOOOOO000O000 in OO0O00OO0OOO0O0O0 .iterrows ():#line:2697
					O0OO00OOO0000O0O0 =O0OO00OOO0000O0O0 +str (O0O0OOOOOO000O000 ["事件分类"])+":"+str (O0O0OOOOOO000O000 ["总数量"])+";"#line:2698
				O000OO0O00O0O00OO .loc [OO0OOO0OO0000OOO0 ,"主要故障分类"]=O0OO00OOO0000O0O0 #line:2699
			else :#line:2700
				break #line:2701
		O000OO0O00O0O00OO =O000OO0O00O0O00OO [["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","证号计数","严重伤害数","死亡数量","总体评分","风险评分-影响","风险评分-月份","风险评分-批号","主要故障分类","评分说明","单位个数","单位列表","批号个数","批号列表","型号个数","型号列表","规格个数","规格列表","待评价数","严重伤害待评价数","高度关注关键字","二级敏感词","月份均值","月份标准差","月份CI上限","高峰批号均值","高峰批号标准差","高峰批号CI上限","型号","型号计数","产品批号","批号计数"]]#line:2705
		O000OO0O00O0O00OO ["报表类型"]="dfx_zhenghao"#line:2706
		TABLE_tree_Level_2 (O000OO0O00O0O00OO ,1 ,OO0O00O00OOOO00OO ,OO0000O00000O0000 )#line:2707
		pass #line:2708
	O0OO000O000OO0000 =Toplevel ()#line:2711
	O0OO000O000OO0000 .title ('风险预警')#line:2712
	O0O0OOO0OOO0OOOOO =O0OO000O000OO0000 .winfo_screenwidth ()#line:2713
	O00OO0OOO0OOOO00O =O0OO000O000OO0000 .winfo_screenheight ()#line:2715
	OO0OOOOOO0O0OO0O0 =350 #line:2717
	OO0OO0OOOOOO00OOO =35 #line:2718
	OOOO0OO00O0O000O0 =(O0O0OOO0OOO0OOOOO -OO0OOOOOO0O0OO0O0 )/2 #line:2720
	OO000O0O0O0OOOOO0 =(O00OO0OOO0OOOO00O -OO0OO0OOOOOO00OOO )/2 #line:2721
	O0OO000O000OO0000 .geometry ("%dx%d+%d+%d"%(OO0OOOOOO0O0OO0O0 ,OO0OO0OOOOOO00OOO ,OOOO0OO00O0O000O0 ,OO000O0O0O0OOOOO0 ))#line:2722
	OOO0OO00OO00O0000 =Label (O0OO000O000OO0000 ,text ="预警日期：")#line:2724
	OOO0OO00OO00O0000 .grid (row =1 ,column =0 ,sticky ="w")#line:2725
	O000OO0O00O000OOO =Entry (O0OO000O000OO0000 ,width =30 )#line:2726
	O000OO0O00O000OOO .insert (0 ,datetime .date .today ())#line:2727
	O000OO0O00O000OOO .grid (row =1 ,column =1 ,sticky ="w")#line:2728
	O0O0O00OOO0O0000O =Button (O0OO000O000OO0000 ,text ="确定",width =10 ,command =lambda :TABLE_tree_Level_2 (OOO0O00O00OOOO000 (O000OO0O00O000OOO .get (),OO0OO000O0000O00O ),1 ,OO0OO000O0000O00O ))#line:2732
	O0O0O00OOO0O0000O .grid (row =1 ,column =3 ,sticky ="w")#line:2733
	pass #line:2735
def TOOLS_count_elements (OOOOOOO000O0O0O0O ,O0O000O0O0OO0OO0O ,OO00O0O0O000OOO00 ):#line:2737
    ""#line:2738
    OOOO000OOO0O0000O =pd .DataFrame (columns =[OO00O0O0O000OOO00 ,'count'])#line:2740
    OO0OO0OO0O000OOO0 =[]#line:2741
    OOOO0OO00O0O00000 =[]#line:2742
    for OO0O0O0OO00OOO00O in TOOLS_get_list (O0O000O0O0OO0OO0O ):#line:2745
        O00OO00O0000OOO00 =OOOOOOO000O0O0O0O [OOOOOOO000O0O0O0O [OO00O0O0O000OOO00 ].str .contains (OO0O0O0OO00OOO00O )].shape [0 ]#line:2747
        if O00OO00O0000OOO00 >0 :#line:2750
            OO0OO0OO0O000OOO0 .append (O00OO00O0000OOO00 )#line:2751
            OOOO0OO00O0O00000 .append (OO0O0O0OO00OOO00O )#line:2752
    OO000OOOO0OOO000O =pd .DataFrame ({"index":OOOO0OO00O0O00000 ,'计数':OO0OO0OO0O000OOO0 })#line:2753
    OO000OOOO0OOO000O ["构成比(%)"]=round (100 *OO000OOOO0OOO000O ["计数"]/OO000OOOO0OOO000O ["计数"].sum (),2 )#line:2754
    OO000OOOO0OOO000O ["报表类型"]="dfx_deepvie2"+"_"+str ([OO00O0O0O000OOO00 ])#line:2755
    return OO000OOOO0OOO000O #line:2757
def TOOLS_autocount (OO00OOO0O000OO0OO ,OO00000O0O000O0O0 ):#line:2759
    ""#line:2760
    O000O0O00000O0O0O =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="监测机构",header =0 ,index_col =0 ).reset_index ()#line:2763
    OOOOOOOOO00O00OOO =pd .read_excel (peizhidir +"0（范例）上报单位.xls",sheet_name ="报告单位",header =0 ,index_col =0 ).reset_index ()#line:2766
    OO000OOO00O0O0OO0 =OOOOOOOOO00O00OOO [(OOOOOOOOO00O00OOO ["是否属于二级以上医疗机构"]=="是")]#line:2767
    if OO00000O0O000O0O0 =="药品":#line:2770
        OO00OOO0O000OO0OO =OO00OOO0O000OO0OO .reset_index (drop =True )#line:2771
        if "再次使用可疑药是否出现同样反应"not in OO00OOO0O000OO0OO .columns :#line:2772
            showinfo (title ="错误信息",message ="导入的疑似不是药品报告表。")#line:2773
            return 0 #line:2774
        OOOO0O0O00000O000 =Countall (OO00OOO0O000OO0OO ).df_org ("监测机构")#line:2776
        OOOO0O0O00000O000 =pd .merge (OOOO0O0O00000O000 ,O000O0O00000O0O0O ,on ="监测机构",how ="left")#line:2777
        OOOO0O0O00000O000 =OOOO0O0O00000O000 [["监测机构序号","监测机构","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2778
        O00OO000O0O0O0O00 =["药品数量指标","审核通过数","报告数量"]#line:2779
        OOOO0O0O00000O000 [O00OO000O0O0O0O00 ]=OOOO0O0O00000O000 [O00OO000O0O0O0O00 ].apply (lambda O00000OO0OOOOOOO0 :O00000OO0OOOOOOO0 .astype (int ))#line:2780
        OOOO00OOO0OO000O0 =Countall (OO00OOO0O000OO0OO ).df_user ()#line:2782
        OOOO00OOO0OO000O0 =pd .merge (OOOO00OOO0OO000O0 ,OOOOOOOOO00O00OOO ,on =["监测机构","单位名称"],how ="left")#line:2783
        OOOO00OOO0OO000O0 =pd .merge (OOOO00OOO0OO000O0 ,O000O0O00000O0O0O [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2784
        OOOO00OOO0OO000O0 =OOOO00OOO0OO000O0 [["监测机构序号","监测机构","单位名称","药品数量指标","报告数量","审核通过数","新严比","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2786
        O00OO000O0O0O0O00 =["药品数量指标","审核通过数","报告数量"]#line:2787
        OOOO00OOO0OO000O0 [O00OO000O0O0O0O00 ]=OOOO00OOO0OO000O0 [O00OO000O0O0O0O00 ].apply (lambda OO000000OOO0O0OO0 :OO000000OOO0O0OO0 .astype (int ))#line:2788
        O0O0O0000000O00O0 =pd .merge (OO000OOO00O0O0OO0 ,OOOO00OOO0OO000O0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2790
        O0O0O0000000O00O0 =O0O0O0000000O00O0 [(O0O0O0000000O00O0 ["审核通过数"]<1 )]#line:2791
        O0O0O0000000O00O0 =O0O0O0000000O00O0 [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2792
    if OO00000O0O000O0O0 =="器械":#line:2794
        OO00OOO0O000OO0OO =OO00OOO0O000OO0OO .reset_index (drop =True )#line:2795
        if "产品编号"not in OO00OOO0O000OO0OO .columns :#line:2796
            showinfo (title ="错误信息",message ="导入的疑似不是器械报告表。")#line:2797
            return 0 #line:2798
        OOOO0O0O00000O000 =Countall (OO00OOO0O000OO0OO ).df_org ("监测机构")#line:2800
        OOOO0O0O00000O000 =pd .merge (OOOO0O0O00000O000 ,O000O0O00000O0O0O ,on ="监测机构",how ="left")#line:2801
        OOOO0O0O00000O000 =OOOO0O0O00000O000 [["监测机构序号","监测机构","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2802
        O00OO000O0O0O0O00 =["器械数量指标","审核通过数","报告数量"]#line:2803
        OOOO0O0O00000O000 [O00OO000O0O0O0O00 ]=OOOO0O0O00000O000 [O00OO000O0O0O0O00 ].apply (lambda OOOOOO0OOO0O0O0OO :OOOOOO0OOO0O0O0OO .astype (int ))#line:2804
        OOOO00OOO0OO000O0 =Countall (OO00OOO0O000OO0OO ).df_user ()#line:2806
        OOOO00OOO0OO000O0 =pd .merge (OOOO00OOO0OO000O0 ,OOOOOOOOO00O00OOO ,on =["监测机构","单位名称"],how ="left")#line:2807
        OOOO00OOO0OO000O0 =pd .merge (OOOO00OOO0OO000O0 ,O000O0O00000O0O0O [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2808
        OOOO00OOO0OO000O0 =OOOO00OOO0OO000O0 [["监测机构序号","监测机构","单位名称","器械数量指标","报告数量","审核通过数","严重比","超时比"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2810
        O00OO000O0O0O0O00 =["器械数量指标","审核通过数","报告数量"]#line:2811
        OOOO00OOO0OO000O0 [O00OO000O0O0O0O00 ]=OOOO00OOO0OO000O0 [O00OO000O0O0O0O00 ].apply (lambda O0O00O0O0000O0000 :O0O00O0O0000O0000 .astype (int ))#line:2813
        O0O0O0000000O00O0 =pd .merge (OO000OOO00O0O0OO0 ,OOOO00OOO0OO000O0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2815
        O0O0O0000000O00O0 =O0O0O0000000O00O0 [(O0O0O0000000O00O0 ["审核通过数"]<1 )]#line:2816
        O0O0O0000000O00O0 =O0O0O0000000O00O0 [["监测机构","单位名称","报告数量","审核通过数","严重比","超时比"]]#line:2817
    if OO00000O0O000O0O0 =="化妆品":#line:2820
        OO00OOO0O000OO0OO =OO00OOO0O000OO0OO .reset_index (drop =True )#line:2821
        if "初步判断"not in OO00OOO0O000OO0OO .columns :#line:2822
            showinfo (title ="错误信息",message ="导入的疑似不是化妆品报告表。")#line:2823
            return 0 #line:2824
        OOOO0O0O00000O000 =Countall (OO00OOO0O000OO0OO ).df_org ("监测机构")#line:2826
        OOOO0O0O00000O000 =pd .merge (OOOO0O0O00000O000 ,O000O0O00000O0O0O ,on ="监测机构",how ="left")#line:2827
        OOOO0O0O00000O000 =OOOO0O0O00000O000 [["监测机构序号","监测机构","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号"],ascending =True ,na_position ="last").fillna (0 )#line:2828
        O00OO000O0O0O0O00 =["化妆品数量指标","审核通过数","报告数量"]#line:2829
        OOOO0O0O00000O000 [O00OO000O0O0O0O00 ]=OOOO0O0O00000O000 [O00OO000O0O0O0O00 ].apply (lambda O00000OO00O0OOOOO :O00000OO00O0OOOOO .astype (int ))#line:2830
        OOOO00OOO0OO000O0 =Countall (OO00OOO0O000OO0OO ).df_user ()#line:2832
        OOOO00OOO0OO000O0 =pd .merge (OOOO00OOO0OO000O0 ,OOOOOOOOO00O00OOO ,on =["监测机构","单位名称"],how ="left")#line:2833
        OOOO00OOO0OO000O0 =pd .merge (OOOO00OOO0OO000O0 ,O000O0O00000O0O0O [["监测机构序号","监测机构"]],on ="监测机构",how ="left")#line:2834
        OOOO00OOO0OO000O0 =OOOO00OOO0OO000O0 [["监测机构序号","监测机构","单位名称","化妆品数量指标","报告数量","审核通过数"]].sort_values (by =["监测机构序号","报告数量"],ascending =[True ,False ],na_position ="last").fillna (0 )#line:2835
        O00OO000O0O0O0O00 =["化妆品数量指标","审核通过数","报告数量"]#line:2836
        OOOO00OOO0OO000O0 [O00OO000O0O0O0O00 ]=OOOO00OOO0OO000O0 [O00OO000O0O0O0O00 ].apply (lambda O000O0O0OO0OO00O0 :O000O0O0OO0OO00O0 .astype (int ))#line:2837
        O0O0O0000000O00O0 =pd .merge (OO000OOO00O0O0OO0 ,OOOO00OOO0OO000O0 ,on =["监测机构","单位名称"],how ="left").sort_values (by =["监测机构"],ascending =True ,na_position ="last").fillna (0 )#line:2839
        O0O0O0000000O00O0 =O0O0O0000000O00O0 [(O0O0O0000000O00O0 ["审核通过数"]<1 )]#line:2840
        O0O0O0000000O00O0 =O0O0O0000000O00O0 [["监测机构","单位名称","报告数量","审核通过数"]]#line:2841
    O0O0OO0O0O0O00OO0 =filedialog .asksaveasfilename (title =u"保存文件",initialfile =OO00000O0O000O0O0 ,defaultextension ="xls",filetypes =[("Excel 97-2003 工作簿","*.xls")],)#line:2848
    OO0O00000O0OOO0O0 =pd .ExcelWriter (O0O0OO0O0O0O00OO0 ,engine ="xlsxwriter")#line:2849
    OOOO0O0O00000O000 .to_excel (OO0O00000O0OOO0O0 ,sheet_name ="监测机构")#line:2850
    OOOO00OOO0OO000O0 .to_excel (OO0O00000O0OOO0O0 ,sheet_name ="上报单位")#line:2851
    O0O0O0000000O00O0 .to_excel (OO0O00000O0OOO0O0 ,sheet_name ="未上报的二级以上医疗机构")#line:2852
    OO0O00000O0OOO0O0 .close ()#line:2853
    showinfo (title ="提示",message ="文件写入成功。")#line:2854
def TOOLS_web_view (O0O0O0000000OOOO0 ):#line:2856
    ""#line:2857
    import pybi as pbi #line:2858
    O00OO00O0O0000000 =pd .ExcelWriter ("temp_webview.xls")#line:2859
    O0O0O0000000OOOO0 .to_excel (O00OO00O0O0000000 ,sheet_name ="temp_webview")#line:2860
    O00OO00O0O0000000 .close ()#line:2861
    O0O0O0000000OOOO0 =pd .read_excel ("temp_webview.xls",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:2862
    OO0OO000O00OO0O00 =pbi .set_source (O0O0O0000000OOOO0 )#line:2863
    with pbi .flowBox ():#line:2864
        for OOO000O000O0O0O00 in O0O0O0000000OOOO0 .columns :#line:2865
            pbi .add_slicer (OO0OO000O00OO0O00 [OOO000O000O0O0O00 ])#line:2866
    pbi .add_table (OO0OO000O00OO0O00 )#line:2867
    O0O0OO000000OOOOO ="temp_webview.html"#line:2868
    pbi .to_html (O0O0OO000000OOOOO )#line:2869
    webbrowser .open_new_tab (O0O0OO000000OOOOO )#line:2870
def TOOLS_Autotable_0 (O000OO0OO0O0O0O00 ,O0OO0O0OO0O0OO000 ,*O00OOO00O0000O0O0 ):#line:2875
    ""#line:2876
    O000OO00OO0OOOOO0 =[O00OOO00O0000O0O0 [0 ],O00OOO00O0000O0O0 [1 ],O00OOO00O0000O0O0 [2 ]]#line:2878
    OO00OOO00OOOO000O =list (set ([O0O00000OO0OOOO00 for O0O00000OO0OOOO00 in O000OO00OO0OOOOO0 if O0O00000OO0OOOO00 !='']))#line:2880
    OO00OOO00OOOO000O .sort (key =O000OO00OO0OOOOO0 .index )#line:2881
    if len (OO00OOO00OOOO000O )==0 :#line:2882
        showinfo (title ="提示信息",message ="分组项请选择至少一列。")#line:2883
        return 0 #line:2884
    OO0O000O0OOOOO0OO =[O00OOO00O0000O0O0 [3 ],O00OOO00O0000O0O0 [4 ]]#line:2885
    if (O00OOO00O0000O0O0 [3 ]==""or O00OOO00O0000O0O0 [4 ]=="")and O0OO0O0OO0O0OO000 in ["数据透视","分组统计"]:#line:2886
        if "报告编码"in O000OO0OO0O0O0O00 .columns :#line:2887
            OO0O000O0OOOOO0OO [0 ]="报告编码"#line:2888
            OO0O000O0OOOOO0OO [1 ]="nunique"#line:2889
            text .insert (END ,"值项未配置,将使用报告编码进行唯一值计数。")#line:2890
        else :#line:2891
            showinfo (title ="提示信息",message ="值项未配置。")#line:2892
            return 0 #line:2893
    if O00OOO00O0000O0O0 [4 ]=="计数":#line:2895
        OO0O000O0OOOOO0OO [1 ]="count"#line:2896
    elif O00OOO00O0000O0O0 [4 ]=="求和":#line:2897
        OO0O000O0OOOOO0OO [1 ]="sum"#line:2898
    elif O00OOO00O0000O0O0 [4 ]=="唯一值计数":#line:2899
        OO0O000O0OOOOO0OO [1 ]="nunique"#line:2900
    if O0OO0O0OO0O0OO000 =="分组统计":#line:2903
        TABLE_tree_Level_2 (TOOLS_deep_view (O000OO0OO0O0O0O00 ,OO00OOO00OOOO000O ,OO0O000O0OOOOO0OO ,0 ),1 ,O000OO0OO0O0O0O00 )#line:2904
    if O0OO0O0OO0O0OO000 =="数据透视":#line:2906
        TABLE_tree_Level_2 (TOOLS_deep_view (O000OO0OO0O0O0O00 ,OO00OOO00OOOO000O ,OO0O000O0OOOOO0OO ,1 ),1 ,O000OO0OO0O0O0O00 )#line:2907
    if O0OO0O0OO0O0OO000 =="描述性统计(X)":#line:2909
        TABLE_tree_Level_2 (O000OO0OO0O0O0O00 [OO00OOO00OOOO000O ].describe ().reset_index (),1 ,O000OO0OO0O0O0O00 )#line:2910
    if O0OO0O0OO0O0OO000 =="拆分成字典(X-Y)":#line:2913
        O00OO000O0OO0OO0O =O000OO0OO0O0O0O00 .copy ()#line:2916
        O00OO000O0OO0OO0O ["c"]="c"#line:2917
        OOOOO0O000OO0OOO0 =O00OO000O0OO0OO0O .groupby ([O00OOO00O0000O0O0 [0 ]]).agg (计数 =("c","count")).reset_index ()#line:2918
        OOOOO0OO00O000OOO =OOOOO0O000OO0OOO0 .copy ()#line:2919
        OOOOO0OO00O000OOO [O00OOO00O0000O0O0 [0 ]]=OOOOO0OO00O000OOO [O00OOO00O0000O0O0 [0 ]].str .replace ("*","",regex =False )#line:2920
        OOOOO0OO00O000OOO ["所有项目"]=""#line:2921
        O0000OO0O000OOOOO =1 #line:2922
        O0OO0000O00OO0O00 =int (len (OOOOO0OO00O000OOO ))#line:2923
        for OOO000O0000OO0O0O ,O0O0OOO0OO0O0OOOO in OOOOO0OO00O000OOO .iterrows ():#line:2924
            O0O0OOO0000O00O00 =O00OO000O0OO0OO0O [(O00OO000O0OO0OO0O [O00OOO00O0000O0O0 [0 ]]==O0O0OOO0OO0O0OOOO [O00OOO00O0000O0O0 [0 ]])]#line:2926
            OO00OO0000OO0OO00 =str (Counter (TOOLS_get_list0 ("use("+str (O00OOO00O0000O0O0 [1 ])+").file",O0O0OOO0000O00O00 ,1000 ))).replace ("Counter({","{")#line:2928
            OO00OO0000OO0OO00 =OO00OO0000OO0OO00 .replace ("})","}")#line:2929
            import ast #line:2930
            OO0OO0OOO000O0O0O =ast .literal_eval (OO00OO0000OO0OO00 )#line:2931
            OO00OOO00000O0OOO =TOOLS_easyreadT (pd .DataFrame ([OO0OO0OOO000O0O0O ]))#line:2932
            OO00OOO00000O0OOO =OO00OOO00000O0OOO .rename (columns ={"逐条查看":"名称规整"})#line:2933
            PROGRAM_change_schedule (O0000OO0O000OOOOO ,O0OO0000O00OO0O00 )#line:2935
            O0000OO0O000OOOOO =O0000OO0O000OOOOO +1 #line:2936
            for O0OO0OOOOO0OOOO0O ,OOOOOO0OOOO0OO000 in OO00OOO00000O0OOO .iterrows ():#line:2937
                    if "分隔符"not in OOOOOO0OOOO0OO000 ["条目"]:#line:2938
                        OO0O0O0OO00O00O00 ="'"+str (OOOOOO0OOOO0OO000 ["条目"])+"':"+str (OOOOOO0OOOO0OO000 ["详细描述T"])+","#line:2939
                        OOOOO0OO00O000OOO .loc [OOO000O0000OO0O0O ,"所有项目"]=OOOOO0OO00O000OOO .loc [OOO000O0000OO0O0O ,"所有项目"]+OO0O0O0OO00O00O00 #line:2940
        OOOOO0OO00O000OOO ["所有项目"]="{"+OOOOO0OO00O000OOO ["所有项目"]+"}"#line:2942
        OOOOO0OO00O000OOO ["报表类型"]="dfx_deepview_"+str ([O00OOO00O0000O0O0 [0 ]])#line:2943
        TABLE_tree_Level_2 (OOOOO0OO00O000OOO .sort_values (by ="计数",ascending =[False ],na_position ="last"),1 ,O00OO000O0OO0OO0O )#line:2945
    if O0OO0O0OO0O0OO000 =="追加外部表格信息":#line:2947
        OO0O000O0O0000OO0 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2950
        O0000OO0O000OOOOO =[pd .read_excel (OOO000OO0O0O0000O ,header =0 ,sheet_name =0 )for OOO000OO0O0O0000O in OO0O000O0O0000OO0 ]#line:2951
        OO00O00O00O0OOO00 =pd .concat (O0000OO0O000OOOOO ,ignore_index =True ).drop_duplicates (OO00OOO00OOOO000O )#line:2952
        OO0O000OO0000O0O0 =pd .merge (O000OO0OO0O0O0O00 ,OO00O00O00O0OOO00 ,on =OO00OOO00OOOO000O ,how ="left")#line:2953
        TABLE_tree_Level_2 (OO0O000OO0000O0O0 ,1 ,OO0O000OO0000O0O0 )#line:2954
    if O0OO0O0OO0O0OO000 =="添加到外部表格":#line:2956
        OO0O000O0O0000OO0 =filedialog .askopenfilenames (filetypes =[("XLS",".xls"),("XLSX",".xlsx")])#line:2959
        O0000OO0O000OOOOO =[pd .read_excel (OOO0000OOOO000OOO ,header =0 ,sheet_name =0 )for OOO0000OOOO000OOO in OO0O000O0O0000OO0 ]#line:2960
        OO00O00O00O0OOO00 =pd .concat (O0000OO0O000OOOOO ,ignore_index =True ).drop_duplicates ()#line:2961
        OO0O000OO0000O0O0 =pd .merge (OO00O00O00O0OOO00 ,O000OO0OO0O0O0O00 .drop_duplicates (OO00OOO00OOOO000O ),on =OO00OOO00OOOO000O ,how ="left")#line:2962
        TABLE_tree_Level_2 (OO0O000OO0000O0O0 ,1 ,OO0O000OO0000O0O0 )#line:2963
    if O0OO0O0OO0O0OO000 =="饼图(XY)":#line:2966
        DRAW_make_one (O000OO0OO0O0O0O00 ,"饼图",O00OOO00O0000O0O0 [0 ],O00OOO00O0000O0O0 [1 ],"饼图")#line:2967
    if O0OO0O0OO0O0OO000 =="柱状图(XY)":#line:2968
        DRAW_make_one (O000OO0OO0O0O0O00 ,"柱状图",O00OOO00O0000O0O0 [0 ],O00OOO00O0000O0O0 [1 ],"柱状图")#line:2969
    if O0OO0O0OO0O0OO000 =="折线图(XY)":#line:2970
        DRAW_make_one (O000OO0OO0O0O0O00 ,"折线图",O00OOO00O0000O0O0 [0 ],O00OOO00O0000O0O0 [1 ],"折线图")#line:2971
    if O0OO0O0OO0O0OO000 =="托帕斯图(XY)":#line:2972
        DRAW_make_one (O000OO0OO0O0O0O00 ,"托帕斯图",O00OOO00O0000O0O0 [0 ],O00OOO00O0000O0O0 [1 ],"托帕斯图")#line:2973
    if O0OO0O0OO0O0OO000 =="堆叠柱状图（X-YZ）":#line:2974
        DRAW_make_mutibar (O000OO0OO0O0O0O00 ,O000OO00OO0OOOOO0 [1 ],O000OO00OO0OOOOO0 [2 ],O000OO00OO0OOOOO0 [0 ],O000OO00OO0OOOOO0 [1 ],O000OO00OO0OOOOO0 [2 ],"堆叠柱状图")#line:2975
def STAT_countx (OOO0O0OOO000O000O ):#line:2985
	""#line:2986
	return OOO0O0OOO000O000O .value_counts ().to_dict ()#line:2987
def STAT_countpx (OO0O0O0OO00O00OO0 ,OOOOO000O0OO0OOOO ):#line:2989
	""#line:2990
	return len (OO0O0O0OO00O00OO0 [(OO0O0O0OO00O00OO0 ==OOOOO000O0OO0OOOO )])#line:2991
def STAT_countnpx (OOO0O0OOO0000O0O0 ,OO0OOO0OO0O0OO0O0 ):#line:2993
	""#line:2994
	return len (OOO0O0OOO0000O0O0 [(OOO0O0OOO0000O0O0 not in OO0OOO0OO0O0OO0O0 )])#line:2995
def STAT_get_max (OO000O0O00000O0O0 ):#line:2997
	""#line:2998
	return OO000O0O00000O0O0 .value_counts ().max ()#line:2999
def STAT_get_mean (OOOO0O0OOOO0OOO00 ):#line:3001
	""#line:3002
	return round (OOOO0O0OOOO0OOO00 .value_counts ().mean (),2 )#line:3003
def STAT_get_std (OOO0OOO0OOOO00O0O ):#line:3005
	""#line:3006
	return round (OOO0OOO0OOOO00O0O .value_counts ().std (ddof =1 ),2 )#line:3007
def STAT_get_95ci (OOO0OO0OOOO000OOO ):#line:3009
	""#line:3010
	O0OO0O0O000O0000O =0.95 #line:3011
	OO00000O0OOO0OOOO =OOO0OO0OOOO000OOO .value_counts ().tolist ()#line:3012
	if len (OO00000O0OOO0OOOO )<30 :#line:3013
		OOOOOOOOOO000O0O0 =st .t .interval (O0OO0O0O000O0000O ,df =len (OO00000O0OOO0OOOO )-1 ,loc =np .mean (OO00000O0OOO0OOOO ),scale =st .sem (OO00000O0OOO0OOOO ))#line:3014
	else :#line:3015
		OOOOOOOOOO000O0O0 =st .norm .interval (O0OO0O0O000O0000O ,loc =np .mean (OO00000O0OOO0OOOO ),scale =st .sem (OO00000O0OOO0OOOO ))#line:3016
	return round (OOOOOOOOOO000O0O0 [1 ],2 )#line:3017
def STAT_get_mean_std_ci (OO0OOO0OO00OOOO00 ,OOO0OOOO000OO0O00 ):#line:3019
	""#line:3020
	warnings .filterwarnings ("ignore")#line:3021
	OO0OO0OO0OO0OOOO0 =TOOLS_strdict_to_pd (str (OO0OOO0OO00OOOO00 ))["content"].values /OOO0OOOO000OO0O00 #line:3022
	OOOO000OOOOOOOO00 =round (OO0OO0OO0OO0OOOO0 .mean (),2 )#line:3023
	O0O00OO0O0OO0O00O =round (OO0OO0OO0OO0OOOO0 .std (ddof =1 ),2 )#line:3024
	if len (OO0OO0OO0OO0OOOO0 )<30 :#line:3026
		OO0000OOO0OOO000O =st .t .interval (0.95 ,df =len (OO0OO0OO0OO0OOOO0 )-1 ,loc =np .mean (OO0OO0OO0OO0OOOO0 ),scale =st .sem (OO0OO0OO0OO0OOOO0 ))#line:3027
	else :#line:3028
		OO0000OOO0OOO000O =st .norm .interval (0.95 ,loc =np .mean (OO0OO0OO0OO0OOOO0 ),scale =st .sem (OO0OO0OO0OO0OOOO0 ))#line:3029
	return pd .Series ((OOOO000OOOOOOOO00 ,O0O00OO0O0OO0O00O ,OO0000OOO0OOO000O [1 ]))#line:3033
def STAT_findx_value (OOOO00OOO0OO0OOOO ,O00OO0OO0O0OOOOO0 ):#line:3035
	""#line:3036
	warnings .filterwarnings ("ignore")#line:3037
	O000OO0O0OOO0OOOO =TOOLS_strdict_to_pd (str (OOOO00OOO0OO0OOOO ))#line:3038
	O00O000OO000O000O =O000OO0O0OOO0OOOO .where (O000OO0O0OOO0OOOO ["index"]==str (O00OO0OO0O0OOOOO0 ))#line:3040
	print (O00O000OO000O000O )#line:3041
	return O00O000OO000O000O #line:3042
def STAT_judge_x (O000O00O0OO0OO0OO ,OO00O0OOO0O0OO00O ):#line:3044
	""#line:3045
	for OO00O00OO0OOO00OO in OO00O0OOO0O0OO00O :#line:3046
		if O000O00O0OO0OO0OO .find (OO00O00OO0OOO00OO )>-1 :#line:3047
			return 1 #line:3048
def STAT_recent30 (OO00OOOO000OO00O0 ,OOO00OO0000OOO000 ):#line:3050
	""#line:3051
	import datetime #line:3052
	OOOOOO0OOO00OOOO0 =OO00OOOO000OO00O0 [(OO00OOOO000OO00O0 ["报告日期"].dt .date >(datetime .date .today ()-datetime .timedelta (days =30 )))]#line:3056
	O0OO00OOO0O000OO0 =OOOOOO0OOO00OOOO0 .drop_duplicates (["报告编码"]).groupby (OOO00OO0000OOO000 ).agg (最近30天报告数 =("报告编码","nunique"),最近30天报告严重伤害数 =("伤害",lambda O0O0O0O00000OOOOO :STAT_countpx (O0O0O0O00000OOOOO .values ,"严重伤害")),最近30天报告死亡数量 =("伤害",lambda O0OO00O0O0O00OOO0 :STAT_countpx (O0OO00O0O0O00OOO0 .values ,"死亡")),最近30天报告单位个数 =("单位名称","nunique"),).reset_index ()#line:3063
	O0OO00OOO0O000OO0 =STAT_basic_risk (O0OO00OOO0O000OO0 ,"最近30天报告数","最近30天报告严重伤害数","最近30天报告死亡数量","最近30天报告单位个数").fillna (0 )#line:3064
	O0OO00OOO0O000OO0 =O0OO00OOO0O000OO0 .rename (columns ={"风险评分":"最近30天风险评分"})#line:3066
	return O0OO00OOO0O000OO0 #line:3067
def STAT_PPR_ROR_1 (O0O0O0OO00O0O0000 ,OOOO0O00000OO00O0 ,O0OO0O0O0OO0O0O00 ,O000O00OO0000O000 ,OOOO0O0OO00OO00OO ):#line:3070
    ""#line:3071
    OO000OOO0OO0O0O00 =OOOO0O0OO00OO00OO [(OOOO0O0OO00OO00OO [O0O0O0OO00O0O0000 ]==OOOO0O00000OO00O0 )]#line:3074
    O0OO0000000OO00OO =OO000OOO0OO0O0O00 .loc [OO000OOO0OO0O0O00 [O0OO0O0O0OO0O0O00 ].str .contains (O000O00OO0000O000 ,na =False )]#line:3075
    OOO000OOO0OOOO0O0 =OOOO0O0OO00OO00OO [(OOOO0O0OO00OO00OO [O0O0O0OO00O0O0000 ]!=OOOO0O00000OO00O0 )]#line:3076
    O00OOO0O0O0O00OOO =OOO000OOO0OOOO0O0 .loc [OOO000OOO0OOOO0O0 [O0OO0O0O0OO0O0O00 ].str .contains (O000O00OO0000O000 ,na =False )]#line:3077
    O000OO000OOO0O00O =(len (O0OO0000000OO00OO ),(len (OO000OOO0OO0O0O00 )-len (O0OO0000000OO00OO )),len (O00OOO0O0O0O00OOO ),(len (OOO000OOO0OOOO0O0 )-len (O00OOO0O0O0O00OOO )))#line:3078
    if len (O0OO0000000OO00OO )>0 :#line:3079
        O00OOOOOOOOOO0000 =STAT_PPR_ROR_0 (len (O0OO0000000OO00OO ),(len (OO000OOO0OO0O0O00 )-len (O0OO0000000OO00OO )),len (O00OOO0O0O0O00OOO ),(len (OOO000OOO0OOOO0O0 )-len (O00OOO0O0O0O00OOO )))#line:3080
    else :#line:3081
        O00OOOOOOOOOO0000 =(0 ,0 ,0 ,0 ,0 )#line:3082
    O000O00OOO00OO000 =len (OO000OOO0OO0O0O00 )#line:3085
    if O000O00OOO00OO000 ==0 :#line:3086
        O000O00OOO00OO000 =0.5 #line:3087
    return (O000O00OO0000O000 ,len (O0OO0000000OO00OO ),round (len (O0OO0000000OO00OO )/O000O00OOO00OO000 *100 ,2 ),round (O00OOOOOOOOOO0000 [0 ],2 ),round (O00OOOOOOOOOO0000 [1 ],2 ),round (O00OOOOOOOOOO0000 [2 ],2 ),round (O00OOOOOOOOOO0000 [3 ],2 ),round (O00OOOOOOOOOO0000 [4 ],2 ),str (O000OO000OOO0O00O ),)#line:3098
def STAT_basic_risk (OOO0000OO0OOO00O0 ,OO0OOO0O0O000OOOO ,O00OOO00OOO0O0O00 ,O00OOOO000OO00000 ,O0000O0OO000O000O ):#line:3102
	""#line:3103
	OOO0000OO0OOO00O0 ["风险评分"]=0 #line:3104
	OOO0000OO0OOO00O0 .loc [((OOO0000OO0OOO00O0 [OO0OOO0O0O000OOOO ]>=3 )&(OOO0000OO0OOO00O0 [O00OOO00OOO0O0O00 ]>=1 ))|(OOO0000OO0OOO00O0 [OO0OOO0O0O000OOOO ]>=5 ),"风险评分"]=OOO0000OO0OOO00O0 ["风险评分"]+5 #line:3105
	OOO0000OO0OOO00O0 .loc [(OOO0000OO0OOO00O0 [O00OOO00OOO0O0O00 ]>=3 ),"风险评分"]=OOO0000OO0OOO00O0 ["风险评分"]+1 #line:3106
	OOO0000OO0OOO00O0 .loc [(OOO0000OO0OOO00O0 [O00OOOO000OO00000 ]>=1 ),"风险评分"]=OOO0000OO0OOO00O0 ["风险评分"]+10 #line:3107
	OOO0000OO0OOO00O0 ["风险评分"]=OOO0000OO0OOO00O0 ["风险评分"]+OOO0000OO0OOO00O0 [O0000O0OO000O000O ]/100 #line:3108
	return OOO0000OO0OOO00O0 #line:3109
def STAT_PPR_ROR_0 (OO0000O0OO000O0OO ,OOOO0O0OO00OOOO00 ,O0O00000O0OOOOO00 ,OO0O0OO0OOO00O0O0 ):#line:3112
    ""#line:3113
    if OO0000O0OO000O0OO *OOOO0O0OO00OOOO00 *O0O00000O0OOOOO00 *OO0O0OO0OOO00O0O0 ==0 :#line:3118
        OO0000O0OO000O0OO =OO0000O0OO000O0OO +1 #line:3119
        OOOO0O0OO00OOOO00 =OOOO0O0OO00OOOO00 +1 #line:3120
        O0O00000O0OOOOO00 =O0O00000O0OOOOO00 +1 #line:3121
        OO0O0OO0OOO00O0O0 =OO0O0OO0OOO00O0O0 +1 #line:3122
    OOO000OOO00000O00 =(OO0000O0OO000O0OO /(OO0000O0OO000O0OO +OOOO0O0OO00OOOO00 ))/(O0O00000O0OOOOO00 /(O0O00000O0OOOOO00 +OO0O0OO0OOO00O0O0 ))#line:3123
    OO0OO000000O0O0O0 =math .sqrt (1 /OO0000O0OO000O0OO -1 /(OO0000O0OO000O0OO +OOOO0O0OO00OOOO00 )+1 /O0O00000O0OOOOO00 -1 /(O0O00000O0OOOOO00 +OO0O0OO0OOO00O0O0 ))#line:3124
    O0000OOOOOO0000O0 =(math .exp (math .log (OOO000OOO00000O00 )-1.96 *OO0OO000000O0O0O0 ),math .exp (math .log (OOO000OOO00000O00 )+1.96 *OO0OO000000O0O0O0 ),)#line:3128
    OOO0OO0O0O0000OOO =(OO0000O0OO000O0OO /O0O00000O0OOOOO00 )/(OOOO0O0OO00OOOO00 /OO0O0OO0OOO00O0O0 )#line:3129
    O00O0O00OO0O00OOO =math .sqrt (1 /OO0000O0OO000O0OO +1 /OOOO0O0OO00OOOO00 +1 /O0O00000O0OOOOO00 +1 /OO0O0OO0OOO00O0O0 )#line:3130
    O000O0OOOOO0OOO0O =(math .exp (math .log (OOO0OO0O0O0000OOO )-1.96 *O00O0O00OO0O00OOO ),math .exp (math .log (OOO0OO0O0O0000OOO )+1.96 *O00O0O00OO0O00OOO ),)#line:3134
    OO0OOOOO0O00O00OO =((OO0000O0OO000O0OO *OOOO0O0OO00OOOO00 -OOOO0O0OO00OOOO00 *O0O00000O0OOOOO00 )*(OO0000O0OO000O0OO *OOOO0O0OO00OOOO00 -OOOO0O0OO00OOOO00 *O0O00000O0OOOOO00 )*(OO0000O0OO000O0OO +OOOO0O0OO00OOOO00 +O0O00000O0OOOOO00 +OO0O0OO0OOO00O0O0 ))/((OO0000O0OO000O0OO +OOOO0O0OO00OOOO00 )*(O0O00000O0OOOOO00 +OO0O0OO0OOO00O0O0 )*(OO0000O0OO000O0OO +O0O00000O0OOOOO00 )*(OOOO0O0OO00OOOO00 +OO0O0OO0OOO00O0O0 ))#line:3137
    return OOO0OO0O0O0000OOO ,O000O0OOOOO0OOO0O [0 ],OOO000OOO00000O00 ,O0000OOOOOO0000O0 [0 ],OO0OOOOO0O00O00OO #line:3138
def STAT_find_keyword_risk (OO00O000O0O0OO0O0 ,OOOOO0OO0O000O00O ,O000OO0OO0OO0O00O ,O000O0O0OO0OO0OOO ,OO0O0OO00O000OO0O ):#line:3140
		""#line:3141
		OO00O000O0O0OO0O0 =OO00O000O0O0OO0O0 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3142
		OO00O0000O0OOOOO0 =OO00O000O0O0OO0O0 .groupby (OOOOO0OO0O000O00O ).agg (证号关键字总数量 =(O000OO0OO0OO0O00O ,"count"),包含元素个数 =(O000O0O0OO0OO0OOO ,"nunique"),包含元素 =(O000O0O0OO0OO0OOO ,STAT_countx ),).reset_index ()#line:3147
		OOO0O000OOOOO0O0O =OOOOO0OO0O000O00O .copy ()#line:3149
		OOO0O000OOOOO0O0O .append (O000O0O0OO0OO0OOO )#line:3150
		O0OOOOOO0OOOOOO0O =OO00O000O0O0OO0O0 .groupby (OOO0O000OOOOO0O0O ).agg (计数 =(O000O0O0OO0OO0OOO ,"count"),严重伤害数 =("伤害",lambda O0O0O0O0000OOOOO0 :STAT_countpx (O0O0O0O0000OOOOO0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O0000000O0OOO00 :STAT_countpx (O0O0000000O0OOO00 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3157
		OOOOO00OOOOOO00O0 =OOO0O000OOOOO0O0O .copy ()#line:3160
		OOOOO00OOOOOO00O0 .remove ("关键字")#line:3161
		O00OOO00O00O0O0OO =OO00O000O0O0OO0O0 .groupby (OOOOO00OOOOOO00O0 ).agg (该元素总数 =(O000O0O0OO0OO0OOO ,"count"),).reset_index ()#line:3164
		O0OOOOOO0OOOOOO0O ["证号总数"]=OO0O0OO00O000OO0O #line:3166
		OO0O0O0OOO0000OO0 =pd .merge (O0OOOOOO0OOOOOO0O ,OO00O0000O0OOOOO0 ,on =OOOOO0OO0O000O00O ,how ="left")#line:3167
		if len (OO0O0O0OOO0000OO0 )>0 :#line:3172
			OO0O0O0OOO0000OO0 [['数量均值','数量标准差','数量CI']]=OO0O0O0OOO0000OO0 .包含元素 .apply (lambda OOOO000OOO00OOOOO :STAT_get_mean_std_ci (OOOO000OOO00OOOOO ,1 ))#line:3173
		return OO0O0O0OOO0000OO0 #line:3176
def STAT_find_risk (OOOO0OOO00O0OOOO0 ,O00O0000O0OO0OOO0 ,O0000OO0O0OO00O0O ,OO0000OOO0OOOO0O0 ):#line:3182
		""#line:3183
		OOOO0OOO00O0OOOO0 =OOOO0OOO00O0OOOO0 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:3184
		O0OOO000O00O0O00O =OOOO0OOO00O0OOOO0 .groupby (O00O0000O0OO0OOO0 ).agg (证号总数量 =(O0000OO0O0OO00O0O ,"count"),包含元素个数 =(OO0000OOO0OOOO0O0 ,"nunique"),包含元素 =(OO0000OOO0OOOO0O0 ,STAT_countx ),均值 =(OO0000OOO0OOOO0O0 ,STAT_get_mean ),标准差 =(OO0000OOO0OOOO0O0 ,STAT_get_std ),CI上限 =(OO0000OOO0OOOO0O0 ,STAT_get_95ci ),).reset_index ()#line:3192
		OO00O0000O0O0OOO0 =O00O0000O0OO0OOO0 .copy ()#line:3194
		OO00O0000O0O0OOO0 .append (OO0000OOO0OOOO0O0 )#line:3195
		OOO0O00OO0000O0O0 =OOOO0OOO00O0OOOO0 .groupby (OO00O0000O0O0OOO0 ).agg (计数 =(OO0000OOO0OOOO0O0 ,"count"),严重伤害数 =("伤害",lambda O0000O00O0OOOO000 :STAT_countpx (O0000O00O0OOOO000 .values ,"严重伤害")),死亡数量 =("伤害",lambda OO000000OO0OO0O00 :STAT_countpx (OO000000OO0OO0O00 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:3202
		OOOO0OOOO00O0O000 =pd .merge (OOO0O00OO0000O0O0 ,O0OOO000O00O0O00O ,on =O00O0000O0OO0OOO0 ,how ="left")#line:3204
		OOOO0OOOO00O0O000 ["风险评分"]=0 #line:3206
		OOOO0OOOO00O0O000 ["报表类型"]="dfx_findrisk"+OO0000OOO0OOOO0O0 #line:3207
		OOOO0OOOO00O0O000 .loc [((OOOO0OOOO00O0O000 ["计数"]>=3 )&(OOOO0OOOO00O0O000 ["严重伤害数"]>=1 )|(OOOO0OOOO00O0O000 ["计数"]>=5 )),"风险评分"]=OOOO0OOOO00O0O000 ["风险评分"]+5 #line:3208
		OOOO0OOOO00O0O000 .loc [(OOOO0OOOO00O0O000 ["计数"]>=(OOOO0OOOO00O0O000 ["均值"]+OOOO0OOOO00O0O000 ["标准差"])),"风险评分"]=OOOO0OOOO00O0O000 ["风险评分"]+1 #line:3209
		OOOO0OOOO00O0O000 .loc [(OOOO0OOOO00O0O000 ["计数"]>=OOOO0OOOO00O0O000 ["CI上限"]),"风险评分"]=OOOO0OOOO00O0O000 ["风险评分"]+1 #line:3210
		OOOO0OOOO00O0O000 .loc [(OOOO0OOOO00O0O000 ["严重伤害数"]>=3 )&(OOOO0OOOO00O0O000 ["风险评分"]>=7 ),"风险评分"]=OOOO0OOOO00O0O000 ["风险评分"]+1 #line:3211
		OOOO0OOOO00O0O000 .loc [(OOOO0OOOO00O0O000 ["死亡数量"]>=1 ),"风险评分"]=OOOO0OOOO00O0O000 ["风险评分"]+10 #line:3212
		OOOO0OOOO00O0O000 ["风险评分"]=OOOO0OOOO00O0O000 ["风险评分"]+OOOO0OOOO00O0O000 ["单位个数"]/100 #line:3213
		OOOO0OOOO00O0O000 =OOOO0OOOO00O0O000 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:3214
		return OOOO0OOOO00O0O000 #line:3216
def TABLE_tree_Level_2 (O0OO00000O0OO0000 ,O0O00000OO00OOOOO ,O0O00000OOOOO0OOO ,*O0O00OOO0O0O000OO ):#line:3223
    ""#line:3224
    try :#line:3226
        OOOO0O0O0000O0OOO =O0OO00000O0OO0000 .columns #line:3227
    except :#line:3228
        return 0 #line:3229
    if "报告编码"in O0OO00000O0OO0000 .columns :#line:3231
        O0O00000OO00OOOOO =0 #line:3232
    try :#line:3233
        O00O0OOOO0OOO0OO0 =len (np .unique (O0OO00000O0OO0000 ["注册证编号/曾用注册证编号"].values ))#line:3234
    except :#line:3235
        O00O0OOOO0OOO0OO0 =10 #line:3236
    OOOO000000OOOOOO0 =Toplevel ()#line:3239
    OOOO000000OOOOOO0 .title ("报表查看器")#line:3240
    OOOO0OOOOOOOOOO00 =OOOO000000OOOOOO0 .winfo_screenwidth ()#line:3241
    OOO0O00O000OOOO00 =OOOO000000OOOOOO0 .winfo_screenheight ()#line:3243
    OOO0O0OOO0OOO00O0 =1350 #line:3245
    OOO0O000OO0OO00O0 =600 #line:3246
    try :#line:3247
        if O0O00OOO0O0O000OO [0 ]=="tools_x":#line:3248
           OOO0O000OO0OO00O0 =60 #line:3249
    except :#line:3250
            pass #line:3251
    O0OOOOOOOO0OO0O0O =(OOOO0OOOOOOOOOO00 -OOO0O0OOO0OOO00O0 )/2 #line:3254
    OOOOOO00000OO0O0O =(OOO0O00O000OOOO00 -OOO0O000OO0OO00O0 )/2 #line:3255
    OOOO000000OOOOOO0 .geometry ("%dx%d+%d+%d"%(OOO0O0OOO0OOO00O0 ,OOO0O000OO0OO00O0 ,O0OOOOOOOO0OO0O0O ,OOOOOO00000OO0O0O ))#line:3256
    OOO0OOO00OOOOOOOO =ttk .Frame (OOOO000000OOOOOO0 ,width =1310 ,height =20 )#line:3259
    OOO0OOO00OOOOOOOO .pack (side =TOP )#line:3260
    O0OO0O0OO00OOO000 =ttk .Frame (OOOO000000OOOOOO0 ,width =1310 ,height =20 )#line:3261
    O0OO0O0OO00OOO000 .pack (side =BOTTOM )#line:3262
    OO0O0000OO0000000 =ttk .Frame (OOOO000000OOOOOO0 ,width =1310 ,height =600 )#line:3263
    OO0O0000OO0000000 .pack (fill ="both",expand ="false")#line:3264
    if O0O00000OO00OOOOO ==0 :#line:3268
        PROGRAM_Menubar (OOOO000000OOOOOO0 ,O0OO00000O0OO0000 ,O0O00000OO00OOOOO ,O0O00000OOOOO0OOO )#line:3269
    try :#line:3272
        OO000000O000O0OO0 =StringVar ()#line:3273
        OO000000O000O0OO0 .set ("产品类别")#line:3274
        def O0000OOOOOOO00O00 (*OO00OO0O00O00O0O0 ):#line:3275
            OO000000O000O0OO0 .set (OOO000000O000O000 .get ())#line:3276
        OO00O0O0O0OO0O0OO =StringVar ()#line:3277
        OO00O0O0O0OO0O0OO .set ("无源|诊断试剂")#line:3278
        O00OO0O0OO0OOO000 =Label (OOO0OOO00OOOOOOOO ,text ="")#line:3279
        O00OO0O0OO0OOO000 .pack (side =LEFT )#line:3280
        O00OO0O0OO0OOO000 =Label (OOO0OOO00OOOOOOOO ,text ="位置：")#line:3281
        O00OO0O0OO0OOO000 .pack (side =LEFT )#line:3282
        O0000OOOO00O000O0 =StringVar ()#line:3283
        OOO000000O000O000 =ttk .Combobox (OOO0OOO00OOOOOOOO ,width =12 ,height =30 ,state ="readonly",textvariable =O0000OOOO00O000O0 )#line:3286
        OOO000000O000O000 ["values"]=O0OO00000O0OO0000 .columns .tolist ()#line:3287
        OOO000000O000O000 .current (0 )#line:3288
        OOO000000O000O000 .bind ("<<ComboboxSelected>>",O0000OOOOOOO00O00 )#line:3289
        OOO000000O000O000 .pack (side =LEFT )#line:3290
        O00O0OOO0O0OO000O =Label (OOO0OOO00OOOOOOOO ,text ="检索：")#line:3291
        O00O0OOO0O0OO000O .pack (side =LEFT )#line:3292
        O0000OOOO0OOO0000 =Entry (OOO0OOO00OOOOOOOO ,width =12 ,textvariable =OO00O0O0O0OO0O0OO ).pack (side =LEFT )#line:3293
        def O0O000OO0OO00OO0O ():#line:3295
            pass #line:3296
        O0OO0OO0OOOO0OOO0 =Button (OOO0OOO00OOOOOOOO ,text ="导出",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_save_dict (O0OO00000O0OO0000 ),)#line:3310
        O0OO0OO0OOOO0OOO0 .pack (side =LEFT )#line:3311
        O00O00OOOO0OO0OOO =Button (OOO0OOO00OOOOOOOO ,text ="视图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyreadT (O0OO00000O0OO0000 ),1 ,O0O00000OOOOO0OOO ),)#line:3320
        if "详细描述T"not in O0OO00000O0OO0000 .columns :#line:3321
            O00O00OOOO0OO0OOO .pack (side =LEFT )#line:3322
        O00O00OOOO0OO0OOO =Button (OOO0OOO00OOOOOOOO ,text ="网",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_web_view (O0OO00000O0OO0000 ),)#line:3332
        if "详细描述T"not in O0OO00000O0OO0000 .columns :#line:3333
            pass #line:3334
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="含",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .loc [O0OO00000O0OO0000 [OO000000O000O0OO0 .get ()].astype (str ).str .contains (str (OO00O0O0O0OO0O0OO .get ()),na =False )],1 ,O0O00000OOOOO0OOO ,),)#line:3353
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3354
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="无",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .loc [~O0OO00000O0OO0000 [OO000000O000O0OO0 .get ()].astype (str ).str .contains (str (OO00O0O0O0OO0O0OO .get ()),na =False )],1 ,O0O00000OOOOO0OOO ,),)#line:3371
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3372
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="大",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .loc [O0OO00000O0OO0000 [OO000000O000O0OO0 .get ()].astype (float )>float (OO00O0O0O0OO0O0OO .get ())],1 ,O0O00000OOOOO0OOO ,),)#line:3387
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3388
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="小",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .loc [O0OO00000O0OO0000 [OO000000O000O0OO0 .get ()].astype (float )<float (OO00O0O0O0OO0O0OO .get ())],1 ,O0O00000OOOOO0OOO ,),)#line:3403
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3404
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="等",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .loc [O0OO00000O0OO0000 [OO000000O000O0OO0 .get ()].astype (float )==float (OO00O0O0O0OO0O0OO .get ())],1 ,O0O00000OOOOO0OOO ,),)#line:3419
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3420
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="式",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_findin (O0OO00000O0OO0000 ,O0O00000OOOOO0OOO ))#line:3429
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3430
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="前",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .head (int (OO00O0O0O0OO0O0OO .get ())),1 ,O0O00000OOOOO0OOO ,),)#line:3445
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3446
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="升",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .sort_values (by =(OO000000O000O0OO0 .get ()),ascending =[True ],na_position ="last"),1 ,O0O00000OOOOO0OOO ,),)#line:3461
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3462
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="降",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .sort_values (by =(OO000000O000O0OO0 .get ()),ascending =[False ],na_position ="last"),1 ,O0O00000OOOOO0OOO ,),)#line:3477
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3478
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="重",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 .drop_duplicates (OO000000O000O0OO0 .get ()),1 ,O0O00000OOOOO0OOO ,),)#line:3494
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3495
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="统",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (STAT_pinzhong (O0OO00000O0OO0000 ,OO000000O000O0OO0 .get (),0 ),1 ,O0O00000OOOOO0OOO ,),)#line:3510
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3511
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="SQL",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_sql (O0OO00000O0OO0000 ),)#line:3522
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3523
    except :#line:3526
        pass #line:3527
    if ini ["模式"]!="其他":#line:3530
        OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="近月",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 [(O0OO00000O0OO0000 ["最近30天报告单位个数"]>=1 )],1 ,O0O00000OOOOO0OOO ,),)#line:3543
        if "最近30天报告数"in O0OO00000O0OO0000 .columns :#line:3544
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3545
        O0OO0OO0OOOOOOO0O =Button (OOO0OOO00OOOOOOOO ,text ="图表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (O0OO00000O0OO0000 ),)#line:3557
        if O0O00000OO00OOOOO !=0 :#line:3558
            O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3559
        def O0O0OO00OOO0O0OO0 ():#line:3564
            pass #line:3565
        if O0O00000OO00OOOOO ==0 :#line:3568
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="精简",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_easyread2 (O0OO00000O0OO0000 ),1 ,O0O00000OOOOO0OOO ,),)#line:3582
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3583
        if O0O00000OO00OOOOO ==0 :#line:3586
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="证号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_zhenghao (),1 ,O0O00000OOOOO0OOO ,),)#line:3600
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3601
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0OO00000O0OO0000 ).df_zhenghao ()))#line:3610
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3611
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="批号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_pihao (),1 ,O0O00000OOOOO0OOO ,),)#line:3626
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3627
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0OO00000O0OO0000 ).df_pihao ()))#line:3636
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3637
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="型号",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_xinghao (),1 ,O0O00000OOOOO0OOO ,),)#line:3652
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3653
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0OO00000O0OO0000 ).df_xinghao ()))#line:3662
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3663
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="规格",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_guige (),1 ,O0O00000OOOOO0OOO ,),)#line:3678
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3679
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="图",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_pre (Countall (O0OO00000O0OO0000 ).df_guige ()))#line:3688
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3689
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="企业",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_chiyouren (),1 ,O0O00000OOOOO0OOO ,),)#line:3704
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3705
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="县区",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_org ("监测机构"),1 ,O0O00000OOOOO0OOO ,),)#line:3721
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3722
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="单位",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_user (),1 ,O0O00000OOOOO0OOO ,),)#line:3735
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3736
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="年龄",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_age (),1 ,O0O00000OOOOO0OOO ,),)#line:3750
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3751
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="时隔",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_deep_view (O0OO00000O0OO0000 ,["时隔"],["报告编码","nunique"],0 ),1 ,O0O00000OOOOO0OOO ,),)#line:3765
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3766
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (Countall (O0OO00000O0OO0000 ).df_psur (),1 ,O0O00000OOOOO0OOO ,),)#line:3780
            if "UDI"not in O0OO00000O0OO0000 .columns :#line:3781
                OO0O0OO0O00O000OO .pack (side =LEFT )#line:3782
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="表现",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (TOOLS_get_guize2 (O0OO00000O0OO0000 ),1 ,O0O00000OOOOO0OOO ,),)#line:3795
            if "UDI"in O0OO00000O0OO0000 .columns :#line:3796
                OO0O0OO0O00O000OO .pack (side =LEFT )#line:3797
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="发生时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_time (O0OO00000O0OO0000 ,"事件发生日期",0 ),)#line:3806
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3807
            OO0O0OO0O00O000OO =Button (OOO0OOO00OOOOOOOO ,text ="报告时间",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :DRAW_make_one (TOOLS_time (O0OO00000O0OO0000 ,"报告日期",1 ),"时间托帕斯图","time","报告总数","超级托帕斯图(严重伤害数)"),)#line:3817
            OO0O0OO0O00O000OO .pack (side =LEFT )#line:3818
    try :#line:3824
        OO0O000O000OO000O =ttk .Label (O0OO0O0OO00OOO000 ,text ="方法：")#line:3826
        OO0O000O000OO000O .pack (side =LEFT )#line:3827
        OO00OOOO00O00OOO0 =StringVar ()#line:3828
        O0O0000O000000O0O =ttk .Combobox (O0OO0O0OO00OOO000 ,width =15 ,textvariable =OO00OOOO00O00OOO0 ,state ='readonly')#line:3829
        O0O0000O000000O0O ['values']=("分组统计","数据透视","拆分成字典(X-Y)","描述性统计(X)","饼图(XY)","柱状图(XY)","折线图(XY)","托帕斯图(XY)","堆叠柱状图（X-YZ）","追加外部表格信息","添加到外部表格")#line:3830
        O0O0000O000000O0O .pack (side =LEFT )#line:3834
        O0O0000O000000O0O .current (0 )#line:3835
        O0O000O000000O00O =ttk .Label (O0OO0O0OO00OOO000 ,text ="分组列（X-Y-Z）:")#line:3836
        O0O000O000000O00O .pack (side =LEFT )#line:3837
        OO0O00OO0OOOOOOO0 =StringVar ()#line:3840
        OOO00O0OO0O00O00O =ttk .Combobox (O0OO0O0OO00OOO000 ,width =15 ,textvariable =OO0O00OO0OOOOOOO0 ,state ='readonly')#line:3841
        OOO00O0OO0O00O00O ['values']=O0OO00000O0OO0000 .columns .tolist ()#line:3842
        OOO00O0OO0O00O00O .pack (side =LEFT )#line:3843
        O0OO00OO00O00OO0O =StringVar ()#line:3844
        OOOOO00O00O000000 =ttk .Combobox (O0OO0O0OO00OOO000 ,width =15 ,textvariable =O0OO00OO00O00OO0O ,state ='readonly')#line:3845
        OOOOO00O00O000000 ['values']=O0OO00000O0OO0000 .columns .tolist ()#line:3846
        OOOOO00O00O000000 .pack (side =LEFT )#line:3847
        O0O0O00000OOO0O0O =StringVar ()#line:3848
        OOOO00000OO00O0OO =ttk .Combobox (O0OO0O0OO00OOO000 ,width =15 ,textvariable =O0O0O00000OOO0O0O ,state ='readonly')#line:3849
        OOOO00000OO00O0OO ['values']=O0OO00000O0OO0000 .columns .tolist ()#line:3850
        OOOO00000OO00O0OO .pack (side =LEFT )#line:3851
        OOOOOO0000OOOO0O0 =StringVar ()#line:3852
        OO0OOO0O0OO0O0OOO =StringVar ()#line:3853
        O0O000O000000O00O =ttk .Label (O0OO0O0OO00OOO000 ,text ="计算列（V-M）:")#line:3854
        O0O000O000000O00O .pack (side =LEFT )#line:3855
        O0O000000O0O0O00O =ttk .Combobox (O0OO0O0OO00OOO000 ,width =10 ,textvariable =OOOOOO0000OOOO0O0 ,state ='readonly')#line:3857
        O0O000000O0O0O00O ['values']=O0OO00000O0OO0000 .columns .tolist ()#line:3858
        O0O000000O0O0O00O .pack (side =LEFT )#line:3859
        O0OO0O0000O0O0OO0 =ttk .Combobox (O0OO0O0OO00OOO000 ,width =10 ,textvariable =OO0OOO0O0OO0O0OOO ,state ='readonly')#line:3860
        O0OO0O0000O0O0OO0 ['values']=["计数","求和","唯一值计数"]#line:3861
        O0OO0O0000O0O0OO0 .pack (side =LEFT )#line:3862
        OO0000O0OO00O0O0O =Button (O0OO0O0OO00OOO000 ,text ="自助报表",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TOOLS_Autotable_0 (O0OO00000O0OO0000 ,O0O0000O000000O0O .get (),OO0O00OO0OOOOOOO0 .get (),O0OO00OO00O00OO0O .get (),O0O0O00000OOO0O0O .get (),OOOOOO0000OOOO0O0 .get (),OO0OOO0O0OO0O0OOO .get (),O0OO00000O0OO0000 ))#line:3864
        OO0000O0OO00O0O0O .pack (side =LEFT )#line:3865
        O0OO0OO0OOOOOOO0O =Button (O0OO0O0OO00OOO000 ,text ="去首行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 [1 :],1 ,O0O00000OOOOO0OOO ,))#line:3882
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3883
        O0OO0OO0OOOOOOO0O =Button (O0OO0O0OO00OOO000 ,text ="去尾行",bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (O0OO00000O0OO0000 [:-1 ],1 ,O0O00000OOOOO0OOO ,),)#line:3898
        O0OO0OO0OOOOOOO0O .pack (side =LEFT )#line:3899
        OO0O0OO0O00O000OO =Button (O0OO0O0OO00OOO000 ,text ="行数:"+str (len (O0OO00000O0OO0000 )),bg ="white",font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",)#line:3909
        OO0O0OO0O00O000OO .pack (side =LEFT )#line:3910
    except :#line:3913
        showinfo (title ="提示信息",message ="界面初始化失败。")#line:3914
    try :#line:3919
        if O0O00OOO0O0O000OO [0 ]=="tools_x":#line:3920
           return 0 #line:3921
    except :#line:3922
            pass #line:3923
    OOOOOO000OOO0OOO0 =O0OO00000O0OO0000 .values .tolist ()#line:3926
    O000OOOOOO000O00O =O0OO00000O0OO0000 .columns .values .tolist ()#line:3927
    O000O00000OOO0000 =ttk .Treeview (OO0O0000OO0000000 ,columns =O000OOOOOO000O00O ,show ="headings",height =45 )#line:3928
    for O000O0O0OO00O0O00 in O000OOOOOO000O00O :#line:3931
        O000O00000OOO0000 .heading (O000O0O0OO00O0O00 ,text =O000O0O0OO00O0O00 )#line:3932
    for O00OOOOO0OO0O0OOO in OOOOOO000OOO0OOO0 :#line:3933
        O000O00000OOO0000 .insert ("","end",values =O00OOOOO0OO0O0OOO )#line:3934
    for OO0O0OOO0OO000OO0 in O000OOOOOO000O00O :#line:3936
        try :#line:3937
            O000O00000OOO0000 .column (OO0O0OOO0OO000OO0 ,minwidth =0 ,width =80 ,stretch =NO )#line:3938
            if "只剩"in OO0O0OOO0OO000OO0 :#line:3939
                O000O00000OOO0000 .column (OO0O0OOO0OO000OO0 ,minwidth =0 ,width =150 ,stretch =NO )#line:3940
        except :#line:3941
            pass #line:3942
    OOO00000O0OOO0OOO =["评分说明"]#line:3946
    OO0OO0O0OOOO0000O =["该单位喜好上报的品种统计","报告编码","产品名称","上报机构描述","持有人处理描述","该注册证编号/曾用注册证编号报告数量","通用名称","该批准文号报告数量","上市许可持有人名称",]#line:3959
    O0OOO000OOO00000O =["注册证编号/曾用注册证编号","监测机构","报告月份","报告季度","单位列表","单位名称",]#line:3967
    OOO0O0OOO0OOOOOO0 =["管理类别",]#line:3971
    for OO0O0OOO0OO000OO0 in OO0OO0O0OOOO0000O :#line:3974
        try :#line:3975
            O000O00000OOO0000 .column (OO0O0OOO0OO000OO0 ,minwidth =0 ,width =200 ,stretch =NO )#line:3976
        except :#line:3977
            pass #line:3978
    for OO0O0OOO0OO000OO0 in O0OOO000OOO00000O :#line:3981
        try :#line:3982
            O000O00000OOO0000 .column (OO0O0OOO0OO000OO0 ,minwidth =0 ,width =140 ,stretch =NO )#line:3983
        except :#line:3984
            pass #line:3985
    for OO0O0OOO0OO000OO0 in OOO0O0OOO0OOOOOO0 :#line:3986
        try :#line:3987
            O000O00000OOO0000 .column (OO0O0OOO0OO000OO0 ,minwidth =0 ,width =40 ,stretch =NO )#line:3988
        except :#line:3989
            pass #line:3990
    for OO0O0OOO0OO000OO0 in OOO00000O0OOO0OOO :#line:3991
        try :#line:3992
            O000O00000OOO0000 .column (OO0O0OOO0OO000OO0 ,minwidth =0 ,width =800 ,stretch =NO )#line:3993
        except :#line:3994
            pass #line:3995
    try :#line:3997
        O000O00000OOO0000 .column ("请选择需要查看的表格",minwidth =1 ,width =300 ,stretch =NO )#line:4000
    except :#line:4001
        pass #line:4002
    try :#line:4004
        O000O00000OOO0000 .column ("详细描述T",minwidth =1 ,width =2300 ,stretch =NO )#line:4007
    except :#line:4008
        pass #line:4009
    OO00OO0000OO0000O =Scrollbar (OO0O0000OO0000000 ,orient ="vertical")#line:4011
    OO00OO0000OO0000O .pack (side =RIGHT ,fill =Y )#line:4012
    OO00OO0000OO0000O .config (command =O000O00000OOO0000 .yview )#line:4013
    O000O00000OOO0000 .config (yscrollcommand =OO00OO0000OO0000O .set )#line:4014
    O0000OO00OOOOO0OO =Scrollbar (OO0O0000OO0000000 ,orient ="horizontal")#line:4016
    O0000OO00OOOOO0OO .pack (side =BOTTOM ,fill =X )#line:4017
    O0000OO00OOOOO0OO .config (command =O000O00000OOO0000 .xview )#line:4018
    O000O00000OOO0000 .config (yscrollcommand =OO00OO0000OO0000O .set )#line:4019
    def O0OO000O0OOOOOOO0 (OO0OO000OO0OOOO0O ,O00O0000O00O0OOO0 ,OOO0O0O000OOO0OOO ):#line:4022
        for OOOO0OO00OO0OOO0O in O000O00000OOO0000 .selection ():#line:4024
            O0O00O00O00OOO000 =O000O00000OOO0000 .item (OOOO0OO00OO0OOO0O ,"values")#line:4025
        O00O0OOO0OOOOOOOO =dict (zip (O00O0000O00O0OOO0 ,O0O00O00O00OOO000 ))#line:4026
        if "详细描述T"in O00O0000O00O0OOO0 and "{"in O00O0OOO0OOOOOOOO ["详细描述T"]:#line:4030
            O00OOO0O0000O0O0O =eval (O00O0OOO0OOOOOOOO ["详细描述T"])#line:4031
            O00OOO0O0000O0O0O =pd .DataFrame .from_dict (O00OOO0O0000O0O0O ,orient ="index",columns =["content"]).reset_index ()#line:4032
            O00OOO0O0000O0O0O =O00OOO0O0000O0O0O .sort_values (by ="content",ascending =[False ],na_position ="last")#line:4033
            DRAW_make_one (O00OOO0O0000O0O0O ,O00O0OOO0OOOOOOOO ["条目"],"index","content","饼图")#line:4034
            return 0 #line:4035
        if "dfx_deepview"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4040
            OOOOO00OOO0O00O0O =eval (O00O0OOO0OOOOOOOO ["报表类型"][13 :])#line:4041
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO .copy ()#line:4042
            for O0OOOOOO0OO0OOOO0 in OOOOO00OOO0O00O0O :#line:4043
                OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 [(OOOOOOOOO0OO0O000 [O0OOOOOO0OO0OOOO0 ].astype (str )==O0O00O00O00OOO000 [OOOOO00OOO0O00O0O .index (O0OOOOOO0OO0OOOO0 )])].copy ()#line:4044
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_deepview"#line:4045
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4046
            return 0 #line:4047
        if "dfx_deepvie2"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4050
            OOOOO00OOO0O00O0O =eval (O00O0OOO0OOOOOOOO ["报表类型"][13 :])#line:4051
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO .copy ()#line:4052
            for O0OOOOOO0OO0OOOO0 in OOOOO00OOO0O00O0O :#line:4053
                OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 [OOOOOOOOO0OO0O000 [O0OOOOOO0OO0OOOO0 ].str .contains (O0O00O00O00OOO000 [OOOOO00OOO0O00O0O .index (O0OOOOOO0OO0OOOO0 )],na =False )].copy ()#line:4054
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_deepview"#line:4055
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4056
            return 0 #line:4057
        if "dfx_zhenghao"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4061
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["注册证编号/曾用注册证编号"]==O00O0OOO0OOOOOOOO ["注册证编号/曾用注册证编号"])].copy ()#line:4062
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_zhenghao"#line:4063
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4064
            return 0 #line:4065
        if ("dfx_pihao"in O00O0OOO0OOOOOOOO ["报表类型"]or "dfx_findrisk"in O00O0OOO0OOOOOOOO ["报表类型"]or "dfx_xinghao"in O00O0OOO0OOOOOOOO ["报表类型"]or "dfx_guige"in O00O0OOO0OOOOOOOO ["报表类型"])and O00O0OOOO0OOO0OO0 ==1 :#line:4069
            OO0O00O0OOO00OO00 ="CLT"#line:4070
            if "pihao"in O00O0OOO0OOOOOOOO ["报表类型"]or "产品批号"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4071
                OO0O00O0OOO00OO00 ="产品批号"#line:4072
            if "xinghao"in O00O0OOO0OOOOOOOO ["报表类型"]or "型号"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4073
                OO0O00O0OOO00OO00 ="型号"#line:4074
            if "guige"in O00O0OOO0OOOOOOOO ["报表类型"]or "规格"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4075
                OO0O00O0OOO00OO00 ="规格"#line:4076
            if "事件发生季度"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4077
                OO0O00O0OOO00OO00 ="事件发生季度"#line:4078
            if "事件发生月份"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4079
                OO0O00O0OOO00OO00 ="事件发生月份"#line:4080
            if "性别"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4081
                OO0O00O0OOO00OO00 ="性别"#line:4082
            if "年龄段"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4083
                OO0O00O0OOO00OO00 ="年龄段"#line:4084
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["注册证编号/曾用注册证编号"]==O00O0OOO0OOOOOOOO ["注册证编号/曾用注册证编号"])&(OOO0O0O000OOO0OOO [OO0O00O0OOO00OO00 ]==O00O0OOO0OOOOOOOO [OO0O00O0OOO00OO00 ])].copy ()#line:4085
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_pihao"#line:4086
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4087
            return 0 #line:4088
        if ("findrisk"in O00O0OOO0OOOOOOOO ["报表类型"]or "dfx_pihao"in O00O0OOO0OOOOOOOO ["报表类型"]or "dfx_xinghao"in O00O0OOO0OOOOOOOO ["报表类型"]or "dfx_guige"in O00O0OOO0OOOOOOOO ["报表类型"])and O00O0OOOO0OOO0OO0 !=1 :#line:4092
            OOOOOOOOO0OO0O000 =O0OO00000O0OO0000 [(O0OO00000O0OO0000 ["注册证编号/曾用注册证编号"]==O00O0OOO0OOOOOOOO ["注册证编号/曾用注册证编号"])].copy ()#line:4093
            OOOOOOOOO0OO0O000 ["报表类型"]=O00O0OOO0OOOOOOOO ["报表类型"]+"1"#line:4094
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,1 ,OOO0O0O000OOO0OOO )#line:4095
            return 0 #line:4097
        if "dfx_org监测机构"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4100
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["监测机构"]==O00O0OOO0OOOOOOOO ["监测机构"])].copy ()#line:4101
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_org"#line:4102
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4103
            return 0 #line:4104
        if "dfx_org市级监测机构"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4106
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["市级监测机构"]==O00O0OOO0OOOOOOOO ["市级监测机构"])].copy ()#line:4107
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_org"#line:4108
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4109
            return 0 #line:4110
        if "dfx_user"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4113
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["单位名称"]==O00O0OOO0OOOOOOOO ["单位名称"])].copy ()#line:4114
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_user"#line:4115
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4116
            return 0 #line:4117
        if "dfx_chiyouren"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4121
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["上市许可持有人名称"]==O00O0OOO0OOOOOOOO ["上市许可持有人名称"])].copy ()#line:4122
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_chiyouren"#line:4123
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4124
            return 0 #line:4125
        if "dfx_chanpin"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4127
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["产品名称"]==O00O0OOO0OOOOOOOO ["产品名称"])].copy ()#line:4128
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_chanpin"#line:4129
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4130
            return 0 #line:4131
        if "dfx_findrisk事件发生季度1"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4136
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["注册证编号/曾用注册证编号"]==O00O0OOO0OOOOOOOO ["注册证编号/曾用注册证编号"])&(OOO0O0O000OOO0OOO ["事件发生季度"]==O00O0OOO0OOOOOOOO ["事件发生季度"])].copy ()#line:4137
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_findrisk事件发生季度"#line:4138
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4139
            return 0 #line:4140
        if "dfx_findrisk事件发生月份1"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4143
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["注册证编号/曾用注册证编号"]==O00O0OOO0OOOOOOOO ["注册证编号/曾用注册证编号"])&(OOO0O0O000OOO0OOO ["事件发生月份"]==O00O0OOO0OOOOOOOO ["事件发生月份"])].copy ()#line:4144
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_dfx_findrisk事件发生月份"#line:4145
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4146
            return 0 #line:4147
        if ("keyword_findrisk"in O00O0OOO0OOOOOOOO ["报表类型"])and O00O0OOOO0OOO0OO0 ==1 :#line:4150
            OO0O00O0OOO00OO00 ="CLT"#line:4151
            if "批号"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4152
                OO0O00O0OOO00OO00 ="产品批号"#line:4153
            if "事件发生季度"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4154
                OO0O00O0OOO00OO00 ="事件发生季度"#line:4155
            if "事件发生月份"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4156
                OO0O00O0OOO00OO00 ="事件发生月份"#line:4157
            if "性别"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4158
                OO0O00O0OOO00OO00 ="性别"#line:4159
            if "年龄段"in O00O0OOO0OOOOOOOO ["报表类型"]:#line:4160
                OO0O00O0OOO00OO00 ="年龄段"#line:4161
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO [(OOO0O0O000OOO0OOO ["注册证编号/曾用注册证编号"]==O00O0OOO0OOOOOOOO ["注册证编号/曾用注册证编号"])&(OOO0O0O000OOO0OOO [OO0O00O0OOO00OO00 ]==O00O0OOO0OOOOOOOO [OO0O00O0OOO00OO00 ])].copy ()#line:4162
            OOOOOOOOO0OO0O000 ["关键字查找列"]=""#line:4163
            for OOOO00O0000O0OOO0 in TOOLS_get_list (O00O0OOO0OOOOOOOO ["关键字查找列"]):#line:4164
                OOOOOOOOO0OO0O000 ["关键字查找列"]=OOOOOOOOO0OO0O000 ["关键字查找列"]+OOOOOOOOO0OO0O000 [OOOO00O0000O0OOO0 ].astype ("str")#line:4165
            OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 [(OOOOOOOOO0OO0O000 ["关键字查找列"].str .contains (O00O0OOO0OOOOOOOO ["关键字组合"],na =False ))]#line:4166
            if str (O00O0OOO0OOOOOOOO ["排除值"])!="nan":#line:4168
                OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 .loc [~OOOOOOOOO0OO0O000 ["关键字查找列"].str .contains (O00O0OOO0OOOOOOOO ["排除值"],na =False )]#line:4169
            OOOOOOOOO0OO0O000 ["报表类型"]="ori_"+O00O0OOO0OOOOOOOO ["报表类型"]#line:4171
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4172
            return 0 #line:4173
        if ("PSUR"in O00O0OOO0OOOOOOOO ["报表类型"]):#line:4178
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO .copy ()#line:4179
            if ini ["模式"]=="器械":#line:4180
                OOOOOOOOO0OO0O000 ["关键字查找列"]=OOOOOOOOO0OO0O000 ["器械故障表现"].astype (str )+OOOOOOOOO0OO0O000 ["伤害表现"].astype (str )+OOOOOOOOO0OO0O000 ["使用过程"].astype (str )+OOOOOOOOO0OO0O000 ["事件原因分析描述"].astype (str )+OOOOOOOOO0OO0O000 ["初步处置情况"].astype (str )#line:4181
            else :#line:4182
                OOOOOOOOO0OO0O000 ["关键字查找列"]=OOOOOOOOO0OO0O000 ["器械故障表现"]#line:4183
            if "-其他关键字-"in str (O00O0OOO0OOOOOOOO ["关键字标记"]):#line:4185
                OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 .loc [~OOOOOOOOO0OO0O000 ["关键字查找列"].str .contains (O00O0OOO0OOOOOOOO ["关键字标记"],na =False )].copy ()#line:4186
                TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4187
                return 0 #line:4188
            OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 [(OOOOOOOOO0OO0O000 ["关键字查找列"].str .contains (O00O0OOO0OOOOOOOO ["关键字标记"],na =False ))]#line:4191
            if str (O00O0OOO0OOOOOOOO ["排除值"])!="没有排除值":#line:4192
                OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 .loc [~OOOOOOOOO0OO0O000 ["关键字查找列"].str .contains (O00O0OOO0OOOOOOOO ["排除值"],na =False )]#line:4193
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4197
            return 0 #line:4198
        if ("ROR"in O00O0OOO0OOOOOOOO ["报表类型"]):#line:4201
            OOO0OOOOOOO00000O ={'nan':"-未定义-"}#line:4202
            O0O0OOO0O0O0OO00O =eval (O00O0OOO0OOOOOOOO ["报表定位"],OOO0OOOOOOO00000O )#line:4203
            OOOOOOOOO0OO0O000 =OOO0O0O000OOO0OOO .copy ()#line:4204
            for OOOO0000OOOO0O0O0 ,O0O0000OOOO0OO0O0 in O0O0OOO0O0O0OO00O .items ():#line:4206
                if OOOO0000OOOO0O0O0 =="合并列"and O0O0000OOOO0OO0O0 !={}:#line:4208
                    for OOOO0O00OO00O0OO0 ,O00OOOO0OO00OO0O0 in O0O0000OOOO0OO0O0 .items ():#line:4209
                        if O00OOOO0OO00OO0O0 !="-未定义-":#line:4210
                            OOOOO0O0OO0OO00O0 =TOOLS_get_list (O00OOOO0OO00OO0O0 )#line:4211
                            OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ]=""#line:4212
                            for O0OO000O0O00OO000 in OOOOO0O0OO0OO00O0 :#line:4213
                                OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ]=OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ]+OOOOOOOOO0OO0O000 [O0OO000O0O00OO000 ].astype ("str")#line:4214
                if OOOO0000OOOO0O0O0 =="等于"and O0O0000OOOO0OO0O0 !={}:#line:4216
                    for OOOO0O00OO00O0OO0 ,O00OOOO0OO00OO0O0 in O0O0000OOOO0OO0O0 .items ():#line:4217
                        OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 [(OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ]==O00OOOO0OO00OO0O0 )]#line:4218
                if OOOO0000OOOO0O0O0 =="不等于"and O0O0000OOOO0OO0O0 !={}:#line:4220
                    for OOOO0O00OO00O0OO0 ,O00OOOO0OO00OO0O0 in O0O0000OOOO0OO0O0 .items ():#line:4221
                        if O00OOOO0OO00OO0O0 !="-未定义-":#line:4222
                            OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 [(OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ]!=O00OOOO0OO00OO0O0 )]#line:4223
                if OOOO0000OOOO0O0O0 =="包含"and O0O0000OOOO0OO0O0 !={}:#line:4225
                    for OOOO0O00OO00O0OO0 ,O00OOOO0OO00OO0O0 in O0O0000OOOO0OO0O0 .items ():#line:4226
                        if O00OOOO0OO00OO0O0 !="-未定义-":#line:4227
                            OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 .loc [OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ].str .contains (O00OOOO0OO00OO0O0 ,na =False )]#line:4228
                if OOOO0000OOOO0O0O0 =="不包含"and O0O0000OOOO0OO0O0 !={}:#line:4230
                    for OOOO0O00OO00O0OO0 ,O00OOOO0OO00OO0O0 in O0O0000OOOO0OO0O0 .items ():#line:4231
                        if O00OOOO0OO00OO0O0 !="-未定义-":#line:4232
                            OOOOOOOOO0OO0O000 =OOOOOOOOO0OO0O000 .loc [~OOOOOOOOO0OO0O000 [OOOO0O00OO00O0OO0 ].str .contains (O00OOOO0OO00OO0O0 ,na =False )]#line:4233
            TABLE_tree_Level_2 (OOOOOOOOO0OO0O000 ,0 ,OOOOOOOOO0OO0O000 )#line:4235
            return 0 #line:4236
    if ("关键字标记"in OOO000000O000O000 ["values"])and ("该类别不良事件计数"in OOO000000O000O000 ["values"]):#line:4239
            def O0OO00O00OO00OOOO (event =None ):#line:4240
                for O0O0O0OOOOO0OOOO0 in O000O00000OOO0000 .selection ():#line:4241
                    O0OO0000O0O000OO0 =O000O00000OOO0000 .item (O0O0O0OOOOO0OOOO0 ,"values")#line:4242
                O0OO0O00OOO0OOOO0 =dict (zip (O000OOOOOO000O00O ,O0OO0000O0O000OO0 ))#line:4243
                OO0OOOOOOOO000OO0 =O0O00000OOOOO0OOO .copy ()#line:4244
                if ini ["模式"]=="器械":#line:4245
                    OO0OOOOOOOO000OO0 ["关键字查找列"]=OO0OOOOOOOO000OO0 ["器械故障表现"].astype (str )+OO0OOOOOOOO000OO0 ["伤害表现"].astype (str )+OO0OOOOOOOO000OO0 ["使用过程"].astype (str )+OO0OOOOOOOO000OO0 ["事件原因分析描述"].astype (str )+OO0OOOOOOOO000OO0 ["初步处置情况"].astype (str )#line:4246
                else :#line:4247
                    OO0OOOOOOOO000OO0 ["关键字查找列"]=OO0OOOOOOOO000OO0 ["器械故障表现"]#line:4248
                if "-其他关键字-"in str (O0OO0O00OOO0OOOO0 ["关键字标记"]):#line:4249
                    OO0OOOOOOOO000OO0 =OO0OOOOOOOO000OO0 .loc [~OO0OOOOOOOO000OO0 ["关键字查找列"].str .contains (O0OO0O00OOO0OOOO0 ["关键字标记"],na =False )].copy ()#line:4250
                OO0OOOOOOOO000OO0 =OO0OOOOOOOO000OO0 [(OO0OOOOOOOO000OO0 ["关键字查找列"].str .contains (O0OO0O00OOO0OOOO0 ["关键字标记"],na =False ))]#line:4252
                if str (O0OO0O00OOO0OOOO0 ["排除值"])!="没有排除值":#line:4253
                    OO0OOOOOOOO000OO0 =OO0OOOOOOOO000OO0 .loc [~OO0OOOOOOOO000OO0 ["关键字查找列"].str .contains (O0OO0O00OOO0OOOO0 ["排除值"],na =False )]#line:4254
                OOOO0OO0O000O00O0 =TOOLS_count_elements (OO0OOOOOOOO000OO0 ,O0OO0O00OOO0OOOO0 ["关键字标记"],"关键字查找列")#line:4255
                OOOO0OO0O000O00O0 =OOOO0OO0O000O00O0 .sort_values (by ="计数",ascending =[False ],na_position ="last").reset_index (drop =True )#line:4256
                TABLE_tree_Level_2 (OOOO0OO0O000O00O0 ,1 ,OO0OOOOOOOO000OO0 )#line:4257
            OO0000OOOO0O0O00O =Menu (OOOO000000OOOOOO0 ,tearoff =False ,)#line:4258
            OO0000OOOO0O0O00O .add_command (label ="表现具体细项",command =O0OO00O00OO00OOOO )#line:4259
            def OO0O0O0000000000O (OO0O00O00000O00OO ):#line:4260
                OO0000OOOO0O0O00O .post (OO0O00O00000O00OO .x_root ,OO0O00O00000O00OO .y_root )#line:4261
            OOOO000000OOOOOO0 .bind ("<Button-3>",OO0O0O0000000000O )#line:4262
    try :#line:4266
        if O0O00OOO0O0O000OO [1 ]=="dfx_zhenghao":#line:4267
            O0OO000O0000O00O0 ="dfx_zhenghao"#line:4268
            O0OO000O0OOO0O0O0 =""#line:4269
    except :#line:4270
            O0OO000O0000O00O0 =""#line:4271
            O0OO000O0OOO0O0O0 ="近一年"#line:4272
    if (("总体评分"in OOO000000O000O000 ["values"])and ("高峰批号均值"in OOO000000O000O000 ["values"])and ("月份均值"in OOO000000O000O000 ["values"]))or O0OO000O0000O00O0 =="dfx_zhenghao":#line:4274
            def O000OOOO0OOOO00O0 (event =None ):#line:4277
                for O00O0000O0O0OOO0O in O000O00000OOO0000 .selection ():#line:4278
                    O00O0OOOO00O00000 =O000O00000OOO0000 .item (O00O0000O0O0OOO0O ,"values")#line:4279
                O0O00OO00000O000O =dict (zip (O000OOOOOO000O00O ,O00O0OOOO00O00000 ))#line:4280
                OO0O00O00000OOO00 =O0O00000OOOOO0OOO [(O0O00000OOOOO0OOO ["注册证编号/曾用注册证编号"]==O0O00OO00000O000O ["注册证编号/曾用注册证编号"])].copy ()#line:4281
                OO0O00O00000OOO00 ["报表类型"]=O0O00OO00000O000O ["报表类型"]+"1"#line:4282
                TABLE_tree_Level_2 (OO0O00O00000OOO00 ,1 ,O0O00000OOOOO0OOO )#line:4283
            def OO00O00OO00O00OO0 (event =None ):#line:4284
                for OO0O0OO0O0OO00OOO in O000O00000OOO0000 .selection ():#line:4285
                    OOO00O000O0O000OO =O000O00000OOO0000 .item (OO0O0OO0O0OO00OOO ,"values")#line:4286
                OOOOO0O0OO000O0OO =dict (zip (O000OOOOOO000O00O ,OOO00O000O0O000OO ))#line:4287
                O0000OO000OO0O00O =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==OOOOO0O0OO000O0OO ["注册证编号/曾用注册证编号"])].copy ()#line:4288
                O0000OO000OO0O00O ["报表类型"]=OOOOO0O0OO000O0OO ["报表类型"]+"1"#line:4289
                TABLE_tree_Level_2 (O0000OO000OO0O00O ,1 ,O0O00OOO0O0O000OO [0 ])#line:4290
            def OO0O0OO00O0OO0O0O (OO0O000000OO0000O ):#line:4291
                for O0000O00OOO0O0OO0 in O000O00000OOO0000 .selection ():#line:4292
                    OOOOOO00000OO00OO =O000O00000OOO0000 .item (O0000O00OOO0O0OO0 ,"values")#line:4293
                O0O000O0O00O0O00O =dict (zip (O000OOOOOO000O00O ,OOOOOO00000OO00OO ))#line:4294
                O0OOO00OO00O0O0O0 =O0O00000OOOOO0OOO [(O0O00000OOOOO0OOO ["注册证编号/曾用注册证编号"]==O0O000O0O00O0O00O ["注册证编号/曾用注册证编号"])].copy ()#line:4297
                O0OOO00OO00O0O0O0 ["报表类型"]=O0O000O0O00O0O00O ["报表类型"]+"1"#line:4298
                O0OOO0O000O0000O0 =Countall (O0OOO00OO00O0O0O0 ).df_psur (OO0O000000OO0000O ,O0O000O0O00O0O00O ["规整后品类"])[["关键字标记","总数量","严重比"]]#line:4299
                O0OOO0O000O0000O0 =O0OOO0O000O0000O0 .rename (columns ={"总数量":"最近30天总数量"})#line:4300
                O0OOO0O000O0000O0 =O0OOO0O000O0000O0 .rename (columns ={"严重比":"最近30天严重比"})#line:4301
                O0OOO00OO00O0O0O0 =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==O0O000O0O00O0O00O ["注册证编号/曾用注册证编号"])].copy ()#line:4303
                O0OOO00OO00O0O0O0 ["报表类型"]=O0O000O0O00O0O00O ["报表类型"]+"1"#line:4304
                O0OOO0O00O0000000 =Countall (O0OOO00OO00O0O0O0 ).df_psur (OO0O000000OO0000O ,O0O000O0O00O0O00O ["规整后品类"])#line:4305
                O00000O0O00OO0OO0 =pd .merge (O0OOO0O00O0000000 ,O0OOO0O000O0000O0 ,on ="关键字标记",how ="left")#line:4307
                del O00000O0O00OO0OO0 ["报表类型"]#line:4308
                O00000O0O00OO0OO0 ["报表类型"]="PSUR"#line:4309
                TABLE_tree_Level_2 (O00000O0O00OO0OO0 ,1 ,O0OOO00OO00O0O0O0 )#line:4311
            def OOO0O000O0O0OOOOO (OO0OOO0OOOOO0000O ):#line:4314
                for OO0OO0OOOO0OOOOOO in O000O00000OOO0000 .selection ():#line:4315
                    O0O0OOO00000O0OO0 =O000O00000OOO0000 .item (OO0OO0OOOO0OOOOOO ,"values")#line:4316
                OO00OOO000OO0O0OO =dict (zip (O000OOOOOO000O00O ,O0O0OOO00000O0OO0 ))#line:4317
                OO0OO0O0O0O000OOO =O0O00OOO0O0O000OO [0 ]#line:4318
                if OO00OOO000OO0O0OO ["规整后品类"]=="N":#line:4319
                    if OO0OOO0OOOOO0000O =="特定品种":#line:4320
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4321
                        return 0 #line:4322
                    OO0OO0O0O0O000OOO =OO0OO0O0O0O000OOO .loc [OO0OO0O0O0O000OOO ["产品名称"].str .contains (OO00OOO000OO0O0OO ["产品名称"],na =False )].copy ()#line:4323
                else :#line:4324
                    OO0OO0O0O0O000OOO =OO0OO0O0O0O000OOO .loc [OO0OO0O0O0O000OOO ["规整后品类"].str .contains (OO00OOO000OO0O0OO ["规整后品类"],na =False )].copy ()#line:4325
                OO0OO0O0O0O000OOO =OO0OO0O0O0O000OOO .loc [OO0OO0O0O0O000OOO ["产品类别"].str .contains (OO00OOO000OO0O0OO ["产品类别"],na =False )].copy ()#line:4326
                OO0OO0O0O0O000OOO ["报表类型"]=OO00OOO000OO0O0OO ["报表类型"]+"1"#line:4328
                if OO0OOO0OOOOO0000O =="特定品种":#line:4329
                    TABLE_tree_Level_2 (Countall (OO0OO0O0O0O000OOO ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],OO00OOO000OO0O0OO ["规整后品类"],OO00OOO000OO0O0OO ["注册证编号/曾用注册证编号"]),1 ,OO0OO0O0O0O000OOO )#line:4330
                else :#line:4331
                    TABLE_tree_Level_2 (Countall (OO0OO0O0O0O000OOO ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],OO0OOO0OOOOO0000O ,OO00OOO000OO0O0OO ["注册证编号/曾用注册证编号"]),1 ,OO0OO0O0O0O000OOO )#line:4332
            def O00OO0O0OO0OO0O0O (event =None ):#line:4334
                for OOOO00OO0O00O00O0 in O000O00000OOO0000 .selection ():#line:4335
                    OO00OO000OOOO000O =O000O00000OOO0000 .item (OOOO00OO0O00O00O0 ,"values")#line:4336
                O000O00OOOO00O000 =dict (zip (O000OOOOOO000O00O ,OO00OO000OOOO000O ))#line:4337
                O0OO0O00OOO0O0OOO =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==O000O00OOOO00O000 ["注册证编号/曾用注册证编号"])].copy ()#line:4338
                O0OO0O00OOO0O0OOO ["报表类型"]=O000O00OOOO00O000 ["报表类型"]+"1"#line:4339
                TABLE_tree_Level_2 (Countall (O0OO0O00OOO0O0OOO ).df_pihao (),1 ,O0OO0O00OOO0O0OOO ,)#line:4344
            def OO00O00OO000O0O00 (event =None ):#line:4346
                for OOO00OO000OOOO0OO in O000O00000OOO0000 .selection ():#line:4347
                    O0000000O00O000O0 =O000O00000OOO0000 .item (OOO00OO000OOOO0OO ,"values")#line:4348
                OO0OO0O000OOOO000 =dict (zip (O000OOOOOO000O00O ,O0000000O00O000O0 ))#line:4349
                OOOO000O0O0O00O00 =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==OO0OO0O000OOOO000 ["注册证编号/曾用注册证编号"])].copy ()#line:4350
                OOOO000O0O0O00O00 ["报表类型"]=OO0OO0O000OOOO000 ["报表类型"]+"1"#line:4351
                TABLE_tree_Level_2 (Countall (OOOO000O0O0O00O00 ).df_xinghao (),1 ,OOOO000O0O0O00O00 ,)#line:4356
            def O000OOOO0000O0O0O (event =None ):#line:4358
                for O0O0O000OOOO0O0O0 in O000O00000OOO0000 .selection ():#line:4359
                    OO0O0O00OOO0OO0O0 =O000O00000OOO0000 .item (O0O0O000OOOO0O0O0 ,"values")#line:4360
                O0000OOOO0000O0OO =dict (zip (O000OOOOOO000O00O ,OO0O0O00OOO0OO0O0 ))#line:4361
                OOO000O00OO00O00O =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==O0000OOOO0000O0OO ["注册证编号/曾用注册证编号"])].copy ()#line:4362
                OOO000O00OO00O00O ["报表类型"]=O0000OOOO0000O0OO ["报表类型"]+"1"#line:4363
                TABLE_tree_Level_2 (Countall (OOO000O00OO00O00O ).df_user (),1 ,OOO000O00OO00O00O ,)#line:4368
            def OO0O0OO0O000OOO0O (event =None ):#line:4370
                for OO0OOO0O000OO00O0 in O000O00000OOO0000 .selection ():#line:4372
                    OO0OOOO0OOOOO00OO =O000O00000OOO0000 .item (OO0OOO0O000OO00O0 ,"values")#line:4373
                OO00O0OO00OO00000 =dict (zip (O000OOOOOO000O00O ,OO0OOOO0OOOOO00OO ))#line:4374
                OOO0OOO00OOOOO0O0 =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==OO00O0OO00OO00000 ["注册证编号/曾用注册证编号"])].copy ()#line:4375
                OOO0OOO00OOOOO0O0 ["报表类型"]=OO00O0OO00OO00000 ["报表类型"]+"1"#line:4376
                OOO0O00OOOOO00000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name =0 ).reset_index (drop =True )#line:4377
                if ini ["模式"]=="药品":#line:4378
                    OOO0O00OOOOO00000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="药品").reset_index (drop =True )#line:4379
                if ini ["模式"]=="器械":#line:4380
                    OOO0O00OOOOO00000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="器械").reset_index (drop =True )#line:4381
                if ini ["模式"]=="化妆品":#line:4382
                    OOO0O00OOOOO00000 =pd .read_excel (peizhidir +"0（范例）预警参数.xlsx",header =0 ,sheet_name ="化妆品").reset_index (drop =True )#line:4383
                OOO0O0OO00O000000 =OOO0O00OOOOO00000 ["值"][3 ]+"|"+OOO0O00OOOOO00000 ["值"][4 ]#line:4384
                if ini ["模式"]=="器械":#line:4385
                    OOO0OOO00OOOOO0O0 ["关键字查找列"]=OOO0OOO00OOOOO0O0 ["器械故障表现"].astype (str )+OOO0OOO00OOOOO0O0 ["伤害表现"].astype (str )+OOO0OOO00OOOOO0O0 ["使用过程"].astype (str )+OOO0OOO00OOOOO0O0 ["事件原因分析描述"].astype (str )+OOO0OOO00OOOOO0O0 ["初步处置情况"].astype (str )#line:4386
                else :#line:4387
                    OOO0OOO00OOOOO0O0 ["关键字查找列"]=OOO0OOO00OOOOO0O0 ["器械故障表现"].astype (str )#line:4388
                OOO0OOO00OOOOO0O0 =OOO0OOO00OOOOO0O0 .loc [OOO0OOO00OOOOO0O0 ["关键字查找列"].str .contains (OOO0O0OO00O000000 ,na =False )].copy ().reset_index (drop =True )#line:4389
                TABLE_tree_Level_2 (OOO0OOO00OOOOO0O0 ,0 ,OOO0OOO00OOOOO0O0 ,)#line:4395
            def OO0O00OOOOO00O000 (event =None ):#line:4398
                for O000OO00O0OOO0000 in O000O00000OOO0000 .selection ():#line:4399
                    OOOOO0O000OOOOOO0 =O000O00000OOO0000 .item (O000OO00O0OOO0000 ,"values")#line:4400
                OOOOOO0O00OO0O000 =dict (zip (O000OOOOOO000O00O ,OOOOO0O000OOOOOO0 ))#line:4401
                OOOO0O0O00OO0OOO0 =O0O00OOO0O0O000OO [0 ][(O0O00OOO0O0O000OO [0 ]["注册证编号/曾用注册证编号"]==OOOOOO0O00OO0O000 ["注册证编号/曾用注册证编号"])].copy ()#line:4402
                OOOO0O0O00OO0OOO0 ["报表类型"]=OOOOOO0O00OO0O000 ["报表类型"]+"1"#line:4403
                TOOLS_time (OOOO0O0O00OO0OOO0 ,"事件发生日期",0 )#line:4404
            def OO0O0O000O0O0OO00 (O0O00O0OO00000OOO ,O00O0OO0O0O0O00O0 ):#line:4406
                for O0O000OOO00OO0OO0 in O000O00000OOO0000 .selection ():#line:4408
                    OO000O000000O0O0O =O000O00000OOO0000 .item (O0O000OOO00OO0OO0 ,"values")#line:4409
                OOOO00O0OOO0OOO00 =dict (zip (O000OOOOOO000O00O ,OO000O000000O0O0O ))#line:4410
                OOOO0O0000O0OO00O =O0O00OOO0O0O000OO [0 ]#line:4411
                if OOOO00O0OOO0OOO00 ["规整后品类"]=="N":#line:4412
                    if O0O00O0OO00000OOO =="特定品种":#line:4413
                        showinfo (title ="关于",message ="未能适配该品种规则，可能未制定或者数据规整不完善。")#line:4414
                        return 0 #line:4415
                OOOO0O0000O0OO00O =OOOO0O0000O0OO00O .loc [OOOO0O0000O0OO00O ["注册证编号/曾用注册证编号"].str .contains (OOOO00O0OOO0OOO00 ["注册证编号/曾用注册证编号"],na =False )].copy ()#line:4416
                OOOO0O0000O0OO00O ["报表类型"]=OOOO00O0OOO0OOO00 ["报表类型"]+"1"#line:4417
                if O0O00O0OO00000OOO =="特定品种":#line:4418
                    TABLE_tree_Level_2 (Countall (OOOO0O0000O0OO00O ).df_find_all_keword_risk (O00O0OO0O0O0O00O0 ,OOOO00O0OOO0OOO00 ["规整后品类"]),1 ,OOOO0O0000O0OO00O )#line:4419
                else :#line:4420
                    TABLE_tree_Level_2 (Countall (OOOO0O0000O0OO00O ).df_find_all_keword_risk (O00O0OO0O0O0O00O0 ,O0O00O0OO00000OOO ),1 ,OOOO0O0000O0OO00O )#line:4421
            OO0000OOOO0O0O00O =Menu (OOOO000000OOOOOO0 ,tearoff =False ,)#line:4425
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"故障表现分类（无源）",command =lambda :OO0O0OO00O0OO0O0O ("通用无源"))#line:4426
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"故障表现分类（有源）",command =lambda :OO0O0OO00O0OO0O0O ("通用有源"))#line:4427
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"故障表现分类（特定品种）",command =lambda :OO0O0OO00O0OO0O0O ("特定品种"))#line:4428
            OO0000OOOO0O0O00O .add_separator ()#line:4430
            if O0OO000O0000O00O0 =="":#line:4431
                OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"同类比较(ROR-无源)",command =lambda :OOO0O000O0O0OOOOO ("无源"))#line:4432
                OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"同类比较(ROR-有源)",command =lambda :OOO0O000O0O0OOOOO ("有源"))#line:4433
                OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"同类比较(ROR-特定品种)",command =lambda :OOO0O000O0O0OOOOO ("特定品种"))#line:4434
            OO0000OOOO0O0O00O .add_separator ()#line:4436
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(批号-无源)",command =lambda :OO0O0O000O0O0OO00 ("无源","产品批号"))#line:4437
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(批号-特定品种)",command =lambda :OO0O0O000O0O0OO00 ("特定品种","产品批号"))#line:4438
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(月份-无源)",command =lambda :OO0O0O000O0O0OO00 ("无源","事件发生月份"))#line:4439
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(月份-有源)",command =lambda :OO0O0O000O0O0OO00 ("有源","事件发生月份"))#line:4440
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(月份-特定品种)",command =lambda :OO0O0O000O0O0OO00 ("特定品种","事件发生月份"))#line:4441
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(季度-无源)",command =lambda :OO0O0O000O0O0OO00 ("无源","事件发生季度"))#line:4442
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(季度-有源)",command =lambda :OO0O0O000O0O0OO00 ("有源","事件发生季度"))#line:4443
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"关键字趋势(季度-特定品种)",command =lambda :OO0O0O000O0O0OO00 ("特定品种","事件发生季度"))#line:4444
            OO0000OOOO0O0O00O .add_separator ()#line:4446
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"各批号报送情况",command =O00OO0O0OO0OO0O0O )#line:4447
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"各型号报送情况",command =OO00O00OO000O0O00 )#line:4448
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"报告单位情况",command =O000OOOO0000O0O0O )#line:4449
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"事件发生时间曲线",command =OO0O00OOOOO00O000 )#line:4450
            OO0000OOOO0O0O00O .add_separator ()#line:4451
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"原始数据",command =OO00O00OO00O00OO0 )#line:4452
            if O0OO000O0000O00O0 =="":#line:4453
                OO0000OOOO0O0O00O .add_command (label ="近30天原始数据",command =O000OOOO0OOOO00O0 )#line:4454
            OO0000OOOO0O0O00O .add_command (label =O0OO000O0OOO0O0O0 +"高度关注(一级和二级)",command =OO0O0OO0O000OOO0O )#line:4455
            def OO0O0O0000000000O (O0OO00O0000OO0O0O ):#line:4457
                OO0000OOOO0O0O00O .post (O0OO00O0000OO0O0O .x_root ,O0OO00O0000OO0O0O .y_root )#line:4458
            OOOO000000OOOOOO0 .bind ("<Button-3>",OO0O0O0000000000O )#line:4459
    if O0O00000OO00OOOOO ==0 or "规整编码"in O0OO00000O0OO0000 .columns :#line:4462
        O000O00000OOO0000 .bind ("<Double-1>",lambda O000OOO0O00000O00 :O0OO0O00000OOO000 (O000OOO0O00000O00 ,O0OO00000O0OO0000 ))#line:4463
    if O0O00000OO00OOOOO ==1 and "规整编码"not in O0OO00000O0OO0000 .columns :#line:4464
        O000O00000OOO0000 .bind ("<Double-1>",lambda OOO00O000OO0OOO00 :O0OO000O0OOOOOOO0 (OOO00O000OO0OOO00 ,O000OOOOOO000O00O ,O0O00000OOOOO0OOO ))#line:4465
    def OO0O00O0OO00000O0 (O00O0O000OO00O00O ,O00OOOO0O0O0OO0O0 ,OO00O000OOO0000OO ):#line:4468
        OOO0O0O000OOOOOOO =[(O00O0O000OO00O00O .set (O0OO0OO0O00OOOOO0 ,O00OOOO0O0O0OO0O0 ),O0OO0OO0O00OOOOO0 )for O0OO0OO0O00OOOOO0 in O00O0O000OO00O00O .get_children ("")]#line:4469
        OOO0O0O000OOOOOOO .sort (reverse =OO00O000OOO0000OO )#line:4470
        for OO00O000O0O0O00OO ,(O0O0O0O0OOO0O0O0O ,O0OO0O00OOO000000 )in enumerate (OOO0O0O000OOOOOOO ):#line:4472
            O00O0O000OO00O00O .move (O0OO0O00OOO000000 ,"",OO00O000O0O0O00OO )#line:4473
        O00O0O000OO00O00O .heading (O00OOOO0O0O0OO0O0 ,command =lambda :OO0O00O0OO00000O0 (O00O0O000OO00O00O ,O00OOOO0O0O0OO0O0 ,not OO00O000OOO0000OO ))#line:4476
    for OO0OO0OO00O00O000 in O000OOOOOO000O00O :#line:4478
        O000O00000OOO0000 .heading (OO0OO0OO00O00O000 ,text =OO0OO0OO00O00O000 ,command =lambda _col =OO0OO0OO00O00O000 :OO0O00O0OO00000O0 (O000O00000OOO0000 ,_col ,False ),)#line:4483
    def O0OO0O00000OOO000 (OO0O000O0O0OOOOO0 ,OOO0O0OO0O0O0O000 ):#line:4487
        if "规整编码"in OOO0O0OO0O0O0O000 .columns :#line:4489
            OOO0O0OO0O0O0O000 =OOO0O0OO0O0O0O000 .rename (columns ={"规整编码":"报告编码"})#line:4490
        for OO00000O0OOO0OO0O in O000O00000OOO0000 .selection ():#line:4492
            O0OOOOOO00O0OOOOO =O000O00000OOO0000 .item (OO00000O0OOO0OO0O ,"values")#line:4493
            O000OOOO0OO0000O0 =Toplevel ()#line:4496
            O0O0OOOO000000OOO =O000OOOO0OO0000O0 .winfo_screenwidth ()#line:4498
            OO0O000O0OO000O0O =O000OOOO0OO0000O0 .winfo_screenheight ()#line:4500
            O0000O000000O0OOO =800 #line:4502
            OOO00000O0O00OO0O =600 #line:4503
            OOO0O0O0OO0O0OOO0 =(O0O0OOOO000000OOO -O0000O000000O0OOO )/2 #line:4505
            O0OOOO0OO0O0O000O =(OO0O000O0OO000O0O -OOO00000O0O00OO0O )/2 #line:4506
            O000OOOO0OO0000O0 .geometry ("%dx%d+%d+%d"%(O0000O000000O0OOO ,OOO00000O0O00OO0O ,OOO0O0O0OO0O0OOO0 ,O0OOOO0OO0O0O000O ))#line:4507
            OO00O0OO00O0O0000 =ScrolledText (O000OOOO0OO0000O0 ,height =1100 ,width =1100 ,bg ="#FFFFFF")#line:4511
            OO00O0OO00O0O0000 .pack (padx =10 ,pady =10 )#line:4512
            def O0O000000OOOOOO00 (event =None ):#line:4513
                OO00O0OO00O0O0000 .event_generate ('<<Copy>>')#line:4514
            def O0O0O0O0000OO0000 (O0O0OO0O0OOO00OOO ,OOOOO0O0O0OO000OO ):#line:4515
                TOOLS_savetxt (O0O0OO0O0OOO00OOO ,OOOOO0O0O0OO000OO ,1 )#line:4516
            O0O0O000OO000000O =Menu (OO00O0OO00O0O0000 ,tearoff =False ,)#line:4517
            O0O0O000OO000000O .add_command (label ="复制",command =O0O000000OOOOOO00 )#line:4518
            O0O0O000OO000000O .add_command (label ="导出",command =lambda :PROGRAM_thread_it (O0O0O0O0000OO0000 ,OO00O0OO00O0O0000 .get (1.0 ,'end'),filedialog .asksaveasfilename (title =u"保存文件",initialfile =OOO0O0OO0O0O0O000 .iloc [0 ,0 ],defaultextension ="txt",filetypes =[("txt","*.txt")])))#line:4519
            def OOOO000OO0O0OOOOO (O0O0OO00OOO00OO0O ):#line:4521
                O0O0O000OO000000O .post (O0O0OO00OOO00OO0O .x_root ,O0O0OO00OOO00OO0O .y_root )#line:4522
            OO00O0OO00O0O0000 .bind ("<Button-3>",OOOO000OO0O0OOOOO )#line:4523
            try :#line:4525
                O000OOOO0OO0000O0 .title (str (O0OOOOOO00O0OOOOO [0 ]))#line:4526
                OOO0O0OO0O0O0O000 ["报告编码"]=OOO0O0OO0O0O0O000 ["报告编码"].astype ("str")#line:4527
                OOO00O000OO000000 =OOO0O0OO0O0O0O000 [(OOO0O0OO0O0O0O000 ["报告编码"]==str (O0OOOOOO00O0OOOOO [0 ]))]#line:4528
            except :#line:4529
                pass #line:4530
            O0O000O00OOO0000O =OOO0O0OO0O0O0O000 .columns .values .tolist ()#line:4532
            for O0O0O0OOO0OOO0O00 in range (len (O0O000O00OOO0000O )):#line:4533
                try :#line:4535
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="报告编码.1":#line:4536
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4537
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="产品名称":#line:4538
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4539
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="事件发生日期":#line:4540
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4541
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="是否开展了调查":#line:4542
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4543
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="市级监测机构":#line:4544
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4545
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="上报机构描述":#line:4546
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4547
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]=="持有人处理描述":#line:4548
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4549
                    if O0O0O0OOO0OOO0O00 >1 and O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 -1 ]=="持有人处理描述":#line:4550
                        OO00O0OO00O0O0000 .insert (END ,"\n\n")#line:4551
                except :#line:4553
                    pass #line:4554
                try :#line:4555
                    if O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ]in ["单位名称","产品名称ori","上报机构描述","持有人处理描述","产品名称","注册证编号/曾用注册证编号","型号","规格","产品批号","上市许可持有人名称ori","上市许可持有人名称","伤害","伤害表现","器械故障表现","使用过程","事件原因分析描述","初步处置情况","调查情况","关联性评价","事件原因分析.1","具体控制措施"]:#line:4556
                        OO00O0OO00O0O0000 .insert (END ,"●")#line:4557
                except :#line:4558
                    pass #line:4559
                OO00O0OO00O0O0000 .insert (END ,O0O000O00OOO0000O [O0O0O0OOO0OOO0O00 ])#line:4560
                OO00O0OO00O0O0000 .insert (END ,"：")#line:4561
                try :#line:4562
                    OO00O0OO00O0O0000 .insert (END ,OOO00O000OO000000 .iloc [0 ,O0O0O0OOO0OOO0O00 ])#line:4563
                except :#line:4564
                    OO00O0OO00O0O0000 .insert (END ,O0OOOOOO00O0OOOOO [O0O0O0OOO0OOO0O00 ])#line:4565
                OO00O0OO00O0O0000 .insert (END ,"\n")#line:4566
            OO00O0OO00O0O0000 .config (state =DISABLED )#line:4567
    O000O00000OOO0000 .pack ()#line:4569
def TOOLS_get_guize2 (O0O000O0O0O0O0O00 ):#line:4572
	""#line:4573
	O0OO000O00OO00OOO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:4574
	O00OOO00O000OOO0O =pd .read_excel (O0OO000O00OO00OOO ,header =0 ,sheet_name ="器械")#line:4575
	O0000OOO0O000OOOO =O00OOO00O000OOO0O [["适用范围列","适用范围"]].drop_duplicates ("适用范围")#line:4576
	text .insert (END ,O0000OOO0O000OOOO )#line:4577
	text .see (END )#line:4578
	O0O0000OOO0OOO0O0 =Toplevel ()#line:4579
	O0O0000OOO0OOO0O0 .title ('切换通用规则')#line:4580
	OOOO0OOOOO0OOO00O =O0O0000OOO0OOO0O0 .winfo_screenwidth ()#line:4581
	O000000O000O0000O =O0O0000OOO0OOO0O0 .winfo_screenheight ()#line:4583
	O0O0O000OO00O000O =450 #line:4585
	OO0OO00OOO00O0000 =100 #line:4586
	OOO00000O0OO000O0 =(OOOO0OOOOO0OOO00O -O0O0O000OO00O000O )/2 #line:4588
	OOOO000OO0O0000OO =(O000000O000O0000O -OO0OO00OOO00O0000 )/2 #line:4589
	O0O0000OOO0OOO0O0 .geometry ("%dx%d+%d+%d"%(O0O0O000OO00O000O ,OO0OO00OOO00O0000 ,OOO00000O0OO000O0 ,OOOO000OO0O0000OO ))#line:4590
	O0O000O000OOO0OO0 =Label (O0O0000OOO0OOO0O0 ,text ="查找位置：器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况")#line:4591
	O0O000O000OOO0OO0 .pack ()#line:4592
	OO000OO0O00O0OO0O =Label (O0O0000OOO0OOO0O0 ,text ="请选择您所需要的通用规则关键字：")#line:4593
	OO000OO0O00O0OO0O .pack ()#line:4594
	def OOO0OOO00OO00O00O (*O0O0O0O0O0O000O0O ):#line:4595
		O000OO000OOOOOOOO .set (OOO0OO0OOO0OOO0O0 .get ())#line:4596
	O000OO000OOOOOOOO =StringVar ()#line:4597
	OOO0OO0OOO0OOO0O0 =ttk .Combobox (O0O0000OOO0OOO0O0 ,width =14 ,height =30 ,state ="readonly",textvariable =O000OO000OOOOOOOO )#line:4598
	OOO0OO0OOO0OOO0O0 ["values"]=O0000OOO0O000OOOO ["适用范围"].to_list ()#line:4599
	OOO0OO0OOO0OOO0O0 .current (0 )#line:4600
	OOO0OO0OOO0OOO0O0 .bind ("<<ComboboxSelected>>",OOO0OOO00OO00O00O )#line:4601
	OOO0OO0OOO0OOO0O0 .pack ()#line:4602
	O0O0O0O0O0O000000 =LabelFrame (O0O0000OOO0OOO0O0 )#line:4605
	OO0O000OO000000O0 =Button (O0O0O0O0O0O000000 ,text ="确定",width =10 ,command =lambda :OOO00O0O00O000000 (O00OOO00O000OOO0O ,O000OO000OOOOOOOO .get ()))#line:4606
	OO0O000OO000000O0 .pack (side =LEFT ,padx =1 ,pady =1 )#line:4607
	O0O0O0O0O0O000000 .pack ()#line:4608
	def OOO00O0O00O000000 (OOOOOOOOOO0OO00OO ,OOO000O0OOOOOOO0O ):#line:4610
		O0OOO00OO0O00O0OO =OOOOOOOOOO0OO00OO .loc [OOOOOOOOOO0OO00OO ["适用范围"].str .contains (OOO000O0OOOOOOO0O ,na =False )].copy ().reset_index (drop =True )#line:4611
		TABLE_tree_Level_2 (Countall (O0O000O0O0O0O0O00 ).df_psur ("特定品种作为通用关键字",O0OOO00OO0O00O0OO ),1 ,O0O000O0O0O0O0O00 )#line:4612
def TOOLS_findin (OOO0OOOOO0OOO0OOO ,OOOOOO0OO0OO0OOO0 ):#line:4613
	""#line:4614
	OO0000OOO00O0000O =Toplevel ()#line:4615
	OO0000OOO00O0000O .title ('高级查找')#line:4616
	OOO0O0O000OO0OO00 =OO0000OOO00O0000O .winfo_screenwidth ()#line:4617
	O0OO000OO0O000OO0 =OO0000OOO00O0000O .winfo_screenheight ()#line:4619
	O00OOOOOO00OOOO00 =400 #line:4621
	O0OOO00000O0OO0O0 =120 #line:4622
	O00000OOOOO0OO00O =(OOO0O0O000OO0OO00 -O00OOOOOO00OOOO00 )/2 #line:4624
	OO0O0O0O000OOO000 =(O0OO000OO0O000OO0 -O0OOO00000O0OO0O0 )/2 #line:4625
	OO0000OOO00O0000O .geometry ("%dx%d+%d+%d"%(O00OOOOOO00OOOO00 ,O0OOO00000O0OO0O0 ,O00000OOOOO0OO00O ,OO0O0O0O000OOO000 ))#line:4626
	O0O0000OOOO0OOO0O =Label (OO0000OOO00O0000O ,text ="需要查找的关键字（用|隔开）：")#line:4627
	O0O0000OOOO0OOO0O .pack ()#line:4628
	O00000O000O0OO00O =Label (OO0000OOO00O0000O ,text ="在哪些列查找（用|隔开）：")#line:4629
	OOO0O0OOO0OOO0OOO =Entry (OO0000OOO00O0000O ,width =80 )#line:4631
	OOO0O0OOO0OOO0OOO .insert (0 ,"破裂|断裂")#line:4632
	O0O000OOOOO00O0O0 =Entry (OO0000OOO00O0000O ,width =80 )#line:4633
	O0O000OOOOO00O0O0 .insert (0 ,"器械故障表现|伤害表现")#line:4634
	OOO0O0OOO0OOO0OOO .pack ()#line:4635
	O00000O000O0OO00O .pack ()#line:4636
	O0O000OOOOO00O0O0 .pack ()#line:4637
	O0O00OO0O00O00O00 =LabelFrame (OO0000OOO00O0000O )#line:4638
	OOOOOO0000O0OO00O =Button (O0O00OO0O00O00O00 ,text ="确定",width =10 ,command =lambda :PROGRAM_thread_it (TABLE_tree_Level_2 ,O00O0OOO00OO0OOO0 (OOO0O0OOO0OOO0OOO .get (),O0O000OOOOO00O0O0 .get (),OOO0OOOOO0OOO0OOO ),1 ,OOOOOO0OO0OO0OOO0 ))#line:4639
	OOOOOO0000O0OO00O .pack (side =LEFT ,padx =1 ,pady =1 )#line:4640
	O0O00OO0O00O00O00 .pack ()#line:4641
	def O00O0OOO00OO0OOO0 (O0O0OOOO0OOOOO000 ,O000OOO0O00OOO00O ,OO0OO000OO0O00000 ):#line:4644
		OO0OO000OO0O00000 ["关键字查找列10"]="######"#line:4645
		for O00O0OO00OO00O00O in TOOLS_get_list (O000OOO0O00OOO00O ):#line:4646
			OO0OO000OO0O00000 ["关键字查找列10"]=OO0OO000OO0O00000 ["关键字查找列10"].astype (str )+OO0OO000OO0O00000 [O00O0OO00OO00O00O ].astype (str )#line:4647
		OO0OO000OO0O00000 =OO0OO000OO0O00000 .loc [OO0OO000OO0O00000 ["关键字查找列10"].str .contains (O0O0OOOO0OOOOO000 ,na =False )]#line:4648
		del OO0OO000OO0O00000 ["关键字查找列10"]#line:4649
		return OO0OO000OO0O00000 #line:4650
def PROGRAM_about ():#line:4652
    ""#line:4653
    OO0O0OO0O00OOOO00 =" 佛山市食品药品检验检测中心 \n(佛山市药品不良反应监测中心)\n蔡权周（QQ或微信411703730）\n仅供政府设立的不良反应监测机构使用。"#line:4654
    showinfo (title ="关于",message =OO0O0OO0O00OOOO00 )#line:4655
def PROGRAM_thread_it (O000O0O0OOO00OOOO ,*O000O000O0OO0O0OO ):#line:4658
    ""#line:4659
    OOO0O00O000OOO00O =threading .Thread (target =O000O0O0OOO00OOOO ,args =O000O000O0OO0O0OO )#line:4661
    OOO0O00O000OOO00O .setDaemon (True )#line:4663
    OOO0O00O000OOO00O .start ()#line:4665
def PROGRAM_Menubar (OOO000OO0O0OOOOOO ,OOOO000O00OOOO00O ,O00OOO00O0OO000OO ,O0000OO00OO000OOO ):#line:4666
	""#line:4667
	OOO0O0OO0O0O0O0O0 =Menu (OOO000OO0O0OOOOOO )#line:4669
	OOO000OO0O0OOOOOO .config (menu =OOO0O0OO0O0O0O0O0 )#line:4671
	O0OOO0OO0O0OOO000 =Menu (OOO0O0OO0O0O0O0O0 ,tearoff =0 )#line:4673
	OOO0O0OO0O0O0O0O0 .add_cascade (label ="实用工具",menu =O0OOO0OO0O0OOO000 )#line:4674
	O0OOO0OO0O0OOO000 .add_command (label ="统计工具箱",command =lambda :TABLE_tree_Level_2 (OOOO000O00OOOO00O ,1 ,O0000OO00OO000OOO ,"tools_x"))#line:4676
	O0OOO0OO0O0OOO000 .add_command (label ="数据规整（自定义）",command =lambda :TOOL_guizheng (OOOO000O00OOOO00O ,0 ,False ))#line:4678
	O0OOO0OO0O0OOO000 .add_command (label ="批量筛选（自定义）",command =lambda :TOOLS_xuanze (OOOO000O00OOOO00O ,0 ))#line:4680
	O0OOO0OO0O0OOO000 .add_separator ()#line:4681
	O0OOO0OO0O0OOO000 .add_command (label ="原始导入",command =TOOLS_fileopen )#line:4683
	if ini ["模式"]=="其他":#line:4688
		return 0 #line:4689
	if ini ["模式"]=="药品"or ini ["模式"]=="器械":#line:4691
		O00OO00OOOOOOOOO0 =Menu (OOO0O0OO0O0O0O0O0 ,tearoff =0 )#line:4692
		OOO0O0OO0O0O0O0O0 .add_cascade (label ="信号检测",menu =O00OO00OOOOOOOOO0 )#line:4693
		O00OO00OOOOOOOOO0 .add_command (label ="预警（单日）",command =lambda :TOOLS_keti (OOOO000O00OOOO00O ))#line:4695
		O00OO00OOOOOOOOO0 .add_separator ()#line:4696
		O00OO00OOOOOOOOO0 .add_command (label ="数量比例失衡监测-证号内批号",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_findrisk ("产品批号"),1 ,O0000OO00OO000OOO ))#line:4698
		O00OO00OOOOOOOOO0 .add_command (label ="数量比例失衡监测-证号内季度",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_findrisk ("事件发生季度"),1 ,O0000OO00OO000OOO ))#line:4700
		O00OO00OOOOOOOOO0 .add_command (label ="数量比例失衡监测-证号内月份",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_findrisk ("事件发生月份"),1 ,O0000OO00OO000OOO ))#line:4702
		O00OO00OOOOOOOOO0 .add_command (label ="数量比例失衡监测-证号内性别",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_findrisk ("性别"),1 ,O0000OO00OO000OOO ))#line:4704
		O00OO00OOOOOOOOO0 .add_command (label ="数量比例失衡监测-证号内年龄段",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_findrisk ("年龄段"),1 ,O0000OO00OO000OOO ))#line:4706
		O00OO00OOOOOOOOO0 .add_separator ()#line:4708
		O00OO00OOOOOOOOO0 .add_command (label ="关键字检测（同证号内不同批号比对）",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_find_all_keword_risk ("产品批号"),1 ,O0000OO00OO000OOO ))#line:4710
		O00OO00OOOOOOOOO0 .add_command (label ="关键字检测（同证号内不同月份比对）",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_find_all_keword_risk ("事件发生月份"),1 ,O0000OO00OO000OOO ))#line:4712
		O00OO00OOOOOOOOO0 .add_command (label ="关键字检测（同证号内不同季度比对）",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_find_all_keword_risk ("事件发生季度"),1 ,O0000OO00OO000OOO ))#line:4714
		O00OO00OOOOOOOOO0 .add_command (label ="关键字检测（同证号内不同性别比对）",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_find_all_keword_risk ("性别"),1 ,O0000OO00OO000OOO ))#line:4716
		O00OO00OOOOOOOOO0 .add_command (label ="关键字检测（同证号内不同年龄段比对）",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_find_all_keword_risk ("年龄段"),1 ,O0000OO00OO000OOO ))#line:4718
		O00OO00OOOOOOOOO0 .add_separator ()#line:4720
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同证号的批号间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","产品批号"]),1 ,O0000OO00OO000OOO ))#line:4722
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同证号的月份间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生月份"]),1 ,O0000OO00OO000OOO ))#line:4724
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同证号的季度间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","事件发生季度"]),1 ,O0000OO00OO000OOO ))#line:4726
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同证号的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","年龄段"]),1 ,O0000OO00OO000OOO ))#line:4728
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同证号的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号","性别"]),1 ,O0000OO00OO000OOO ))#line:4730
		O00OO00OOOOOOOOO0 .add_separator ()#line:4732
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同品名的证号间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]),1 ,O0000OO00OO000OOO ))#line:4734
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同品名的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["产品类别","规整后品类","产品名称","年龄段"]),1 ,O0000OO00OO000OOO ))#line:4736
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同品名的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["产品类别","规整后品类","产品名称","性别"]),1 ,O0000OO00OO000OOO ))#line:4738
		O00OO00OOOOOOOOO0 .add_separator ()#line:4740
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同类别的名称间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["产品类别","产品名称"]),1 ,O0000OO00OO000OOO ))#line:4742
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同类别的年龄段间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["产品类别","年龄段"]),1 ,O0000OO00OO000OOO ))#line:4744
		O00OO00OOOOOOOOO0 .add_command (label ="关键字ROR-页面内同类别的性别间比对",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_ror (["产品类别","性别"]),1 ,O0000OO00OO000OOO ))#line:4746
	O00OO0000OO0OOOO0 =Menu (OOO0O0OO0O0O0O0O0 ,tearoff =0 )#line:4750
	OOO0O0OO0O0O0O0O0 .add_cascade (label ="简报制作",menu =O00OO0000OO0OOOO0 )#line:4751
	O00OO0000OO0OOOO0 .add_command (label ="药品简报",command =lambda :TOOLS_autocount (OOOO000O00OOOO00O ,"药品"))#line:4754
	O00OO0000OO0OOOO0 .add_command (label ="器械简报",command =lambda :TOOLS_autocount (OOOO000O00OOOO00O ,"器械"))#line:4756
	O00OO0000OO0OOOO0 .add_command (label ="化妆品简报",command =lambda :TOOLS_autocount (OOOO000O00OOOO00O ,"化妆品"))#line:4758
	OOO0O00O00O0OO000 =Menu (OOO0O0OO0O0O0O0O0 ,tearoff =0 )#line:4762
	OOO0O0OO0O0O0O0O0 .add_cascade (label ="品种评价",menu =OOO0O00O00O0OO000 )#line:4763
	OOO0O00O00O0OO000 .add_command (label ="报告年份",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"报告年份",-1 ))#line:4765
	OOO0O00O00O0OO000 .add_command (label ="发生年份",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"事件发生年份",-1 ))#line:4767
	OOO0O00O00O0OO000 .add_separator ()#line:4768
	OOO0O00O00O0OO000 .add_command (label ="涉及企业",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"上市许可持有人名称",1 ))#line:4771
	OOO0O00O00O0OO000 .add_command (label ="产品名称",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"产品名称",1 ))#line:4773
	OOO0O00O00O0OO000 .add_command (label ="注册证号",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_zhenghao (),1 ,O0000OO00OO000OOO ))#line:4775
	OOO0O00O00O0OO000 .add_separator ()#line:4776
	OOO0O00O00O0OO000 .add_command (label ="年龄段分布",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"年龄段",1 ))#line:4778
	OOO0O00O00O0OO000 .add_command (label ="性别分布",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"性别",1 ))#line:4780
	OOO0O00O00O0OO000 .add_command (label ="年龄性别分布",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_age (),1 ,O0000OO00OO000OOO ,))#line:4782
	OOO0O00O00O0OO000 .add_separator ()#line:4783
	OOO0O00O00O0OO000 .add_command (label ="事件发生时间",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"时隔",1 ))#line:4785
	if ini ["模式"]=="器械":#line:4786
		OOO0O00O00O0OO000 .add_command (label ="事件分布（故障表现）",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"器械故障表现",0 ))#line:4788
		OOO0O00O00O0OO000 .add_command (label ="事件分布（关键词）",command =lambda :TOOLS_get_guize2 (OOOO000O00OOOO00O ))#line:4790
	if ini ["模式"]=="药品":#line:4791
		OOO0O00O00O0OO000 .add_command (label ="怀疑/并用",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"怀疑/并用",1 ))#line:4793
		OOO0O00O00O0OO000 .add_command (label ="报告类型-严重程度",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"报告类型-严重程度",1 ))#line:4795
		OOO0O00O00O0OO000 .add_command (label ="停药减药后反应是否减轻或消失",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"停药减药后反应是否减轻或消失",1 ))#line:4797
		OOO0O00O00O0OO000 .add_command (label ="再次使用可疑药是否出现同样反应",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"再次使用可疑药是否出现同样反应",1 ))#line:4799
		OOO0O00O00O0OO000 .add_command (label ="对原患疾病影响",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"对原患疾病影响",1 ))#line:4801
		OOO0O00O00O0OO000 .add_command (label ="不良反应结果",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"不良反应结果",1 ))#line:4803
		OOO0O00O00O0OO000 .add_command (label ="报告单位关联性评价",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"关联性评价",1 ))#line:4805
		OOO0O00O00O0OO000 .add_separator ()#line:4806
		OOO0O00O00O0OO000 .add_command (label ="不良反应转归情况",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"不良反应结果2",4 ))#line:4808
		OOO0O00O00O0OO000 .add_command (label ="品种评价-关联性评价汇总",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"关联性评价汇总",5 ))#line:4810
		OOO0O00O00O0OO000 .add_separator ()#line:4814
		OOO0O00O00O0OO000 .add_command (label ="不良反应-术语",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"器械故障表现",0 ))#line:4816
		OOO0O00O00O0OO000 .add_command (label ="不良反应器官系统-术语",command =lambda :TABLE_tree_Level_2 (Countall (OOOO000O00OOOO00O ).df_psur (),1 ,O0000OO00OO000OOO ))#line:4818
		if "不良反应-code"in OOOO000O00OOOO00O .columns :#line:4819
			OOO0O00O00O0OO000 .add_command (label ="不良反应-由code转化",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"不良反应-code",2 ))#line:4821
			OOO0O00O00O0OO000 .add_command (label ="不良反应器官系统-由code转化",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"不良反应-code",3 ))#line:4823
			OOO0O00O00O0OO000 .add_separator ()#line:4824
		OOO0O00O00O0OO000 .add_command (label ="疾病名称-术语",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"相关疾病信息[疾病名称]-术语",0 ))#line:4826
		if "不良反应-code"in OOOO000O00OOOO00O .columns :#line:4827
			OOO0O00O00O0OO000 .add_command (label ="疾病名称-由code转化",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"相关疾病信息[疾病名称]-code",2 ))#line:4829
			OOO0O00O00O0OO000 .add_command (label ="疾病器官系统-由code转化",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"相关疾病信息[疾病名称]-code",3 ))#line:4831
			OOO0O00O00O0OO000 .add_separator ()#line:4832
		OOO0O00O00O0OO000 .add_command (label ="适应症-术语",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"治疗适应症-术语",0 ))#line:4834
		if "不良反应-code"in OOOO000O00OOOO00O .columns :#line:4835
			OOO0O00O00O0OO000 .add_command (label ="适应症-由code转化",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"治疗适应症-code",2 ))#line:4837
			OOO0O00O00O0OO000 .add_command (label ="适应症器官系统-由code转化",command =lambda :STAT_pinzhong (OOOO000O00OOOO00O ,"治疗适应症-code",3 ))#line:4839
	if ini ["模式"]=="药品":#line:4841
		O000O000OO0000OO0 =Menu (OOO0O0OO0O0O0O0O0 ,tearoff =0 )#line:4842
		OOO0O0OO0O0O0O0O0 .add_cascade (label ="药品探索",menu =O000O000OO0000OO0 )#line:4843
		O000O000OO0000OO0 .add_command (label ="新的不良反应检测(证号)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0000OO00OO000OOO ,"证号"))#line:4844
		O000O000OO0000OO0 .add_command (label ="新的不良反应检测(品种)",command =lambda :PROGRAM_thread_it (TOOLS_get_new ,O0000OO00OO000OOO ,"品种"))#line:4845
		O000O000OO0000OO0 .add_separator ()#line:4846
		O000O000OO0000OO0 .add_command (label ="基础信息批量操作（品名）",command =lambda :TOOLS_ror_mode1 (OOOO000O00OOOO00O ,"产品名称"))#line:4848
		O000O000OO0000OO0 .add_command (label ="器官系统分类批量操作（品名）",command =lambda :TOOLS_ror_mode4 (OOOO000O00OOOO00O ,"产品名称"))#line:4850
		O000O000OO0000OO0 .add_command (label ="器官系统ROR批量操作（品名）",command =lambda :TOOLS_ror_mode2 (OOOO000O00OOOO00O ,"产品名称"))#line:4852
		O000O000OO0000OO0 .add_command (label ="ADR-ROR批量操作（品名）",command =lambda :TOOLS_ror_mode3 (OOOO000O00OOOO00O ,"产品名称"))#line:4854
		O000O000OO0000OO0 .add_separator ()#line:4855
		O000O000OO0000OO0 .add_command (label ="基础信息批量操作（批准文号）",command =lambda :TOOLS_ror_mode1 (OOOO000O00OOOO00O ,"注册证编号/曾用注册证编号"))#line:4857
		O000O000OO0000OO0 .add_command (label ="器官系统分类批量操作（批准文号）",command =lambda :TOOLS_ror_mode4 (OOOO000O00OOOO00O ,"注册证编号/曾用注册证编号"))#line:4859
		O000O000OO0000OO0 .add_command (label ="器官系统ROR批量操作（批准文号）",command =lambda :TOOLS_ror_mode2 (OOOO000O00OOOO00O ,"注册证编号/曾用注册证编号"))#line:4861
		O000O000OO0000OO0 .add_command (label ="ADR-ROR批量操作（批准文号）",command =lambda :TOOLS_ror_mode3 (OOOO000O00OOOO00O ,"注册证编号/曾用注册证编号"))#line:4863
	O000O0OOO000000OO =Menu (OOO0O0OO0O0O0O0O0 ,tearoff =0 )#line:4880
	OOO0O0OO0O0O0O0O0 .add_cascade (label ="其他",menu =O000O0OOO000000OO )#line:4881
	O000O0OOO000000OO .add_command (label ="数据规整（报告单位）",command =lambda :TOOL_guizheng (OOOO000O00OOOO00O ,2 ,False ))#line:4885
	O000O0OOO000000OO .add_command (label ="数据规整（产品名称）",command =lambda :TOOL_guizheng (OOOO000O00OOOO00O ,3 ,False ))#line:4887
	O000O0OOO000000OO .add_command (label ="脱敏保存",command =lambda :TOOLS_data_masking (OOOO000O00OOOO00O ))#line:4889
	O000O0OOO000000OO .add_separator ()#line:4890
	O000O0OOO000000OO .add_command (label ="评价人员（广东化妆品）",command =lambda :TOOL_person (OOOO000O00OOOO00O ))#line:4892
	O000O0OOO000000OO .add_command (label ="意见反馈",command =lambda :PROGRAM_helper (["","  药械妆不良反应报表统计分析工作站","  开发者：蔡权周","  邮箱：411703730@qq.com","  微信号：sysucai","  手机号：18575757461"]))#line:4894
	O000O0OOO000000OO .add_command (label ="更改用户组",command =lambda :PROGRAM_thread_it (display_random_number ))#line:4896
def PROGRAM_helper (O0O0OO0OO0OOO00OO ):#line:4900
    ""#line:4901
    OO0O00OOO000O00O0 =Toplevel ()#line:4902
    OO0O00OOO000O00O0 .title ("信息查看")#line:4903
    OO0O00OOO000O00O0 .geometry ("700x500")#line:4904
    O0OO0OOOOO00OO000 =Scrollbar (OO0O00OOO000O00O0 )#line:4906
    OO0O0O00O00OO00OO =Text (OO0O00OOO000O00O0 ,height =80 ,width =150 ,bg ="#FFFFFF",font ="微软雅黑")#line:4907
    O0OO0OOOOO00OO000 .pack (side =RIGHT ,fill =Y )#line:4908
    OO0O0O00O00OO00OO .pack ()#line:4909
    O0OO0OOOOO00OO000 .config (command =OO0O0O00O00OO00OO .yview )#line:4910
    OO0O0O00O00OO00OO .config (yscrollcommand =O0OO0OOOOO00OO000 .set )#line:4911
    for OOO0000O0O0O0000O in O0O0OO0OO0OOO00OO :#line:4913
        OO0O0O00O00OO00OO .insert (END ,OOO0000O0O0O0000O )#line:4914
        OO0O0O00O00OO00OO .insert (END ,"\n")#line:4915
    def OOOO00OOOOOOOOO00 (event =None ):#line:4918
        OO0O0O00O00OO00OO .event_generate ('<<Copy>>')#line:4919
    O0OOOO000O0OO0000 =Menu (OO0O0O00O00OO00OO ,tearoff =False ,)#line:4922
    O0OOOO000O0OO0000 .add_command (label ="复制",command =OOOO00OOOOOOOOO00 )#line:4923
    def O0OOOO0OO0O00OO0O (O0O0O0O0OOOOOO0OO ):#line:4924
         O0OOOO000O0OO0000 .post (O0O0O0O0OOOOOO0OO .x_root ,O0O0O0O0OOOOOO0OO .y_root )#line:4925
    OO0O0O00O00OO00OO .bind ("<Button-3>",O0OOOO0OO0O00OO0O )#line:4926
    OO0O0O00O00OO00OO .config (state =DISABLED )#line:4928
def PROGRAM_change_schedule (OOO00O0OO00OO00OO ,O0OO000OOO0OO0O00 ):#line:4930
    ""#line:4931
    canvas .coords (fill_rec ,(5 ,5 ,(OOO00O0OO00OO00OO /O0OO000OOO0OO0O00 )*680 ,25 ))#line:4933
    root .update ()#line:4934
    x .set (str (round (OOO00O0OO00OO00OO /O0OO000OOO0OO0O00 *100 ,2 ))+"%")#line:4935
    if round (OOO00O0OO00OO00OO /O0OO000OOO0OO0O00 *100 ,2 )==100.00 :#line:4936
        x .set ("完成")#line:4937
def PROGRAM_showWelcome ():#line:4940
    ""#line:4941
    OOOO0OO000000OO00 =roox .winfo_screenwidth ()#line:4942
    OO000000O00OO000O =roox .winfo_screenheight ()#line:4944
    roox .overrideredirect (True )#line:4946
    roox .attributes ("-alpha",1 )#line:4947
    O0OO00OO0OO0OOOO0 =(OOOO0OO000000OO00 -475 )/2 #line:4948
    O0O0O0OO0OO000OOO =(OO000000O00OO000O -200 )/2 #line:4949
    roox .geometry ("675x130+%d+%d"%(O0OO00OO0OO0OOOO0 ,O0O0O0OO0OO000OOO ))#line:4951
    roox ["bg"]="royalblue"#line:4952
    OOOOO0000OOOO0O0O =Label (roox ,text =title_all2 ,fg ="white",bg ="royalblue",font =("微软雅黑",20 ))#line:4955
    OOOOO0000OOOO0O0O .place (x =0 ,y =15 ,width =675 ,height =90 )#line:4956
    O00O00OO0O00OO0OO =Label (roox ,text ="仅供监测机构使用 ",fg ="white",bg ="cornflowerblue",font =("微软雅黑",15 ))#line:4959
    O00O00OO0O00OO0OO .place (x =0 ,y =90 ,width =675 ,height =40 )#line:4960
def PROGRAM_closeWelcome ():#line:4963
    ""#line:4964
    for OOOOOOO0000OO0OO0 in range (2 ):#line:4965
        root .attributes ("-alpha",0 )#line:4966
        time .sleep (1 )#line:4967
    root .attributes ("-alpha",1 )#line:4968
    roox .destroy ()#line:4969
class Countall ():#line:4984
	""#line:4985
	def __init__ (OO000O00O000OO0O0 ,O00OOOOOOOOO00O00 ):#line:4986
		""#line:4987
		OO000O00O000OO0O0 .df =O00OOOOOOOOO00O00 #line:4988
		OO000O00O000OO0O0 .mode =ini ["模式"]#line:4989
	def df_org (O0O0O00000O0000O0 ,O0OOOOOO000O0OOO0 ):#line:4991
		""#line:4992
		OOO000OOOOO0O000O =O0O0O00000O0000O0 .df .drop_duplicates (["报告编码"]).groupby ([O0OOOOOO000O0OOO0 ]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OOOO000OOOOOOO000 :STAT_countpx (OOOO000OOOOOOO000 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0O00O0O0O000O0O0 :STAT_countpx (O0O00O0O0O000O0O0 .values ,"死亡")),超时报告数 =("超时标记",lambda OO0OOOOOOOOO0OO00 :STAT_countpx (OO0OOOOOOOOO0OO00 .values ,1 )),有源 =("产品类别",lambda OOOO0O0OOOOOO0OO0 :STAT_countpx (OOOO0O0OOOOOO0OO0 .values ,"有源")),无源 =("产品类别",lambda O0OOOO00OOOOOO000 :STAT_countpx (O0OOOO00OOOOOO000 .values ,"无源")),体外诊断试剂 =("产品类别",lambda O0OO00O0O0OOOO0O0 :STAT_countpx (O0OO00O0O0OOOO0O0 .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda O00OO0OO0OO00O0OO :STAT_countpx (O00OO0OO0OO00O0OO .values ,"Ⅲ类")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:5007
		OO0OO0O0OOO0OO0O0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量","单位个数"]#line:5009
		OOO000OOOOO0O000O .loc ["合计"]=OOO000OOOOO0O000O [OO0OO0O0OOO0OO0O0 ].apply (lambda O000O0O0OO0OO000O :O000O0O0OO0OO000O .sum ())#line:5010
		OOO000OOOOO0O000O [OO0OO0O0OOO0OO0O0 ]=OOO000OOOOO0O000O [OO0OO0O0OOO0OO0O0 ].apply (lambda O00OOOO00OO000O00 :O00OOOO00OO000O00 .astype (int ))#line:5011
		OOO000OOOOO0O000O .iloc [-1 ,0 ]="合计"#line:5012
		OOO000OOOOO0O000O ["严重比"]=round ((OOO000OOOOO0O000O ["严重伤害数"]+OOO000OOOOO0O000O ["死亡数量"])/OOO000OOOOO0O000O ["报告数量"]*100 ,2 )#line:5014
		OOO000OOOOO0O000O ["Ⅲ类比"]=round ((OOO000OOOOO0O000O ["三类数量"])/OOO000OOOOO0O000O ["报告数量"]*100 ,2 )#line:5015
		OOO000OOOOO0O000O ["超时比"]=round ((OOO000OOOOO0O000O ["超时报告数"])/OOO000OOOOO0O000O ["报告数量"]*100 ,2 )#line:5016
		OOO000OOOOO0O000O ["报表类型"]="dfx_org"+O0OOOOOO000O0OOO0 #line:5017
		if ini ["模式"]=="药品":#line:5020
			del OOO000OOOOO0O000O ["有源"]#line:5022
			del OOO000OOOOO0O000O ["无源"]#line:5023
			del OOO000OOOOO0O000O ["体外诊断试剂"]#line:5024
			OOO000OOOOO0O000O =OOO000OOOOO0O000O .rename (columns ={"三类数量":"新的和严重的数量"})#line:5025
			OOO000OOOOO0O000O =OOO000OOOOO0O000O .rename (columns ={"Ⅲ类比":"新严比"})#line:5026
		return OOO000OOOOO0O000O #line:5028
	def df_user (OO0O0OO000OOO000O ):#line:5032
		""#line:5033
		OO0O0OO000OOO000O .df ["医疗机构类别"]=OO0O0OO000OOO000O .df ["医疗机构类别"].fillna ("未填写")#line:5034
		O00OOOO00OOO00000 =OO0O0OO000OOO000O .df .drop_duplicates (["报告编码"]).groupby (["监测机构","单位名称","医疗机构类别"]).agg (报告数量 =("注册证编号/曾用注册证编号","count"),审核通过数 =("有效报告","sum"),严重伤害数 =("伤害",lambda OOO0O0000O0O0O000 :STAT_countpx (OOO0O0000O0O0O000 .values ,"严重伤害")),死亡数量 =("伤害",lambda O00OOO0OO0O00O0OO :STAT_countpx (O00OOO0OO0O00O0OO .values ,"死亡")),超时报告数 =("超时标记",lambda O0O0OOOO0OOOO0OOO :STAT_countpx (O0O0OOOO0OOOO0OOO .values ,1 )),有源 =("产品类别",lambda OOOOOO000O0OOOOOO :STAT_countpx (OOOOOO000O0OOOOOO .values ,"有源")),无源 =("产品类别",lambda O0OO000OO00OOOO0O :STAT_countpx (O0OO000OO00OOOO0O .values ,"无源")),体外诊断试剂 =("产品类别",lambda O00O0OOO0O0OO00O0 :STAT_countpx (O00O0OOO0O0OO00O0 .values ,"体外诊断试剂")),三类数量 =("管理类别",lambda OOO00O00000OOO0O0 :STAT_countpx (OOO00O00000OOO0O0 .values ,"Ⅲ类")),产品数量 =("产品名称","nunique"),产品清单 =("产品名称",STAT_countx ),报告季度 =("报告季度",STAT_countx ),报告月份 =("报告月份",STAT_countx ),).sort_values (by ="报告数量",ascending =[False ],na_position ="last").reset_index ()#line:5049
		O0OO0OO0000O00OO0 =["报告数量","审核通过数","严重伤害数","死亡数量","超时报告数","有源","无源","体外诊断试剂","三类数量"]#line:5052
		O00OOOO00OOO00000 .loc ["合计"]=O00OOOO00OOO00000 [O0OO0OO0000O00OO0 ].apply (lambda OO0O0OOOOO0O000O0 :OO0O0OOOOO0O000O0 .sum ())#line:5053
		O00OOOO00OOO00000 [O0OO0OO0000O00OO0 ]=O00OOOO00OOO00000 [O0OO0OO0000O00OO0 ].apply (lambda O0000OOOO00O0OOOO :O0000OOOO00O0OOOO .astype (int ))#line:5054
		O00OOOO00OOO00000 .iloc [-1 ,0 ]="合计"#line:5055
		O00OOOO00OOO00000 ["严重比"]=round ((O00OOOO00OOO00000 ["严重伤害数"]+O00OOOO00OOO00000 ["死亡数量"])/O00OOOO00OOO00000 ["报告数量"]*100 ,2 )#line:5057
		O00OOOO00OOO00000 ["Ⅲ类比"]=round ((O00OOOO00OOO00000 ["三类数量"])/O00OOOO00OOO00000 ["报告数量"]*100 ,2 )#line:5058
		O00OOOO00OOO00000 ["超时比"]=round ((O00OOOO00OOO00000 ["超时报告数"])/O00OOOO00OOO00000 ["报告数量"]*100 ,2 )#line:5059
		O00OOOO00OOO00000 ["报表类型"]="dfx_user"#line:5060
		if ini ["模式"]=="药品":#line:5062
			del O00OOOO00OOO00000 ["有源"]#line:5064
			del O00OOOO00OOO00000 ["无源"]#line:5065
			del O00OOOO00OOO00000 ["体外诊断试剂"]#line:5066
			O00OOOO00OOO00000 =O00OOOO00OOO00000 .rename (columns ={"三类数量":"新的和严重的数量"})#line:5067
			O00OOOO00OOO00000 =O00OOOO00OOO00000 .rename (columns ={"Ⅲ类比":"新严比"})#line:5068
		return O00OOOO00OOO00000 #line:5070
	def df_zhenghao (OO00OOO00OO000OO0 ):#line:5075
		""#line:5076
		OOO00O0O0O0OO0O00 =OO00OOO00OO000OO0 .df .groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (证号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="证号计数",ascending =[False ],na_position ="last").reset_index ()#line:5086
		OO0O0OOO0O0OOO00O =OO00OOO00OO000OO0 .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (严重伤害数 =("伤害",lambda OO0O000000OO00O0O :STAT_countpx (OO0O000000OO00O0O .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOO0O000O00OOO0O :STAT_countpx (OOOO0O000O00OOO0O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOOOO0OOO0O0OOO00 :STAT_countpx (OOOOO0OOO0O0OOO00 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O000OO00O0OOOO0O0 :STAT_countpx (O000OO00O0OOOO0O0 .values ,"严重伤害待评价")),).reset_index ()#line:5095
		OOOO000O0OO0O000O =pd .merge (OOO00O0O0O0OO0O00 ,OO0O0OOO0O0OOO00O ,on =["上市许可持有人名称","产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"],how ="left")#line:5097
		OOOO000O0OO0O000O =STAT_basic_risk (OOOO000O0OO0O000O ,"证号计数","严重伤害数","死亡数量","单位个数")#line:5098
		OOOO000O0OO0O000O =pd .merge (OOOO000O0OO0O000O ,STAT_recent30 (OO00OOO00OO000OO0 .df ,["注册证编号/曾用注册证编号"]),on =["注册证编号/曾用注册证编号"],how ="left")#line:5100
		OOOO000O0OO0O000O ["最近30天报告数"]=OOOO000O0OO0O000O ["最近30天报告数"].fillna (0 ).astype (int )#line:5101
		OOOO000O0OO0O000O ["最近30天报告严重伤害数"]=OOOO000O0OO0O000O ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:5102
		OOOO000O0OO0O000O ["最近30天报告死亡数量"]=OOOO000O0OO0O000O ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:5103
		OOOO000O0OO0O000O ["最近30天报告单位个数"]=OOOO000O0OO0O000O ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:5104
		OOOO000O0OO0O000O ["最近30天风险评分"]=OOOO000O0OO0O000O ["最近30天风险评分"].fillna (0 ).astype (int )#line:5105
		OOOO000O0OO0O000O ["报表类型"]="dfx_zhenghao"#line:5107
		if ini ["模式"]=="药品":#line:5109
			OOOO000O0OO0O000O =OOOO000O0OO0O000O .rename (columns ={"待评价数":"新的数量"})#line:5110
			OOOO000O0OO0O000O =OOOO000O0OO0O000O .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5111
		return OOOO000O0OO0O000O #line:5113
	def df_pihao (O0OOO0OO0OO0000O0 ):#line:5115
		""#line:5116
		O00000O0OO00O00OO =O0OOO0OO0OO0000O0 .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (批号计数 =("报告编码","nunique"),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="批号计数",ascending =[False ],na_position ="last").reset_index ()#line:5123
		OO0O0O0OOOO00OOOO =O0OOO0OO0OO0000O0 .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"]).agg (严重伤害数 =("伤害",lambda O0OOO00OO0OO0OO0O :STAT_countpx (O0OOO00OO0OO0OO0O .values ,"严重伤害")),死亡数量 =("伤害",lambda OOOOO0OO00OOOOOO0 :STAT_countpx (OOOOO0OO00OOOOOO0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda O0000OO000OOO00O0 :STAT_countpx (O0000OO000OOO00O0 .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OO0OOOO00OOO0O000 :STAT_countpx (OO0OOOO00OOO0O000 .values ,"严重伤害待评价")),).reset_index ()#line:5132
		OOOO0O0O0O0OOO000 =pd .merge (O00000O0OO00O00OO ,OO0O0O0OOOO00OOOO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","产品批号"],how ="left")#line:5134
		OOOO0O0O0O0OOO000 =STAT_basic_risk (OOOO0O0O0O0OOO000 ,"批号计数","严重伤害数","死亡数量","单位个数")#line:5136
		OOOO0O0O0O0OOO000 =pd .merge (OOOO0O0O0O0OOO000 ,STAT_recent30 (O0OOO0OO0OO0000O0 .df ,["注册证编号/曾用注册证编号","产品批号"]),on =["注册证编号/曾用注册证编号","产品批号"],how ="left")#line:5138
		OOOO0O0O0O0OOO000 ["最近30天报告数"]=OOOO0O0O0O0OOO000 ["最近30天报告数"].fillna (0 ).astype (int )#line:5139
		OOOO0O0O0O0OOO000 ["最近30天报告严重伤害数"]=OOOO0O0O0O0OOO000 ["最近30天报告严重伤害数"].fillna (0 ).astype (int )#line:5140
		OOOO0O0O0O0OOO000 ["最近30天报告死亡数量"]=OOOO0O0O0O0OOO000 ["最近30天报告死亡数量"].fillna (0 ).astype (int )#line:5141
		OOOO0O0O0O0OOO000 ["最近30天报告单位个数"]=OOOO0O0O0O0OOO000 ["最近30天报告单位个数"].fillna (0 ).astype (int )#line:5142
		OOOO0O0O0O0OOO000 ["最近30天风险评分"]=OOOO0O0O0O0OOO000 ["最近30天风险评分"].fillna (0 ).astype (int )#line:5143
		OOOO0O0O0O0OOO000 ["报表类型"]="dfx_pihao"#line:5145
		if ini ["模式"]=="药品":#line:5146
			OOOO0O0O0O0OOO000 =OOOO0O0O0O0OOO000 .rename (columns ={"待评价数":"新的数量"})#line:5147
			OOOO0O0O0O0OOO000 =OOOO0O0O0O0OOO000 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5148
		return OOOO0O0O0O0OOO000 #line:5149
	def df_xinghao (OO0OO000O0O0O0000 ):#line:5151
		""#line:5152
		O00O00000OO00O000 =OO0OO000O0O0O0000 .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (型号计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),规格个数 =("规格","nunique"),规格列表 =("规格",STAT_countx ),).sort_values (by ="型号计数",ascending =[False ],na_position ="last").reset_index ()#line:5159
		O0O00OO00OO00O0O0 =OO0OO000O0O0O0000 .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"]).agg (严重伤害数 =("伤害",lambda OOO00OO0O0000OOO0 :STAT_countpx (OOO00OO0O0000OOO0 .values ,"严重伤害")),死亡数量 =("伤害",lambda O000000OO0OOO000O :STAT_countpx (O000000OO0OOO000O .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOO00OO0OOO0000OO :STAT_countpx (OOO00OO0OOO0000OO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda OOO0O00OOO000OOO0 :STAT_countpx (OOO0O00OOO000OOO0 .values ,"严重伤害待评价")),).reset_index ()#line:5168
		OOOOOOO0OOOO00OO0 =pd .merge (O00O00000OO00O000 ,O0O00OO00OO00O0O0 ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","型号"],how ="left")#line:5170
		OOOOOOO0OOOO00OO0 ["报表类型"]="dfx_xinghao"#line:5173
		if ini ["模式"]=="药品":#line:5174
			OOOOOOO0OOOO00OO0 =OOOOOOO0OOOO00OO0 .rename (columns ={"待评价数":"新的数量"})#line:5175
			OOOOOOO0OOOO00OO0 =OOOOOOO0OOOO00OO0 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5176
		return OOOOOOO0OOOO00OO0 #line:5178
	def df_guige (O00000OO0O0OOO0O0 ):#line:5180
		""#line:5181
		OOOOO0OOO0OOO0OOO =O00000OO0O0OOO0O0 .df .groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (规格计数 =("报告编码","nunique"),批号个数 =("产品批号","nunique"),批号列表 =("产品批号",STAT_countx ),型号个数 =("型号","nunique"),型号列表 =("型号",STAT_countx ),).sort_values (by ="规格计数",ascending =[False ],na_position ="last").reset_index ()#line:5188
		OO00OO0O00OO00OOO =O00000OO0O0OOO0O0 .df .drop_duplicates (["报告编码"]).groupby (["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"]).agg (严重伤害数 =("伤害",lambda O0O0O00O0OO0OOO00 :STAT_countpx (O0O0O00O0OO0OOO00 .values ,"严重伤害")),死亡数量 =("伤害",lambda O0000OO0000OO0OO0 :STAT_countpx (O0000OO0000OO0OO0 .values ,"死亡")),单位个数 =("单位名称","nunique"),单位列表 =("单位名称",STAT_countx ),待评价数 =("持有人报告状态",lambda OOO00O00OOO0OOOOO :STAT_countpx (OOO00O00OOO0OOOOO .values ,"待评价")),严重伤害待评价数 =("伤害与评价",lambda O0OOOOO0O0OO0OO00 :STAT_countpx (O0OOOOO0O0OO0OO00 .values ,"严重伤害待评价")),).reset_index ()#line:5197
		O0OOOO00OOOO00000 =pd .merge (OOOOO0OOO0OOO0OOO ,OO00OO0O00OO00OOO ,on =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","规格"],how ="left")#line:5199
		O0OOOO00OOOO00000 ["报表类型"]="dfx_guige"#line:5201
		if ini ["模式"]=="药品":#line:5202
			O0OOOO00OOOO00000 =O0OOOO00OOOO00000 .rename (columns ={"待评价数":"新的数量"})#line:5203
			O0OOOO00OOOO00000 =O0OOOO00OOOO00000 .rename (columns ={"严重伤害待评价数":"新的严重的数量"})#line:5204
		return O0OOOO00OOOO00000 #line:5206
	def df_findrisk (OO0O0O000OO00OO0O ,O0O0O0OOO00O0O0O0 ):#line:5208
		""#line:5209
		if O0O0O0OOO00O0O0O0 =="产品批号":#line:5210
			return STAT_find_risk (OO0O0O000OO00OO0O .df [(OO0O0O000OO00OO0O .df ["产品类别"]!="有源")],["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",O0O0O0OOO00O0O0O0 )#line:5211
		else :#line:5212
			return STAT_find_risk (OO0O0O000OO00OO0O .df ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"],"注册证编号/曾用注册证编号",O0O0O0OOO00O0O0O0 )#line:5213
	def df_find_all_keword_risk (O0OO0OOOOO0OOO0OO ,OO000OO0O0O0OOOOO ,*O0O0O00000O000O0O ):#line:5215
		""#line:5216
		OO000OOO0O0OOO000 =O0OO0OOOOO0OOO0OO .df .copy ()#line:5218
		OO000OOO0O0OOO000 =OO000OOO0O0OOO000 .drop_duplicates (["报告编码"]).reset_index (drop =True )#line:5219
		O00OOO0OO000O0000 =time .time ()#line:5220
		OOO00OOOOOOO0O0O0 =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5221
		if "报告类型-新的"in OO000OOO0O0OOO000 .columns :#line:5222
			O000OO00O00OOO0O0 ="药品"#line:5223
		else :#line:5224
			O000OO00O00OOO0O0 ="器械"#line:5225
		OOO0O0OO0O0000000 =pd .read_excel (OOO00OOOOOOO0O0O0 ,header =0 ,sheet_name =O000OO00O00OOO0O0 ).reset_index (drop =True )#line:5226
		try :#line:5229
			if len (O0O0O00000O000O0O [0 ])>0 :#line:5230
				OOO0O0OO0O0000000 =OOO0O0OO0O0000000 .loc [OOO0O0OO0O0000000 ["适用范围"].str .contains (O0O0O00000O000O0O [0 ],na =False )].copy ().reset_index (drop =True )#line:5231
		except :#line:5232
			pass #line:5233
		OOOOOO00000O000OO =["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号"]#line:5235
		O0OO00000000O0O00 =OOOOOO00000O000OO [-1 ]#line:5236
		OOO0O0OO0OOOO0O0O =OO000OOO0O0OOO000 .groupby (OOOOOO00000O000OO ).agg (总数量 =(O0OO00000000O0O00 ,"count"),严重伤害数 =("伤害",lambda O0O00OO0O0OOO000O :STAT_countpx (O0O00OO0O0OOO000O .values ,"严重伤害")),死亡数量 =("伤害",lambda OO0OO00O0OO0O0OO0 :STAT_countpx (OO0OO00O0OO0O0OO0 .values ,"死亡")),)#line:5241
		O0OO00000000O0O00 =OOOOOO00000O000OO [-1 ]#line:5242
		OOO000OOOO0O0OOO0 =OOOOOO00000O000OO .copy ()#line:5244
		OOO000OOOO0O0OOO0 .append (OO000OO0O0O0OOOOO )#line:5245
		OOO00OOO0O000OOOO =OO000OOO0O0OOO000 .groupby (OOO000OOOO0O0OOO0 ).agg (该元素总数量 =(O0OO00000000O0O00 ,"count"),).reset_index ()#line:5248
		OOO0O0OO0OOOO0O0O =OOO0O0OO0OOOO0O0O [(OOO0O0OO0OOOO0O0O ["总数量"]>=3 )].reset_index ()#line:5251
		O00O000000000O00O =[]#line:5252
		O0O0OO0000OO00OOO =0 #line:5256
		O00OOO0OO0OO0000O =int (len (OOO0O0OO0OOOO0O0O ))#line:5257
		for O00O00OO000O0O00O ,O0000OOOO00OOOO0O ,OO0OOOO0OOO00OOOO ,OOO000000O0O000OO in zip (OOO0O0OO0OOOO0O0O ["产品名称"].values ,OOO0O0OO0OOOO0O0O ["产品类别"].values ,OOO0O0OO0OOOO0O0O [O0OO00000000O0O00 ].values ,OOO0O0OO0OOOO0O0O ["总数量"].values ):#line:5258
			O0O0OO0000OO00OOO +=1 #line:5259
			if (time .time ()-O00OOO0OO000O0000 )>3 :#line:5261
				root .attributes ("-topmost",True )#line:5262
				PROGRAM_change_schedule (O0O0OO0000OO00OOO ,O00OOO0OO0OO0000O )#line:5263
				root .attributes ("-topmost",False )#line:5264
			O000000O00000O0OO =OO000OOO0O0OOO000 [(OO000OOO0O0OOO000 [O0OO00000000O0O00 ]==OO0OOOO0OOO00OOOO )].copy ()#line:5265
			OOO0O0OO0O0000000 ["SELECT"]=OOO0O0OO0O0000000 .apply (lambda OOO0OO0O0OOO0OOO0 :(OOO0OO0O0OOO0OOO0 ["适用范围"]in O00O00OO000O0O00O )or (OOO0OO0O0OOO0OOO0 ["适用范围"]in O0000OOOO00OOOO0O )or (OOO0OO0O0OOO0OOO0 ["适用范围"]=="通用"),axis =1 )#line:5266
			OOO0OOOO000O0OOOO =OOO0O0OO0O0000000 [(OOO0O0OO0O0000000 ["SELECT"]==True )].reset_index ()#line:5267
			if len (OOO0OOOO000O0OOOO )>0 :#line:5268
				for O0O0OO0O00OOOO00O ,OO00000OO0OOOO000 ,OOO0OOOOO0OO000OO in zip (OOO0OOOO000O0OOOO ["值"].values ,OOO0OOOO000O0OOOO ["查找位置"].values ,OOO0OOOO000O0OOOO ["排除值"].values ):#line:5270
					O00000O00OOO0OO0O =O000000O00000O0OO .copy ()#line:5271
					O0OOOO0000OO0O0O0 =TOOLS_get_list (O0O0OO0O00OOOO00O )[0 ]#line:5272
					O00000O00OOO0OO0O ["关键字查找列"]=""#line:5274
					for OOO00O0O0OOOOO0OO in TOOLS_get_list (OO00000OO0OOOO000 ):#line:5275
						O00000O00OOO0OO0O ["关键字查找列"]=O00000O00OOO0OO0O ["关键字查找列"]+O00000O00OOO0OO0O [OOO00O0O0OOOOO0OO ].astype ("str")#line:5276
					O00000O00OOO0OO0O .loc [O00000O00OOO0OO0O ["关键字查找列"].str .contains (O0O0OO0O00OOOO00O ,na =False ),"关键字"]=O0OOOO0000OO0O0O0 #line:5278
					if str (OOO0OOOOO0OO000OO )!="nan":#line:5281
						O00000O00OOO0OO0O =O00000O00OOO0OO0O .loc [~O00000O00OOO0OO0O ["关键字查找列"].str .contains (OOO0OOOOO0OO000OO ,na =False )].copy ()#line:5282
					if (len (O00000O00OOO0OO0O ))<1 :#line:5284
						continue #line:5285
					O0O0O0O0O0OOOO0OO =STAT_find_keyword_risk (O00000O00OOO0OO0O ,["上市许可持有人名称","产品类别","产品名称","注册证编号/曾用注册证编号","关键字"],"关键字",OO000OO0O0O0OOOOO ,int (OOO000000O0O000OO ))#line:5287
					if len (O0O0O0O0O0OOOO0OO )>0 :#line:5288
						O0O0O0O0O0OOOO0OO ["关键字组合"]=O0O0OO0O00OOOO00O #line:5289
						O0O0O0O0O0OOOO0OO ["排除值"]=OOO0OOOOO0OO000OO #line:5290
						O0O0O0O0O0OOOO0OO ["关键字查找列"]=OO00000OO0OOOO000 #line:5291
						O00O000000000O00O .append (O0O0O0O0O0OOOO0OO )#line:5292
		O00OOO00O0O0O00O0 =pd .concat (O00O000000000O00O )#line:5296
		O00OOO00O0O0O00O0 =pd .merge (O00OOO00O0O0O00O0 ,OOO00OOO0O000OOOO ,on =OOO000OOOO0O0OOO0 ,how ="left")#line:5299
		O00OOO00O0O0O00O0 ["关键字数量比例"]=round (O00OOO00O0O0O00O0 ["计数"]/O00OOO00O0O0O00O0 ["该元素总数量"],2 )#line:5300
		O00OOO00O0O0O00O0 =O00OOO00O0O0O00O0 .reset_index (drop =True )#line:5302
		if len (O00OOO00O0O0O00O0 )>0 :#line:5303
			O00OOO00O0O0O00O0 ["风险评分"]=0 #line:5304
			O00OOO00O0O0O00O0 ["报表类型"]="keyword_findrisk"+OO000OO0O0O0OOOOO #line:5305
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["计数"]>=3 ),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+3 #line:5306
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["计数"]>=(O00OOO00O0O0O00O0 ["数量均值"]+O00OOO00O0O0O00O0 ["数量标准差"])),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+1 #line:5307
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["计数"]>=O00OOO00O0O0O00O0 ["数量CI"]),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+1 #line:5308
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["关键字数量比例"]>0.5 )&(O00OOO00O0O0O00O0 ["计数"]>=3 ),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+1 #line:5309
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["严重伤害数"]>=3 ),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+1 #line:5310
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["单位个数"]>=3 ),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+1 #line:5311
			O00OOO00O0O0O00O0 .loc [(O00OOO00O0O0O00O0 ["死亡数量"]>=1 ),"风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+10 #line:5312
			O00OOO00O0O0O00O0 ["风险评分"]=O00OOO00O0O0O00O0 ["风险评分"]+O00OOO00O0O0O00O0 ["单位个数"]/100 #line:5313
			O00OOO00O0O0O00O0 =O00OOO00O0O0O00O0 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5314
		print ("耗时：",(time .time ()-O00OOO0OO000O0000 ))#line:5320
		return O00OOO00O0O0O00O0 #line:5321
	def df_ror (O0OOOO0000O0O0O0O ,O0O0OOO00OOO000O0 ,*OO000O00OOO0O0OO0 ):#line:5324
		""#line:5325
		O0OOOO0O0OO000OO0 =O0OOOO0000O0O0O0O .df .copy ()#line:5327
		OO000OOOO0OO000O0 =time .time ()#line:5328
		OOOOOO000OO0O000O =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5329
		if "报告类型-新的"in O0OOOO0O0OO000OO0 .columns :#line:5330
			O000O0O0O000O00O0 ="药品"#line:5331
		else :#line:5333
			O000O0O0O000O00O0 ="器械"#line:5334
		OO00O00O0O0O0OOO0 =pd .read_excel (OOOOOO000OO0O000O ,header =0 ,sheet_name =O000O0O0O000O00O0 ).reset_index (drop =True )#line:5335
		if "css"in O0OOOO0O0OO000OO0 .columns :#line:5338
			O0OOOOO00O0O0000O =O0OOOO0O0OO000OO0 .copy ()#line:5339
			O0OOOOO00O0O0000O ["器械故障表现"]=O0OOOOO00O0O0000O ["器械故障表现"].fillna ("未填写")#line:5340
			O0OOOOO00O0O0000O ["器械故障表现"]=O0OOOOO00O0O0000O ["器械故障表现"].str .replace ("*","",regex =False )#line:5341
			OOOO000OOOO0O0000 ="use("+str ("器械故障表现")+").file"#line:5342
			OOOOOO0O0O0OOO00O =str (Counter (TOOLS_get_list0 (OOOO000OOOO0O0000 ,O0OOOOO00O0O0000O ,1000 ))).replace ("Counter({","{")#line:5343
			OOOOOO0O0O0OOO00O =OOOOOO0O0O0OOO00O .replace ("})","}")#line:5344
			OOOOOO0O0O0OOO00O =ast .literal_eval (OOOOOO0O0O0OOO00O )#line:5345
			OO00O00O0O0O0OOO0 =pd .DataFrame .from_dict (OOOOOO0O0O0OOO00O ,orient ="index",columns =["计数"]).reset_index ()#line:5346
			OO00O00O0O0O0OOO0 ["适用范围列"]="产品类别"#line:5347
			OO00O00O0O0O0OOO0 ["适用范围"]="无源"#line:5348
			OO00O00O0O0O0OOO0 ["查找位置"]="伤害表现"#line:5349
			OO00O00O0O0O0OOO0 ["值"]=OO00O00O0O0O0OOO0 ["index"]#line:5350
			OO00O00O0O0O0OOO0 ["排除值"]="-没有排除值-"#line:5351
			del OO00O00O0O0O0OOO0 ["index"]#line:5352
		OOO00OOOO00000OOO =O0O0OOO00OOO000O0 [-2 ]#line:5355
		OOOOOO0O000O000OO =O0O0OOO00OOO000O0 [-1 ]#line:5356
		O0O0O0O000O0O00OO =O0O0OOO00OOO000O0 [:-1 ]#line:5357
		try :#line:5360
			if len (OO000O00OOO0O0OO0 [0 ])>0 :#line:5361
				OOO00OOOO00000OOO =O0O0OOO00OOO000O0 [-3 ]#line:5362
				OO00O00O0O0O0OOO0 =OO00O00O0O0O0OOO0 .loc [OO00O00O0O0O0OOO0 ["适用范围"].str .contains (OO000O00OOO0O0OO0 [0 ],na =False )].copy ().reset_index (drop =True )#line:5363
				O000O00O0O0O0O0O0 =O0OOOO0O0OO000OO0 .groupby (["产品类别","规整后品类","产品名称","注册证编号/曾用注册证编号"]).agg (该元素总数量 =(OOOOOO0O000O000OO ,"count"),该元素严重伤害数 =("伤害",lambda O0OO00O00000OOOO0 :STAT_countpx (O0OO00O00000OOOO0 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O0O0O0OOO0O0O0OO0 :STAT_countpx (O0O0O0OOO0O0O0OO0 .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5370
				O0O0000O0OO0O000O =O0OOOO0O0OO000OO0 .groupby (["产品类别","规整后品类"]).agg (所有元素总数量 =(OOO00OOOO00000OOO ,"count"),所有元素严重伤害数 =("伤害",lambda OOOO0OOO0OOOOO00O :STAT_countpx (OOOO0OOO0OOOOO00O .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O0000000OO00OO00O :STAT_countpx (O0000000OO00OO00O .values ,"死亡")),)#line:5375
				if len (O0O0000O0OO0O000O )>1 :#line:5376
					text .insert (END ,"注意，产品类别有两种，产品名称规整疑似不正确！")#line:5377
				O000O00O0O0O0O0O0 =pd .merge (O000O00O0O0O0O0O0 ,O0O0000O0OO0O000O ,on =["产品类别","规整后品类"],how ="left").reset_index ()#line:5379
		except :#line:5381
			text .insert (END ,"\n目前结果为未进行名称规整的结果！\n")#line:5382
			O000O00O0O0O0O0O0 =O0OOOO0O0OO000OO0 .groupby (O0O0OOO00OOO000O0 ).agg (该元素总数量 =(OOOOOO0O000O000OO ,"count"),该元素严重伤害数 =("伤害",lambda O0O0O0O0O0O00O000 :STAT_countpx (O0O0O0O0O0O00O000 .values ,"严重伤害")),该元素死亡数量 =("伤害",lambda O00000OO000O00OO0 :STAT_countpx (O00000OO000O00OO0 .values ,"死亡")),该元素单位个数 =("单位名称","nunique"),该元素单位列表 =("单位名称",STAT_countx ),).reset_index ()#line:5389
			O0O0000O0OO0O000O =O0OOOO0O0OO000OO0 .groupby (O0O0O0O000O0O00OO ).agg (所有元素总数量 =(OOO00OOOO00000OOO ,"count"),所有元素严重伤害数 =("伤害",lambda OOO000000OO0000OO :STAT_countpx (OOO000000OO0000OO .values ,"严重伤害")),所有元素死亡数量 =("伤害",lambda O00OOOOOO00O00000 :STAT_countpx (O00OOOOOO00O00000 .values ,"死亡")),)#line:5395
			O000O00O0O0O0O0O0 =pd .merge (O000O00O0O0O0O0O0 ,O0O0000O0OO0O000O ,on =O0O0O0O000O0O00OO ,how ="left").reset_index ()#line:5399
		O0O0000O0OO0O000O =O0O0000O0OO0O000O [(O0O0000O0OO0O000O ["所有元素总数量"]>=3 )].reset_index ()#line:5401
		O0OO0OO0O0OO0O00O =[]#line:5402
		if ("产品名称"not in O0O0000O0OO0O000O .columns )and ("规整后品类"not in O0O0000O0OO0O000O .columns ):#line:5404
			O0O0000O0OO0O000O ["产品名称"]=O0O0000O0OO0O000O ["产品类别"]#line:5405
		if "规整后品类"not in O0O0000O0OO0O000O .columns :#line:5411
			O0O0000O0OO0O000O ["规整后品类"]="不适用"#line:5412
		O000O00OO00OO0O00 =0 #line:5415
		OOO0O00OOO0OOO0O0 =int (len (O0O0000O0OO0O000O ))#line:5416
		for OO0O000000OOOO000 ,OOO00O00000O0OO0O ,OOOO000O0OO0O0OOO ,O0OOOOOOOO00OO000 in zip (O0O0000O0OO0O000O ["规整后品类"],O0O0000O0OO0O000O ["产品类别"],O0O0000O0OO0O000O [OOO00OOOO00000OOO ],O0O0000O0OO0O000O ["所有元素总数量"]):#line:5417
			O000O00OO00OO0O00 +=1 #line:5418
			if (time .time ()-OO000OOOO0OO000O0 )>3 :#line:5419
				root .attributes ("-topmost",True )#line:5420
				PROGRAM_change_schedule (O000O00OO00OO0O00 ,OOO0O00OOO0OOO0O0 )#line:5421
				root .attributes ("-topmost",False )#line:5422
			OOO0000OOO0O00O0O =O0OOOO0O0OO000OO0 [(O0OOOO0O0OO000OO0 [OOO00OOOO00000OOO ]==OOOO000O0OO0O0OOO )].copy ()#line:5423
			OO00O00O0O0O0OOO0 ["SELECT"]=OO00O00O0O0O0OOO0 .apply (lambda O0O00O00OO0O000O0 :((OO0O000000OOOO000 in O0O00O00OO0O000O0 ["适用范围"])or (O0O00O00OO0O000O0 ["适用范围"]in OOO00O00000O0OO0O )),axis =1 )#line:5424
			O000O0000O00OOOO0 =OO00O00O0O0O0OOO0 [(OO00O00O0O0O0OOO0 ["SELECT"]==True )].reset_index ()#line:5425
			if len (O000O0000O00OOOO0 )>0 :#line:5426
				for OOO00O000OO0O0000 ,OOO0O0O000O0O0OOO ,OOO00O000OO0O00OO in zip (O000O0000O00OOOO0 ["值"].values ,O000O0000O00OOOO0 ["查找位置"].values ,O000O0000O00OOOO0 ["排除值"].values ):#line:5428
					O00O00OO000OOOO0O =OOO0000OOO0O00O0O .copy ()#line:5429
					OO00O0O00O000000O =TOOLS_get_list (OOO00O000OO0O0000 )[0 ]#line:5430
					OOOO0OOOOO0O0OO0O ="关键字查找列"#line:5431
					O00O00OO000OOOO0O [OOOO0OOOOO0O0OO0O ]=""#line:5432
					for O00000OO0O00OO00O in TOOLS_get_list (OOO0O0O000O0O0OOO ):#line:5433
						O00O00OO000OOOO0O [OOOO0OOOOO0O0OO0O ]=O00O00OO000OOOO0O [OOOO0OOOOO0O0OO0O ]+O00O00OO000OOOO0O [O00000OO0O00OO00O ].astype ("str")#line:5434
					O00O00OO000OOOO0O .loc [O00O00OO000OOOO0O [OOOO0OOOOO0O0OO0O ].str .contains (OOO00O000OO0O0000 ,na =False ),"关键字"]=OO00O0O00O000000O #line:5436
					if str (OOO00O000OO0O00OO )!="nan":#line:5439
						O00O00OO000OOOO0O =O00O00OO000OOOO0O .loc [~O00O00OO000OOOO0O ["关键字查找列"].str .contains (OOO00O000OO0O00OO ,na =False )].copy ()#line:5440
					if (len (O00O00OO000OOOO0O ))<1 :#line:5443
						continue #line:5444
					for O00O0O0O000OO000O in zip (O00O00OO000OOOO0O [OOOOOO0O000O000OO ].drop_duplicates ()):#line:5446
						try :#line:5449
							if O00O0O0O000OO000O [0 ]!=OO000O00OOO0O0OO0 [1 ]:#line:5450
								continue #line:5451
						except :#line:5452
							pass #line:5453
						OOOO0O0OOO0OO0000 ={"合并列":{OOOO0OOOOO0O0OO0O :OOO0O0O000O0O0OOO },"等于":{OOO00OOOO00000OOO :OOOO000O0OO0O0OOO ,OOOOOO0O000O000OO :O00O0O0O000OO000O [0 ]},"不等于":{},"包含":{OOOO0OOOOO0O0OO0O :OOO00O000OO0O0000 },"不包含":{OOOO0OOOOO0O0OO0O :OOO00O000OO0O00OO }}#line:5461
						O0O000O0OO000O0OO =STAT_PPR_ROR_1 (OOOOOO0O000O000OO ,str (O00O0O0O000OO000O [0 ]),"关键字查找列",OOO00O000OO0O0000 ,O00O00OO000OOOO0O )+(OOO00O000OO0O0000 ,OOO00O000OO0O00OO ,OOO0O0O000O0O0OOO ,OOOO000O0OO0O0OOO ,O00O0O0O000OO000O [0 ],str (OOOO0O0OOO0OO0000 ))#line:5463
						if O0O000O0OO000O0OO [1 ]>0 :#line:5465
							OOO0O00000O000000 =pd .DataFrame (columns =["特定关键字","出现频次","占比","ROR值","ROR值的95%CI下限","PRR值","PRR值的95%CI下限","卡方值","四分表","关键字组合","排除值","关键字查找列",OOO00OOOO00000OOO ,OOOOOO0O000O000OO ,"报表定位"])#line:5467
							OOO0O00000O000000 .loc [0 ]=O0O000O0OO000O0OO #line:5468
							O0OO0OO0O0OO0O00O .append (OOO0O00000O000000 )#line:5469
		OOOOOOO0OOO0O0O00 =pd .concat (O0OO0OO0O0OO0O00O )#line:5473
		OOOOOOO0OOO0O0O00 =pd .merge (O000O00O0O0O0O0O0 ,OOOOOOO0OOO0O0O00 ,on =[OOO00OOOO00000OOO ,OOOOOO0O000O000OO ],how ="right")#line:5477
		OOOOOOO0OOO0O0O00 =OOOOOOO0OOO0O0O00 .reset_index (drop =True )#line:5478
		del OOOOOOO0OOO0O0O00 ["index"]#line:5479
		if len (OOOOOOO0OOO0O0O00 )>0 :#line:5480
			OOOOOOO0OOO0O0O00 ["风险评分"]=0 #line:5481
			OOOOOOO0OOO0O0O00 ["报表类型"]="ROR"#line:5482
			OOOOOOO0OOO0O0O00 .loc [(OOOOOOO0OOO0O0O00 ["出现频次"]>=3 ),"风险评分"]=OOOOOOO0OOO0O0O00 ["风险评分"]+3 #line:5483
			OOOOOOO0OOO0O0O00 .loc [(OOOOOOO0OOO0O0O00 ["ROR值的95%CI下限"]>1 ),"风险评分"]=OOOOOOO0OOO0O0O00 ["风险评分"]+1 #line:5484
			OOOOOOO0OOO0O0O00 .loc [(OOOOOOO0OOO0O0O00 ["PRR值的95%CI下限"]>1 ),"风险评分"]=OOOOOOO0OOO0O0O00 ["风险评分"]+1 #line:5485
			OOOOOOO0OOO0O0O00 ["风险评分"]=OOOOOOO0OOO0O0O00 ["风险评分"]+OOOOOOO0OOO0O0O00 ["该元素单位个数"]/100 #line:5486
			OOOOOOO0OOO0O0O00 =OOOOOOO0OOO0O0O00 .sort_values (by ="风险评分",ascending =[False ],na_position ="last").reset_index (drop =True )#line:5487
		print ("耗时：",(time .time ()-OO000OOOO0OO000O0 ))#line:5493
		return OOOOOOO0OOO0O0O00 #line:5494
	def df_chiyouren (O00O00O0000O0O000 ):#line:5500
		""#line:5501
		O0OOO0OO0OOO0O0OO =O00O00O0000O0O000 .df .copy ().reset_index (drop =True )#line:5502
		O0OOO0OO0OOO0O0OO ["总报告数"]=data ["报告编码"].copy ()#line:5503
		O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"总待评价数量"]=data ["报告编码"]#line:5504
		O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害"),"严重伤害报告数"]=data ["报告编码"]#line:5505
		O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价")&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害"),"严重伤害待评价数量"]=data ["报告编码"]#line:5506
		O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价")&(O0OOO0OO0OOO0O0OO ["伤害"]=="其他"),"其他待评价数量"]=data ["报告编码"]#line:5507
		O0O0OO0000OOO0O00 =O0OOO0OO0OOO0O0OO .groupby (["上市许可持有人名称"]).aggregate ({"总报告数":"nunique","总待评价数量":"nunique","严重伤害报告数":"nunique","严重伤害待评价数量":"nunique","其他待评价数量":"nunique"})#line:5510
		O0O0OO0000OOO0O00 ["严重伤害待评价比例"]=round (O0O0OO0000OOO0O00 ["严重伤害待评价数量"]/O0O0OO0000OOO0O00 ["严重伤害报告数"]*100 ,2 )#line:5515
		O0O0OO0000OOO0O00 ["总待评价比例"]=round (O0O0OO0000OOO0O00 ["总待评价数量"]/O0O0OO0000OOO0O00 ["总报告数"]*100 ,2 )#line:5518
		O0O0OO0000OOO0O00 ["总报告数"]=O0O0OO0000OOO0O00 ["总报告数"].fillna (0 )#line:5519
		O0O0OO0000OOO0O00 ["总待评价比例"]=O0O0OO0000OOO0O00 ["总待评价比例"].fillna (0 )#line:5520
		O0O0OO0000OOO0O00 ["严重伤害报告数"]=O0O0OO0000OOO0O00 ["严重伤害报告数"].fillna (0 )#line:5521
		O0O0OO0000OOO0O00 ["严重伤害待评价比例"]=O0O0OO0000OOO0O00 ["严重伤害待评价比例"].fillna (0 )#line:5522
		O0O0OO0000OOO0O00 ["总报告数"]=O0O0OO0000OOO0O00 ["总报告数"].astype (int )#line:5523
		O0O0OO0000OOO0O00 ["总待评价比例"]=O0O0OO0000OOO0O00 ["总待评价比例"].astype (int )#line:5524
		O0O0OO0000OOO0O00 ["严重伤害报告数"]=O0O0OO0000OOO0O00 ["严重伤害报告数"].astype (int )#line:5525
		O0O0OO0000OOO0O00 ["严重伤害待评价比例"]=O0O0OO0000OOO0O00 ["严重伤害待评价比例"].astype (int )#line:5526
		O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .sort_values (by =["总报告数","总待评价比例"],ascending =[False ,False ],na_position ="last")#line:5529
		if "场所名称"in O0OOO0OO0OOO0O0OO .columns :#line:5531
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["审核日期"]=="未填写"),"审核日期"]=3000 -12 -12 #line:5532
			O0OOO0OO0OOO0O0OO ["报告时限"]=pd .Timestamp .today ()-pd .to_datetime (O0OOO0OO0OOO0O0OO ["审核日期"])#line:5533
			O0OOO0OO0OOO0O0OO ["报告时限2"]=45 -(pd .Timestamp .today ()-pd .to_datetime (O0OOO0OO0OOO0O0OO ["审核日期"])).dt .days #line:5534
			O0OOO0OO0OOO0O0OO ["报告时限"]=O0OOO0OO0OOO0O0OO ["报告时限"].dt .days #line:5535
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限"]>45 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（严重）"]=1 #line:5536
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限"]>45 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="其他")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"待评价且超出当前日期45天（其他）"]=1 #line:5537
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限"]>30 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="死亡")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"待评价且超出当前日期30天（死亡）"]=1 #line:5538
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]<=1 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["报告时限2"]>0 )&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩1天"]=1 #line:5540
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]>1 )&(O0OOO0OO0OOO0O0OO ["报告时限2"]<=3 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩1-3天"]=1 #line:5541
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]>3 )&(O0OOO0OO0OOO0O0OO ["报告时限2"]<=5 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩3-5天"]=1 #line:5542
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]>5 )&(O0OOO0OO0OOO0O0OO ["报告时限2"]<=10 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩5-10天"]=1 #line:5543
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]>10 )&(O0OOO0OO0OOO0O0OO ["报告时限2"]<=20 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩10-20天"]=1 #line:5544
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]>20 )&(O0OOO0OO0OOO0O0OO ["报告时限2"]<=30 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩20-30天"]=1 #line:5545
			O0OOO0OO0OOO0O0OO .loc [(O0OOO0OO0OOO0O0OO ["报告时限2"]>30 )&(O0OOO0OO0OOO0O0OO ["报告时限2"]<=45 )&(O0OOO0OO0OOO0O0OO ["伤害"]=="严重伤害")&(O0OOO0OO0OOO0O0OO ["持有人报告状态"]=="待评价"),"严重待评价且只剩30-45天"]=1 #line:5546
			del O0OOO0OO0OOO0O0OO ["报告时限2"]#line:5547
			OOO0OO0O00OOOOOOO =(O0OOO0OO0OOO0O0OO .groupby (["上市许可持有人名称"]).aggregate ({"待评价且超出当前日期45天（严重）":"sum","待评价且超出当前日期45天（其他）":"sum","待评价且超出当前日期30天（死亡）":"sum","严重待评价且只剩1天":"sum","严重待评价且只剩1-3天":"sum","严重待评价且只剩3-5天":"sum","严重待评价且只剩5-10天":"sum","严重待评价且只剩10-20天":"sum","严重待评价且只剩20-30天":"sum","严重待评价且只剩30-45天":"sum"}).reset_index ())#line:5549
			O0O0OO0000OOO0O00 =pd .merge (O0O0OO0000OOO0O00 ,OOO0OO0O00OOOOOOO ,on =["上市许可持有人名称"],how ="outer",)#line:5550
			O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（严重）"]=O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（严重）"].fillna (0 )#line:5551
			O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（严重）"]=O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（严重）"].astype (int )#line:5552
			O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（其他）"]=O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（其他）"].fillna (0 )#line:5553
			O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（其他）"]=O0O0OO0000OOO0O00 ["待评价且超出当前日期45天（其他）"].astype (int )#line:5554
			O0O0OO0000OOO0O00 ["待评价且超出当前日期30天（死亡）"]=O0O0OO0000OOO0O00 ["待评价且超出当前日期30天（死亡）"].fillna (0 )#line:5555
			O0O0OO0000OOO0O00 ["待评价且超出当前日期30天（死亡）"]=O0O0OO0000OOO0O00 ["待评价且超出当前日期30天（死亡）"].astype (int )#line:5556
			O0O0OO0000OOO0O00 ["严重待评价且只剩1天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩1天"].fillna (0 )#line:5558
			O0O0OO0000OOO0O00 ["严重待评价且只剩1天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩1天"].astype (int )#line:5559
			O0O0OO0000OOO0O00 ["严重待评价且只剩1-3天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩1-3天"].fillna (0 )#line:5560
			O0O0OO0000OOO0O00 ["严重待评价且只剩1-3天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩1-3天"].astype (int )#line:5561
			O0O0OO0000OOO0O00 ["严重待评价且只剩3-5天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩3-5天"].fillna (0 )#line:5562
			O0O0OO0000OOO0O00 ["严重待评价且只剩3-5天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩3-5天"].astype (int )#line:5563
			O0O0OO0000OOO0O00 ["严重待评价且只剩5-10天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩5-10天"].fillna (0 )#line:5564
			O0O0OO0000OOO0O00 ["严重待评价且只剩5-10天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩5-10天"].astype (int )#line:5565
			O0O0OO0000OOO0O00 ["严重待评价且只剩10-20天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩10-20天"].fillna (0 )#line:5566
			O0O0OO0000OOO0O00 ["严重待评价且只剩10-20天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩10-20天"].astype (int )#line:5567
			O0O0OO0000OOO0O00 ["严重待评价且只剩20-30天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩20-30天"].fillna (0 )#line:5568
			O0O0OO0000OOO0O00 ["严重待评价且只剩20-30天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩20-30天"].astype (int )#line:5569
			O0O0OO0000OOO0O00 ["严重待评价且只剩30-45天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩30-45天"].fillna (0 )#line:5570
			O0O0OO0000OOO0O00 ["严重待评价且只剩30-45天"]=O0O0OO0000OOO0O00 ["严重待评价且只剩30-45天"].astype (int )#line:5571
		O0O0OO0000OOO0O00 ["总待评价数量"]=O0O0OO0000OOO0O00 ["总待评价数量"].fillna (0 )#line:5573
		O0O0OO0000OOO0O00 ["总待评价数量"]=O0O0OO0000OOO0O00 ["总待评价数量"].astype (int )#line:5574
		O0O0OO0000OOO0O00 ["严重伤害待评价数量"]=O0O0OO0000OOO0O00 ["严重伤害待评价数量"].fillna (0 )#line:5575
		O0O0OO0000OOO0O00 ["严重伤害待评价数量"]=O0O0OO0000OOO0O00 ["严重伤害待评价数量"].astype (int )#line:5576
		O0O0OO0000OOO0O00 ["其他待评价数量"]=O0O0OO0000OOO0O00 ["其他待评价数量"].fillna (0 )#line:5577
		O0O0OO0000OOO0O00 ["其他待评价数量"]=O0O0OO0000OOO0O00 ["其他待评价数量"].astype (int )#line:5578
		O0O0O0O0O0O0000O0 =["总报告数","总待评价数量","严重伤害报告数","严重伤害待评价数量","其他待评价数量"]#line:5581
		O0O0OO0000OOO0O00 .loc ["合计"]=O0O0OO0000OOO0O00 [O0O0O0O0O0O0000O0 ].apply (lambda O0OOOOO00OOOO0O0O :O0OOOOO00OOOO0O0O .sum ())#line:5582
		O0O0OO0000OOO0O00 [O0O0O0O0O0O0000O0 ]=O0O0OO0000OOO0O00 [O0O0O0O0O0O0000O0 ].apply (lambda OO0OOOOOO0000OO00 :OO0OOOOOO0000OO00 .astype (int ))#line:5583
		O0O0OO0000OOO0O00 .iloc [-1 ,0 ]="合计"#line:5584
		if "场所名称"in O0OOO0OO0OOO0O0OO .columns :#line:5586
			O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .reset_index (drop =True )#line:5587
		else :#line:5588
			O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .reset_index ()#line:5589
		if ini ["模式"]=="药品":#line:5591
			O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .rename (columns ={"总待评价数量":"新的数量"})#line:5592
			O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .rename (columns ={"严重伤害待评价数量":"新的严重的数量"})#line:5593
			O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .rename (columns ={"严重伤害待评价比例":"新的严重的比例"})#line:5594
			O0O0OO0000OOO0O00 =O0O0OO0000OOO0O00 .rename (columns ={"总待评价比例":"新的比例"})#line:5595
			del O0O0OO0000OOO0O00 ["其他待评价数量"]#line:5597
		O0O0OO0000OOO0O00 ["报表类型"]="dfx_chiyouren"#line:5598
		return O0O0OO0000OOO0O00 #line:5599
	def df_age (OO0O0OOOO0O0OOO00 ):#line:5601
		""#line:5602
		OOO0OO0OO00000O00 =OO0O0OOOO0O0OOO00 .df .copy ()#line:5603
		OOO0OO0OO00000O00 =OOO0OO0OO00000O00 .drop_duplicates ("报告编码").copy ()#line:5604
		O00O0O000O0OOOOOO =pd .pivot_table (OOO0OO0OO00000O00 .drop_duplicates ("报告编码"),values =["报告编码"],index ="年龄段",columns ="性别",aggfunc ={"报告编码":"nunique"},fill_value ="0",margins =True ,dropna =False ,).rename (columns ={"报告编码":"数量"}).reset_index ()#line:5605
		O00O0O000O0OOOOOO .columns =O00O0O000O0OOOOOO .columns .droplevel (0 )#line:5606
		O00O0O000O0OOOOOO ["构成比(%)"]=round (100 *O00O0O000O0OOOOOO ["All"]/len (OOO0OO0OO00000O00 ),2 )#line:5607
		O00O0O000O0OOOOOO ["累计构成比(%)"]=O00O0O000O0OOOOOO ["构成比(%)"].cumsum ()#line:5608
		O00O0O000O0OOOOOO ["报表类型"]="年龄性别表"#line:5609
		return O00O0O000O0OOOOOO #line:5610
	def df_psur (O0OOOOO00000O0O0O ,*OO0O00O0000000O00 ):#line:5612
		""#line:5613
		OO0OOOO00OO0O0OOO =O0OOOOO00000O0O0O .df .copy ()#line:5614
		O0000O00O0O000OOO =peizhidir +"0（范例）比例失衡关键字库.xls"#line:5615
		OOOO0O0O0OO00O0O0 =len (OO0OOOO00OO0O0OOO .drop_duplicates ("报告编码"))#line:5616
		if "报告类型-新的"in OO0OOOO00OO0O0OOO .columns :#line:5620
			OOOO0OOO000O0OOO0 ="药品"#line:5621
		elif "皮损形态"in OO0OOOO00OO0O0OOO .columns :#line:5622
			OOOO0OOO000O0OOO0 ="化妆品"#line:5623
		else :#line:5624
			OOOO0OOO000O0OOO0 ="器械"#line:5625
		OO0OOOOO0O00O000O =pd .read_excel (O0000O00O0O000OOO ,header =0 ,sheet_name =OOOO0OOO000O0OOO0 )#line:5628
		O0O0O0OOO000OO0OO =(OO0OOOOO0O00O000O .loc [OO0OOOOO0O00O000O ["适用范围"].str .contains ("通用监测关键字|无源|有源",na =False )].copy ().reset_index (drop =True ))#line:5631
		try :#line:5634
			if OO0O00O0000000O00 [0 ]in ["特定品种","通用无源","通用有源"]:#line:5635
				O0OO00O0O00OOOO00 =""#line:5636
				if OO0O00O0000000O00 [0 ]=="特定品种":#line:5637
					O0OO00O0O00OOOO00 =OO0OOOOO0O00O000O .loc [OO0OOOOO0O00O000O ["适用范围"].str .contains (OO0O00O0000000O00 [1 ],na =False )].copy ().reset_index (drop =True )#line:5638
				if OO0O00O0000000O00 [0 ]=="通用无源":#line:5640
					O0OO00O0O00OOOO00 =OO0OOOOO0O00O000O .loc [OO0OOOOO0O00O000O ["适用范围"].str .contains ("通用监测关键字|无源",na =False )].copy ().reset_index (drop =True )#line:5641
				if OO0O00O0000000O00 [0 ]=="通用有源":#line:5642
					O0OO00O0O00OOOO00 =OO0OOOOO0O00O000O .loc [OO0OOOOO0O00O000O ["适用范围"].str .contains ("通用监测关键字|有源",na =False )].copy ().reset_index (drop =True )#line:5643
				if OO0O00O0000000O00 [0 ]=="体外诊断试剂":#line:5644
					O0OO00O0O00OOOO00 =OO0OOOOO0O00O000O .loc [OO0OOOOO0O00O000O ["适用范围"].str .contains ("体外诊断试剂",na =False )].copy ().reset_index (drop =True )#line:5645
				if len (O0OO00O0O00OOOO00 )<1 :#line:5646
					showinfo (title ="提示",message ="未找到相应的自定义规则，任务结束。")#line:5647
					return 0 #line:5648
				else :#line:5649
					O0O0O0OOO000OO0OO =O0OO00O0O00OOOO00 #line:5650
		except :#line:5652
			pass #line:5653
		try :#line:5657
			if OOOO0OOO000O0OOO0 =="器械"and OO0O00O0000000O00 [0 ]=="特定品种作为通用关键字":#line:5658
				O0O0O0OOO000OO0OO =OO0O00O0000000O00 [1 ]#line:5659
		except dddd :#line:5661
			pass #line:5662
		OOOOO0OO0OO0O00O0 =""#line:5665
		OOO0OO00O00O0OOO0 ="-其他关键字-不含："#line:5666
		for OOOO00O0O0OOOO00O ,OOO00O00O0O000O0O in O0O0O0OOO000OO0OO .iterrows ():#line:5667
			OOO0OO00O00O0OOO0 =OOO0OO00O00O0OOO0 +"|"+str (OOO00O00O0O000O0O ["值"])#line:5668
			O0O0000000OOOOO00 =OOO00O00O0O000O0O #line:5669
		O0O0000000OOOOO00 [2 ]="通用监测关键字"#line:5670
		O0O0000000OOOOO00 [4 ]=OOO0OO00O00O0OOO0 #line:5671
		O0O0O0OOO000OO0OO .loc [len (O0O0O0OOO000OO0OO )]=O0O0000000OOOOO00 #line:5672
		O0O0O0OOO000OO0OO =O0O0O0OOO000OO0OO .reset_index (drop =True )#line:5673
		if ini ["模式"]=="器械":#line:5677
			OO0OOOO00OO0O0OOO ["关键字查找列"]=OO0OOOO00OO0O0OOO ["器械故障表现"].astype (str )+OO0OOOO00OO0O0OOO ["伤害表现"].astype (str )+OO0OOOO00OO0O0OOO ["使用过程"].astype (str )+OO0OOOO00OO0O0OOO ["事件原因分析描述"].astype (str )+OO0OOOO00OO0O0OOO ["初步处置情况"].astype (str )#line:5678
		else :#line:5679
			OO0OOOO00OO0O0OOO ["关键字查找列"]=OO0OOOO00OO0O0OOO ["器械故障表现"]#line:5680
		text .insert (END ,"\n药品查找列默认为不良反应表现,药品规则默认为通用规则。\n器械默认查找列为器械故障表现+伤害表现+使用过程+事件原因分析描述+初步处置情况，器械默认规则为无源通用规则+有源通用规则。\n")#line:5681
		O0O0OOO00O0O0O0OO =[]#line:5683
		for OOOO00O0O0OOOO00O ,OOO00O00O0O000O0O in O0O0O0OOO000OO0OO .iterrows ():#line:5685
			OO000000OOOOOO0OO =OOO00O00O0O000O0O ["值"]#line:5686
			if "-其他关键字-"not in OO000000OOOOOO0OO :#line:5688
				OO0OO0O000OO000O0 =OO0OOOO00OO0O0OOO .loc [OO0OOOO00OO0O0OOO ["关键字查找列"].str .contains (OO000000OOOOOO0OO ,na =False )].copy ()#line:5691
				if str (OOO00O00O0O000O0O ["排除值"])!="nan":#line:5692
					OO0OO0O000OO000O0 =OO0OO0O000OO000O0 .loc [~OO0OO0O000OO000O0 ["关键字查找列"].str .contains (str (OOO00O00O0O000O0O ["排除值"]),na =False )].copy ()#line:5694
			else :#line:5696
				OO0OO0O000OO000O0 =OO0OOOO00OO0O0OOO .loc [~OO0OOOO00OO0O0OOO ["关键字查找列"].str .contains (OO000000OOOOOO0OO ,na =False )].copy ()#line:5699
			OO0OO0O000OO000O0 ["关键字标记"]=str (OO000000OOOOOO0OO )#line:5700
			OO0OO0O000OO000O0 ["关键字计数"]=1 #line:5701
			if len (OO0OO0O000OO000O0 )>0 :#line:5707
				try :#line:5708
					OOOO0O0OO00000OO0 =pd .pivot_table (OO0OO0O000OO000O0 .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害PSUR",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5718
				except :#line:5720
					OOOO0O0OO00000OO0 =pd .pivot_table (OO0OO0O000OO000O0 .drop_duplicates ("报告编码"),values =["关键字计数"],index ="关键字标记",columns ="伤害",aggfunc ={"关键字计数":"count"},fill_value ="0",margins =True ,dropna =False ,)#line:5730
				OOOO0O0OO00000OO0 =OOOO0O0OO00000OO0 [:-1 ]#line:5731
				OOOO0O0OO00000OO0 .columns =OOOO0O0OO00000OO0 .columns .droplevel (0 )#line:5732
				OOOO0O0OO00000OO0 =OOOO0O0OO00000OO0 .reset_index ()#line:5733
				if len (OOOO0O0OO00000OO0 )>0 :#line:5736
					OOOO0O00O00O0000O =str (Counter (TOOLS_get_list0 ("use(器械故障表现).file",OO0OO0O000OO000O0 ,1000 ))).replace ("Counter({","{")#line:5737
					OOOO0O00O00O0000O =OOOO0O00O00O0000O .replace ("})","}")#line:5738
					OOOO0O00O00O0000O =ast .literal_eval (OOOO0O00O00O0000O )#line:5739
					OOOO0O0OO00000OO0 .loc [0 ,"事件分类"]=str (TOOLS_get_list (OOOO0O0OO00000OO0 .loc [0 ,"关键字标记"])[0 ])#line:5741
					O000OO00OO00000O0 ={O0OOOOOO0000OOOOO :OOO0O0O0OO000OOO0 for O0OOOOOO0000OOOOO ,OOO0O0O0OO000OOO0 in OOOO0O00O00O0000O .items ()if STAT_judge_x (str (O0OOOOOO0000OOOOO ),TOOLS_get_list (OO000000OOOOOO0OO ))==1 }#line:5742
					OOOO0O0OO00000OO0 .loc [0 ,"该类别不良事件计数"]=str (O000OO00OO00000O0 )#line:5744
					O0O0O0O0O00OOOO00 ={OOO0OO000OOO0OOO0 :OOO000OOO0OO0O000 for OOO0OO000OOO0OOO0 ,OOO000OOO0OO0O000 in OOOO0O00O00O0000O .items ()if STAT_judge_x (str (OOO0OO000OOO0OOO0 ),TOOLS_get_list (OO000000OOOOOO0OO ))!=1 }#line:5745
					OOOO0O0OO00000OO0 .loc [0 ,"同时存在的其他类别不良事件计数"]=str (O0O0O0O0O00OOOO00 )#line:5746
					if "-其他关键字-"in str (OO000000OOOOOO0OO ):#line:5748
						O000OO00OO00000O0 =O0O0O0O0O00OOOO00 #line:5749
						OOOO0O0OO00000OO0 .loc [0 ,"该类别不良事件计数"]=OOOO0O0OO00000OO0 .loc [0 ,"同时存在的其他类别不良事件计数"]#line:5750
					OOOO0O0OO00000OO0 .loc [0 ,"不良事件总例次"]=str (sum (O000OO00OO00000O0 .values ()))#line:5752
					if ini ["模式"]=="药品":#line:5762
						for O0O00000O0OO0O00O in ["SOC","HLGT","HLT","PT"]:#line:5763
							OOOO0O0OO00000OO0 [O0O00000O0OO0O00O ]=OOO00O00O0O000O0O [O0O00000O0OO0O00O ]#line:5764
					if ini ["模式"]=="器械":#line:5765
						for O0O00000O0OO0O00O in ["国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]:#line:5766
							OOOO0O0OO00000OO0 [O0O00000O0OO0O00O ]=OOO00O00O0O000O0O [O0O00000O0OO0O00O ]#line:5767
					O0O0OOO00O0O0O0OO .append (OOOO0O0OO00000OO0 )#line:5770
		OOOOO0OO0OO0O00O0 =pd .concat (O0O0OOO00O0O0O0OO )#line:5771
		OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .sort_values (by =["All"],ascending =[False ],na_position ="last")#line:5776
		OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .reset_index ()#line:5777
		OOOOO0OO0OO0O00O0 ["All占比"]=round (OOOOO0OO0OO0O00O0 ["All"]/OOOO0O0O0OO00O0O0 *100 ,2 )#line:5779
		OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .rename (columns ={"All":"总数量","All占比":"总数量占比"})#line:5780
		try :#line:5781
			OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .rename (columns ={"其他":"一般"})#line:5782
		except :#line:5783
			pass #line:5784
		try :#line:5786
			OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .rename (columns ={" 一般":"一般"})#line:5787
		except :#line:5788
			pass #line:5789
		try :#line:5790
			OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .rename (columns ={" 严重":"严重"})#line:5791
		except :#line:5792
			pass #line:5793
		try :#line:5794
			OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .rename (columns ={"严重伤害":"严重"})#line:5795
		except :#line:5796
			pass #line:5797
		try :#line:5798
			OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 .rename (columns ={"死亡":"死亡(仅支持器械)"})#line:5799
		except :#line:5800
			pass #line:5801
		for OO0O000O0O00OOO0O in ["一般","新的一般","严重","新的严重"]:#line:5804
			if OO0O000O0O00OOO0O not in OOOOO0OO0OO0O00O0 .columns :#line:5805
				OOOOO0OO0OO0O00O0 [OO0O000O0O00OOO0O ]=0 #line:5806
		try :#line:5808
			OOOOO0OO0OO0O00O0 ["严重比"]=round ((OOOOO0OO0OO0O00O0 ["严重"].fillna (0 )+OOOOO0OO0OO0O00O0 ["死亡(仅支持器械)"].fillna (0 ))/OOOOO0OO0OO0O00O0 ["总数量"]*100 ,2 )#line:5809
		except :#line:5810
			OOOOO0OO0OO0O00O0 ["严重比"]=round ((OOOOO0OO0OO0O00O0 ["严重"].fillna (0 )+OOOOO0OO0OO0O00O0 ["新的严重"].fillna (0 ))/OOOOO0OO0OO0O00O0 ["总数量"]*100 ,2 )#line:5811
		OOOOO0OO0OO0O00O0 ["构成比"]=round ((OOOOO0OO0OO0O00O0 ["不良事件总例次"].astype (float ).fillna (0 ))/OOOOO0OO0OO0O00O0 ["不良事件总例次"].astype (float ).sum ()*100 ,2 )#line:5813
		if ini ["模式"]=="药品":#line:5815
			try :#line:5816
				OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)","SOC","HLGT","HLT","PT"]]#line:5817
			except :#line:5818
				OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","SOC","HLGT","HLT","PT"]]#line:5819
		elif ini ["模式"]=="器械":#line:5820
			try :#line:5821
				OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5822
			except :#line:5823
				OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","国家故障术语集（大类）","国家故障术语集（小类）","IMDRF有关术语（故障）","国家伤害术语集（大类）","国家伤害术语集（小类）","IMDRF有关术语（伤害）"]]#line:5824
		else :#line:5826
			try :#line:5827
				OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数","死亡(仅支持器械)"]]#line:5828
			except :#line:5829
				OOOOO0OO0OO0O00O0 =OOOOO0OO0OO0O00O0 [["关键字标记","一般","新的一般","严重","新的严重","总数量","总数量占比","严重比","事件分类","不良事件总例次","构成比","该类别不良事件计数","同时存在的其他类别不良事件计数"]]#line:5830
		for O0000O0OO0O0O000O ,O0OOOOO000O0OOO00 in O0O0O0OOO000OO0OO .iterrows ():#line:5832
			OOOOO0OO0OO0O00O0 .loc [(OOOOO0OO0OO0O00O0 ["关键字标记"].astype (str )==str (O0OOOOO000O0OOO00 ["值"])),"排除值"]=O0OOOOO000O0OOO00 ["排除值"]#line:5833
		OOOOO0OO0OO0O00O0 ["排除值"]=OOOOO0OO0OO0O00O0 ["排除值"].fillna ("没有排除值")#line:5835
		for OO00OOOO0O0O0OO0O in ["一般","新的一般","严重","新的严重","总数量","总数量占比","严重比"]:#line:5839
			OOOOO0OO0OO0O00O0 [OO00OOOO0O0O0OO0O ]=OOOOO0OO0OO0O00O0 [OO00OOOO0O0O0OO0O ].fillna (0 )#line:5840
		for OO00OOOO0O0O0OO0O in ["一般","新的一般","严重","新的严重","总数量"]:#line:5842
			OOOOO0OO0OO0O00O0 [OO00OOOO0O0O0OO0O ]=OOOOO0OO0OO0O00O0 [OO00OOOO0O0O0OO0O ].astype (int )#line:5843
		OOOOO0OO0OO0O00O0 ["RPN"]="未定义"#line:5846
		OOOOO0OO0OO0O00O0 ["故障原因"]="未定义"#line:5847
		OOOOO0OO0OO0O00O0 ["可造成的伤害"]="未定义"#line:5848
		OOOOO0OO0OO0O00O0 ["应采取的措施"]="未定义"#line:5849
		OOOOO0OO0OO0O00O0 ["发生率"]="未定义"#line:5850
		OOOOO0OO0OO0O00O0 ["报表类型"]="PSUR"#line:5852
		return OOOOO0OO0OO0O00O0 #line:5853
def A0000_Main ():#line:5863
	print ("")#line:5864
if __name__ =='__main__':#line:5866
	root =Tk .Tk ()#line:5869
	root .title (title_all )#line:5870
	try :#line:5871
		root .iconphoto (True ,PhotoImage (file =peizhidir +"0（范例）ico.png"))#line:5872
	except :#line:5873
		pass #line:5874
	sw_root =root .winfo_screenwidth ()#line:5875
	sh_root =root .winfo_screenheight ()#line:5877
	ww_root =700 #line:5879
	wh_root =620 #line:5880
	x_root =(sw_root -ww_root )/2 #line:5882
	y_root =(sh_root -wh_root )/2 #line:5883
	root .geometry ("%dx%d+%d+%d"%(ww_root ,wh_root ,x_root ,y_root ))#line:5884
	framecanvas =Frame (root )#line:5889
	canvas =Canvas (framecanvas ,width =680 ,height =30 )#line:5890
	canvas .pack ()#line:5891
	x =StringVar ()#line:5892
	out_rec =canvas .create_rectangle (5 ,5 ,680 ,25 ,outline ="silver",width =1 )#line:5893
	fill_rec =canvas .create_rectangle (5 ,5 ,5 ,25 ,outline ="",width =0 ,fill ="silver")#line:5894
	canvas .create_text (350 ,15 ,text ="总执行进度")#line:5895
	framecanvas .pack ()#line:5896
	try :#line:5903
		frame0 =ttk .Frame (root ,width =90 ,height =20 )#line:5904
		frame0 .pack (side =LEFT )#line:5905
		B_open_files1 =Button (frame0 ,text ="导入数据",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =TOOLS_allfileopen ,)#line:5916
		B_open_files1 .pack ()#line:5917
		B_open_files3 =Button (frame0 ,text ="数据查看",bg ="white",height =2 ,width =12 ,font =("微软雅黑",10 ),relief =GROOVE ,activebackground ="green",command =lambda :TABLE_tree_Level_2 (ori ,0 ,ori ),)#line:5932
		B_open_files3 .pack ()#line:5933
	except KEY :#line:5936
		pass #line:5937
	text =ScrolledText (root ,height =400 ,width =400 ,bg ="#FFFFFF")#line:5941
	text .pack (padx =5 ,pady =5 )#line:5942
	text .insert (END ,"\n 本程序适用于整理和分析国家医疗器械不良事件信息系统、国家药品不良反应监测系统和国家化妆品不良反应监测系统中导出的监测数据。如您有改进建议，请点击其-意见反馈。\n")#line:5945
	text .insert (END ,"\n\n")#line:5946
	setting_cfg =read_setting_cfg ()#line:5949
	generate_random_file ()#line:5950
	setting_cfg =open_setting_cfg ()#line:5951
	if setting_cfg ["settingdir"]==0 :#line:5952
		showinfo (title ="提示",message ="未发现默认配置文件夹，请选择一个。如该配置文件夹中并无配置文件，将生成默认配置文件。")#line:5953
		filepathu =filedialog .askdirectory ()#line:5954
		path =get_directory_path (filepathu )#line:5955
		update_setting_cfg ("settingdir",path )#line:5956
	setting_cfg =open_setting_cfg ()#line:5957
	random_number =int (setting_cfg ["sidori"])#line:5958
	input_number =int (str (setting_cfg ["sidfinal"])[0 :6 ])#line:5959
	day_end =convert_and_compare_dates (str (setting_cfg ["sidfinal"])[6 :14 ])#line:5960
	sid =random_number *2 +183576 #line:5961
	if input_number ==sid and day_end =="未过期":#line:5962
		usergroup ="用户组=1"#line:5963
		text .insert (END ,usergroup +"   有效期至：")#line:5964
		text .insert (END ,datetime .strptime (str (int (int (str (setting_cfg ["sidfinal"])[6 :14 ])/4 )),"%Y%m%d"))#line:5965
	else :#line:5966
		text .insert (END ,usergroup )#line:5967
	text .insert (END ,"\n配置文件路径："+setting_cfg ["settingdir"]+"\n")#line:5968
	peizhidir =str (setting_cfg ["settingdir"])+csdir .split ("pinggutools")[0 ][-1 ]#line:5969
	roox =Toplevel ()#line:5973
	tMain =threading .Thread (target =PROGRAM_showWelcome )#line:5974
	tMain .start ()#line:5975
	t1 =threading .Thread (target =PROGRAM_closeWelcome )#line:5976
	t1 .start ()#line:5977
	root .lift ()#line:5979
	root .attributes ("-topmost",True )#line:5980
	root .attributes ("-topmost",False )#line:5981
	root .mainloop ()#line:5985
	print ("done.")#line:5986
