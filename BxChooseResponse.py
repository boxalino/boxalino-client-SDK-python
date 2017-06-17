import json
import BxFacets
class BxChooseResponse:
	_response = None
	_bxRequests = None
	
	def __init__(self,response, bxRequests=[]):
		self._response = response
		if isinstance(bxRequests, list):
			self._bxRequests =  bxRequests
		else :
			self._bxRequests = [bxRequests];

	
	def getResponse(self):
		return self._response;
	
	def getChoiceResponseVariant(self, choice=None, count= None):
	
		for _k , _bxRequest in self._bxRequests():
			if choice == None or choice == _bxRequest.getChoiceId():
				if _count > 0:
					_count-=1
					continue
				return self.getChoiceIdResponseVariant(_k);
	
	def getChoiceIdResponseVariant(self, id=0):
		_response = self.getResponse()
		try:
			if _response.variants != None and _response.variants[id]:
				return _response.variants[id]
		except IndexError:
			pass
		if type(_response).__name__ == 'SearchResult':
			_variant = Variant()
			_variant.searchResult = _response;
			return _variant
		raise Exception('no variant provided in choice response for variant id ' +id)
		
	
	def getFirstPositiveSuggestionSearchResult(self, variant, maxDistance=10):

		if variant.searchRelaxation.suggestionsResults != None :
			return None

		for _searchResult in variant.searchRelaxation.suggestionsResults():
			if _searchResult.totalHitCount > 0:
				if _searchResult.queryText == "" or variant.searchResult.queryText == "":
					continue
				_distance = levenshtein(_searchResult.queryText, variant.searchResult.queryText)
				if _distance <= maxDistance and _distance != -1:
					return _searchResult
		return None
	
	def getVariantSearchResult(self, variant,considerRelaxation=True, maxDistance=10, discardIfSubPhrases = True):

		_searchResult = variant.searchResult
		if considerRelaxation and variant.searchResult.totalHitCount == 0 and  discardIfSubPhrases !=None and self.areThereSubPhrases()!=None:
			return self.getFirstPositiveSuggestionSearchResult(variant, maxDistance)
		return _searchResult
	
	def getSearchResultHitIds(self, searchResult, fieldId='id'):
		_ids = [];
		if _searchResult:
			if _searchResult.hits:
				for _item in _searchResult.hits():
					_ids.append( _item.values[_fieldId][0])
			elif _searchResult.hitsGroups != None:
				for _hitGroup  in _searchResult.hitsGroups():
					_ids.append( _hitGroup.groupValue)
		return _ids
	
	def getHitIds(self, choice=None, considerRelaxation=True, count=0, maxDistance=10, fieldId='id', discardIfSubPhrases = True):
		_variant = self.getChoiceResponseVariant(choice, count)
		return self.getSearchResultHitIds(self.getVariantSearchResult(_variant, considerRelaxation, maxDistance, discardIfSubPhrases), fieldId)

	def retrieveHitFieldValues(self, item, field, fields, hits):
		_fieldValues = [];
		for _bxRequest in self.bxRequests():
			_fieldValues = dict(_fieldValues ,_bxRequest.retrieveHitFieldValues(item, field, fields, hits))
		return _fieldValues
	
	def getSearchHitFieldValues(self, searchResult, fields=None):
		_fieldValues = []
		if searchResult != None:
			_hits = searchResult.hits
			if searchResult.hits == None:
				_hits = []
				for _hitGroup in searchResult.hitsGroups :
					_hits.append(_hitGroup.hits[0])
				
			for _item in _hits:
				_finalFields = fields;
				if _finalFields == None:
					_finalFields = [k for k,v in _item.items() if v == _item.values]
				
				for _field in _finalFields:
					try:
						_item.values[_field]
						if _item.values[_field] != None:
							_fieldValues[_item.values['id'][0]][_field] = _item.values[_field];
					except IndexError: 
						pass
					try:
						if _fieldValues[_item.values['id'][0]][_field]:
							pass
					except	IndexError:
						_fieldValues[_item.values['id'][0]][_field] = self.retrieveHitFieldValues(_item, _field, _searchResult.hits, _finalFields);
		return _fieldValues;
	
	def getRequestFacets(self,  choice=None):
		if choice == None:
			try:
				self.bxRequests[0]
				return self.bxRequests[0].getFacets();
			except IndexError:
				pass
			return None
		for _bxRequest in self.bxRequests:
			if _bxRequest.getChoiceId() == choice:
				return _bxRequest.getFacets();
		return None
	

	def getFacets(self, choice=None, considerRelaxation=True, count=0, maxDistance=10, discardIfSubPhrases = True):
		
		_variant = self.getChoiceResponseVariant(choice, count)
		_searchResult = self.getVariantSearchResult(_variant, considerRelaxation, maxDistance, discardIfSubPhrases)
		_facets = self.getRequestFacets(choice)

		if _facets==None or _searchResult == None:
			return BxFacets()
		
		_facets.setSearchResults(_searchResult)
		return _facets


	def getHitFieldValues(self, fields, choice=None, considerRelaxation=True, count=0, maxDistance=10, discardIfSubPhrases = True):
		_variant = self.getChoiceResponseVariant(choice, count)
		return self.getSearchHitFieldValues(self.getVariantSearchResult(_variant, considerRelaxation, maxDistance, discardIfSubPhrases), fields)
	
	def getFirstHitFieldValue(self, field=None, returnOneValue=True, hitIndex=0, choice=None, count=0, maxDistance=10):
		_fieldNames = None
		if field != None:
			_fieldNames = [field]
		_count = 0
		for _id , _fieldValueMap in self.getHitFieldValues(_fieldNames, choice, True, count, maxDistance):
			count += 1
			if count < hitIndex:
				continue
			
			for _fieldName , _fieldValues in _fieldValueMap:
				if len(_fieldValues)>0:
					if _returnOneValue==True:
						return _fieldValues[0]
					else:
						return _fieldValues
		return None
	
	def  getTotalHitCount(choice=None, considerRelaxation=True, count=0, maxDistance=10, discardIfSubPhrases = True):
		_variant = self.getChoiceResponseVariant(choice, count)
		_searchResult = self.getVariantSearchResult(_variant, considerRelaxation, maxDistance, discardIfSubPhrases)
		if _searchResult == None:
			return 0
		return _searchResult.totalHitCount


	def areResultsCorrected(self, choice=None, count=0, maxDistance=10):
		return self.getTotalHitCount(choice, False, count) == 0 and self.getTotalHitCount(choice, True, count, maxDistance) > 0 and self.areThereSubPhrases() == False
	
	
	def areResultsCorrectedAndAlsoProvideSubPhrases(self, choice=None, count=0, maxDistance=10):
		return self.getTotalHitCount(choice, False, count) == 0 and self.getTotalHitCount(choice, True, count, maxDistance, False) > 0 and self.areThereSubPhrases() == True
	
	
	def getCorrectedQuery(self, choice=None, count=0, maxDistance=10):
		_variant = self.getChoiceResponseVariant(choice, count)
		_searchResult = self.getVariantSearchResult(variant, True, maxDistance, False)
		if _searchResult == True:
			return _searchResult.queryText
		
		return None


	def areThereSubPhrases(self, choice=None, count=0, maxBaseResults=0):
		_variant = self.getChoiceResponseVariant(choice, count)
		try:
			return _variant.searchRelaxation.subphrasesResults and len(_variant.searchRelaxation.subphrasesResults) > 0 and self.getTotalHitCount(choice, False, count) <= maxBaseResults
		except IndexError:
			pass
	
	def getSubPhrasesQueries(self, choice=None, count=0):
		if self.areThereSubPhrases(self, choice, count)== False:
			return []
		
		_queries = []
		_variant = self.getChoiceResponseVariant(choice, count)
		for _searchResult in _variant.searchRelaxation.subphrasesResults:
			_queries.append(_searchResult.queryText)
		
		return _queries
	
	
	def getSubPhraseSearchResult(self , queryText, choice=None, count=0):
		if self.areThereSubPhrases(choice, count)== False:
			return None
		
		_variant = self.getChoiceResponseVariant(choice, count)
		for _searchResult in _variant.searchRelaxation.subphrasesResults:
			if _searchResult.queryText == queryText:
				return _searchResult;
			
		
		return None
	
	def getSubPhraseTotalHitCount(self , queryText, choice=None, count=0):
		_searchResult = self.getSubPhraseSearchResult(queryText, choice, count)
		if _searchResult!= None:
			return _searchResult.totalHitCount
		return 0
	

	def getSubPhraseHitIds(self, queryText, choice=None, count=0, fieldId='id'):
		_searchResult = self.getSubPhraseSearchResult(queryText, choice, count)
		if _searchResult != None:
			return self.getSearchResultHitIds(_searchResult, fieldId)
		return []


	def getSubPhraseHitFieldValues(self, queryText, fields, choice=None, considerRelaxation=True, count=0):
		_searchResult = self.getSubPhraseSearchResult(queryText, choice, count)
		if  _searchResult!= None:
			return self.getSearchHitFieldValues(_searchResult, fields)
		return []

	
	def toJson(fields):
		_object = []
		_object['hits'] = []
		for _id , _fieldValueMap in self.getHitFieldValues(fields):
			_hitFieldValues = {}
			for _fieldName , _fieldValues in _fieldValueMap:
				_hitFieldValues[_fieldName] = {}
				_hitFieldValues[_fieldName]['values'] = fieldValues
			_object['hits'].append({})
			_object['hits']['id'] = _id
			_object['hits']['fieldValues'] = _hitFieldValues
		return json.dumps(_object)



	def levenshtein(a,b):

		n, m = len(a), len(b)
		if n > m:
			# Make sure n <= m, to use O(min(n,m)) space
			a,b = b,a
			n,m = m,n

		current = range(n+1)
		for i in range(1,m+1):
			previous, current = current, [i]+[0]*n
			for j in range(1,n+1):
				add, delete = previous[j]+1, current[j-1]+1
				change = previous[j-1]
				if a[j-1] != b[i-1]:
					change = change + 1
				current[j] = min(add, delete, change)

		return current[n]

