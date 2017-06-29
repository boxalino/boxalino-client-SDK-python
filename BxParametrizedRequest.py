from BxRequest import *
import BxFacets
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
		BxRequest.__init__(self,language, choiceId, max,min )
		
		if bxReturnFields != None:
			self._bxReturnFields = bxReturnFields
		
		self._getItemFieldsCB = getItemFieldsCB
	
	
	def setRequestParametersPrefix(self, requestParametersPrefix) :
		self._requestParametersPrefix = requestParametersPrefix
	
	
	def getRequestParametersPrefix(self) :
		return self._requestParametersPrefix
	
	
	def setRequestWeightedParametersPrefix(self, requestWeightedParametersPrefix) :
		self._requestWeightedParametersPrefix = requestWeightedParametersPrefix
	
	
	def getRequestWeightedParametersPrefix(self) :
		return self._requestWeightedParametersPrefix
	
	
	def setRequestFiltersPrefix(self, requestFiltersPrefix) :
		self._requestFiltersPrefix = requestFiltersPrefix
	
	
	def getRequestFiltersPrefix(self) :
		return self._requestFiltersPrefix
	
	
	def setRequestFacetsPrefix(self, requestFacetsPrefix) :
		self._requestFacetsPrefix = requestFacetsPrefix
	
	
	def getRequestFacetsPrefix(self) :
		return self._requestFacetsPrefix
	
	
	def setRequestSortFieldPrefix(self, requestSortFieldPrefix) :
		self._requestSortFieldPrefix = requestSortFieldPrefix
	
	
	def getRequestSortFieldPrefix(self) :
		return self._requestSortFieldPrefix
	
	
	def setRequestReturnFieldsName(self, requestReturnFieldsName) :
		self._requestReturnFieldsName = requestReturnFieldsName
	
	
	def getRequestReturnFieldsName(self) :
		return self._requestReturnFieldsName
	
	def getPrefixes(self) :
		return [self._requestParametersPrefix , self._requestWeightedParametersPrefix, self._requestFiltersPrefix, self._requestFacetsPrefix, self._requestSortFieldPrefix]
	
	
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
		for _k , _v in self._requestMap:
			if self.matchesPrefix(_k, prefix, checkOtherPrefixes) != None:
				_params[_k[prefix.len():]] = _v
		
		return _params
	
	def getRequestContextParameters(self) :
		_params = {}
		for _name , _values in self.getPrefixedParameters(self.requestWeightedParametersPrefix) :
			_params[_name] = _values
		
		for _name , _values in self.getPrefixedParameters(self.requestParametersPrefix, False):
			if self._requestWeightedParametersPrefix in _name:
				continue
			if self._requestFiltersPrefix in _name:
				continue
			if self._requestFacetsPrefix in _name:
				continue
			if self._requestSortFieldPrefix in _name:
				continue
			if _name == self._requestReturnFieldsName:
				continue
			_params[_name] = _values
		return _params
	
	def getWeightedParameters(self) :
		_params = {}
		for _name , _values in self.getPrefixedParameters(self._requestWeightedParametersPrefix):
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
		_filters = BxRequest.getFilters(self)
		_tempVar = self.getPrefixedParameters(self._requestFiltersPrefix)
		if _tempVar:
			for _fieldName , _value in _tempVar:
				_negative = False
				if '!' not in _value :
					_negative = True
					_value = _value[1:]

				_filters.append(BxFilter(_fieldName, [_value], _negative))
		return _filters
	
	
	def getFacets(self) :
		_facets = BxRequest.getFacets(self)
		if _facets == None:
			_facets = BxFacets.BxFacets()
		
		for _fieldName , _selectedValue  in self.getPrefixedParameters(self._requestFacetsPrefix):
			_facets.addFacet(_fieldName, _selectedValue)
		return _facets
	
	
	def getSortFields(self) :
		_sortFields = BxRequest.getSortFields()
		if _sortFields == None:
			_sortFields = BxSortFields.BxSortFields()
		
		for _name , _value in self.getPrefixedParameters(self._requestSortFieldPrefix):
			_sortFields.push(_name, _value)
		
		return _sortFields
	
	
	def getReturnFields(self) :
		_mergeArray = dict(BxRequest.getReturnFields())
		_mergeArray = update(self._bxReturnFields)
		return list(set(_mergeArray))
	
	
	def getAllReturnFields(self) :
		_returnFields = self.getReturnFields()
		try :
			if self._requestMap[self._requestReturnFieldsName]:
				_mergeArray = _returnFields
				_mergeArray = update(self._requestMap[self._requestReturnFieldsName].split(','))
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
			
			_itemFields = eval(self._getItemFieldsCB)(_ids, fields)
			if isinstance(_itemFields, list):
				self.callBackCache = _itemFields
		return self.callBackCache
	
	def retrieveHitFieldValues(self, item, field, items, fields):
		_itemFields = self.retrieveFromCallBack(items, fields)
		try:
			return _itemFields[item.values['id'][0]][field]
		except Exception as e:
			return BxRequest.retrieveHitFieldValues(item, field, items, fields)
			
	