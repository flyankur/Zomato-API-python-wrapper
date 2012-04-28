import httplib, urllib, urllib2, json

class Zomato:
  '''
  Constructor for the Zomato class.

  Parameters:
    key                    - Zomato API Key.
                             Get it from http://www.zomato.com/api/key
    base_url (optional)    - base URL to be used for making API calls.
                             Defaults to https://api.zomato.com/v1/
  '''
  def __init__(self, key, base_url='https://api.zomato.com/v1/'):
    self.key = key
    self.base_url = base_url

  '''
  Function to make API call.

  Parameters:
    call                  - API call to be made
    method (optional)     - method to be used for making the HTTP request.
                            Defaults to GET.
    params (optional)     - parameters to be sent with the request
    headers  (optional)   - extra headers to be sent with the request

  Returns:
    Response to the call. If the call requested response in XML, then the
    response is returned as it is as a string. If the call requested
    response in JSON, then the response is parsed into a dictionary and 
    the dictionary is returned.

  Example:
    To get a List of Cuisines, you will make the following call:
      https://api.zomato.com/v1/cuisines.json
      Parameter to be sent is city_id with value (say) 1
      Method for making the HTTP request is GET.

    See documentation on Zomato.com to get List of Cuisines:
      http://www.zomato.com/api/documentation#Get-list-of-cuisines

    In the above call,
      https://api.zomato.com/v1/ is the base URL,
      cuisines.json is the call parameter,
      city_id is a parameter with the value 1.

    For the above API call, we will use the request() in the following
    way:

      z = Zomato()
      z.request('cuisines.json', params={'city_id': 1})

    We don't have to send any extra headers for this call. The default
    method used for making the HTTP request is GET so we
    don't have to set that as well.
  '''
  def request(self, call, method='GET', params={}, headers={}):
    url = '%s%s%p' % (self.normal_url, call)

    if method == 'GET':
      url = url + '?' + urllib.urlencode(params)
      request = urllib2.Request(url)
    else:
      request = urllib2.Request(url, urllib.urlencode(params))

    request.add_header('X-Zomato-API-Key', self.key)
    for header, value in headers.iteritems():
      request.add_header(header, value)

    response = urllib2.urlopen(request)
    self.response = response.read()

    return self.parse(call)

  '''
  Parses the response.

  Parameters:
    call              - (string) call parameter passed to the request method.

  Returns:
    XML response string if the call requested XML data. Dictionary if the call
    requested JSON data. The JSON response is parsed into a dictionary and the
    dictionary object is returned.
  '''
  def parse(self, call):
    method = call.split('.')
    method = method[1]

    data = self.response

    if method == 'json':
      data = self.json_parse()

    return data

  '''
  Parses JSON response into a dictionary.

  Returns:
    Dictionary object with the JSON response parsed into it.
  '''
  def json_parse(self):
    json_data = json.loads(self.response)

    return json_data
