from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pandas.core.frame import DataFrame
import re
import csv

def check_link(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Can not connect to target url, please check the url!!!')

def get_target_table(url_address, target_table_index):
	res = requests.get(url_address)
	soup = bs(res.text, 'html.parser')
	all_target_page_tables = soup.select('table')
	return all_target_page_tables[target_table_index]

def get_city_links(main_table, city_link_list):
	for tr in main_table.tbody.findAll('tr'):
		city_column = tr.find('a')
		if not city_column:
			pass
		else:
			link = city_column.get('href')
			# print(link)
			city_link_list.append(link)
	city_link_list.pop(0)
	# print(city_link_list)

def find_timeZone_from_cityLinks(city_link_list, city_timezone_list):
	for link in city_link_list:
		city_table = get_target_table('https://en.wikipedia.org/'+link, 0)
		for tr in city_table.tbody.findAll('tr'):
			check = False
			if not tr.find('th'):
				pass
			elif tr.find('th'):
				label = tr.find('th').getText()
				# print(label)
				# print(type(label))
				if not label:
					pass
				elif(label == 'Time zone'):
					city_timezone_list.append(tr.find('td').getText())
					# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
					# print(tr.find('td').getText())
					check = True
					break
				# elif(label == ('Incorporated (city)'or'Incorporated'or'Consolidated')):
				# 	city_incorporated_date_list.append(tr.find('td').getText())
		if(check):
			pass
		else:
			city_timezone_list.append('null')
	# 		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	# print(city_timezone_list)
	# print(len(city_timezone_list))

# def cleaning_timeZone_list(city_link_list, city_timezone_list):
# 	for link in city_link_list:
# 		city_table = get_target_table('https://en.wikipedia.org/'+link, 1)


def find_incorporated_date_from_cityLinks(city_link_list, city_incorporated_date_list):
	for link in city_link_list:
		city_table = get_target_table('https://en.wikipedia.org/'+link, 0)
		for tr in city_table.tbody.findAll('tr'):
			check = False
			if not tr.find('th'):
				pass
			elif tr.find('th'):
				label = tr.find('th').getText()
				# print(label)
				# print(type(label))
				if not label:
					pass
				elif(label == 'Settled' or label == 'Settled (town)' or label == 'Founded' or label == 'founded' or label == 'Incorporated' or label == 'Incorporated (city)'):
					city_incorporated_date_list.append(tr.find('td').getText())
					# print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
					# print(tr.find('td').getText())
					check = True
					break
				# elif(label == ('Incorporated (city)'or'Incorporated'or'Consolidated')):
				# 	city_incorporated_date_list.append(tr.find('td').getText())
		if(check):
			pass
		else:
			city_incorporated_date_list.append('null')
	# 		print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	# print(city_incorporated_date_list)
	# print(len(city_incorporated_date_list))



def main():
	root_url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
	citypage_table = []
	main_table_list = []
	city_link_list = []
	city_incorporated_date_list = []
	city_timezone_list = []

	rs = check_link(root_url)
	print("################# Reading main table, please wait! ##################")
	main_table = get_target_table(root_url, 4)
	main_table_list.append(pd.concat(pd.read_html(main_table.prettify())))
	df_main = pd.concat(main_table_list)
	print("########## Exporting main table to local file, please wait! #########")
	df_main.to_csv('./main_table(by_Wensong_Liu).csv',index=False,header=True)

	print("############## Reading all cities' links, please wait! ##############")
	get_city_links(main_table, city_link_list)
	print("############# Converting list to DataFrame, please wait! ############")
	dict_cities_link = {"Cities' Wiki Links" : city_link_list}
	df_city_link = DataFrame(dict_cities_link)
	print("###### Exporting all cities' links to local file, please wait! ######")
	df_city_link.to_csv('./city_link.csv',index=False,header=True)

	print("########## Reading all cities' founded date, please wait! ###########")
	find_incorporated_date_from_cityLinks(city_link_list, city_incorporated_date_list)
	print("############# Converting list to DataFrame, please wait! ############")
	dict_founded_date = {"Cities' Founded Date" : city_incorporated_date_list}
	df_founded_date = DataFrame(dict_founded_date)
	print("### Exporting all cities' founded date to local file, please wait! ##")
	df_founded_date.to_csv('./city_founded_date.csv',index=False,header=True)

	print("############ Reading all cities' time zone, please wait! ############")
	find_timeZone_from_cityLinks(city_link_list, city_timezone_list)
	print("############# Converting list to DataFrame, please wait! ############")
	dict_cities_timezone = {"Cities' Time-Zone" : city_timezone_list}
	df_cities_timezone = DataFrame(dict_cities_timezone)
	print("#### Exporting all cities' time zone to local file, please wait! ####")
	df_cities_timezone.to_csv('./city_timezone.csv',index=False,header=True)

	# Concat dataframes we need
	df_result = pd.concat([df_main, df_founded_date, df_cities_timezone], axis = 1)
	
	print("######### Exporting final result to local file, please wait! ########")
	df_result.to_csv('./final_result(by_Wensong_Liu).csv',index=False,header=True)


if __name__ == '__main__':
    main()






