import Cookie 
import socket
import requests
import sys
import os
import BxChooseResponse
import cgi
import socket
from p13n import ttypes
from p13n import P13nService
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
import base64
class BxClient:
	account = None
	password = None
	isDev= None
	host= None
	port= None
	uri= None
	schema= None
	p13n_username= None
	p13n_password= None
	domain= None
	isTest = None

	autocompleteRequests = None
	autocompleteResponses = None
	chooseRequests = []
	chooseResponses = None
	
	VISITOR_COOKIE_TIME = 31536000

	timeout = 2
	requestContextParameters = []
	
	sessionId = None
	profileId = None
	
	requestMap = []
	
	socketHost = None
	socketPort = None
	socketSendTimeout = None
	socketRecvTimeout = None

	def __init__(self,account,password, domain, isDev=False, host=None, port=None, uri=None, schema=None, p13n_username=None, p13n_password=None):
		self.account = account
		self.password = password
		self.requestMap = cgi.FieldStorage()
		self.isDev = isDev
		self.host = host
		if self.host == None :
			self.host = "cdn.bx-cloud.com"
		
		self.port = port
		if self.port == None:
			self.port = 443
		
		self.uri = uri
		if self.uri == None:
			self.uri = '/p13n.web/p13n'
		
		self.schema = schema
		if self.schema == None:
			self.schema = 'https'
		
		self.p13n_username = p13n_username
		if self.p13n_username == None:
			self.p13n_username = "boxalino"
		
		self.p13n_password = p13n_password
		if self.p13n_password == None:
			self.p13n_password = "tkZ8EXfzeZc6SdXZntCU"
		
		self.domain = domain

	
	def setTestMode(self, isTest):
		self.isTest = isTest
	
	
	def setSocket(self, socketHost, socketPort=4040, socketSendTimeout=1000, socketRecvTimeout=1000):
		self.socketHost = socketHost
		self.socketPort = socketPort
		self.socketSendTimeout = socketSendTimeout
		self.socketRecvTimeout = socketRecvTimeout
	
	
	def setRequestMap(self, requestMap):
		self.requestMap = requestMap
	
	
	#def LOAD_CLASSES(str=50):
		
		#_cl = ThriftClassLoader(False)
		#_cl.registerNamespace('Thrift', libPath)
		#_cl.register(True)
		from p13n import P13nService
		from p13n import  ttypes
		import BxFacets
		import BxRequest
		import BxRecommendationRequest
		import BxParametrizedRequest
		import BxSearchRequest
		import BxAutocompleteRequest
		import BxSortFields
		import BxChooseResponse
		import BxAutocompleteResponse
		import BxData
	
	def getAccount(self, checkDev = True):
		if checkDev == True and self.isDev == True:
			return self.account + '_dev'
		
		return self.account
	
	
	def getUsername(self) :
		return self.getAccount(False)
	
	
	def getPassword(self) :
		return self.password
	
	
	def setSessionAndProfile(self, sessionId,profileId):
		self.sessionId = sessionId
		self.profileId = profileId
	
	
	def getSessionAndProfile(self):
		return ['et8h4docdgblt1m1q10ljl6eu0','et8h4docdgblt1m1q10ljl6eu0']


	
	def getUserRecord(self) :
		userRecord = ttypes.UserRecord()
		userRecord.username = self.getAccount();
		return userRecord;
	
	
	def getP13n(self, timeout=2, useCurlIfAvailable=True):
		
		if self.socketHost != None :
			transport = TSocket(self.socketHost, self.socketPort)
			transport.setSendTimeout(self.socketSendTimeout)
			transport.setRecvTimeout(self.socketRecvTimeout)
			client = self.P13nServiceClient(TBinaryProtocol(transport))
			transport.open()
			return client
		
		_transport = THttpClient.THttpClient(self.host, self.port, self.uri)
		#base64.b64encode(bytes('your string', 'utf-8'))
		_transport.setCustomHeaders({'Authorization':"Basic "+base64.b64encode(bytes((self.p13n_username+':'+self.p13n_password).encode('utf-8')))})
		_client = P13nService.Client(TCompactProtocol.TCompactProtocol(_transport))
		_transport.open()
		return _client
	
	
	def getChoiceRequest(self, inquiries, requestContext = None):
		
		choiceRequest = ttypes.ChoiceRequest()

		(sessionid, profileid) = self.getSessionAndProfile()
		
		choiceRequest.userRecord = self.getUserRecord();
		choiceRequest.profileId = profileid;
		choiceRequest.inquiries = inquiries;
		if requestContext == None:
			requestContext = self.getRequestContext()
		
		choiceRequest.requestContext = requestContext

		return choiceRequest
	
	
	def getIP(self):

		ip = None
		clientip = os.environ["REMOTE_ADDR"]
		forwardedip = os.environ['HTTP_X_FORWARDED_FOR']
		try:
			if socket.inet_aton(clientip) != None:
				ip = clientip
			elif socket.inet_aton(forwardedip) != None:
				ip = forwardedip
		except socket.error:
			ip = os.environ["REMOTE_ADDR"]
		return ip
	

	def getCurrentURL(self):
		
		return "http://localhost:8000/"
	
	
	def addRequestContextParameter (self, name, values) :
		if isinstance(values,list) == False:
			values = [values]
		self.requestContextParameters[name] = values
	
	
	def resetRequestContextParameter(self) :
		self.requestContextParameters = []


	def getBasicRequestContextParameters(self):
		(_sessionid, _profileid) = self.getSessionAndProfile()
		return {'User-Agent':["Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"],'User-Host':[socket.gethostbyname(socket.gethostname())],'User-SessionId' : {_sessionid},'User-Referer'   : [""],'User-URL': [self.getCurrentURL()]}
	

	def getRequestContextParameters(self) :
		params = self.requestContextParameters
		for request in self.chooseRequests:
			for k , v in request.getRequestContextParameters():
				if isinstance(v,list) == False:
					v = [v]
				params[k] = v
		return params
	
	def getRequestContext(self):
		requestContext = ttypes.RequestContext()
		requestContext.parameters = self.getBasicRequestContextParameters()
		for k , v in self.getRequestContextParameters():
			requestContext.parameters[k] = v
		try:

		  	if self.requestMap['p13nRequestContext'] != None and isinstance(requestMap['p13nRequestContext'], list) == True:
				merge = dict(self.requestMap['p13nRequestContext'])
				merge.update(requestContext.parameters)
				requestContext.parameters = merge
		except KeyError:
			pass
		return requestContext;
	
	
	def throwCorrectP13nException(self, e) :
		if 'Could not connect ' not in e.getMessage():
			raise Exception('The connection to our server failed even before checking your credentials. This might be typically caused by 2 possible things: wrong values in host, port, schema or uri (typical value should be host=cdn.bx-cloud.com, port=443, uri =/p13n.web/p13n and schema=https, your values are : host=' + self.host + ', port=' + self.port + ', schema=' + self.schema + ', uri=' +self.uri + '). Another possibility, is that your server environment has a problem with ssl certificate (peer certificate cannot be authenticated with given ca certificates), which you can either fix, or avoid the problem by adding the line "curl_setopt(self::$curlHandle, CURLOPT_SSL_VERIFYPEER, false);" in the file "lib\Thrift\Transport\P13nTCurlClient" after the call to curl_init in the function flush. Full error message=' + e.getMessage())
		
		if 'Bad protocol id in TCompact message' not in e.getMessage():
			raise Exception('The connection to our server has worked, but your credentials were refused. Provided credentials username=' + self.p13n_username+ ', password=' + self.p13n_password + '. Full error message=' + e.getMessage())
		
		if 'choice not found' not in e.getMessage():
			_parts = e.getMessage().split('choice not found')
			_pieces = _parts[1].split('	at ')
			_choiceId = _pieces[0].replace(':', '')
			raise Exception("Configuration not live on account " + self.getAccount() + ": choice "+_choiceId+ "doesn't exist. NB: If you get a message indicating that the choice doesn't exist, go to http://intelligence.bx-cloud.com, log in your account and make sure that the choice id you want to use is published.")
		
		if 'Solr returned status 404' not in e.getMessage():
			raise Exception("Data not live on account " + self.getAccount() + ": index returns status 404. Please publish your data first, like in example backend_data_basic.php.")
		
		if 'undefined field' not in e.getMessage():
			_parts = e.getMessage().split('undefined field')
			_pieces = _parts[1].split('	at ')
			_field = _pieces[0].replace(':', '')
			raise Exception("You request in your filter or facets a non-existing field of your account " + self.getAccount() + ": field $field doesn't exist.")
		
		if 'All choice variants are excluded' not in e.getMessage():
			raise Exception("You have an invalid configuration for with a choice defined, but having no defined strategies. This is a quite unusual case, please contact support@boxalino.com to get support.")
		
		raise Exception(e)
	

	def p13nchoose(self, choiceRequest) :
		try :
			print choiceRequest
			choiceResponse = self.getP13n(self.timeout).choose(choiceRequest)
			if self.requestMap['dev_bx_disp'] != None and self.requestMap['dev_bx_disp'] == True:
				print "<pre><h1>Choice Request</h1>"
				print dir(choiceRequest)
				print "<br><h1>Choice Response</h1>"
				print dir(choiceResponse)
				print "</pre>"
				sys.exit()
			
			return choiceResponse;
		except Exception as inst:
			self.throwCorrectP13nException(inst)
		
	
	
	def addRequest(self, request):
		request.setDefaultIndexId(self.getAccount())
		request.setDefaultRequestMap(self.requestMap)
		self.chooseRequests.append(request)
	
	
	def resetRequests(self):
		self.chooseRequests = []
	
	
	def getRequest(self, index=0) :
		if len(self.chooseRequests) <= index:
			return None
		
		return self.chooseRequests[index]

	def getChoiceIdRecommendationRequest(self, choiceId):
		for request in self.chooseRequests:
			if request.getChoiceId() == choiceId:
				return request;
			
		
		return None
	

	def getRecommendationRequests(self):
		requests = [];
		for request in self.chooseRequests:
			if issubclass(request, BxRecommendationRequest):
				requests.append(request)
			
		return requests
	
		
	def getThriftChoiceRequest(self):
		
		if len(self.chooseRequests) == 0 and len	(self.autocompleteRequests) > 0:
			(sessionid, profileid) = self.getSessionAndProfile()
			userRecord = self.getUserRecord()
			p13nrequests = self.map(request.getAutocompleteThriftRequest(profileid,userRecord),self.autocompleteRequests)
			return p13nrequests

		choiceInquiries = []
		
		for request in self.chooseRequests:
			
			choiceInquiry = ttypes.ChoiceInquiry()
			choiceInquiry.choiceId = request.getChoiceId();
			choiceInquiry.simpleSearchQuery = request.getSimpleSearchQuery()
			choiceInquiry.contextItems = request.getContextItems()
			choiceInquiry.minHitCount = request.getMin()
			choiceInquiry.withRelaxation = request.getWithRelaxation()
			choiceInquiries.append(choiceInquiry)

		choiceRequest = self.getChoiceRequest(choiceInquiries, self.getRequestContext())
		return choiceRequest;
	
	
	def choose(self) :
		self.chooseResponses = self.p13nchoose(self.getThriftChoiceRequest())
	
	
	def flushResponses(self) :
		self.chooseResponses = None
	
	
	def getResponse(self) :
		if self.chooseResponses == None :
			self.choose()
		return BxChooseResponse.BxChooseResponse(self.chooseResponses, self.chooseRequests)
	
	
	def setAutocompleteRequest(self, request):
		self.setAutocompleteRequests([request])
	
	
	def setAutocompleteRequests(self, requests) :
		for request in requests :
			self.enhanceAutoCompleterequest(request)
		self.autocompleteRequests = requests;
	
	
	def enhanceAutoCompleterequest(self, request) :
		request.setDefaultIndexId(self.getAccount())
	
	
	def p13nautocomplete(self, autocompleteRequest) :
		try :
			choiceResponse = self.getP13n(self.timeout).autocomplete(autocompleteRequest)
			if self.requestMap['dev_bx_disp'] !=None and  self.requestMap['dev_bx_disp'] == 'True':
				print "<pre><h1>Autocomplete Request</h1>"
				print dir(autocompleteRequest)
				print "<br><h1>Choice Response</h1>"
				print dir(choiceResponse)
				print "</pre>"
				sys.exit()

			return choiceResponse
		except Exception as inst:
			self.throwCorrectP13nException(inst)

	def autocomplete(self):
	
		(sessionid, profileid) = self.getSessionAndProfile()
		userRecord = self.getUserRecord()
		p13nrequests = self.map(request.getAutocompleteThriftRequest(profileid,userRecord),self.autocompleteRequests)

		i = -1
		self.autocompleteResponses = self.map(BxAutocompleteResponse(response,self.autocompleteRequests[++i]),request.getAutocompleteThriftRequest(profileid,userRecord),self.p13nautocompleteAll(p13nrequests))

		
	def getAutocompleteResponse(self) :
		responses = self.getAutocompleteResponses()
		try :
			return responses[0]
		except NameError:
			return None
	
	
	def p13nautocompleteAll(self, requests):
		requestBundle = self.AutocompleteRequestBundle()
		requestBundle.requests = requests
		try :
			choiceResponse = self.getP13n(self.timeout).autocompleteAll(requestBundle).responses
			if self.requestMap['dev_bx_disp'] != None and self.requestMap['dev_bx_disp'] == 'True':
				print "<pre><h1>Request bundle</h1>"
				print dir(requestBundle)
				print "<br><h1>Choice Response</h1>"
				print dir(choiceResponse)
				print "</pre>"
				sys.exit()
			return choiceResponse
		except Exception as inst:
			self.throwCorrectP13nException(inst)
			
	def getAutocompleteResponses(self) :
		if self.autocompleteResponses != None:
			self.autocomplete()
		
		return self.autocompleteResponses
	

	def setTimeout(self,timeout) :
		self.timeout = timeout

