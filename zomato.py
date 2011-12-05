import httplib, urllib, urllib2

class Zomato:
	def __init__(self, key, base_url=''):
		self.key = key

		if base_url != '':
			self.base_url = base_url
		else:
			self.base_url = 'https://api.zomato.com/v1/'

	def request(self, call, method='GET', params={}, headers={}):
		url = '%s%s' % (self.base_url, call)

		if method == 'GET':
			url = url + '?' + urllib.urlencode(params)
			req = urllib2.Request(url)
		else:
			req = urllib2.Request(url, urllib.urlencode(params))

		req.add_header('X-Zomato-API-Key', self.key)
		for header, value in headers.iteritems():
			req.add_header(header, value)

		r = urllib2.urlopen(req)
		return r.read()
