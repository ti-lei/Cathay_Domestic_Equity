from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import requests
import json
import datetime
import pandas as pd
import os
import shutil
import datetime

path = "/home/ec2-user/Cathay_Domestic_Equity/Data.csv"
Data = pd.read_csv(path)
Old_Data = Data.to_dict('records')

countries = {
'AppleWatch4':{
'Cn': ['MU642CH/A','MTVA2CH/A','MU6A2CH/A','MTVR2CH/A'],
'Jp': ['MU642J/A','MU6A2J/A','MTVA2J/A','MTVR2J/A'],
'Hk': ['MU642ZP/A','MU6A2ZP/A','MTVA2ZP/A','MTVR2ZP/A'],
'Uk': ['MU642B/A','MU6A2B/A','MTVA2B/A','MTVR2B/A'],
'De': ['MU642FD/A','MU6A2FD/A','MTVA2FD/A','MTVR2FD/A'],
'Ru': ['MU642RU/A','MU6A2RU/A'], #38.42 GPS
'Fr': ['MU642NF/A','MU6A2NF/A','MTVA2NF/A','MTVR2NF/A'],
'Sg': ['MU642ZA/A','MU6A2ZA/A','MTVA2ZA/A','MTVR2ZA/A']
},


'AppleWatch3':{
'Tw': ['MTEY2TA/A','MTGN2TA/A', 'MTF22TA/A', 'MTH12TA/A'],
'Cn': ['MTEY2CH/A','MTGK2CH/A','MTF22CH/A','MTGX2CH/A'],
'Jp': ['MTEY2J/A', 'MTGN2J/A','MTF22J/A','MTH12J/A'],
'Hk': ['MTEY2ZP/A', 'MTGN2ZP/A', 'MTF22ZP/A','MTH12ZP/A'],
'Uk': ['MTEY2B/A','MTGN2B/A','MTF22B/A','MTH12B/A'],
'De': ['MTEY2ZD/A','MTGN2ZD/A','MTF22ZD/A','MTH12ZD/A'],
'Ru': ['MTEY2RU/A','MTF22RU/A'], #38.42 GPS
'Fr': ['MTEY2ZD/A','MTGN2ZD/A','MTF22ZD/A','MTH12ZD/A'],
'Sg': ['MTEY2ZP/A','MTGN2ZP/A','MTF22ZP/A','MTH12ZP/A']
},

'IphoneXs-Max':{
'Tw':['MT512TA/A','MT542TA/A','MT572TA/A','MT502TA/A','MT532TA/A','MT562TA/A','MT522TA/A','MT552TA/A','MT582TA/A'],
'Cn':['MT722CH/A','MT752CH/A','MT782CH/A','MT712CH/A','MT742CH/A','MT772CH/A','MT732CH/A','MT762CH/A','MT792CH/A'],
'Jp':['MT6R2J/A','MT6V2J/A','MT6Y2J/A','MT6Q2J/A','MT6U2J/A','MT6X2J/A','MT6T2J/A','MT6W2J/A','MT702J/A'],
'Hk':['MT722ZA/A','MT752ZA/A','MT782ZA/A','MT712ZA/A','MT742ZA/A','MT772ZA/A','MT732ZA/A','MT762ZA/A','MT792ZA/A'],
'Uk':['MT512B/A','MT542B/A','MT572B/A','MT502B/A','MT532B/A','MT562B/A','MT522B/A','MT552B/A','MT582B/A'],
'De':['MT512ZD/A','MT542ZD/A','MT572ZD/A','MT502ZD/A','MT532ZD/A','MT562ZD/A','MT522ZD/A','MT552ZD/A','MT582ZD/A'],
'Ru':['MT512RU/A','MT542RU/A','MT572RU/A','MT502RU/A','MT532RU/A','MT562RU/A','MT522RU/A','MT552RU/A','MT582RU/A'],
'Fr':['MT512ZD/A','MT542ZD/A','MT572ZD/A','MT502ZD/A','MT532ZD/A','MT562ZD/A','MT522ZD/A','MT552ZD/A','MT582ZD/A'],
'Sg':['MT512ZP/A','MT542ZP/A','MT572ZP/A','MT502ZP/A','MT532ZP/A','MT562ZP/A','MT522ZP/A','MT552ZP/A','MT582ZP/A']},

'IphoneXs':{
'Tw':['MT9F2TA/A','MT9J2TA/A','MT9M2TA/A','MT9E2TA/A','MT9H2TA/A','MT9L2TA/A','MT9G2TA/A','MT9K2TA/A','MT9N2TA/A'],
'Cn':['MT9Q2CH/A','MT9U2CH/A','MT9X2CH/A','MT9P2CH/A','MT9T2CH/A','MT9W2CH/A','MT9R2CH/A','MT9V2CH/A','MT9Y2CH/A'],
'Jp':['MTAX2J/A','MTE12J/A','MTE42J/A','MTAW2J/A','MTE02J/A','MTE32J/A','MTAY2J/A','MTE22J/A','MTE52J/A'],
'Hk':['MT952ZA/A','MT982ZA/A','MT9C2ZA/A','MT942ZA/A','MT972ZA/A','MT9A2ZA/A','MT962ZA/A','MT992ZA/A','MT9D2ZA/A'],
'Uk':['MT9F2B/A','MT9J2B/A','MT9M2B/A','MT9E2B/A','MT9H2B/A','MT9L2B/A','MT9G2B/A','MT9K2B/A','MT9N2B/A'],
'De':['MT9F2ZD/A','MT9J2ZD/A','MT9M2ZD/A','MT9E2ZD/A','MT9H2ZD/A','MT9L2ZD/A','MT9G2ZD/A','MT9K2ZD/A','MT9N2ZD/A'],
'Ru':['MT9F2RU/A','MT9J2RU/A','MT9M2RU/A','MT9E2RU/A','MT9H2RU/A','MT9L2RU/A','MT9G2RU/A','MT9K2RU/A','MT9N2RU/A'],
'Fr':['MT9F2ZD/A','MT9J2ZD/A','MT9M2ZD/A','MT9E2ZD/A','MT9H2ZD/A','MT9L2ZD/A','MT9G2ZD/A','MT9K2ZD/A','MT9N2ZD/A'],
'Sg':['MT9F2ZP/A','MT9J2ZP/A','MT9M2ZP/A','MT9E2ZP/A','MT9H2ZP/A','MT9L2ZP/A','MT9G2ZP/A','MT9K2ZP/A','MT9N2ZP/A']},

'IphoneXr':{
'Tw': ['MRY52TA/A', 'MRYD2TA/A','MRYL2TA/A','MRY42TA/A','MRY92TA/A', 'MRYJ2TA/A','MRYA2TA/A','MRYH2TA/A',
	'MRYQ2TA/A','MRY72TA/A','MRYF2TA/A','MRYN2TA/A', 'MRY82TA/A','MRYG2TA/A','MRYP2TA/A', 'MRY62TA/A','MRYE2TA/A','MRYM2TA/A'],

'Cn': ['MT132CH/A', 'MT1A2CH/A','MT1J2CH/A','MT122CH/A','MT192CH/A', 'MT1H2CH/A','MT182CH/A','MT1G2CH/A', 
	'MT1Q2CH/A','MT162CH/A','MT1E2CH/A','MT1M2CH/A', 'MT172CH/A','MT1F2CH/A','MT1P2CH/A' ,'MT142CH/A','MT1D2CH/A','MT1L2CH/A'],

'Jp': ['MT032J/A', 'MT0J2J/A','MT0W2J/A','MT002J/A','MT0G2J/A', 'MT0V2J/A','MT0E2J/A','MT0U2J/A', 'MT112J/A',
'MT082J/A','MT0Q2J/A','MT0Y2J/A', 'MT0A2J/A','MT0T2J/A','MT102J/A', 'MT062J/A','MT0N2J/A','MT0X2J/A'],

'Hk': ['MT132ZA/A', 'MT1A2ZA/A','MT1J2ZA/A','MT122ZA/A','MT192ZA/A', 'MT1H2ZA/A','MT182ZA/A','MT1G2ZA/A',
 'MT1Q2ZA/A','MT162ZA/A','MT1E2ZA/A','MT1M2ZA/A', 'MT172ZA/A','MT1F2ZA/A','MT1P2ZA/A', 'MT142ZA/A','MT1D2ZA/A','MT1L2ZA/A'],

'Uk': ['MRY52B/A', 'MRYD2B/A','MRYL2B/A','MRY42B/A','MRY92B/A', 'MRYJ2B/A','MRYA2B/A','MRYH2B/A', 'MRYQ2B/A',
'MRY72B/A','MRYF2B/A','MRYN2B/A', 'MRY82B/A','MRYG2B/A','MRYP2B/A', 'MRY62B/A','MRYE2B/A','MRYM2B/A'],

'De': ['MRY52ZD/A','MRYD2ZD/A','MRYL2ZD/A','MRY42ZD/A','MRY92ZD/A', 'MRYJ2ZD/A','MRYA2ZD/A','MRYH2ZD/A',
 'MRYQ2ZD/A','MRY72ZD/A','MRYF2ZD/A','MRYN2ZD/A', 'MRY82ZD/A','MRYG2ZD/A','MRYP2ZD/A', 'MRY62ZD/A','MRYE2ZD/A','MRYM2ZD/A'],

'Ru': ['MRY52RU/A','MRYD2RU/A','MRYL2RU/A','MRY42RU/A','MRY92RU/A', 'MRYJ2RU/A','MRYA2RU/A','MRYH2RU/A',
 'MRYQ2RU/A','MRY72RU/A','MRYF2RU/A','MRYN2RU/A', 'MRY82RU/A','MRYG2RU/A','MRYP2RU/A', 'MRY62RU/A','MRYE2RU/A','MRYM2RU/A'],

'Fr': ['MRY52ZD/A','MRYD2ZD/A','MRYL2ZD/A','MRY42ZD/A','MRY92ZD/A', 'MRYJ2ZD/A','MRYA2ZD/A','MRYH2ZD/A',
 'MRYQ2ZD/A','MRY72ZD/A','MRYF2ZD/A','MRYN2ZD/A', 'MRY82ZD/A','MRYG2ZD/A','MRYP2ZD/A', 'MRY62ZD/A','MRYE2ZD/A','MRYM2ZD/A'],

'Sg': ['MRY52ZP/A','MRYD2ZP/A','MRYL2ZP/A','MRY42ZP/A','MRY92ZP/A', 'MRYJ2ZP/A','MRYA2ZP/A','MRYH2ZP/A',
 'MRYQ2ZP/A','MRY72ZP/A','MRYF2ZP/A','MRYN2ZP/A', 'MRY82ZP/A','MRYG2ZP/A','MRYP2ZP/A', 'MRY62ZP/A','MRYE2ZP/A','MRYM2ZP/A']},


'Iphone8-plus':{
'Tw': ['MQ8M2TA/A', 'MQ8Q2TA/A','MQ8L2TA/A','MQ8P2TA/A','MQ8N2TA/A', 'MQ8R2TA/A'],
'Cn': ['MQ8E2CH/A','MQ8H2CH/A','MQ8F2CH/A','MQ8J2CH/A','MQ8D2CH/A','MQ8G2CH/A'],
'Jp': ['MQ9L2J/A','MQ9P2J/A','MQ9M2J/A','MQ9Q2J/A','MQ9K2J/A','MQ9N2J/A'],
'Hk': ['MQ8E2ZP/A','MQ8H2ZP/A','MQ8F2ZP/A','MQ8J2ZP/A','MQ8D2ZP/A','MQ8G2ZP/A'],
'Uk': ['MQ8M2B/A','MQ8Q2B/A','MQ8N2B/A','MQ8R2B/A','MQ8L2B/A','MQ8P2B/A'],
'De': ['MQ8M2ZD/A','MQ8Q2ZD/A','MQ8N2ZD/A','MQ8R2ZD/A','MQ8L2ZD/A','MQ8P2ZD/A'],
'Ru': ['MQ8M2RU/A','MQ8Q2RU/A','MQ8N2RU/A','MQ8R2RU/A','MQ8L2RU/A','MQ8P2RU/A'],
'Fr': ['MQ8M2ZD/A','MQ8Q2ZD/A','MQ8N2ZD/A','MQ8R2ZD/A','MQ8L2ZD/A','MQ8P2ZD/A'],
'Sg': ['MQ8M2ZP/A','MQ8Q2ZP/A','MQ8N2ZP/A','MQ8R2ZP/A','MQ8L2ZP/A','MQ8P2ZP/A']},


'Iphone8':{
'Tw': ['MQ6H2TA/A', 'MQ7D2TA/A','MQ6J2TA/A','MQ7E2TA/A','MQ6G2TA/A', 'MQ7C2TA/A'],
'Cn': ['MQ6L2CH/A', 'MQ7G2CH/A','MQ6M2CH/A','MQ7H2CH/A','MQ6K2CH/A', 'MQ7F2CH/A'],
'Jp': ['MQ792J/A', 'MQ852J/A','MQ7A2J/A','MQ862J/A','MQ782J/A', 'MQ842J/A'],
'Hk': ['MQ6L2ZP/A', 'MQ7G2ZP/A','MQ6M2ZP/A','MQ7H2ZP/A','MQ6K2ZP/A', 'MQ7F2ZP/A'],
'Uk': ['MQ6H2B/A', 'MQ7D2B/A','MQ6J2B/A','MQ7E2B/A','MQ6G2B/A', 'MQ7C2B/A'],
'De': ['MQ6H2ZD/A','MQ7D2ZD/A','MQ6J2ZD/A','MQ7E2ZD/A','MQ6G2ZD/A', 'MQ7C2ZD/A'],
'Ru': ['MQ6H2RU/A','MQ7D2RU/A','MQ6J2RU/A','MQ7E2RU/A','MQ6G2RU/A', 'MQ7C2RU/A'],
'Fr': ['MQ6H2ZD/A','MQ7D2ZD/A','MQ6J2ZD/A','MQ7E2ZD/A','MQ6G2ZD/A', 'MQ7C2ZD/A'],
'Sg': ['MQ6H2ZP/A','MQ7D2ZP/A','MQ6J2ZP/A','MQ7E2ZP/A','MQ6G2ZP/A', 'MQ7C2ZP/A']
}}


