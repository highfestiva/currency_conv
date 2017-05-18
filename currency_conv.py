#!/usr/bin/env python3

import requests
import time
import urllib.request
from zipfile import ZipFile


cur2eur = {}
csvname  = 'eurofxref.csv'
filename = 'data/eurofxref.zip'
ecb_url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip'
updated = 0
refresh_threshold = 24*60*60


def load():
	try:
		r = requests.get(ecb_url, proxies=urllib.request.getproxies())
		if r.status_code == 200:
			with open(filename, 'wb') as f:
				f.write(r.content)
				global updated
				updated = time.time()
	except Exception as e:
		print(e)
		pass	# Better luck next time.

	with ZipFile(filename, 'r') as z:
		csv = z.read(csvname).decode()
	lines = csv.strip().splitlines()
	currencies = [w.strip() for w in lines[0].split(',')[1:] if w.strip()]
	rates = [float(w.strip()) for w in lines[1].split(',')[1:] if w.strip()]
	for c,r in zip(currencies,rates):
		cur2eur[c] = r


def convert(amount, from_currency, to_currency):
	if not cur2eur or time.time()-updated > refresh_threshold:
		load()
	eur = amount
	if from_currency != 'EUR':
		eur = amount / cur2eur[from_currency]
	res = eur
	if to_currency != 'EUR':
		res = eur * cur2eur[to_currency]
	return res
