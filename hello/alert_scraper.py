#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 02:04:22 2021

@author: rufus
"""

import requests,bs4,re,time,sys,smtplib

# Create/open a csv file to store data
# file = open('~/Documents/Python for Regular Use/BitcoinAlerts.csv','a')
# file.write('Date,Time,Price\n')

# Date and Time
nowDate = time.strftime('%d/%m/%y' , time.localtime())
nowTime = time.strftime('%H.%M' , time.localtime())

# Go to Webpage
webpage = requests.get('https://www.coindesk.com/price/bitcoin')

# Raise exception if there is an error
if webpage.status_code != requests.codes.ok:
    raise Exception("Error while downloading webpage")

# Copy price text from html
parser = bs4.BeautifulSoup(webpage.text,'html.parser')
elemsPrice = parser.select('#export-chart-element > div > section > div.coin-info-list.price-list > div:nth-child(1) > div.data-definition > div')

# Extract the price
string1 = str(elemsPrice).replace(',','')  # Replace commas in price
NumRegex = re.compile(r'\d+.\d+')
num = NumRegex.findall(string1)
print('The price of Bitcoin on {} at {} is ${}'.format(nowDate , nowTime, num[0]))

# Copy percentage change text from html
elemsChange = parser.select('#export-chart-element > div > section > div.coin-info-list.price-list > div:nth-child(2) > div.data-definition > div > span > span.percent-value-text')

# Extract the percent change
string2 = str(elemsChange)
PercentRegex = re.compile(r'((-)*\d+.\d+)')
percent24 = PercentRegex.findall(string2)
print('The 24hr percent-change of Bitcoin price on {} at {} is {}%'.format(nowDate , nowTime, percent24[0][0]))

# Adding Data to csv file
file = open('/home/rufus/Documents/Python for Regular Use/BitcoinAlerts.csv','a')
file.write('{},{},{}\n'.format(nowDate , nowTime, num[0]))
file.close()

# Sending email Alerts

# Checking if password is provided
if len(sys.argv) > 1:
    password = ' '.join(sys.argv[1:])
else:
    raise Exception("Please provide password")

# Preliminary Setup and check
conn = smtplib.SMTP('smtp.gmail.com',587)
ehlocheck = conn.ehlo()
if ehlocheck[0] != 250:
    raise Exception('Something Wrong with connecting to Gmail')     
starttlscheck = conn.starttls()
if starttlscheck[0] != 220:
    raise Exception('Something Wrong with connecting to Gmail')

# Sending and Receiving Email Addresses 
send_address = 'aakashbiswal@gmail.com'
receive_address = 'aakashbiswal@gmail.com'

# Entering Password
logincheck = conn.login( send_address , password )
if logincheck[0] != 235:
    raise Exception('Password Incorrect')
    
# Send Mail
checksend = conn.sendmail( send_address, receive_address, 'Subject: Bitcon Alert\n\nDear Subscriber\nThe price of Bitcoin at {} is ${}.\n\nBest\nAkash'.format(nowTime,num[0]))
if len(checksend) != 0:
    raise Exception('Unable to send mail')
    
conn.quit()
                                                

    