Us ={
	'IphoneXr':[
	'MT3L2LL/A', 'MT3U2LL/A','MT412LL/A','MT3K2LL/A','MT3T2LL/A', 'MT402LL/A','MT3R2LL/A','MT3Y2LL/A', 'MT462LL/A',
	'MT3N2LL/A','MT3W2LL/A','MT442LL/A', 'MT3Q2LL/A','MT3X2LL/A','MT452LL/A', 'MT3M2LL/A','MT3V2LL/A','MT422LL/A'],

	'IphoneXs-Max':['MT5A2LL/A','MT5E2LL/A','MT5H2LL/A','MT592LL/A','MT5D2LL/A','MT5G2LL/A','MT5C2LL/A','MT5F2LL/A','MT5J2LL/A'],
	'IphoneXs':['MT952LL/A','MT982LL/A','MT9C2LL/A','MT942LL/A','MT972LL/A','MT9A2LL/A','MT962LL/A','MT992LL/A','MT9D2LL/A'],
	'Iphone8-plus':['MQ8E2LL/A','MQ8H2LL/A','MQ8F2LL/A','MQ8J2LL/A','MQ8D2LL/A','MQ8G2LL/A'],
	'Iphone8':['MQ6L2LL/A', 'MQ7G2LL/A','MQ6M2LL/A', 'MQ7H2LL/A','MQ6K2LL/A','MQ7F2LL/A'],
	'AppleWatch3':['MTEY2LL/A', 'MTGG2LL/A', 'MTF22LL/A', 'MTGR2LL/A'],
	'AppleWatch4':['MU642LL/A',	'MU6A2LL/A','MTUD2LL/A','MTUU2LL/A']}

