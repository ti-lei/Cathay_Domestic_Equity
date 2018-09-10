from flask import Flask, jsonify, request, send_from_directory, url_for
from flask import render_template
import requests
import json
import datetime
import pandas as pd
import os

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route("/update")
def Update():

	Data = pd.read_csv("Data.csv")
	Old_Data = Data.to_dict('records')

	countries = {
	'Iphone8plus':{	'Cn': ['MQ8E2CH/A','MQ8H2CH/A','MQ8F2CH/A','MQ8J2CH/A','MQ8D2CH/A','MQ8G2CH/A','MRT72CH/A','MRT82CH/A'],
	'Jp': ['MQ9L2J/A','MQ9P2J/A','MQ9M2J/A','MQ9Q2J/A','MQ9K2J/A','MQ9N2J/A','MRTL2J/A','MRTM2J/A'],
	'Hk': ['MQ8E2ZP/A','MQ8H2ZP/A','MQ8F2ZP/A','MQ8J2ZP/A','MQ8D2ZP/A','MQ8G2ZP/A','MRT72ZP/A','MRT82ZP/A'],
	'Uk': ['MQ8M2B/A','MQ8Q2B/A','MQ8N2B/A','MQ8R2B/A','MQ8L2B/A','MQ8P2B/A','MRT92B/A','MRTA2B/A'],
	'De': ['MQ8M2ZD/A','MQ8Q2ZD/A','MQ8N2ZD/A','MQ8R2ZD/A','MQ8L2ZD/A','MQ8P2ZD/A','MRT92ZD/A','MRTA2ZD/A'],
	'Ru': ['MQ8M2RU/A','MQ8Q2RU/A','MQ8N2RU/A','MQ8R2RU/A','MQ8L2RU/A','MQ8P2RU/A','MRT92RU/A','MRTA2RU/A'],
	'Fr': ['MQ8M2ZD/A','MQ8Q2ZD/A','MQ8N2ZD/A','MQ8R2ZD/A','MQ8L2ZD/A','MQ8P2ZD/A','MRT92ZD/A','MRTA2ZD/A'],
	'Sg': ['MQ8M2ZP/A','MQ8Q2ZP/A','MQ8N2ZP/A','MQ8R2ZP/A','MQ8L2ZP/A','MQ8P2ZP/A','MRT92ZP/A','MRTA2ZP/A'],
	},

	'IphoneX':{ 'Cn': ['MQA62CH/A', 'MQA92CH/A','MQA52CH/A','MQA82CH/A'],
	'Jp': ['MQAY2J/A', 'MQC22J/A','MQAX2J/A','MQC12J/A'],
	'Hk': ['MQA62ZP/A', 'MQA92ZP/A','MQA52ZP/A','MQA82ZP/A'],
	'Uk': ['MQAG2B/A', 'MQAD2B/A','MQAF2B/A','MQAC2B/A'],
	'De': ['MQAC2ZD/A','MQAF2ZD/A','MQAG2ZD/A','MQAD2ZD/A'],
	'Ru': ['MQAG2RU/A','MQAD2RU/A','MQAC2RU/A','MQAF2RU/A'],
	'Fr': ['MQAG2ZD/A','MQAD2ZD/A','MQAC2ZD/A','MQAF2ZD/A'],
	'Sg': ['MQAG2ZP/A','MQAD2ZP/A','MQAF2ZP/A','MQAC2ZP/A']}
	}
		
	#Iphone8plus
	US = ['MQ8E2LL/A','MQ8H2LL/A','MQ8F2LL/A','MQ8J2LL/A','MQ8D2LL/A','MQ8G2LL/A','MRT72LL/A','MRT82LL/A',
		#IphoneX
		'MQA62LL/A','MQA92LL/A','MQA52LL/A','MQA82LL/A']

	Silver = ['MQ8E2', 'MQ9E2', 'MQ972', 'MQ8H2', 'MQ9A2', 'MQ9H2', 'MQ8M2', 'MQ8U2', 'MQ912', 'MQ8Q2', 'MQ8X2', 'MQ942','MQ9L2','MQ9P2',
				'MQAK2', 'MQAR2', 'MQAD2', 'MQAN2', 'MQAV2', 'MQAG2', 'MQCT2', 'MQCL2', 'MQAY2', 'MQA62','MQCW2', 'MQCP2', 'MQC22', 'MQA92']

	Gold = ['MQ8F2', 'MQ9F2', 'MQ982','MQ8J2', 'MQ9C2', 'MQ9J2', 'MQ8N2', 'MQ8V2', 'MQ922','MQ8R2', 'MQ8Y2', 'MQ952','MQ9M2','MQ9Q2']

	Gray = ['MQ8D2', 'MQ9D2', 'MQ962', 'MQ8G2', 'MQ9G2', 'MQ992', 'MQ8L2', 'MQ8T2', 'MQ902', 'MQ8P2', 'MQ8W2', 'MQ932','MQ9K2','MQ9N2',
			'MQAJ2', 'MQAQ2', 'MQAC2', 'MQAM2', 'MQAU2', 'MQAF2','MQCR2', 'MQCK2', 'MQAX2', 'MQA52','MQCV2', 'MQCN2', 'MQC12', 'MQA82']


	Red = ['MRTG2', 'MRTJ2', 'MRT72', 'MRTH2', 'MRTK2', 'MRT82', 'MRTC2', 'MRTE2', 'MRT92', 'MRTA2', 'MRTD2', 'MRTF2','MRTL2','MRTM2']

	Sixfour = ['MQ8F2', 'MQ9F2', 'MQ982', 'MQ8E2', 'MQ9E2', 'MQ972', 'MQ8D2', 'MQ9D2', 'MQ962', 'MRTG2', 'MRTJ2', 'MRT72',
				'MQ8N2', 'MQ8V2', 'MQ922', 'MQ8M2', 'MQ8U2', 'MQ912', 'MQ8L2', 'MQ8T2', 'MQ902', 'MRTC2', 'MRTE2', 'MRT92',
				'MQ9L2', 'MQ9M2', 'MQ9K2', 'MRTL2', 'MQAK2', 'MQAR2', 'MQAD2', 'MQCT2', 'MQCL2', 'MQAY2', 'MQA62', 'MQCR2',
				'MQCK2', 'MQAX2', 'MQA52', 'MQAJ2', 'MQAQ2', 'MQAC2']

	Iphone8plus_us = ['MQ8E2LL/A','MQ8H2LL/A','MQ8F2LL/A','MQ8J2LL/A','MQ8D2LL/A','MQ8G2LL/A','MRT72LL/A','MRT82LL/A']
	IphoneX_us = ['MQA62LL/A','MQA92LL/A','MQA52LL/A','MQA82LL/A']



	#---------------------拿到所有 iphone 分 不同產品的 model 的型號--------------------------#

	#拿到所有的 國家 的 value，但此時所有的value 會形成兩層的list 要把這兩層的list解開
	mylist = [v for v in countries['Iphone8plus'].values()]
	# 把list 展開成一層
	Iphone8plus = [newlist for sublist in mylist for newlist in sublist]

	mylist = [v for v in countries['IphoneX'].values()]
	# 把list 展開成一層
	IphoneX = [newlist for sublist in mylist for newlist in sublist]


	res=[]

	#美國的要單獨跑 因為地址網址的dictionary 是空的
	for Model in US:
		d = {} #清空dictionary
		d['Country'] = 'Us'
		d['Size'] = '64GB' if Model[0:5] in Sixfour else '256GB'
		d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")

		if Model in Iphone8plus_us:
			d['Product'] = 'Iphone8plus'
		elif Model in IphoneX_us:
			d['Product'] = 'IphoneX'
		else:
			d['Product'] = 'Iphone8'


		if Model[0:5] in Silver:
			d['Color'] = 'Silver'
		elif Model[0:5] in Gold:
			d['Color'] = 'Gold'
		elif Model[0:5] in Gray:
			d['Color'] = 'Gray'
		elif Model[0:5] in Red:
			d['Color'] = 'Red'

		url = 'https://www.apple.com/shop/delivery-message?parts.0=%s&little=true' % ( Model )
		r = requests.get(url)
		response = json.loads(r.text)
		d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
		res.append(d)

	#%%
	#最外迴圈跑產品別
	for Product in countries:
		#外迴圈跑國家
		for Country in countries[Product]:
		    #內迴圈跑型號
		    for Model in countries[Product][Country]:
		        d = {} #清空dictionary
		        d['Country'] = Country
		        d['Size'] = '64GB' if Model[0:5] in Sixfour else '256GB'
		        d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")

		        if Model in Iphone8plus:
		        	d['Product'] = 'Iphone8plus'
		        elif Model in IphoneX:
		        	d['Product'] = 'IphoneX'
		        else:
		        	d['Product'] = 'IphoneX'


		        if Model[0:5] in Silver:
		        	d['Color'] = 'Silver'
		        elif Model[0:5] in Gold:
		        	d['Color'] = 'Gold'
		        elif Model[0:5] in Gray:
		        	d['Color'] = 'Gray'
		        elif Model[0:5] in Red:
		        	d['Color'] = 'Red'


		        
		        #單獨擷取一個產品
		        url = 'https://www.apple.com/%s/shop/delivery-message?parts.0=%s&little=true' % (Country.lower(), Model)
		        r = requests.get(url)
		        response = json.loads(r.text)
		        #try:
		        #    d['quote'] = response['body']['content']['deliveryMessage'][Model]['quote'].split()[1]
		        #except:
		        d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
		        res.append(d)

	#把舊資料跟新資料合起來

	newres = res + Old_Data

	df = pd.DataFrame(newres)

    # Pivot value:欲處理的資訊(相加 取平均 等等等)
    #index:列向量
    #columns:行向量

	df.to_csv('Data.csv',encoding='utf_8_sig', index=False)
	return "true"

