import BxSortFields
class BxRequest:
 
	_language = None 
	_groupBy = None 
	_choiceId = None 
	_min = None 
	_max = None 
	_withRelaxation = None 
	 
	_indexId = None 
	_requestMap = None 
	_returnFields = None
	_offset = 0 
	_queryText = "" 
	_bxFacets = None 
	_bxSortFields = None 
	_bxFilters = None
	_orFilters = False 
	 
	def __init__(self, language, choiceId, max=10, min=0) :
		if choiceId == '': 
			raise Exception('BxRequest created with None choiceId') 
		 
		self._language = language
		self._choiceId = choiceId
		self._min = min
		self._max = max
		if self._max == 0:
			self._max = 1
		 
		self._withRelaxation = choiceId == 'search'
	 
	 
	def getWithRelaxation(self) : 
		return self._withRelaxation
	 
	 
	def setWithRelaxation(self, withRelaxation) : 
		self._withRelaxation = withRelaxation
	 
	 
	def getReturnFields(self) : 
		return self._returnFields
	 
	 
	def setReturnFields(self, returnFields) : 
		self._returnFields = returnFields
	 
	 
	def getOffset(self) : 
		return self._offset
	 
	 
	def setOffset(self, offset) : 
		self._offset = offset
	 
	 
	def getQuerytext(self) : 
		return self._queryText
	 
	 
	def setQuerytext(self, queryText) : 
		self._queryText = queryText
	 
	 
	def getFacets(self) :
		return self._bxFacets
	 
	 
	def setFacets(self, bxFacets) : 
		self._bxFacets = bxFacets
	 
	 
	def getSortFields(self) : 
		return self._bxSortFields
	 
	 
	def setSortFields(self, bxSortFields) : 
		self._bxSortFields = bxSortFields
	 
	 
	def getFilters(self) : 
		_filters = self._bxFilters
		if BxRequest.getFacets(self) != None:
			for _filter in self.getFacets().getFilters() :
				_filters.append( _filter )
		 
		return self._bxFilters
	 
	 
	def setFilters(self, bxFilters) : 
		self._bxFilters = bxFilters
	 
	 
	def addFilter(self , bxFilter) : 
		self.bxFilters[bxFilter.getFieldName()] = bxFilter 
	 
	 
	def getOrFilters(self) : 
		return self.orFilters 
	 
	 
	def setOrFilters(self, orFilters) : 
		self.orFilters = orFilters 
	 
	 
	def addSortField(self, field, reverse =False) : 
		if self.bxSortFields == None: 
			self.bxSortFields = BxSortFields() 
		 
		self.bxSortFields.push(field, reverse) 
	 
	 
	def getChoiceId(self) : 
		return self.choiceId 
	 
	 
	def setChoiceId(self, choiceId) : 
		self.choiceId = choiceId 
	 
	 
	def getMax(self) : 
		return self.max 
	 
	 
	def setMax(self, max) : 
		self.max = max 
	 
 
	def getMin(self) : 
		return self.min 
	 
	 
	def setMin(min) : 
		self.min = min 
	 
 
	def getIndexId(self) :
		return self._indexId
	 
	 
	def setIndexId(self, indexId) : 
		self._indexId = indexId
		for _k, _contextItem in self.__contextItems :
			if _contextItem._indexId == None :
				self.__contextItems[_k]._indexId = _indexId
			 
		 
	 
	 
	def setDefaultIndexId(self, indexId) : 
		if self._indexId == None :
			self.setIndexId(indexId) 
		 
	 
	 
	def setDefaultRequestMap(self, requestMap) : 
		if self._requestMap == None :
			self._requestMap = requestMap
		 
	 
 
	def getLanguage(self) : 
		return self.language 
	 
	 
	def setLanguage(self, language) : 
		self.language = language 
	 
 
	def getGroupBy(self): 
		return self.groupBy 
	 
 
	def setGroupBy(self, groupBy): 
		self.groupBy = groupBy 
	 
 
	def getSimpleSearchQuery(self) : 
		 
		_searchQuery = SimpleSearchQuery() 
		_searchQuery._indexId = self.getIndexId()
		_searchQuery.language = self.getLanguage() 
		_searchQuery.returnFields = self.getReturnFields() 
		_searchQuery.offset = self.getOffset() 
		_searchQuery.hitCount = self.getMax() 
		_searchQuery.queryText = self.getQueryText() 
		_searchQuery.groupBy = self.groupBy 
		if len(self.getFilters()) > 0 :
			_searchQuery.filters = {} 
			for _filter in self.getFilters() : 
				_searchQuery.filters.append( _filter.getThriftFilter() )
			 
		 
		_searchQuery.orFilters = self.getOrFilters() 
		if self.getFacets() != None : 
			_searchQuery.facetRequests = self.getFacets().getThriftFacets() 
		 
		if self.getSortFields() != None : 
			_searchQuery.sortFields = self.getSortFields().getThriftSortFields() 
		return _searchQuery 
	 
	 
	__contextItems = {} 
	def setProductContext(self, fieldName, contextItemId, role = 'mainProduct') : 
		_contextItem = ContextItem() 
		_contextItem._indexId = self.getIndexId()
		_contextItem.fieldName = fieldName 
		_contextItem.__contextItemId = contextItemId
		_contextItem.role = role 
		self.__contextItems.append( _contextItem )
	 
	def usort(_a, _b):
		if _a['price'] > _b['price'] : 
			return -1 
		elif b['price'] > a['price'] :
			return 1 
		 
		return 0 


	def setBasketProductWithPrices(self, fieldName, basketContent, role = 'mainProduct', subRole = 'mainProduct') : 
		if basketContent != False and len(basketContent) != None :
			 
			# Sort basket content by price 

			sorted(basketContent, usort) 
 
			_basketItem = basketContent.pop(0) 
 
			_contextItem = ContextItem() 
			_contextItem._indexId = self.getIndexId()
			_contextItem.fieldName = fieldName 
			_contextItem.contextItemId = _basketItem['id'] 
			_contextItem.role = role 
 
			self.__contextItems.append( _contextItem )
 
			for _basketItem in _basketContent: 
				_contextItem = ContextItem() 
				_contextItem._indexId = self.getIndexId()
				_contextItem.fieldName = fieldName 
				_contextItem.contextItemId = _basketItem['id'] 
				_contextItem.role = subRole 
				self.__contextItems.append( _contextItem )
			 
	 
	 
	def getContextItems(self) : 
		return self.__contextItems
	 
	 
	def getRequestContextParameters(self) : 
		return [] 
	 
	 
	def retrieveHitFieldValues(self, item,field, items,fields) : 
		return []
 
 