Product_Us_R = {k: key for key, value in Us.items() for k in value}

#---------------------------------------------------------------- Color-----------------------------------------------------------#
Color = {
'Silver' : ['MQ8E2', 'MQ9E2', 'MQ972', 'MQ8H2', 'MQ9A2', 'MQ9H2', 'MQ8M2', 'MQ8U2', 'MQ912', 'MQ8Q2', 'MQ8X2', 'MQ942','MQ9L2','MQ9P2',
		'MQAK2', 'MQAR2', 'MQAD2', 'MQAN2', 'MQAV2', 'MQAG2', 'MQCT2', 'MQCL2', 'MQAY2', 'MQA62','MQCW2', 'MQCP2', 'MQC22', 'MQA92',
		#iphone8
		'MQ6H2', 'MQ6W2', 'MQ702','MQ7D2', 'MQ7R2', 'MQ7V2','MQ6L2', 'MQ732', 'MQ762','MQ7G2', 'MQ7Y2', 'MQ822','MQ792','MQ852',
		#iphoneXs
		'MT952','MT982','MT9C2','MT9F2','MT9J2','MT9M2','MT9Q2','MT9U2','MT9X2','MTAX2','MTE12','MTE42',
		#iphoneXsMax
		'MT512','MT542','MT572','MT5A2','MT5E2','MT5H2','MT6R2','MT6V2','MT6Y2','MT722','MT752','MT782'],


'Gold' : ['MQ8F2', 'MQ9F2', 'MQ982','MQ8J2', 'MQ9C2', 'MQ9J2', 'MQ8N2', 'MQ8V2', 'MQ922','MQ8R2', 'MQ8Y2', 'MQ952','MQ9M2','MQ9Q2',
		#iphone8
		'MQ6M2', 'MQ742', 'MQ772', 'MQ7H2', 'MQ802', 'MQ832', 'MQ6J2', 'MQ6X2', 'MQ712', 'MQ7E2', 'MQ7T2', 'MQ7W2','MQ7A2','MQ862',
		#iphoneXs
		'MT962','MT992','MT9D2','MT9G2','MT9K2','MT9N2','MT9R2','MT9V2','MT9Y2','MTAY2','MTE22','MTE52',
		#iphoneXsMax
		'MT522','MT552','MT5F2','MT582','MT5C2','MT6W2','MT5J2','MT6T2','MT762','MT702','MT732','MT792'],

'Gray' : ['MQ8D2', 'MQ9D2', 'MQ962', 'MQ8G2', 'MQ9G2', 'MQ992', 'MQ8L2', 'MQ8T2', 'MQ902', 'MQ8P2', 'MQ8W2', 'MQ932','MQ9K2','MQ9N2',
		'MQAJ2', 'MQAQ2', 'MQAC2', 'MQAM2', 'MQAU2', 'MQAF2','MQCR2', 'MQCK2', 'MQAX2', 'MQA52','MQCV2', 'MQCN2', 'MQC12', 'MQA82',
		#iphone8
		'MQ6K2','MQ722','MQ752','MQ7F2','MQ7X2','MQ812','MQ6G2','MQ6V2', 'MQ6Y2','MQ7C2','MQ7Q2','MQ7U2','MQ782','MQ842',
		#iphoneXs
		'MT942','MT972','MT9A2','MT9E2','MT9H2','MT9L2','MT9P2','MT9T2','MT9W2','MTAW2','MTE02','MTE32',
		#iphoneXsMax
		'MT502','MT532','MT562','MT592','MT5D2','MT5G2','MT6Q2','MT6U2','MT6X2','MT712','MT742','MT772'],

'Red' : ['MRTG2', 'MRTJ2', 'MRT72', 'MRTH2', 'MRTK2', 'MRT82', 'MRTC2', 'MRTE2', 'MRT92', 'MRTA2', 'MRTD2', 'MRTF2','MRTL2','MRTM2',
		#iphone8
		'MRRK2', 'MRRR2', 'MRRT2', 'MRRL2', 'MRRW2', 'MRRX2', 'MRRM2', 'MRRP2', 'MRRQ2', 'MRRN2', 'MRRU2', 'MRRV2',
		#iphoneXr
		 'MT3M2','MT3V2','MT422','MRY62','MRYE2','MRYM2','MT142','MT1D2','MT1L2','MT062','MT0N2','MT0X2'],

'White' : [#iphoneXr
		'MT3L2', 'MT3U2','MT412','MRY52', 'MRYD2', 'MRYL2', 'MT132', 'MT1A2', 'MT1J2', 'MT032', 'MT0J2', 'MT0W2'],

'Black' : [#iphoneXr
		'MT3K2','MT3T2', 'MT402','MRY42','MRY92', 'MRYJ2','MT122','MT192', 'MT1H2','MT002','MT0G2', 'MT0V2'],

'Blue' : [#iphoneXr
		'MT3R2','MT3Y2', 'MT462','MRYA2','MRYH2', 'MRYQ2','MT182','MT1G2', 'MT1Q2','MT0E2','MT0U2', 'MT112'],

'Yellow' : [#iphoneXr 
		'MT3N2','MT3W2','MT442', 'MRY72','MRYF2','MRYN2','MT162','MT1E2','MT1M2','MT082','MT0Q2','MT0Y2'],

'Coral' : [#iphoneXr
		'MT3Q2','MT3X2','MT452','MRY82','MRYG2','MRYP2','MT172','MT1F2','MT1P2','MT0A2','MT0T2','MT102'],


'GPS' : [# Iphone Watch 3
		'MTEY2', 'MTF22',
		# Iphone Watch 4
		'MU642','MU6A2'],

'GPSCelluar' :[# Iphone Watch 3
			'MTGG2', 'MTGN2', 'MTGK2','MTGR2','MTGX2','MTH12',
			# Iphone Watch 4
			'MTUD2','MTUU2','MTVA2','MTVR2']}



