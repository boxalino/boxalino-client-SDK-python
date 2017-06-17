import Cookie, request, myrequire, socket, sys
import os
import BxChooseResponse
import cgi
class BxClient:
	__account = None
	__password = None
	__isDev= None
	__host= None
	__port= None
	__uri= None
	__schema= None
	__p13n_username= None
	__p13n_password= None
	__domain= None
	
	__isTest = None

	__autocompleteRequests = None
	__autocompleteResponses = None
	
	__chooseRequests = []
	__chooseResponses = None
	
	VISITOR_COOKIE_TIME = 31536000

	__timeout = 2
	__requestContextParameters = []
	
	__sessionId = None
	__profileId = None
	
	__requestMap = []
	
	__socketHost = None
	__socketPort = None
	__socketSendTimeout = None
	__socketRecvTimeout = None

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
	
	
	def LOAD_CLASSES(libPath):
		
		_cl = ThriftClassLoader(False)
		_cl.registerNamespace('Thrift', libPath)
		_cl.register(True)
		myrequire.require_once(libPath .join('/P13nService.py'))
		myrequire.require_once(libPath .join('/Types.py'))
		myrequire.require_once(libPath .join('/BxFacets.py'))
		myrequire.require_once(libPath .join('/BxRequest.py'))
		myrequire.require_once(libPath .join('/BxRecommendationRequest.py'))
		myrequire.require_once(libPath .join('/BxParametrizedRequest.py'))
		myrequire.require_once(libPath .join('/BxSearchRequest.py'))
		myrequire.require_once(libPath .join('/BxAutocompleteRequest.py'))
		myrequire.require_once(libPath .join('/BxSortFields.py'))
		myrequire.require_once(libPath .join('/BxChooseResponse.py'))
		myrequire.require_once(libPath .join('/BxAutocompleteResponse.py'))
		myrequire.require_once(libPath .join('/BxData.py'))
	
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

		return self.httpContext.getSessionAndProfile(null, null, this.domain)


	
	def getUserRecord(self) :
		_userRecord = UserRecord()
		_userRecord.username = self.getAccount();
		return _userRecord;
	
	
	def getP13n(self, timeout=2, useCurlIfAvailable=True):
		
		if self.socketHost != None :
			_transport = TSocket(self.socketHost, self.socketPort)
			_transport.setSendTimeout(self.socketSendTimeout)
			_transport.setRecvTimeout(self.socketRecvTimeout)
			_client = P13nServiceClient(TBinaryProtocol(_transport))
			_transport.open()
			return _client
		
		try:
			func = locals()[ curl_version ]
			if useCurlIfAvailable != None and callable(func):
				_transport = P13nTCurlClient(self.host, self.port, self.uri, self.schema)
		except:
				_transport = P13nTHttpClient(self.host, self.port, self.uri, self.schema)
			
		_transport.setAuthorization(self.p13n_username, self.p13n_password)
		_transport.setTimeoutSecs(timeout)
		_client = P13nServiceClient(TCompactProtocol(_transport))
		_transport.open()
		return _client
	
	
	def getChoiceRequest(inquiries, requestContext = None):
		
		_choiceRequest = ChoiceRequest()

		(_sessionid, _profileid) = self.getSessionAndProfile()
		
		_choiceRequest.userRecord = selfgetUserRecord();
		_choiceRequest.profileId = _profileid;
		_choiceRequest.inquiries = inquiries;
		if requestContext == None:
			requestContext = self.getRequestContext()
		
		_choiceRequest.requestContext = requestContext

		return _choiceRequest
	
	
	def getIP():

		_ip = None
		_clientip = os.environ["REMOTE_ADDR"]
		_forwardedip = os.environ['HTTP_X_FORWARDED_FOR']
		try:
			if socket.inet_aton(_clientip) != None:
				_ip = _clientip
			elif socket.inet_aton(_forwardedip) != None:
				_ip = _forwardedip
		except socket.error:
			_ip = os.environ["REMOTE_ADDR"]
		return _ip
	

	def getCurrentURL():
		
		return os.environ['REQUEST_URI'];
	
	
	def addRequestContextParameter (self, name, values) :
		if isinstance(values,list) == False:
			values = [values]
		self.requestContextParameters[name] = values
	
	
	def resetRequestContextParameter(self) :
		self.requestContextParameters = []


	def getBasicRequestContextParameters(self):
		(_sessionid, _profileid) = self.getSessionAndProfile()
		return {'User-Agent':[request.headers.get('User-Agent')],'User-Host':[self.getIP()],'User-SessionId' : array(_sessionid),'User-Referer'   : [request.META.get('HTTP_REFERER')],'User-URL': [self.getCurrentURL()]}
	

	def getRequestContextParameters(self) :
		_params = self.requestContextParameters
		for _request in self.chooseRequests():
			for _k , _v in _request.getRequestContextParameters():
				if isinstance(_v,list) == False:
					_v = [_v]
				_params[_k] = _v
		return _params
	
	def getRequestContext(self):
		_requestContext = RequestContext()
		_requestContext.parameters = self.getBasicRequestContextParameters()
		for _k , _v in self.getRequestContextParameters():
			_requestContext.parameters[_k] = _v
		try:
		  if self.requestMap['p13nRequestContext'] != None and isinstance(requestMap['p13nRequestContext'], list) == True:
			_merge = dict(self.requestMap['p13nRequestContext'])
			_merge.update(_requestContext.parameters)
			_requestContext.parameters = _merge
		except NameError:
			pass
		return _requestContext;
	
	
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
			_choiceResponse = self.getP13n(self._timeout).choose(choiceRequest)
			if self.requestMap['dev_bx_disp'] != None and self.requestMap['dev_bx_disp'] == True:
				print "<pre><h1>Choice Request</h1>"
				print dir(choiceRequest)
				print "<br><h1>Choice Response</h1>"
				print dir(_choiceResponse)
				print "</pre>"
				sys.exit()
			
			return _choiceResponse;
		except Exception as inst:
			self.throwCorrectP13nException(inst)
		
	
	
	def addRequest(self, request):
		request.setDefaultIndexId(self.getAccount())
		request.setDefaultRequestMap(self.requestMap)
		self.chooseRequests.append(request)
	
	
	def resetRequests(self):
		self.chooseRequests = []
	
	
	def getRequest(self, index=0) :
		if self.chooseRequests.len() <= index:
			return None
		
		return self.chooseRequests[index]

	def getChoiceIdRecommendationRequest(self, choiceId):
		for _request in self.chooseRequests:
			if _request.getChoiceId() == choiceId:
				return _request;
			
		
		return None
	

	def getRecommendationRequests(self):
		_requests = [];
		for _request in self.chooseRequests:
			if issubclass(request, BxRecommendationRequest):
				_requests.append(_request)
			
		return _requests
	
		
	def getThriftChoiceRequest(self):
		
		if self.chooseRequests.len() == 0 and self.autocompleteRequests.len() > 0:
			(_sessionid, _profileid) = self.getSessionAndProfile()
			_userRecord = self.getUserRecord()
			_p13nrequests = self.map(request.getAutocompleteThriftRequest(_profileid,_userRecord),self.autocompleteRequests)
			return _p13nrequests
		
		
		_choiceInquiries = []
		
		for _request in chooseRequests:
			
			_choiceInquiry = ChoiceInquiry()
			_choiceInquiry.choiceId = _request.getChoiceId();
			if self.isTest == True :
				_choiceInquiry.choiceId += "_debugtest"
			
			elif self.isDev != None and self.isTest == None:
				_choiceInquiry.choiceId += "_debugtest"
			
			_choiceInquiry.simpleSearchQuery = request.getSimpleSearchQuery(self.getAccount())
			_choiceInquiry.contextItems = request.getContextItems()
			_choiceInquiry.minHitCount = request.getMin()
			_choiceInquiry.withRelaxation = request.getWithRelaxation()
			
			_choiceInquiries.append(_choiceInquiry)
		

		_choiceRequest = self.getChoiceRequest(_choiceInquiries, self.getRequestContext())
		return _choiceRequest;
	
	
	def choose(self) :
		self.chooseResponses = self.p13nchoose(self.getThriftChoiceRequest())
	
	
	def flushResponses(self) :
		self.chooseResponses = None
	
	
	def getResponse(self) :
		if self.chooseResponses!=None :
			self.choose()
		return BxChooseResponse(self.chooseResponses, self.chooseRequests)
	
	
	def setAutocompleteRequest(self, request):
		self.setAutocompleteRequests([request])
	
	
	def setAutocompleteRequests(self, requests) :
		for request in requests :
			self.enhanceAutoCompleterequest(request)
		self.autocompleteRequests = requests;
	
	
	def enhanceAutoCompleterequest(request) :
		request.setDefaultIndexId(self.getAccount())
	
	
	def p13nautocomplete(self, autocompleteRequest) :
		try :
			_choiceResponse = self.getP13n(self._timeout).autocomplete(autocompleteRequest)
			if self.requestMap['dev_bx_disp'] !=None and  self.requestMap['dev_bx_disp'] == 'True':
				print "<pre><h1>Autocomplete Request</h1>"
				print dir(autocompleteRequest)
				print "<br><h1>Choice Response</h1>"
				print dir(_choiceResponse)
				print "</pre>"
				sys.exit()

			return _choiceResponse
		except Exception as inst:
			self.throwCorrectP13nException(inst)

	def autocomplete(self):
	
		(_sessionid, _profileid) = self.getSessionAndProfile()
		_userRecord = self.getUserRecord()
		_p13nrequests = self.map(request.getAutocompleteThriftRequest(_profileid,_userRecord),self.autocompleteRequests)

		_i = -1
		self.autocompleteResponses = self.map(BxAutocompleteResponse(_response,self.autocompleteRequests[++_i]),request.getAutocompleteThriftRequest(_profileid,_userRecord),self.p13nautocompleteAll(_p13nrequests))

		
	def getAutocompleteResponse(self) :
		_responses = self.getAutocompleteResponses(self)
		try :
			return _responses[0]
		except IndexError:
			return None
	
	
	def p13nautocompleteAll(self, requests):
		_requestBundle = AutocompleteRequestBundle()
		_requestBundle.requests = requests
		try :
			_choiceResponse = self.getP13n(self._timeout).autocompleteAll(_requestBundle).responses
			if self.requestMap['dev_bx_disp'] != None and self.requestMap['dev_bx_disp'] == 'True':
				print "<pre><h1>Request bundle</h1>"
				print dir(_requestBundle)
				print "<br><h1>Choice Response</h1>"
				print dir(_choiceResponse)
				print "</pre>"
				sys.exit()
			return _choiceResponse
		except Exception as inst:
			self.throwCorrectP13nException(inst)
			
	def getAutocompleteResponses(self) :
		if self.autocompleteResponses !=-None:
			self.autocomplete()
		
		return self.autocompleteResponses
	

	def setTimeout(timeout) :
		self._timeout = timeout

