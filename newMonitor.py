# MIT License

# Copyright (c) 2017 elisha johnsunder

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bs4 import BeautifulSoup
import requests
import re
import tweepy
import os
import time
from random import randint
from time import gmtime, strftime

def bestBuy(url):
	headers = {'User-agent': 'Mozilla/5.0'}
	r  = requests.get(url,headers=headers)
	data = r.text
	soup = BeautifulSoup(data,"html.parser")

	# get status of product
	masterString = ""
	for item in soup.find_all("div",{"class": "cart-button"}):
		masterString += (str(item))

	soldout = re.compile('(add-to-cart-message=\"Sold Out\")')
	inStock = re.compile('(data-add-to-cart-message=\"Add to Cart\")')
	OOS = re.findall(soldout,masterString)
	IN_STOCK = re.findall(inStock,masterString)

	if (len(OOS)):
		return False
	else:
		return True

def otherSites(url):
	headers = {'User-agent': 'Mozilla/5.0'}
	r  = requests.get(url,headers=headers)
	data = r.text
	soup = BeautifulSoup(data,"html.parser")

	retail = soup.find_all("span",{"class": "a-color-price"})
	if(str(retail[0].text)) == "$59.99":
		return True
	return False


def sendTweet(link, site):
	# setup twitter
	C_KEY = ""
	C_SECRET = ""
	A_TOKEN = ""
	A_TOKEN_SECRET = ""
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
	api = tweepy.API(auth) 

	# send tweet
	tweet = "***** NES IN STOCK *****\nSite: "+site+"\n"
	tweet += link+"\n"
	tweet += strftime("%Y-%m-%d %H:%M:%S", gmtime())
	# print(tweet)
	api.update_status(tweet)


def main():
	# Bestbuy
	link_bestBuy = "http://www.bestbuy.com/site/olspage.jsp?skuId="
	sku = input("Enter SKU: ")
	# # NES OVERIDE
	# sku = "5389100"
	#xbox text case
	# sku = "5613745"
	link_bestBuy += sku+"&type=product"

	# amazon
	link_other = "http://a.co/2CJLATT"

	# tweet 5 times a min
	count = 0
	while count < 11:
		if (bestBuy(link_bestBuy)):
			sendTweet(link_bestBuy,"BestBuy")
		if (otherSites(link_other)):
			sendTweet(link_other,"Amazon")
		time.sleep(5)
		count += 1
main()
