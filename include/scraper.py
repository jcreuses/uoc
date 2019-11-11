import csv
import time
from bs4 import BeautifulSoup
import urllib2
import re
import unicodedata
import urllib




class NewsScraper():


	def __init__(self):
		self.url = "https://elpais.com"
		self.data=[]
		self.filename = "dataset.csv"

	def __download_htm(self, url):

		response = urllib.urlopen(url)
		html = response.read()

		return(html)

	def scrape(self):

		start_time = time.time()

		html = self.__download_htm(self.url)

		news_links =self.__get_news_links(html)

		self.n=0
		for i in range(len(news_links)):

			html_new = self.__download_htm(news_links[i])
			self.data.append(self.__news__scrape__(html_new))
			self.n+=1

		end_time = time.time()

		print ("\nelapsed time: " + str(round(((end_time - start_time)), 0)) + " seconds")
		self.data2csv(self.filename)
		print(' I have written the file')

	def __news__scrape__(self, html_new):


		bs_new = BeautifulSoup(html_new, 'html.parser')
		##Author##
		for value in bs_new.findAll(attrs={'class':'autor-nombre' }):
			for link in value.findAll('a', attrs={'href': re.compile(self.url)}):
				scrached_author = link.text
				scrached_author = self.strip_accents(scrached_author)

		##Title##
		title = bs_new.find(attrs={'itemprop':'headline'}).text
		scrached_title = self.strip_accents(title)

		##Location##
		loca = bs_new.find(attrs={'itemprop': 'contentLocation'})
		try:
			location =self.strip_accents(loca.text)
			location= location[1:-1]
		except:
			location = None

		###Fecha ##
		fecha = bs_new.find(attrs={'title': 'Ver todas las noticias de esta fecha'}).text
		date = str(fecha).rstrip()[2:-8];

		###Categoria###
		cat = bs_new.find('a',attrs={'class': 'enlace'}).text
		categoria = self.strip_accents(cat).rstrip()[1:];



		scrached_line = [location,scrached_title, scrached_author, self.coments_url_ls[self.n][0], date, categoria]

		return scrached_line

	def strip_accents(self, text):

		text = text.encode('utf-8')

		try:
			text = unicode(text, 'utf-8')
		except NameError:  # unicode is a default on python 3
			pass

		text = unicodedata.normalize('NFD', text) \
			.encode('ascii', 'ignore') \
			.decode("utf-8")

		return str(text)

	def __get_news_links(self, html):

		bs = BeautifulSoup(html, 'html.parser')

		news_links = []

		fr_search = 'class'
		sc_search = 'articulo-titulo'
		self.coments_url_ls = []


		for links in bs.findAll( attrs={fr_search : sc_search}):

			for link in links.findAll('a', attrs={'href': re.compile(self.url)}):
				theLink = link.get('href')
				news_links.append(theLink)

		for url in news_links:

			coments = bs.find(attrs={'href':url+'#comentarios'})
			try:
				coments = self.strip_accents(coments.text)

			except:
				pass

			url = self.strip_accents(url)
			self.coments_url_ls.append([coments, url])



		return news_links

	def data2csv(self, filename):

		file = open("../csv/" + filename, "w+")
		print(file)
		print(self.data)

		for i in range(len(self.data)):
			for j in range(len(self.data[i])):

				file.write(str(self.data[i][j]) + ";");
			file.write("\n");

		print(filename)