Color_R = {k: key for key, value in Color.items() for k in value}
#---------------------------------------------------------------- SIZE -------------------------------------------------------------#
Size = {
'64GB' : [
			'MQ8F2', 'MQ9F2', 'MQ982', 'MQ8E2', 'MQ9E2', 'MQ972', 'MQ8D2', 'MQ9D2', 'MQ962', 'MRTG2', 'MRTJ2', 'MRT72',
			'MQ8N2', 'MQ8V2', 'MQ922', 'MQ8M2', 'MQ8U2', 'MQ912', 'MQ8L2', 'MQ8T2', 'MQ902', 'MRTC2', 'MRTE2', 'MRT92',
			'MQ9L2', 'MQ9M2', 'MQ9K2', 'MRTL2', 'MQAK2', 'MQAR2', 'MQAD2', 'MQCT2', 'MQCL2', 'MQAY2', 'MQA62', 'MQCR2',
			'MQCK2', 'MQAX2', 'MQA52', 'MQAJ2', 'MQAQ2', 'MQAC2',
			#Iphone8
			'MQ6M2', 'MQ742', 'MQ772','MQ6L2', 'MQ732', 'MQ762','MQ6K2', 'MQ722', 'MQ752','MRRK2', 'MRRR2', 'MRRT2','MQ6J2',
			 'MQ6X2', 'MQ712','MQ6H2', 'MQ6W2', 'MQ702','MQ6G2', 'MQ6V2','MQ6Y2','MRRM2', 'MRRP2', 'MRRQ2','MQ792','MQ7A2','MQ782',

			#IphoneXr
			'MRY52','MRY42','MRYA2','MRY72','MRY82','MRY62','MT132','MT122','MT182','MT162','MT172','MT142','MT032','MT002','MT0E2',
			'MT082','MT0A2','MT062','MT3L2','MT3K2','MT3R2','MT3N2','MT3Q2', 'MT3M2',

			#IphoneXs
			'MT942','MT952','MT962','MT9E2','MT9F2','MT9G2','MT9P2','MT9Q2','MT9R2','MTAW2','MTAX2','MTAY2',

			#IphoneXsMax
			'MT502','MT512','MT522','MT592','MT5A2','MT5C2','MT6Q2','MT6R2','MT6T2','MT712','MT722','MT732'],

'128GB' : [
			#IphonXr
			'MRYD2','MRY92','MRYH2','MRYF2','MRYG2','MRYE2','MT1A2','MT192','MT1G2','MT1E2','MT1F2','MT1D2', 'MT0J2','MT0G2','MT0U2',
			'MT0Q2','MT0T2','MT0N2','MT3U2','MT3T2','MT3Y2','MT3W2','MT3X2','MT3V2'],

				
'256GB' : [
				#Iphone8 
				'MQ7H2', 'MQ802', 'MQ832','MQ7G2', 'MQ7Y2', 'MQ822','MQ7F2', 'MQ7X2', 'MQ812','MRRL2', 'MRRW2', 'MRRX2','MQ7E2',
				'MQ7T2', 'MQ7W2','MQ7D2', 'MQ7R2', 'MQ7V2',	'MQ7C2', 'MQ7Q2', 'MQ7U2','MRRN2', 'MRRU2', 'MRRV2',
				#Iphone8plus
				'MQ8J2', 'MQ9C2', 'MQ9J2','MQ8H2', 'MQ9A2', 'MQ9H2','MQ8G2', 'MQ9G2', 'MQ992','MRTH2', 'MRTK2', 'MRT82','MQ8R2', 'MQ8Y2',
				'MQ952','MQ8Q2', 'MQ8X2', 'MQ942','MQ8P2', 'MQ8W2', 'MQ932','MRTA2', 'MRTD2', 'MRTF2','MQ852','MQ862','MQ842','MQ9P2',
				'MQ9Q2','MQ9N2',
				#IphoneXr
				'MRYL2','MRYJ2','MRYQ2','MRYN2','MRYP2','MRYM2','MT1J2','MT1H2','MT1Q2','MT1M2','MT1P2','MT1L2','MT0W2','MT0V2',
				'MT112','MT0Y2','MT102','MT0X2','MT412', 'MT402', 'MT462','MT442', 'MT452','MT422',
				#IphoneXs
				'MT972','MT982','MT992','MT9H2','MT9J2','MT9K2','MT9T2','MT9U2','MT9V2','MTE02','MTE12','MTE22',
				#IphoneXsMax
				'MT532','MT542','MT552','MT5D2','MT5E2','MT5F2','MT6U2','MT6V2','MT6W2','MT742','MT752','MT762'],

'512GB' : [
				#IphoneXs
				'MT9A2','MT9C2','MT9D2','MT9L2','MT9M2','MT9N2','MT9W2','MT9X2','MT9Y2','MTE32','MTE42','MTE52',
				#IphoneXsMax
				'MT562','MT572','MT582','MT5G2','MT5H2','MT5J2','MT6X2','MT6Y2','MT702','MT772','MT782','MT792'],

#IphoneWatch3
'38mm': ['MTEY2','MTGG2','MTGN2','MTGK2'],
'42mm': ['MTF22','MTGR2','MTH12','MTGX2'],
#IphoneWatch4
'40mm': ['MTUD2','MTVA2','MU642'],
'44mm': ['MTUU2','MTVR2','MU6A2']}
#為了方便接下來 不同的 model 進行 Size 的對應 這裡將 key(size) 跟 value(model) 進行對調 變成 Key 為 model value 為 size 
# eg:'MQ8F2':'Size_SixFour'

