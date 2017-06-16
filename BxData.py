import csv 
import os
import json
import pycurl 
import tempfile
import types
import StringIO
import urllib2
import xml.etree.cElementTree as ET
from phpserialize import serialize, unserialize
class BxData:

	URL_VERIFY_CREDENTIALS = '/frontend/dbmind/en/dbmind/api/credentials/verify'
	URL_XML = '/frontend/dbmind/en/dbmind/api/data/source/update'
    URL_PUBLISH_CONFIGURATION_CHANGES = '/frontend/dbmind/en/dbmind/api/configuration/publish/owner'
	URL_ZIP = '/frontend/dbmind/en/dbmind/api/data/push'
	URL_EXECUTE_TASK = '/frontend/dbmind/en/dbmind/files/task/execute'
	
	_bxClient = None
	_languages = None
	_isDev = None
	_isDelta = None
	
	_sources = []
	
	_host = 'http://di1.bx-cloud.com'
	
	_owner = 'bx_client_data_api'

	def __init__(self, bxClient, languages = [], isDev=False, isDelta=False):
		self.bxClient = bxClient
		self.languages = languages
		self.isDev = isDev
		self.isDelta = isDelta
	
	def setLanguages(self, languages) :
		self.languages = languages
	
	
	def getLanguages() :
		return self.languages
	
	
	def addMainCSVItemFile(self, filePath, itemIdColumn, encoding = 'UTF-8', delimiter = ',', enclosure = "\"", escape = "\\\\", lineSeparator = "\\n", sourceId = 'item_vals', container = 'products', validate=True) :
		_sourceKey = self.addCSVItemFile(self, filePath, itemIdColumn, encoding, delimiter, enclosure, escape, lineSeparator, sourceId, container, validate)
		self.addSourceIdField(self,_sourceKey, itemIdColumn, None, validate) 
		self.addSourceStringField(self,_sourceKey, "bx_item_id", itemIdColumn, None, validate) 
		return _sourceKey
	
	
	def addMainCSVCustomerFile(self, filePath, itemIdColumn, encoding = 'UTF-8', delimiter = ',', enclosure = "\&", escape = "\\\\", lineSeparator = "\\n", sourceId = 'customers', container = 'customers', validate=True) :
		_sourceKey = self.addCSVItemFile(self, filePath, itemIdColumn, encoding, delimiter, enclosure, escape, lineSeparator, sourceId, container, validate)
		self.addSourceIdField(self,_sourceKey, itemIdColumn, None, validate) 
		self.addSourceStringField(self,_sourceKey, "bx_customer_id", itemIdColumn, None, validate) 
		return _sourceKey
	
	
	def addCSVItemFile(self, filePath, itemIdColumn, encoding = 'UTF-8', delimiter = ',', enclosure = "\&", escape = "\\\\", lineSeparator = "\\n", sourceId = None, container = 'products', validate=True) :
		_params = {'itemIdColumn': itemIdColumn, 'encoding':encoding, 'delimiter':delimiter, 'enclosure':enclosure, 'escape':escape, 'lineSeparator':lineSeparator}
		if sourceId == None :
			sourceId = self.getFileNameFromPath(self, filePath, True)
		
		return self.addSourceFile(self, filePath, sourceId, container, 'item_data_file', 'CSV', _params, validate)
	
	
	def addCSVCustomerFile(self, filePath, itemIdColumn, encoding = 'UTF-8', delimiter = ',', enclosure = "\&", escape = "\\\\", lineSeparator = "\\n", sourceId = None, container = 'customers', validate=True) :
		_params = {'itemIdColumn':itemIdColumn, 'encoding':encoding, 'delimiter':delimiter, 'enclosure':enclosure, 'escape':escape, 'lineSeparator':lineSeparator}
		if sourceId == None :
			sourceId = self.getFileNameFromPath(self, filePath, True)
		
		return self.addSourceFile(self, filePath, sourceId, container, 'item_data_file', 'CSV', _params, validate)
	
	
	def addCategoryFile(self, filePath, categoryIdColumn, parentIdColumn, categoryLabelColumns, encoding = 'UTF-8', delimiter = ',', enclosure = "\&", escape = "\\\\", lineSeparator = "\\n", sourceId = 'resource_categories', container = 'products', validate=True) :
		_params = {'referenceIdColumn':categoryIdColumn, 'parentIdColumn':parentIdColumn, 'labelColumns':categoryLabelColumns, 'encoding':encoding, 'delimiter':delimiter, 'enclosure':enclosure, 'escape':escape, 'lineSeparator':lineSeparator}
		return self.addSourceFile(self, filePath, sourceId,container, 'hierarchical', 'CSV', _params, validate)
	
	
	def addResourceFile(self, filePath, categoryIdColumn, labelColumns, encoding = 'UTF-8', delimiter = ',', enclosure = "\&", escape = "\\\\", lineSeparator = "\\n", sourceId = None, container = 'products', validate=True) :
		_params = {'referenceIdColumn':categoryIdColumn, 'labelColumns':labelColumns, 'encoding':encoding, 'delimiter':delimiter, 'enclosure':enclosure, 'escape':escape, 'lineSeparator':lineSeparator}
		if sourceId == None :
			sourceId = 'resource_' + self.getFileNameFromPath(self, filePath, True)
		
		return self.addSourceFile(self, filePath, sourceId, container, 'resource', 'CSV', _params, validate)
	
	
	
	
	def setCSVTransactionFile(self, filePath, orderIdColumn, productIdColumn, customerIdColumn, orderDateIdColumn, totalOrderValueColumn, productListPriceColumn, productDiscountedPriceColumn, productIdField='bx_item_id', customerIdField='bx_customer_id', productsContainer = 'products', customersContainer = 'customers', format = 'CSV', encoding = 'UTF-8', delimiter = ',', enclosure = '"', escape = "\\\\", lineSeparator = "\\n",container = 'transactions', sourceId = 'transactions', validate=True) :
		
		_params = {'encoding':encoding, 'delimiter':delimiter, 'enclosure':enclosure, 'escape':escape, 'lineSeparator':lineSeparator}
		
		_params['file'] = self.getFileNameFromPath(self, filePath)
		_params['orderIdColumn'] = orderIdColumn
		_params['productIdColumn'] = productIdColumn
		_params['product_property_id'] = productIdField
		_params['customerIdColumn'] = customerIdColumn
		_params['customer_property_id'] = customerIdField
		_params['productListPriceColumn'] = productListPriceColumn
		_params['productDiscountedPriceColumn'] = productDiscountedPriceColumn
		_params['totalOrderValueColumn'] = totalOrderValueColumn
		_params['orderReceptionDateColumn'] = orderDateIdColumn
		
		return self.addSourceFile(self, filePath, sourceId, container, 'transactions', format, _params, validate)
	
	
	def addSourceFile(self, filePath, sourceId, container, type, format='CSV', params={}, validate=True) :
		if self.getLanguages().len() == 0 :
			raise Exception('trying to add a source before having declared the languages with method setLanguages')
		
		try :
			if self.sources[container] != None :
			
		except IndexError:
				self.sources[container] = {}

		_params['filePath'] = filePath
		_params['format'] = format
		_params['type'] = type
		self..sources[container][sourceId] = _params
		if validate == True :
			self..validateSource(self, container, sourceId)
		
		self.sourceIdContainers[sourceId] = container
		return self.encodesourceKey(self, container,sourceId)
	
	
	def decodeSourceKey(self, sourceKey) :
		_explodeArray =sourceKey.split('-')
		return _explodeArray
	
	
	def encodesourceKey(self, container, sourceId) :
		return container+'-'+sourceId
	
	
	def getSourceCSVRow(self, container, sourceId, row=0, maxRow = 2) :
		
		try :
			self.sources[container][sourceId]['rows'] 
		except IndexError:
			_handle = fopen(self.sources[container][sourceId]['filePath'])
			if  _handle != False :
				_count = 1
				self.sources[container][sourceId]['rows'] = {}
				_data = csv.reader(_handle, delimiter=',', quotechar='')
				while _data !== False :
					self.sources[container][sourceId]['rows'][] = _data
					if _count++>=maxRow :
						break
					
				_handle.close()
		
		if self.sources[container][sourceId]['rows'][row] != None :
			return self.sources[container][sourceId]['rows'][row]
		return None
	
	
	def validateSource(self, container, sourceId) :
		_source = self.sources[container][sourceId]
		if _source['format'] == 'CSV' :
			if _source['itemIdColumn']!= None :
				self.validateColumnExistance(self, container, sourceId, source['itemIdColumn'])
			
	
	def validateColumnExistance(self, container, sourceId, col) :
		_row = self.getSourceCSVRow(self, container, sourceId, 0)
		if _row !== None and col not in _row :
			raise Exception("the source '$sourceId' in the container '$container' declares an column '$col' which is not present in the header row of the provided CSV file: " + ','.join(_row))
		
	
	
	def addSourceIdField(self, sourceKey, col, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, 'bx_id', "id", False, col, referenceSourceKey, validate)
	
	
	def addSourceTitleField(self, sourceKey, colMap, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, "bx_title", "title", True, colMap, referenceSourceKey, validate)
	
	
	def addSourceDescriptionField(self, sourceKey, colMap, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, "bx_description", "body", True, colMap, referenceSourceKey, validate)
	
	
	def addSourceListPriceField(self, sourceKey, col, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, "bx_listprice", "price", False, col, referenceSourceKey, validate)
	
	
	def addSourceDiscountedPriceField(self, sourceKey, col, referenceSourceKey=None, validate=True) :
		self.addSourceField(self,sourceKey, "bx_discountedprice", "discounted", False, col, referenceSourceKey, validate)
	
	
	def addSourceLocalizedTextField(self, sourceKey, fieldName, colMap, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, fieldName, "text", True, colMap, referenceSourceKey, validate)
	
	
	def addSourceStringField(self, sourceKey, fieldName, col, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, fieldName, "string", False, col, referenceSourceKey, validate)
	
	
	def addSourceNumberField(self, sourceKey, fieldName, col, referenceSourceKey=None, validate=True) :
		self.addSourceField(self, sourceKey, fieldName, "number", False, col, referenceSourceKey, validate)
	
	
	def setCategoryField(self, sourceKey, col, referenceSourceKey="resource_categories", validate=True) :
		if referenceSourceKey == "resource_categories" :
			(_container, _sourceId) = self.decodeSourceKey(self,sourceKey)
			referenceSourceKey = self.encodesourceKey(self,container, referenceSourceKey)
		
		self.addSourceField(self, sourceKey, "category", "hierarchical", False, col, referenceSourceKey, validate)
	
	
	def addSourceField(self, sourceKey, fieldName, type, localized, colMap, referenceSourceKey=None, validate=True) :
		(_container, _sourceId) = self.decodeSourceKey(self, sourceKey)
		try :
			if self.sources[_container][_sourceId]['fields']!= None :
				self.sources[_container][_sourceId]['fields'] = {}
		except IndexError:
			self.sources[_container][_sourceId]['fields'] = {}

		self.sources[_container][_sourceId]['fields'][fieldName] = {'type':type, 'localized':localized, 'map':colMap, 'referenceSourceKey':referenceSourceKey}
		if self.sources[_container][_sourceId]['format'] == 'CSV' :
			if localized and referenceSourceKey == None) :
				if isinstance(colMap,list)==False :
					raise Exception(fieldName+': invalid column field name for a localized field (expect an array with a column name for each language array(lang:colName)): ' + serialize(colMap))
				
				for _lang in self.getLanguages() :
					try:
						if colMap[_lang] != None :

					except :
						raise Exception(fieldName+': no language column provided for language '+lang+' in provided column map): ' + serialize(colMap))
					
					if isinstance(colMap[_lang], str)== False :
						raise Exception(fieldName+': invalid column field name for a non-localized field (expect a string): ' + serialize(colMap))
					
					if validate == True :
						self.validateColumnExistance(self, container, sourceId, colMap[_lang])
					
				
			else:
				if isinstance($colMap,str)==False :
					raise Exception(fieldName+' invalid column field name for a non-localized field (expect a string): ' + serialize(colMap))
				
				if validate== True :
					self.validateColumnExistance(self, container, sourceId, colMap)
				
	
	def setFieldIsMultiValued(self, sourceKey, fieldName, multiValued = True) :
		self.addFieldParameter(self, sourceKey, fieldName, 'multiValued', multiValued ? 'True' : 'False')
	

	def addSourceCustomerGuestProperty(self, sourceKey, parameterValue) :
		self.addSourceParameter(self, sourceKey, "guest_property_id", parameterValue)
	

	def addSourceParameter(self, sourceKey, parameterName, parameterValue) :
		(_container, _sourceId) = self.decodeSourceKey(self, sourceKey)
		try:
			if self.sources[_container][_sourceId] != None:
		
		except :
			raise Exception("trying to add a source parameter on sourceId '$sourceId', container "+_container+" while this source doesn't exist")
		
		self.sources[_container][_sourceId][parameterName] = parameterValue
	

	def addFieldParameter(self, sourceKey, fieldName, parameterName, parameterValue) :
		(_container, _sourceId) = self.decodeSourceKey(self, sourceKey)
		try:
			if self.sources[_container][_sourceId]['fields'][fieldName] != None:

		except IndexError:
			raise ("trying to add a field parameter on sourceId "+_sourceId+", container "+_container+", fieldName "+_fieldName+" while this field doesn't exist")
		
		try:
			if self.sources[_container][_sourceId]['fields'][fieldName]['fieldParameters'] != None:

		except IndexError:
			self.sources[_container][_sourceId]['fields'][fieldName]['fieldParameters'] = {}
		
		self.sources[_container][_sourceId]['fields'][fieldName]['fieldParameters'][parameterName] = parameterValue
	
	
	_ftpSources = {}
	def setFtpSource(self, sourceKey, host="di1.bx-cloud.com", port=21, user=None, password=None, remoteDir = '/sources/production', protocol=0, ttype=0, logontype=1,
				timezoneoffset=0, pasvMode='MODE_DEFAULT', maximumMultipeConnections=0, encodingType='Auto', bypassProxy=0, syncBrowsing=0) :
					
		if user==None:
			$user = self.bxClient.getAccount(False)
		
		
		if password==None:
			$password = self.bxClient.getPassword()
		
		
		_params = array()
		_params['Host'] = host
		_params['Port'] = port
		_params['User'] = user
		_params['Pass'] = password
		_params['Protocol'] = protocol
		_params['Type'] = ttype
		_params['Logontype'] = logontype
		_params['TimezoneOffset'] = timezoneoffset
		_params['PasvMode'] = pasvMode
		_params['MaximumMultipleConnections'] = maximumMultipeConnections
		_params['EncodingType'] = encodingType
		_params['BypassProxy'] = bypassProxy
		_params['Name'] = user + " at " + $host
		_params['RemoteDir'] = remoteDir
		_params['SyncBrowsing'] = syncBrowsing
		(_container, _sourceId) = self.decodeSourceKey(self, sourceKey)
		self.ftpSources[_sourceId] = _params
	
	
	def getXML(self) :
		
		root = ET.Element("root")
		
		languages = ET.SubElement(root, "languages")
		for _lang in self.getLanguages(): 
			ET.SubElement(language, "language", id=_lang)

		containers = ET.SubElement(root, "containers")
        for _containerName , _containerSources in self.sources():
			
			container = ET.SubElement(containers, "container", id=_containerName, type=_containerName)
			
			sources = ET.SubElement(container , 'sources')
			properties = ET.SubElement(container, 'properties')
        
			for _sourceId , _sourceValues in _containerSources ():
				
				try:
					if _sourceValues['additional_item_source'] != None :
						source = ET.SubElement(sources , 'source' , id=_sourceId, type=_sourceValues['type'] , additional_item_source=_sourceValues['additional_item_source'])
					
				except IndexError:
					source = ET.SubElement(sources , 'source' , id=_sourceId, type=_sourceValues['type'])				
					
				
				_sourceValues['file'] = self.getFileNameFromPath(_sourceValues['filePath'])
				
				_parameters = []
				_parameters.append({'file':False, 'format':'CSV', 'encoding':'UTF-8', 'delimiter':',', 'enclosure':'"', 'escape':'\\\\', 'lineSeparator':"\\n" })
				
				if _sourceValues['type'] == 'item_data_file':
					_parameters['itemIdColumn'] = False				
					
				if _sourceValues['type'] == 'hierarchical':
					_parameters['referenceIdColumn'] = False
					_parameters['parentIdColumn'] = False
					_parameters['labelColumns'] = False
					
					
				if _sourceValues['type'] == 'resource':
					_parameters['referenceIdColumn'] = False
					_parameters['itemIdColumn'] = False
					_parameters['labelColumns'] = False
					_sourceValues['itemIdColumn'] = _sourceValues['referenceIdColumn']
					
					
				if _sourceValues['type'] == 'transactions':
					_parameters = _sourceValues
					del _parameters['filePath']
					del _parameters['type']
					del _parameters['product_property_id']
					del _parameters['customer_property_id']
					
				
				
				for _parameter , _defaultValue in _parameters():
					try:
						_value = _sourceValues[_parameter]
					except IndexError:
						_value = _defaultValue
						
					if _value == False :
						raise Exception("source parameter "+_parameter+" required but not defined in source id "+_sourceId+" for container "+_containerName)
					
					param = ET.SubElement(source , _parameter)
					if isinstance(_value, list) ==True:
						for _language , _languageColumn in _value():
							ET.SubElement(param, "language", name=_language, value=_languageColumn)
						
					else :
						ET.SubElement(source , _parameter).set('value', _value)
					
					
					if _sourceValues['type'] == 'transactions':
						if _parameter == 'productIdColumn':
							ET.SubElement(source , _parameter).set('product_property_id',_sourceValues['product_property_id']);
							
							
						if _parameter == 'customerIdColumn':
							ET.SubElement(source , _parameter).set('customer_property_id', _sourceValues['customer_property_id']);
							try:
								ET.SubElement(source , _parameter).set('guest_property_id', _sourceValues['guest_property_id']);
							except :
						
				if self.ftpSources[_sourceId]!=None :
					
					ET.SubElement(source , 'location').set('type', 'ftp');
					
					ftp = ET.SubElement(source , 'ftp').set('name', 'ftp');
					
					for _ftpPn , _ftpPv in self.ftpSources[_sourceId]:
						ftp._ftpPn = _ftpPv
					
				
				if _sourceValues['fields']!=None :
					for _fieldId , _fieldValues in _sourceValues['fields'] :
						
						_property = ET.SubElement(properties, "property", id=_fieldId, type=_fieldValues['type'])
						
						transform = ET.SubElement(_property, "transform")
						logic = ET.SubElement(transform, "logic", source=_sourceId)

						try:
							
							_referenceSourceKey = _fieldValues['referenceSourceKey']
							_logicType = 'reference'
						except IndexError:
							_referenceSourceKey = None
							_logicType =  'direct'  


						if _logicType == 'direct' :
							try:
								for _parameterName , _parameterValue in _fieldValues['fieldParameters'] :
									if _parameterName == 'pc_tables':
										_logicType = 'advanced'
							except IndexError:
						ET.SubElement(transform, "logic").set('type',_logicType)
						
						if isinstance(_fieldValues['map'], list) :
							for _lang in self.getLanguages() :
								_field = ET.SubElement(logic, 'field', column=_fieldValues['map'][_lang], language=_lang)
								
						else :
							_field = ET.SubElement(logic, 'field', column=_fieldValues['map'])
							
						
						_params =  ET.SubElement(_property, 'params')
						
						if _referenceSourceKey!= None :
							referenceSource = ET.SubElement(_params, 'referenceSource')
							(_referenceContainer, _referenceSourceId) = self..decodeSourceKey(_referenceSourceKey)
							ET.SubElement(_params, 'referenceSource').set('value', _referenceSourceId)
						
						try:
							for _parameterName , _parameterValue in _fieldValues['fieldParameters'] :
								fieldParameter = ET.SubElement(_params, 'fieldParameter', name=_parameterName,value=_parameterValue)
							
						except IndexError:
		tree = ET.ElementTree(root)
		return tree.write("filename.xml")
		

    def callAPI(self, fields, url, temporaryFilePath=None):
        
        s = pycurl.Curl()

		
        s.setopt(s.URL, url)
        s.setopt(s.TIMEOUT, 60)
        s.setopt(s.POST, 1)
        s.setopt(s.ENCODING, '')
        s.setopt(s.RETURNTRANSFER, 1)
        s.setopt(s.POSTFIELDS, fields)
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)

        c.perform()
		responseBody = b.getvalue()
		if responseBody == False:
			if "couldn't open file" in s.errstr() :
				if temporaryFilePath !== None :
					raise Exception('There seems to be a problem with the folder BxData uses to temporarily store a zip file with all your files before sending it. As you are currently provided a path, this is most likely the problem. Please make sure it is a valid path, or leave it to None (default value), then BxData will use sys_get_temp_dir() + "/bxclient" which typically works fine.')
				else :
					raise Exception('There seems to be a problem with the folder BxData uses to temporarily store a zip file with all your files before sending it. This means that the default path BxData uses sys_get_temp_dir() + "/bxclient" is not supported and you need to path a working path to the pushData function.')
				
			
			raise Exception('Curl error: ' + s.errstr())
		

        s.close()
        if 'Internal Server Error' in responseBody :
            raise Exception(self.getError(responseBody))
        
        return self.checkResponseBody(responseBody, url)
    
	
	def getError(responseBody) :
		return responseBody
	
	
	def checkResponseBody(responseBody, url) :
		if responseBody == None :
			raise Exception("API response of call to $url is empty string, this is an error!")
		
		value = json.loads(responseBody, True)
		if value.len() != 1 or value['token']!=None :
			if value['changes']!=None :
				raise Exception(responseBody)
			
		return value
	
	
	def pushDataSpecifications(self, ignoreDeltaException=False) :
		
		if ignoreDeltaException != None and self.isDelta!= None :
			raise Exception("You should not push specifications when you are pushing a delta file. Only do it when you are preparing full files. Set method parameter ignoreDeltaException to True to ignore this exception and publish anyway.")
		
		
		fields = {'username' : self.bxClient.getUsername(),'password' : self.bxClient.getPassword(),'account' : self.bxClient.getAccount(False),'owner' : self.owner,'xml' : self.getXML()}

        url = self.host + self.URL_XML
		return self.callAPI(fields, url)
	
	
	def checkChanges(self) :
		self.publishOwnerChanges(False)
	
	
	def publishChanges(self) :
		self.publishOwnerChanges(True)
	
	
	def publishOwnerChanges(self, publish=True) :
		if self.isDev!= None :
			publish = False
		
		fields = {'username' : self.bxClient.getUsername(),'password' : self.bxClient.getPassword(),'account' : self.bxClient.getAccount(False),'owner' : self.owner,'publish' : ($publish ? 'True' : 'False')}

        url = self.host + self.URL_PUBLISH_CONFIGURATION_CHANGES
		return self.callAPI(fields, url)
	
	
	def verifyCredentials(self) :
		$fields = {'username' : self.bxClient.getUsername(),'password' : self.bxClient.getPassword(),'account' : self.bxClient.getAccount(False),'owner' : self.owner}

        url = self.host + self.URL_VERIFY_CREDENTIALS
		return self.callAPI(fields, url)
	
	
	def getFileNameFromPath(filePath, withoutExtension=False) :
		parts = filePath.split('/')
		file = parts[parts.len()-1]
		if withoutExtension== True :
			parts = file.split('.')
			return parts[0]
		
		return file
	
	
	def getFiles(self) :
		files = {}
		for _container , _containerSources in self.sources:
			for _sourceId , _sourceValues in _containerSources  :
				if self.ftpSources[_sourceId]!= None :
					continue
				
				if _sourceValues['file']== None :
					_sourceValues['file'] = self.getFileNameFromPath(_sourceValues['filePath'])
				files[_sourceValues['file']] = _sourceValues['filePath']
		return files
	
	
    def createZip( self , temporaryFilePath=None, name='bxdata.zip'):
		if temporaryFilePath == None :
			temporaryFilePath = tempfile.gettempdir() + '/bxclient'
		
		
		if temporaryFilePath != "" and os.path.exists(temporaryFilePath) != True :
            os.mkdir($temporaryFilePath)
        
		
		zipFilePath = temporaryFilePath + '/' + name
		
        if os.path.exists(zipFilePath) == True :
            os.unlink(zipFilePath)
        
		
		files = self.getFiles()
		zzip = zipfile.ZipFile(zipFilePath, 'w') 
        if zzip == True :

            for _f , _filePath in files :
                if zzip.write($filePath) != True:
                    raise Exception('Synchronization failure: Failed to add file "' +_filePath+ '" to the zip "' +name+ '". Please try again.')
                
            if zzip.writestr('properties.xml', self.getXML()) != True :
                raise Exception('Synchronization failure: Failed to add xml string to the zip "' +name + '". Please try again.')
            

            if zzip.close() != True :
                raise Exception('Synchronization failure: Failed to close the zip "' +name + '". Please try again.')
            
        else :
            raise Exception('Synchronization failure: Failed to open the zip "' +name + '" for writing. Please check the permissions and try again.')
        
		return zipFilePath
    
	
	def pushData(self, temporaryFilePath=None) :
		
		zipFile = self.createZip(temporaryFilePath)
		
		fields = {'username' : self.bxClient.getUsername(),'password' : self.bxClient.getPassword(),'account' : self.bxClient.getAccount(False),'owner' : self.owner,'dev' : self.isDev ? 'True' : 'False','delta' : self.isDelta ? 'True' : 'False','data' : self.getCurlFile($zipFile, "application/zip")}

        url = self.host + self.URL_ZIP
		return self.callAPI(self, fields, url,temporaryFilePath)
	

    def getCurlFile(self, filename, ttype):
        result = False
        result = (eval("type("+className+")") == types.ClassType)
        try :
            if result== True :
                return CURLFile(filename, ttype)
        except :
        	
        return filename+'type='+ttype
    
	
	def getTaskExecuteUrl(self, taskName) :
		return self.host + self.URL_EXECUTE_TASK + '?iframeAccount=' + self.bxClient.getAccount() + '&task_process=' + taskName
	
	
	def publishChoices(self, isTest = False, taskName="generate_optimization") :
		
		if self.isDev== True :
			taskName += '_dev'
		
		if isTest== True :
			taskName += '_test'
		
        url = self.getTaskExecuteUrl(taskName)
		file_get_contents(url)
	
	
	def prepareCorpusIndex(self, taskName="corpus") :
        url = self.getTaskExecuteUrl(taskName)
		file_get_contents(url)
	
	
	def prepareAutocompleteIndex(self, fields, taskName="autocomplete") :
        url = self.getTaskExecuteUrl(taskName)
		file_get_contents(url)
	

	def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = urllib2.urlopen(filename).read()
        if (offset > 0):
            ret = ret[offset:]
        if (maxlen > 0):
            ret = ret[:maxlen]
        return ret
    else:
        fp = open(filename,'rb')
        try:
            if (offset > 0):
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret
        finally:
            fp.close( )

