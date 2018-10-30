import requests
from bs4 import BeautifulSoup

def GetFeaturedArticleDate(articleName):
	articleName = articleName.split('.')[0]
	FeaturedDate = ''
	months = {
	'January': '01',
	'February': '02',
	'March': '03',
	'April': '04',
	'May' : '05',
	'June': '06',
	'July': '07',
	'August': '08',
	'September': '09',
	'October': '10',
	'November': '11',
	'December': '12',
	}

	url = 'https://en.wikipedia.org/wiki/Talk:' + articleName
	headers = {
		'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
	}

	r = requests.get(url, headers=headers)

	if r.status_code == 200:
		html = r.text
		soup = BeautifulSoup(html, 'lxml')

		temp = ''
		for link in soup.find_all('tr', attrs=False):
			if len(link) == 3:
				if 'Featured' in link.get_text() and 'Promoted' in link.get_text():
					temp = link.get_text()
					break

		if temp == '':
			for link in soup.find_all('tr', attrs=False):
				if len(link) == 3:
					if 'Featured' in link.get_text() and 'Kept' in link.get_text():
						temp = link.get_text()
						break
		
		c = 0
		for i in temp:
			if i.isupper() and c!=0:
				temp = temp[:c]
				break
			c += 1

		temp = temp.split(' ')
		if len(temp[1][:-1]) < 2:
			FeaturedDate += temp[-1] + months[temp[0]] + '0' + temp[1][:-1]	
		else:
			FeaturedDate += temp[-1] + months[temp[0]] + temp[1][:-1]
		return int(FeaturedDate)

	else:
		print('Something went wrong!', articleName)

print(GetFeaturedArticleDate('Woolly mammoth')) #yyyymmdd
