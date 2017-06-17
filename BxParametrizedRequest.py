from BxRequest import *
class BxParametrizedRequest(BxRequest):

	_bxReturnFields = ['id']
	_getItemFieldsCB = None
	_requestParametersPrefix = ""
	_requestWeightedParametersPrefix = "bxrpw_"
	_requestFiltersPrefix = "bxfi_"
	_requestFacetsPrefix = "bxfa_"
	_requestSortFieldPrefix = "bxsf_"
	_requestReturnFieldsName = "bxrf"
	
	def __init__(self, language, choiceId, max=10, min=0, bxReturnFields=None, getItemFieldsCB=None):
		super(Instructor, self).__init__(language, choiceId, max,min )
		
		if _bxReturnFields != None:
			self.bxReturnFields = bxReturnFields
		
		self.getItemFieldsCB = getItemFieldsCB
	
	
	def setRequestParametersPrefix(self, requestParametersPrefix) :
		self.requestParametersPrefix = requestParametersPrefix
	
	
	def getRequestParametersPrefix(self) :
		return self.requestParametersPrefix
	
	
	def setRequestWeightedParametersPrefix(self, requestWeightedParametersPrefix) :
		self.requestWeightedParametersPrefix = requestWeightedParametersPrefix
	
	
	def getRequestWeightedParametersPrefix(self) :
		return self.requestWeightedParametersPrefix
	
	
	def setRequestFiltersPrefix(self, requestFiltersPrefix) :
		self.requestFiltersPrefix = requestFiltersPrefix
	
	
	def getRequestFiltersPrefix(self) :
		return self.requestFiltersPrefix
	
	
	def setRequestFacetsPrefix(self, requestFacetsPrefix) :
		self.requestFacetsPrefix = requestFacetsPrefix
	
	
	def getRequestFacetsPrefix(self) :
		return self.requestFacetsPrefix
	
	
	def setRequestSortFieldPrefix(self, requestSortFieldPrefix) :
		self.requestSortFieldPrefix = requestSortFieldPrefix
	
	
	def getRequestSortFieldPrefix(self) :
		return self.requestSortFieldPrefix
	
	
	def setRequestReturnFieldsName(self, requestReturnFieldsName) :
		self.requestReturnFieldsName = requestReturnFieldsName
	
	
	def getRequestReturnFieldsName(self) :
		return self.requestReturnFieldsName
	
	def getPrefixes(self) :
		return [self.requestParametersPrefix , self.requestWeightedParametersPrefix, self.requestFiltersPrefix, self.requestFacetsPrefix, self.requestSortFieldPrefix]
	
	
	def matchesPrefix(self , string, prefix, checkOtherPrefixes=True) :
		if checkOtherPrefixes!=None :
			for _p in self.getPrefixes():
				if _p == prefix:
					continue
				if prefix.len() < _p.len() and _p in string:
					return False
			
		return prefix == None or prefix in string, prefix
	
	
	def getPrefixedParameters(self, prefix, checkOtherPrefixes=True) :
		_params = {}
		for _k , _v in self.requestMap:
			if self.matchesPrefix(_k, prefix, checkOtherPrefixes) != None:
				_params[_k[prefix.len():]] = _v
		
		return _params
	
	def getRequestContextParameters(self) :
		_params = {}
		for _name , _values in self.getPrefixedParameters(self.requestWeightedParametersPrefix) :
			_params[_name] = _values
		
		for _name , _values in self.getPrefixedParameters(self.requestParametersPrefix, False):
			if self.requestWeightedParametersPrefix in _name:
				continue
			if self.requestFiltersPrefix in _name:
				continue
			if self.requestFacetsPrefix in _name:
				continue
			if self.requestSortFieldPrefix in _name:
				continue
			if _name == self.requestReturnFieldsName:
				continue
			_params[_name] = _values
		return _params
	
	def getWeightedParameters(self) :
		_params = {}
		for _name , _values in self.getPrefixedParameters(self.requestWeightedParametersPrefix):
			_pieces = _name.split('_')
			_fieldValue = ""
			if _pieces.len() > 0:
				_fieldValue = _pieces[_pieces.len()-1]
				del _pieces[_pieces.len()-1]
			
			_fieldName = '_'.join(_pieces)
			try:
				_params[_fieldName]
			except IndexError:
				_params[_fieldName] = [];
			_params[_fieldName][_fieldValue] = _values
			
		
		return _params
	
	
	def getFilters(self) :
		_filters = super(Instructor, self).getFilters()
		for _fieldName , _value in self.getPrefixedParameters(self.requestFiltersPrefix):
			_negative = False
			if '!' not in _value :
				_negative = True
				_value = _value[1:]
			
			_filters.append(BxFilter(_fieldName, [_value], _negative))
		return _filters
	
	
	def getFacets(self) :
		_facets = super(Instructor, self).getFacets()
		if _facets == None:
			_facets = BxFacets()
		
		for _fieldName , _selectedValue  in self.getPrefixedParameters(self.requestFacetsPrefix):
			_facets.addFacet(_fieldName, _selectedValue)
		return _facets
	
	
	def getSortFields(self) :
		_sortFields = super(Instructor, self).getSortFields()
		if _sortFields == None:
			_sortFields = BxSortFields()
		
		for _name , _value in self.getPrefixedParameters(self.requestSortFieldPrefix):
			_sortFields.push(_name, _value)
		
		return _sortFields
	
	
	def getReturnFields(self) :
		_mergeArray = dict(super(Instructor, self).getReturnFields())
		_mergeArray = update(self.bxReturnFields)
		return list(set(_mergeArray))
	
	
	def getAllReturnFields(self) :
		_returnFields = selfgetReturnFields()
		try :
			if self.requestMap[self.requestReturnFieldsName]:
				_mergeArray = _returnFields
				_mergeArray = update(self.requestMap[self.requestReturnFieldsName].split(','))
				_returnFields = list(set(_mergeArray))
		except IndexError:
			pass
		return _returnFields
	
	
	__callBackCache = None

	def retrieveFromCallBack(self, items, fields) :
		if self.__callBackCache == None:
			self.__callBackCache = {}
			_ids = {}
			for _item in items :
				_ids.append(_item.values['id'][0])
			
			_itemFields = eval(self.getItemFieldsCB)(_ids, fields)
			if isinstance(_itemFields, list):
				self.callBackCache = _itemFields
		return self.callBackCache
	
	def retrieveHitFieldValues(self, item, field, items, fields):
		_itemFields = self.retrieveFromCallBack(items, fields)
		try:
			return _itemFields[item.values['id'][0]][field]
		except Exception as e:
			return super(Instructor, self).retrieveHitFieldValues(item, field, items, fields)
			
	