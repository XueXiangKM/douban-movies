#coding=utf-8
import expanddouban, csv
from bs4 import BeautifulSoup

def getMovieUrl(category, location):
	"""
	该函数接受类别和地区的输入，返回该地区该类别电影清单的url
	"""
	url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}'.format(category, location)
	return url

def getUrlHtml(category, location):
	#该函数接受电影清单url的输入，返回该url页面的html代码经BeautifulSoup解析后的BeautifulSoup对象
	html_of_url =  expanddouban.getHtml(getMovieUrl(category, location), True, 5) #根据豆瓣robots.txt，waittime设置为5
	soup_of_html = BeautifulSoup(html_of_url, 'html.parser')
	return soup_of_html

class Movie:
	#定义电影类
	def __init__(self, name, rate, location, category, info_link, cover_link):
		self.name = name
		self.rate = rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link

def getMovies(category, location):
	"""
	该函数接受类别和地区的输入，返回该类别该地区评分在9-10分的电影信息列表
	"""
	list_of_movie = []
	html = getUrlHtml(category, location)
	contents_tags = html.find_all('a', class_='item')
	for i in contents_tags:
		name = i.find('img').get('alt') #找到电影名称
		rate = i.find(class_='rate').string #找到电影评分
		info_link = i.get('href') #找到电影链接
		cover_link = i.find('img').get('src') #找到电影海报链接
		movie_info = Movie(name, rate, location, category, info_link, cover_link)
		list_of_movie.append(movie_info)
	return list_of_movie

def makeMoviesInCsv(category, location):
	"""
	该函数接收地区和类别的输入，并将该地区该类别9-10分的电影信息写入movie.csv
	"""
	list_of_movie = getMovies(category, location)
	with open('movies.csv', 'a', newline='') as csvfile:
		writer = csv.writer(csvfile)
		for i in list_of_movie:
			writer.writerow([i.name, i.rate, i.location, i.category, i.info_link, i.cover_link])

def sum_category(movies, category):
	"""
	该函数接收电影信息列表和类别输入，返回该类别的电影总数
	"""
	num_category = 0
	for i in movies:
		if i[3] == category:
			num_category += 1
	return num_category

def rank(movies, category, list_of_location):
	"""
	该函数接收电影信息列表、类别和地区列表输入，返回该类别电影数量前三的国家及其各自所占的百分比（保留两位小数）
	"""
	per_location = []
	num_category = sum_category(movies, category)
	for i in list_of_location:
		sum_i = 0
		for j in movies:
			if j[2] == i and j[3] == category:
				sum_i += 1
		per_location.append([i, round(sum_i / num_category * 100, 2)])
	rank_location = sorted(per_location, key = lambda s: s[1], reverse = True)
	return rank_location

def makeRankInTxt(movies, category, list_of_location):
	"""
	将该类别电影数量排名前三的地区信息输入至output.txt
	"""
	r = rank(movies, category, list_of_location)
	string = '豆瓣{}类9分以上电影数量前三的地区分别为{}、{}、{}，所占百分比分别为{}、{}、{}。\n'
	with open('output.txt', 'a') as f:
		f.write(string.format(category, r[0][0], r[1][0], r[2][0], r[0][1], r[1][1], r[2][1]))

list_of_location = ['大陆', '美国', '香港', '台湾', '日本', '韩国', '英国',  '法国', '德国', 
					'意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚',
					'爱尔兰', '瑞典', '巴西', '丹麦']
list_of_category = ['剧情', '爱情', '文艺']
for i in list_of_category:
	for j in list_of_location:
		makeMoviesInCsv(i, j) #调用makeMoviesInCsv函数，将剧情、爱情、文艺三个类别每个地区的9-10分电影的信息写入movie.csv

with open('movies.csv', 'r') as f:
	reader = csv.reader(f)
	movies = list(reader)
for i in list_of_category:
	makeRankInTxt(movies, i, list_of_location) #调用makeRankInTxt函数，将各个类别电影数量排名前三的电影信息写入output.txt

"""
由于豆瓣自身问题需说明的情况：
1、访问链接'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,美国,剧情'查询剧情类美国9-10分电影时，无法显示9-9.2分段的电影
2、访问链接'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,英国,剧情'查询剧情类英国9-10分电影时，内有一部8.3分的电影
3、极个别查询到的影片无评分
"""