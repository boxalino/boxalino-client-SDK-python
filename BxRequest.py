import BxSortFields
class BxRequest:
 
	language = None 
	groupBy = None 
	choiceId = None 
	min = None
	max = None
	withRelaxation = None 
	 
	indexId = None 
	requestMap = None 
	returnFields = None
	offset = 0 
	queryText = "" 
	bxFacets = None 
	bxSortFields = None 
	bxFilters = None
	orFilters = False 
	 
	def __init__(self, language, choiceId, max=10, min=0) :
		if choiceId == '': 
			raise Exception('BxRequest created with None choiceId') 
		 
		self.language = language
		self.choiceId = choiceId
		self._min = min
		self.max = max
		if self.max == 0:
			self.max = 1
		if choiceId == 'search':
			self.withRelaxation = 1


	 
	 
	def getWithRelaxation(self) : 
		return self.withRelaxation
	 
	 
	def setWithRelaxation(self, withRelaxation) : 
		self.withRelaxation = withRelaxation
	 
	 
	def getReturnFields(self) : 
		return self.returnFields
	 
	 
	def setReturnFields(self, returnFields) : 
		self.returnFields = returnFields
	 
	 
	def getOffset(self) : 
		return self.offset
	 
	 
	def setOffset(self, offset) : 
		self.offset = offset
	 
	 
	def getQuerytext(self) : 
		return self.queryText
	 
	 
	def setQuerytext(self, queryText) : 
		self.queryText = queryText
	 
	 
	def getFacets(self) :
		return self.bxFacets
	 
	 
	def setFacets(self, bxFacets) : 
		self.bxFacets = bxFacets
	 
	 
	def getSortFields(self) : 
		return self.bxSortFields
	 
	 
	def setSortFields(self, bxSortFields) : 
		self.bxSortFields = bxSortFields
	 
	 
	def getFilters(self) : 
		#filters ={ }
		filters = self.bxFilters
		if BxRequest.getFacets(self) != None:
			for _filter in self.getFacets().getFilters() :
				filters.append( _filter )
		 
		return self.bxFilters
	 
	 
	def setFilters(self, bxFilters) : 
		self.bxFilters = bxFilters
	 
	 
	def addFilter(self , bxFilter) : 
		self.bxFilters[bxFilter.getFieldName()] = bxFilter 
	 
	 
	def getOrFilters(self) : 
		return self.orFilters 
	 
	 
	def setOrFilters(self, orFilters) : 
		self.orFilters = orFilters 
	 
	 
	def addSortField(self, field, reverse =False) : 
		if self.bxSortFields == None: 
			self.bxSortFields = BxSortFields.BxSortFields()
		 
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
	 
	 
	def setMin(self, min) :
		self.min = min 
	 
 
	def getIndexId(self) :
		return self.indexId
	 
	 
	def setIndexId(self, indexId) : 
		self.indexId = indexId
		for k, contextItem in self.contextItems.iteritems() :
			if contextItem == None :
				self.contextItems['indexId'] = indexId
			 
		 
	 
	 
	def setDefaultIndexId(self, indexId) : 
		if self.indexId == None :
			self.setIndexId(indexId) 
		 
	 
	 
	def setDefaultRequestMap(self, requestMap) : 
		if self.requestMap == None :
			self.requestMap = requestMap
		 
	 
 
	def getLanguage(self) : 
		return self.language 
	 
	 
	def setLanguage(self, language) : 
		self.language = language 
	 
 
	def getGroupBy(self): 
		return self.groupBy 
	 
 
	def setGroupBy(self, groupBy): 
		self.groupBy = groupBy 
	 
 
	def getSimpleSearchQuery(self) : 
		 
		searchQuery = BxSortFields.ttypes.SimpleSearchQuery()
		searchQuery.indexId = self.getIndexId()
		searchQuery.language = self.getLanguage() 
		searchQuery.returnFields = self.getReturnFields() 
		searchQuery.offset = self.getOffset() 
		searchQuery.hitCount = self.getMax() 
		searchQuery.queryText = self.getQuerytext()
		searchQuery.groupBy = self.groupBy 
		if self.getFilters() !=None :
			searchQuery.filters = {} 
			for _filter in self.getFilters() : 
				searchQuery.filters.append( _filter.getThriftFilter() )
			 
		 
		searchQuery.orFilters = self.getOrFilters() 
		if self.getFacets() != None : 
			searchQuery.facetRequests = self.getFacets().getThriftFacets() 
		 
		if self.getSortFields() != None : 
			searchQuery.sortFields = self.getSortFields().getThriftSortFields() 
		return searchQuery 
	 
	 
	contextItems = {}
	def setProductContext(self, fieldName, contextItemId, role = 'mainProduct') : 
		contextItem = BxSortFields.ttypes.ContextItem()
		contextItem.indexId = self.getIndexId()
		contextItem.fieldName = fieldName 
		contextItem.contextItemId = contextItemId
		contextItem.role = role
		self.contextItems ={'contextItemId': contextItemId ,'fieldName': fieldName,'indexId' :self.getIndexId() ,'role':role}

	 



	def setBasketProductWithPrices(self, fieldName, basketContent, role = 'mainProduct', subRole = 'mainProduct') : 
		if basketContent != False and len(basketContent) != None :
			 
			# Sort basket content by price 
			def usort(_a, _b):
				if _a['price'] > _b['price']:
					return -1
				elif _b['price'] > _a['price']:
					return 1

				return 0
			sorted(basketContent, usort) 
 
			_basketItem = basketContent.pop(0) 
 
			contextItem = BxSortFields.ttypes.ContextItem()
			contextItem._indexId = self.getIndexId()
			contextItem.fieldName = fieldName 
			contextItem.contextItemId = _basketItem['id'] 
			contextItem.role = role 
 
			self.contextItems.update({'indexId' :self.getIndexId(),'fieldName':fieldName,'contextItemId' :_basketItem['id'] , 'role':role })
 
			for _basketItem in basketContent:
				contextItem = BxSortFields.ttypes.ContextItem()
				contextItem.indexId = self.getIndexId()
				contextItem.fieldName = fieldName 
				contextItem.contextItemId = _basketItem['id'] 
				contextItem.role = subRole
				self.contextItems.update({'indexId': self.getIndexId(), 'fieldName': fieldName, 'contextItemId': _basketItem['id'],'role': role})

			 
	 
	 
	def getContextItems(self) : 
		return self.contextItems
	 
	 
	def getRequestContextParameters(self) : 
		return [] 
	 
	 
	def retrieveHitFieldValues(self, item,field, items,fields) : 
		return []
 
 