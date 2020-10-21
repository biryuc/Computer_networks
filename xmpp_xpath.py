#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib.request
import time

from sleekxmpp import ClientXMPP

username = 'n.biryuchkov@xabber.org'
passwd = 'n.biryuchkov'
to = 'alexdevyatovskaya@jabber.uk'
client = ClientXMPP(username, passwd)
client.connect()
client.process()

while True:

        req = urllib.request.Request('http://weather.nsu.ru/weather.xml')
        response = urllib.request.urlopen(req)
        page = response.read()
        str_page = str(page)
        index1 = str_page.find('current')
        index2 = str_page.find('/current')
        data = str_page[index1+8:index2-1]
        print(data)
        client.send_message(to, 'Current temperature: ' + data + '°C')
        print(data)
        time.sleep(1)

client.disconnect()