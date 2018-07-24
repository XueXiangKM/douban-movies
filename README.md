# douban-movies

从豆瓣电影的网页中获取剧情、爱情、文艺三个类别，各个地区的高评分电影，收集他们的名称、评分、电影页面的链接和电影海报的链接，最后对收集的数据进行简单的统计。
该项目利用python进行编程，依次完成了下列任务

## 1：获取每个地区、每个类型页面的URL
从下面这个网址，按照分类和地区查看电影列表。

```
https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影
```
分解 URL 可以看到其中包含

-  `https://movie.douban.com/tag/#/`: 	豆瓣电影分类页面
-  `sort=S`: 按评分排序
-  `range=9,10`: 评分范围 9 ~ 10
-  `tags=电影`: 标签为电影

其中参数tags可以包含多个以逗号分隔的标签，分别选取类型和地区来进行进一步的筛选，例如选择类型为`剧情`，地区为`美国`, 那么 URL 为

```
https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国
```

实现函数构造对应类型和地区的URL地址

```
"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location)
	url = None
	return url
```
## 2: 获取电影页面 HTML

获得URL后，我们获取 URL 对应页面的 HTML

可以使用库 `requests` get 函数。

```
import requests
response = requests.get(url)
html = response.text
```

这样的做法对大多数豆瓣电影列表页面来说没什么问题。但有些列表需要多页显示，我们需要不断模拟点击**加载更多**按钮来显示这个列表上的全部电影。

因此，我们单独在expanddouban.py中通过gethtml函数实现了这个功能，为实现这个函数，需要安装 selenium 和 chromedriver，之后，在DoubanCrawler.py中调用该函数来获取URL对应页面的HTML
```
import expanddouban
html = expanddouban.getHtml(url)
```

## 3: 定义电影类

电影类包含以下成员变量

- 电影名称
- 电影评分
- 电影类型
- 电影地区
- 电影页面链接
- 电影海报图片链接

同时，实现了电影类的构造函数。

```
name = “肖申克的救赎”
rate = 9.6
location = "美国"
category = "剧情"
info_link = "https://movie.douban.com/subject/1292052/"
cover_link = “https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg”

m = Movie(name, rate, location, category, info_link, cover_link)
```

## 4: 获得豆瓣电影的信息

通过URL返回的HTML，我们可以获取网页中所有电影的名称，评分，海报图片链接和页面链接，同时我们在任务1构造URL时，也有类型和地区的信息，因此我们可以完整的构造每一个电影，并得到一个列表。

实现以下函数

```
"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category, location)
	return []
```

## 5: 构造电影信息数据表

从剧情、爱情、文艺三个电影类型，然后获取每个地区的电影信息后，我们可以获得一个包含三个类型、所有地区，评分超过9分的完整电影对象的列表。将列表输出到文件 `movies.csv`，格式如下:
```
肖申克的救赎,9.6,美国,剧情,https://movie.douban.com/subject/1292052/,https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg
霍伊特团队,9.0,香港,动作,https://movie.douban.com/subject/1307914/,https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p2329853674.jpg
....
```

## 6: 统计电影数据

统计每个电影类别中，数量排名前三的地区有哪些，分别占此类别电影总数的百分比为多少？

我们将结果输出文件 `output.txt`
