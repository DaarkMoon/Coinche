#!usrbinpython
import urllib,urllib2

url = 'http://127.0.0.1:8080/coinche'
parameters = {'Mot' : 'Gimp'}

data = urllib.urlencode(parameters)    # Use urllib to encode the parameters
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)    # This request is sent in HTTP POST
page = response.read(200000)