@app.route("/")
#網址後面不管帶什麼東西都會走這條路 如果要帶其他東西就是在 / 後面加東西
#def 函數一定要帶著 要reuturn東西?
def hello():
    # 進行 request
    # 對網頁拿資訊
	Country = request.values.get('Country')
	Index = request.values.get('Index', 'TimeStemp')  #這裡如果get不到index 會給default值 'color'
	Column = request.values.get('Column', 'Size')
	Product = request.values.get('Product','IphoneX')

	# df = get_df()
	df = pd.read_csv("Data.csv")

	#--------------------- Maping 不同的 國家的名字 ---------------------#
	All_countries = {'Us':'美國','Cn':'中國','Jp':'日本','Hk':'香港','Uk':'英國','De':'德國','Ru':'俄羅斯','Fr':'法國','Sg':'新加坡'}

	df['All_countries'] = df.Country.map(All_countries)
	#只把我們要的 product 拿出來
	df = df[df['Product']==Product]


	pivot = pd.pivot_table(df, values='Deliver', index=Index,
	    columns=['All_countries','Color','Size'], aggfunc=lambda x: ' '.join(x)).sort_index(ascending=False)

	#---------------------     協理要的國家排序    ---------------------#
	cols = ['美國','中國','香港','日本','德國','法國','新加坡','俄羅斯']

	pivot = pivot[cols]

	#df_fill_country會把篩選過後的表格輸出
	df_fill_country = df[df['Country']==Country]
	df_fill_country = pd.pivot_table(df_fill_country, values='Deliver', index=Index,
	    columns=['All_countries','Color','Size'], aggfunc=lambda x: ' '.join(x)).sort_index(ascending=False)

	#--------------------- 分產品 返回不同的網頁 --------------------------#

	if Product == 'IphoneX':
	# 如果 Country 不是空的就把全部都秀出來
		if not Country :
		    return render_template("IphoneX.html", table = pivot.to_html(classes = "table table-striped table-hover"),title = 'Overview')
		country_title = All_countries[Country]
		return render_template("IphoneX.html",table = df_fill_country.to_html(classes = "table table-striped table-hover"),title = country_title, country=Country)

	elif Product == 'Iphone8plus':

		if not Country :
		    return render_template("Iphone8plus.html", table = pivot.to_html(classes = "table table-striped table-hover"),title = 'Overview')
		country_title = All_countries[Country]
		return render_template("Iphone8plus.html",table = df_fill_country.to_html(classes = "table table-striped table-hover"),title = country_title)

if __name__ == "__main__":
    # app.run(debug=True, host='0.0.0.0', port=80)
    app.run(debug=True)
