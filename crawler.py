#-*- coding: utf-8 -*-
import sys
import socket
import requests
from lxml import html
import urlparse
import collections
import urllib2
from lxml import etree
from HTMLParser import HTMLParser
from time import sleep
from random import randint
from threading import Thread
from thread import *
import re

def data_clean(text):
	temp = ' '.join(text)
	temp = temp.replace('\n','')
	temp = temp.replace(',','')
	temp = temp.replace('\'','')
	temp = temp.replace('"','')
	temp = temp.replace('.','')
	temp = temp.replace(':','')
	temp = temp.replace('?','')
	temp = temp.replace('-',' ')
	temp = temp.replace('!','')
	temp = temp.replace('  ',' ')
	temp = temp.replace('   ',' ')
	temp = temp.replace('    ',' ')
	temp = re.sub('(\s+)(a|an|and|the|The)(\s+)'.decode('utf8'), '\1\3 '.decode('utf8'), temp)
	temp = re.sub('(\s+)(how|How|what|who|where|when|why)(\s+)'.decode('utf8'), '\1\3 '.decode('utf8'), temp)
	temp = re.sub('(\s+)(on|On|to|for|as|by|with|of|in|into|at)(\s+)'.decode('utf8'), '\1\3 '.decode('utf8'), temp)
	temp = re.sub('(\s+)(or|out|over|from|after|before)(\s+)'.decode('utf8'), '\1\3 '.decode('utf8'), temp)
	temp = re.sub('(\s+)(our|its|his|her|your)(\s+)'.decode('utf8'), '\1\3 '.decode('utf8'), temp)
	result = re.sub('(\s+)(I|you|be|is|are|was|were)(\s+)'.decode('utf8'), '\1\3 '.decode('utf8'), temp)

	return result

#CNN_URL_Queues
CNN_URL = 'http://edition.cnn.com/world'
CNN_urls_queue = collections.deque()
CNN_urls_queue.append(CNN_URL)
CNN_found_urls = set()
CNN_found_urls.add(CNN_URL)

def connCNN(conn):
	print "Start CNN"
	if len(CNN_urls_queue):
		try:
			url = CNN_urls_queue.popleft()
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			html = response.read()

			page = etree.HTML(html)
			#response = requests.get(url)
			#parsed_body = html.fromstring(response.content)

			# Prints the page title
			text = page.xpath("//h1[@class='pg-headline']/descendant::text()")
			text = data_clean(text)
			text2 = page.xpath("//span[@class='cd__headline-text']/descendant::text()")
			text2 = data_clean(text2)
			if text:
				print "Send CNN:"+text
				conn.send(text.encode('utf8'))
				#print text
			if text2:
				print "Send CNN2:"+text2
				conn.send(text2.encode('utf8'))
				#print text2
			# Find all links
			links = {urlparse.urljoin(response.url, url) for url in page.xpath('//a/@href') if urlparse.urljoin(response.url, url).startswith('http')}

			# Set difference to find new URLs
			for link in (links - CNN_found_urls):
				CNN_found_urls.add(link)
				CNN_urls_queue.append(link)
		except Exception, e:
			sys.stderr.write('CNN ERROR: %sn' % str(e))
	conn.close()

#BBC URL
BBC_URL = 'http://www.bbc.com/news/world'
BBC_urls_queue = collections.deque()
BBC_urls_queue.append(BBC_URL)
BBC_found_urls = set()
BBC_found_urls.add(BBC_URL)

def connBBC(conn):
	print "Start BBC"
	if len(BBC_urls_queue):
		try:
			url = BBC_urls_queue.popleft()
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			html = response.read()

			page = etree.HTML(html)
			#response = requests.get(url)
			#parsed_body = html.fromstring(response.content)

			# Prints the page title
			text = page.xpath("//h1[@class='story-body__h1']/descendant::text()")
			text = data_clean(text)
			text2 = page.xpath("//span[@class='title-link__title-text']/descendant::text()")
			text2 = data_clean(text2)
			if text:
				print "Send BBC:"+text
				conn.send(text.encode('utf8'))
				#print text
			if text2:
				print "Send BBC2:"+text2
				conn.send(text2.encode('utf8'))
				#print text2
			# Find all links
			links = {urlparse.urljoin(response.url, url) for url in page.xpath('//a/@href') if urlparse.urljoin(response.url, url).startswith('http')}

			# Set difference to find new URLs
			for link in (links - BBC_found_urls):
				BBC_found_urls.add(link)
				BBC_urls_queue.append(link)
		except Exception, e:
			sys.stderr.write('ERROR BBC: %sn' % str(e))
	conn.close()

#NYTIME URL
NY_URL = 'http://www.nytimes.com/pages/world/'
NY_urls_queue = collections.deque()
NY_urls_queue.append(NY_URL)
NY_found_urls = set()
NY_found_urls.add(NY_URL)

def connNYTIME(conn):
	print "Start NYTIME"
	if len(NY_urls_queue):
		try:
			url = NY_urls_queue.popleft()
			#request = urllib2.Request(url)
			response = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
			html = response.read()

			page = etree.HTML(html)
			#response = requests.get(url)
			#parsed_body = html.fromstring(response.content)

			# Prints the page title
			text = page.xpath("//h1[@class='headline']/descendant::text()")
			text = data_clean(text)
			text2 = page.xpath("//div[@class='story']/h3/descendant::text()")
			text2 = data_clean(text2)
			if text:
				print "Send TIME:"+text
				conn.send(text.encode('utf8'))
				#print text
			if text2:
				print "Send TIME2:"+text2
				conn.send(text2.encode('utf8'))
				#print tex2
			# Find all links
			links = {urlparse.urljoin(response.url, url) for url in page.xpath('//a/@href') if urlparse.urljoin(response.url, url).startswith('http')}
			# Set difference to find new URLs
			for link in (links - NY_found_urls):
				NY_found_urls.add(link)
				NY_urls_queue.append(link)
		except Exception, e:
			sys.stderr.write('ERROR NY: %sn' % str(e))
	conn.close()

"""def connWeb(conn):
	connCNN(conn)
	connBBC(conn)
	connNYTIME(conn)"""

def acceptCNN(s):
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	start_new_thread(connCNN,(conn,))

def acceptBBC(s):
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	start_new_thread(connBBC,(conn,))

def acceptNY(s):
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(connNYTIME,(conn,))		

if __name__ == "__main__":
	HOST = '192.168.16.138'
	PORT = 9999 # Arbitrary non-privileged port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket created'

	#Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print 'Socket bind complete'

	#Start listening on socket
	s.listen(10)
	print 'Socket now listening'

	while 1:
		thread1 = Thread(target = acceptCNN, args = (s,))
		thread2 = Thread(target = acceptBBC, args = (s,))
		thread3 = Thread(target = acceptNY, args = (s,))
		thread1.start()
		thread2.start()
		thread3.start()
		thread1.join()
		thread2.join()
		thread3.join()
		#start_new_thread(acceptCNN,(s,))
		#conn, addr = s.accept()
		#print 'Connected with ' + addr[0] + ':' + str(addr[1])
		#start_new_thread(acceptBBC,(s,))
		#start_new_thread(acceptNY,(s,))
		#start_new_thread(connBBC,(conn,))
		#start_new_thread(connNYTIME,(conn,))
		#sleep(randint(1,3)) # random delays for 1~5 seconds	

	s.close()