Size_R = {k: key for key, value in Size.items() for k in value}
# for key, value in size.items
# 	for k in value
# 		k: key
#---------------------拿到所有 iphone 分 不同產品的 model 的型號--------------------------#

# 除了US以外 其他所有國家以 [產品] 為 key 對應到所有的 value [型號]
# "{}".format(Product_item) 會產生變數名稱 , eg:{'Iphone8':'MQ6H2TA/A'}
Product = {}
for Product_item in countries.keys():
	Product["{}".format(Product_item)]= sum([v for v in countries[Product_item].values()], [])

Product_R = {k: key for key, value in Product.items() for k in value}

#拿到所有以[國家] 為 key 對應到所有的 [型號]
Country = {}
for v in countries.values():
  for k in v.keys():
    Country.setdefault(k,[]) # added key
    Country[k] += v[k]

# print(Country)

#以[型號] 為 key 對應到所有的 [國家]
Country_R = {k: key for key, value in Country.items() for k in value}

# 除了US以外所有的 [型號] 併在一起 , 給for迴圈使用
Model_All = sum(list(Product.values()),[])
# 把US所有的 [型號] 併再一起 , 給for迴圈使用
Model_Us = sum(list(Us.values()),[])

res=[]

# 美國的要單獨跑 因為地址網址的dictionary 是空的
for Model in Model_Us:
	# print(Model)
	d = {} #清空dictionary
	d['Country'] = 'Us'
	d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")

	d['Size'] = Size_R[Model[0:5]]
	d['Product'] = Product_Us_R[Model]
	d['Color'] = Color_R[Model[0:5]]

	url = 'https://www.apple.com/shop/delivery-message?parts.0=%s&little=true' % ( Model )
	r = requests.get(url)
	response = json.loads(r.text)
	d['Deliver'] = response['body']['content']['deliveryMessage'][Model]['quote']
	res.append(d)


for Product in countries:
	#外迴圈跑國家
	for Country in countries[Product]:
		#內迴圈跑型號
		for Model in countries[Product][Country]:

			d = {} #清空dictionary
			d['Country'] = Country
			d['TimeStemp'] = datetime.datetime.today().strftime("%Y-%m-%d")
			d['Size'] = Size_R[Model[0:5]]
			d['Product'] = Product_R[Model]
			d['Color'] = Color_R[Model[0:5]]


			#單獨擷取一個產品
			url = 'https://www.apple.com/%s/shop/delivery-message?parts.0=%s&little=true' % (d['Country'].lower(), Model)
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

df.to_csv(path,encoding='utf_8_sig', index=False)


#要去哪裡
destname = "/home/ec2-user/Cathay_Domestic_Equity/static/Data.csv"
#來源資料
fromname = "/home/ec2-user/Cathay_Domestic_Equity/Data.csv"
shutil.copy2(fromname, destname)

print("ok")