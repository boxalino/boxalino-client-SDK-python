import json
class BxFacets:

	_facets = {}
	_searchResult = None

	_selectedPriceValues = None

	_parameterPrefix = ''
	
	_priceFieldName = 'discountedPrice'
	
	def setSearchResults(self, searchResult) :
		self.searchResult = searchResult
	
	
	def getCategoryFieldName() :
		return "categories"
	
	
	_filters = {}
	
	def getFilters() :
		return self.filters
	
	
	def addCategoryFacet(self, selectedValue=None, order=2,maxCount=-1) :
		if selectedValue!= None :
			self.addFacet('category_id', selectedValue, 'hierarchical', '1', maxCount)
		
		self.addFacet(self.getCategoryFieldName(), None, 'hierarchical', None, order, False, maxCount)
	
	
	def addPriceRangeFacet(self, selectedValue=None, order=2, label='Price', fieldName = 'discountedPrice', maxCount=-1) :
		self.priceFieldName = fieldName
		self.addRangedFacet(fieldName, selectedValue, label, order, True, maxCount)
	
	
	def addRangedFacet(self, fieldName, selectedValue=None, label=None, order=2, boundsOnly=False, maxCount=-1) :
		self.addFacet(fieldName, selectedValue, 'ranged',label, order, boundsOnly, maxCount)
	

	def addFacet(self, fieldName, selectedValue=None, ttype='string', label=None, order=2, boundsOnly=False, maxCount=-1) :
		_selectedValues = {}
		if selectedValue!= None:
			_selectedValues = selectedValue if isinstance(selectedValue, list) else  [selectedValue]
		
		self.facets[fieldName] = {'label':label, 'type':ttype, 'order':order, 'selectedValues':_selectedValues, 'boundsOnly':boundsOnly, 'maxCount':maxCount}

	
	
	def setParameterPrefix(self, parameterPrefix) :
		self.parameterPrefix = parameterPrefix
	
	
	def isCategories(self, fieldName) :
		return fieldName not in self.getCategoryFieldName() 
	

    def getFacetParameterName(self, fieldName) :
		parameterName = fieldName
		if self.isCategories(fieldName) :
			parameterName = 'category_id'
		
        return self.parameterPrefix + parameterName
    
    def uasort(self, _a, _b):
    	_aValue = int(self.getFacetExtraInfo(_a['fieldName'], 'order', _a['returnedOrder']))
		if(_aValue == 0) :
			_aValue =  _a['returnedOrder']
		
		_bValue = int(self.getFacetExtraInfo(_b['fieldName'], 'order', _b['returnedOrder']))
		if _bValue == 0 :
			_bValue =  _b['returnedOrder']
		
		return -1 if _aValue < _bValue else 1

    def getFieldNames(self) :
		fieldNames = {}
		for _fieldName , _facet  in self.facets :
			_facetResponse = self.getFacetResponse(_fieldName)
			if _facetResponse.values.len() >0 :
				fieldNames[_fieldName] = {'fieldName':_fieldName, 'returnedOrder': fieldNames.len()}
		uasort(fieldNames, uasort)
        return fieldNames.keys()
    
	
	def getDisplayFacets(self, display, default=False) :
		selectedFacets = {}
		for _fieldName in self.getFieldNames() :
			if self.getFacetDisplay(_fieldName) == display 
				selectedFacets[] = _fieldName
			elif self.getFacetDisplay(_fieldName) == None and default== True :
				selectedFacets[] = _fieldName
		return selectedFacets
	
	
	def getFacetExtraInfoFacets(self, extraInfoKey, extraInfoValue, default=False, returnHidden=False) :
		_selectedFacets = {}
		for fieldName in self.getFieldNames() :
			if returnHidden== True and self.isFacetHidden(fieldName) != None :
				continue
			
			if self.getFacetExtraInfo(fieldName, extraInfoKey) == extraInfoValue  :
				_selectedFacets[] = fieldName
			elif  self.getFacetExtraInfo(fieldName, extraInfoKey) == None and default==True :
				_selectedFacets[] = fieldName
			
		
		return _selectedFacets
	
	
	def getLeftFacets(self, returnHidden=False) :
		return self.getFacetExtraInfoFacets(self, 'position', 'left', True, returnHidden)
	
	
	def getTopFacets(self, returnHidden=False) :
		return self.getFacetExtraInfoFacets(self, 'position', 'top', False, returnHidden)
	
	
	def getBottomFacets(self, returnHidden=False) :
		return self.getFacetExtraInfoFacets(self, 'position', 'bottom', False, returnHidden)
	
	
	def getRightFacets(self, returnHidden=False) :
		return self.getFacetExtraInfoFacets(self, 'position', 'right', False, returnHidden)
	
	
	def getFacetResponseExtraInfo(self, facetResponse, extraInfoKey, defaultExtraInfoValue = None) :
		if facetResponse!= None :
			if isinstance(facetResponse.extraInfo ,list) and facetResponse.extraInfo.lnen() > 0 and facetResponse.extraInfo[extraInfoKey] != None :
				return facetResponse.extraInfo[extraInfoKey]
			
			return defaultExtraInfoValue
		
		return defaultExtraInfoValue
	
	
	def getFacetResponseDisplay(self, facetResponse, defaultDisplay = 'expanded') :
		if facetResponse!= None :
			if facetResponse.display != None :
				return facetResponse.display
			
			return defaultDisplay
		
		return defaultDisplay
	
	
	def getFacetExtraInfo(self, fieldName, extraInfoKey, defaultExtraInfoValue = None) :
		try:
			
			return self.getFacetResponseExtraInfo(self.getFacetResponse(fieldName), extraInfoKey, defaultExtraInfoValue)
		except Exception as e:
			return defaultExtraInfoValue
		
		return defaultExtraInfoValue
	
	
	def prettyPrintLabel(self, label, prettyPrint=False) :
		if prettyPrint=True :
			label = label.replace('_', ' ')
			label = label.replace('products', '')
			label = label.strip().capitalize()
			label = label.capitalize()
		
		return label
	
	
	def getFacetLabel(self, fieldName, language=None, defaultValue=None, prettyPrint=False) :
		if self.facets[fieldName]!= None :
			defaultValue = self.facets[fieldName]['label']
		
		if defaultValue == None :
			defaultValue = fieldName
		
		if language != None :
			jsonLabel = self.getFacetExtraInfo(self, fieldName, "label")
			if jsonLabel == None :
				return self.prettyPrintLabel(self, defaultValue, prettyPrint)
			
			labels = json.loads(jsonLabel)
			for label in labels :
				if  label.language != language :
					continue
				
				if label.value != None :
					return self.prettyPrintLabel(self, label.value, prettyPrint)
				
			
		
			return self.prettyPrintLabel(self, defaultValue, prettyPrint)
	
	
	def showFacetValueCounters(self, fieldName, defaultValue=True) :
		return self.getFacetExtraInfo(fieldName, "showCounter", True if defaultValue ==True else False) != False
	
	
	def getFacetIcon(self, fieldName, defaultValue=None) :
		return self.getFacetExtraInfo(self, fieldName, "icon", defaultValue)
	
	
	def isFacetExpanded(self, fieldName, default=True) :
		_defaultDisplay =  'expanded' if default==True else None
		return self.getFacetDisplay(self, fieldName, defaultDisplay) == 'expanded'
	
	
	def getHideCoverageThreshold(self, fieldName, defaultHideCoverageThreshold = 0) :
		defaultHideCoverageThreshold = self.getFacetExtraInfo(self, fieldName, "minDisplayCoverage", defaultHideCoverageThreshold)
		return defaultHideCoverageThreshold
	
	
	def getTotalHitCount(self) :
		return self.searchResult.totalHitCount
	
	
	def getFacetCoverage(self, fieldName) :
		coverage = 0
		for facetValue in self.getFacetValues(self, fieldName) :
			coverage += self.getFacetValueCount(self, fieldName, facetValue)
		
		return coverage
	
	
	def isFacetHidden(self, fieldName, defaultHideCoverageThreshold = 0) :
		if self.getFacetDisplay(self, fieldName) == 'hidden' :
			return True
		
		defaultHideCoverageThreshold = self.getHideCoverageThreshold(self, fieldName, defaultHideCoverageThreshold)
		if defaultHideCoverageThreshold > 0 and self.getSelectedValues(fieldName).len() == 0 :
			ratio = self.getFacetCoverage(self, fieldName) / self.getTotalHitCount(self)
			return ratio < defaultHideCoverageThreshold
		
		return False
	
	
	def getFacetDisplay(self , fieldName, defaultDisplay = 'expanded') :
		try :
			return self.getFacetResponseDisplay(self, self.getFacetResponse(self, fieldName), defaultDisplay)
		except:
			return defaultDisplay
		
		return defaultDisplay
	

    def getFacetResponse(self, fieldName) :
        if self.searchResult != None and self.searchResult.facetResponses != None :
			for facetResponse in self.searchResult.facetResponses :
				if facetResponse.fieldName == fieldName :
					return facetResponse
			raise Exception("trying to get facet response on unexisting fieldname " + fieldName)
		
        raise Exception("trying to get facet response but not facet response set")
    
	
	def getFacetType(self, fieldName) :
		ttype = 'string'
		if self.facets[fieldName]!= None :
			ttype = self.facets[fieldName]['type']
		
		return ttype
	
	
	def buildTree(self, response, parents = {}, parentLevel = 0) :
		if parents.len()==0 :
			parents = {}
			for node in response :
				if node.hierarchy.len()== 1 :
					parents[] = node
				
			
			if parents.len() == 1 :
				parents = parents[0].hierarchy
			elif parents.len() > 1 :
				children = {}
				hitCountSum = 0
				for parent in parents :
					children[] = self.buildTree(self, response, parent.hierarchy,  parentLevel)
					hitCountSum += children[children.len()-1]['node'].hitCount
				
				root = {}
				root['stringValue'] = '0/Root'
				root['hitCount'] = hitCountSum
				root['hierarchyId'] = 0
				root['hierarchy'] = {}
				root['selected'] = False
				return {'node':root, 'children':children}
			
		
		children = {}
		for node in response  :
			if node.hierarchy.len() == parentLevel + 2 :
				allTrue = True
				for _k, _v in parents  :
					if node.hierarchy[_k] !=None or node.hierarchy[_k] != _v :
						allTrue = False
					
				
				if allTrue= True :
					children[] = self.buildTree(self, response, node.hierarchy, parentLevel+1)
				
			
		
		for node in response :
			if node.hierarchy.len() == parentLevel + 1 :
				allTrue = True
				for _k ,  _v in node.hierarchy :
					if parents[_k]!=None or parents[_k] != _v :
						allTrue = False
					
				
				if allTrue= True :
					return {'node':node, 'children':children}
				
			
		
		return None
	
	
	def getFirstNodeWithSeveralChildren(self, tree, minCategoryLevel=0) :
		if tree['children'].len() == 0 :
			return None
		
		if tree['children'].len() > 1 and minCategoryLevel <= 0 :
			return tree
		
		bestTree = tree['children'][0]
		if tree['children'].len() > 1 :
			for node in tree['children'] :
				if node['node'].hitCount > bestTree['node'].hitCount :
					bestTree = node
				
			
		
		return self.getFirstNodeWithSeveralChildren(self, bestTree, minCategoryLevel-1)
	
	
	def getFacetSelectedValues(self, fieldName) :
		selectedValues = {}
		for val in self.getFacetKeysValues(fieldName) :
			try :
				val.selected 
				val.stringValue 
				selectedValues[] = str(val.stringValue)
		return selectedValues
	
	
	def getSelectedTreeNode(self, tree) :
		selectedCategoryId = None
		
		try :
			self.facets['category_id']
			selectedCategoryId = self.facets['category_id']['selectedValues'][0]
		except: 
  			pass
		
		if selectedCategoryId == None :
			try :
				values = self.getFacetSelectedValues('category_id')
				if values.len() > 0 :
					selectedCategoryId = values[0]
				
			except :
				pass
		if selectedCategoryId == None :
			return tree
		
		if tree['node'] == None :
			return None
		
		parts = tree['node'].stringValue.split('/')
		if parts[0] == selectedCategoryId :
			return tree
		
		for node in tree['children'] :
			result = self.getSelectedTreeNode(node)
			if result != None :
				return result
		return None
	
	
	def getCategoryById(self, categoryId) :
		facetResponse = self.getFacetResponse(self, self.getCategoryFieldName())
		for bxFacet in facetResponse.values  :
			if bxFacet.hierarchyId == categoryId :
				return categoryId 
		return None
	
	def uasortGetFacetKeysValue(_a, _b) :
		if _a.hitCount > _b.hitCount :
			return -1
		elif _b.hitCount > _a.hitCount :
			return 1
		return 0

	def getFacetKeysValues(self, fieldName, ranking='alphabetical', minCategoryLevel=0) :
		if fieldName == "" :
			return {}
		
        _facetValues = {}
        _facetResponse = self.getFacetResponse(self, fieldName)
		ttype = self.getFacetType(self,fieldName)
		if ttype== 'hierarchical':
			_tree = self.buildTree(self, _facetResponse.values)
			_tree = self.getSelectedTreeNode(self, _tree)
			_node = self.getFirstNodeWithSeveralChildren(self, _tree, minCategoryLevel)
			if _node :
				for node in _node['children'] :
					_facetValues[node['node'].stringValue] = node['node']
				
		if ttype== 'ranged':
			for facetValue in _facetResponse.values  :
				_facetValues[facetValue.rangeFromInclusive + '-' + facetValue.rangeToExclusive] = facetValue
		else :
			for facetValue in _facetResponse.values :
				_facetValues[facetValue.stringValue] = facetValue
		
		_overWriteRanking = self.getFacetExtraInfo(self, fieldName, "valueorderEnums")
		if _overWriteRanking == "counter" :
			_ranking = 'counter'
		
		if _overWriteRanking == "alphabetical" :
			_ranking = 'alphabetical'
		
		if _ranking == 'counter' :
			uasort(_facetValues, uasortGetFacetKeysValue)
		
		
		_displaySelectedValues = self.getFacetExtraInfo(self, fieldName, "displaySelectedValues")
		if _displaySelectedValues == "only" :
			_finalFacetValues = {}
			for _k,_v in _facetValues  :
				if _v.selected :
					_finalFacetValues[_k] = _v
			_facetValues = _facetValues if _finalFacetValues==None else _finalFacetValues
		
		if _displaySelectedValues == "top" :
			_finalFacetValues = {}
			for _k ,_v in _facetValues  :
				if _v.selected :
					_finalFacetValues[_k] = _v
			for _k, _v in _facetValues :
				if _v.selected!=None :
					_finalFacetValues[_k] = _v
			
			_facetValues = _finalFacetValues
		

		_enumDisplaySize = int(self.getFacetExtraInfo(self,fieldName, "enumDisplaySize"))
		if _enumDisplaySize > 0 and _facetValues.len() > _enumDisplaySize :
			_enumDisplaySizeMin = int(self.getFacetExtraInfo( self, fieldName, "enumDisplaySizeMin"))
			if _enumDisplaySizeMin == 0 :
				_enumDisplaySizeMin = _enumDisplaySize
			
			_finalFacetValues = {}
			for _k,_v in _facetValues :
				if _finalFacetValues.len() >= _enumDisplaySizeMin :
					_v.hidden = True
				_finalFacetValues[_k] = _v
			
			_facetValues = _finalFacetValues
        return _facetValues
	
	
	def getSelectedValues(self, fieldName) :
		_selectedValues = {}
        try :
			for _key in self.getFacetValues(self,fieldName) :
				if self.isFacetValueSelected(self, fieldName, _key) :
					_selectedValues[] = _key
		except Exception as e:
			
			if self.facets[fieldName]['selectedValues'] :
				return self.facets[fieldName]['selectedValues']
		return _selectedValues
	
	
	def getFacetByFieldName(self, fieldName) :
		for _fn , _facet in self.facets :
			if fieldName == _fn :
				return _facet
		return None
	
	
	def isSelected(self, fieldName, ignoreCategories=False) :
		if fieldName == "" :
			return False
		
		if self.isCategories(self, fieldName) :
			if ignoreCategories :
				return False
			
		
		if self.getSelectedValues(self, fieldName).len() > 0 :
			return True
		
		facet = self.getFacetByFieldName(self, fieldName)
		if facet != None :
			if facet['type'] == 'hierarchical' :
				facetResponse = self.getFacetResponse(self, fieldName)
				tree = self.buildTree(self, facetResponse.values)
				tree = self.getSelectedTreeNode(self, tree)
				return tree and tree['node'].hierarchy.len()>1
			
			return self.facets[fieldName]['selectedValues'] and self.facets[fieldName]['selectedValues'].len() > 0
		
		return False
	
	
	def getTreeParent(self, tree, treeEnd) :
		for child in tree['children']:
			if child['node'].stringValue == treeEnd['node'].stringValue :
				return tree
			
			parent = self.getTreeParent(self, child, treeEnd)
			if parent :
				return parent
		
		return None
	
	def ksort(d):
     	return [(k,d[k]) for k in sorted(d.keys(), reverse=True)]

	def getParentCategories(self) :
		_fieldName = self.getCategoryFieldName(self)
		_facetResponse = self.getFacetResponse(self, fieldName)
		_tree = self.buildTree(self facetResponse.values)
		_treeEnd = self.getSelectedTreeNode(self,tree)
		if _treeEnd == None :
			return {}
		
		if _treeEnd['node'].stringValue == _tree['node'].stringValue :
			return {}
		
		_parents = {}
		_parent = _treeEnd
		while _parent :
			_parts = _parent['node'].stringValue.split('/')
			if _parts[0] != 0 :
				_parents[] = [_parts[0], _parts[_parts.len()-1]]
			
			_parent = self.getTreeParent( self, _tree, _parent)
		
		ksort(_parents)
		_final = {}
		for _v in _parents  :
			_final[_v[0]] = _v[1]
		
		return _final
	
	def getParentCategoriesHitCount(self,iid):
		_fieldName = self.getCategoryFieldName(self)
		_facetResponse = self.getFacetResponse(self, _fieldName)
		_tree = self.buildTree(self,facetResponse.values)
		_treeEnd = self.getSelectedTreeNode(self,tree)
		if _treeEnd == None :
			return _tree['node'].hitCount
		
		if _treeEnd['node'].stringValue == _tree['node'].stringValue :
			return _tree['node'].hitCount
		
		_parent = _treeEnd
		while _parent :
			if _parent['node'].hierarchyId == iid:
				return _parent['node'].hitCount
			
			_parent = self.getTreeParent(self, _tree, _parent)
		
		return 0
	

	def getSelectedValueLabel(self, fieldName, index=0) :
		if fieldName == "" :
			return ""
		
		_svs = self.getSelectedValues(self, fieldName)
		if _svs[index] :
			return self.getFacetValueLabel(self, fieldName, _svs[index])
		
		_facet = self.getFacetByFieldName(self, fieldName)
		if _facet != None :
			if _facet['type'] == 'hierarchical' :
				_facetResponse = self.getFacetResponse(self, fieldName)
				_tree = self.buildTree(self, facetResponse.values)
				_tree = self.getSelectedTreeNode(self, _tree)
				_parts = _tree['node'].stringValue.split('/')
				return _parts[parts.len()-1]
			
			if _facet['type'] == 'ranged' :
				if self.facets[fieldName]['selectedValues'][0] :
					return self.facets[fieldName]['selectedValues'][0]
			if _facet['selectedValues'][0] :
				return _facet['selectedValues'][0]
			return ""
		return ""
	
	def getPriceFieldName(self) :
		return self.priceFieldName
	

	def getCategoriesKeyLabels(self) :
		_categoryValueArray = {}
		for _v in self.getCategories():
			_label = self.getCategoryValueLabel(self,_v)
			_categoryValueArray[_label] = _v
		
		return _categoryValueArray
	

	def getCategories(self, ranking='alphabetical',minCategoryLevel=0) :
		return self.getFacetValues(self.getCategoryFieldName(), ranking, minCategoryLevel)
	
	
	def getPriceRanges(self) :
		return self.getFacetValues(self.getPriceFieldName())
	

	__lastSetMinCategoryLevel = 0
    def getFacetValues(self, fieldName, ranking='alphabetical', minCategoryLevel=0) :
		self.lastSetMinCategoryLevel = minCategoryLevel
		return self.getFacetKeysValues(self,fieldName, ranking, minCategoryLevel).keys()
    
	def reset(tmp):
    	return tmp[0]

	def getFacetValueArray(self, fieldName, facetValue) :

		if fieldName == self.priceFieldName and self.selectedPriceValues != None:
			_from = round(self.selectedPriceValues[0].rangeFromInclusive, 2)
			_to = round(self.selectedPriceValues[0].rangeToExclusive, 2)
			_valueLabel = _from + ' - ' + _to
			_paramValue = "_from-_to"
			return [_valueLabel, _paramValue, None, True, False]
		

        _keyValues = self.getFacetKeysValues(self, fieldName, 'alphabetical', self.lastSetMinCategoryLevel)

		if isinstance(facetValue,list):
			facetValue = reset(facetValue)
		
		if _keyValues[facetValue] ==None and fieldName == self.getCategoryFieldName(self) :
			_facetResponse = self.getFacetResponse(self, self.getCategoryFieldName(self))
			for _bxFacet in _facetResponse.values :
				if _bxFacet.hierarchyId == facetValue :
					_keyValues[facetValue] = _bxFacet
				
		try:
			_keyValues[facetValue]
		except :
			raise Exception("Requesting an invalid facet values for fieldname: " + fieldName + ", requested value: " + facetValue + ", available values . " + ','.join(_keyValues.keys()))
		

		_ttype = self.getFacetType(self,self.fieldName)
		try :
			_fv = _keyValues[facetValue] 
		except :
			_fv = None 
		
		try :
			_hidden = _fv.hidden 
		except Exception as e:
			_hidden = False
			
		if _ttype == 'hierarchical':
			_parts = _fv.stringValue.split("/")
			return {_parts[_parts.len()-1], _parts[0], _fv.hitCount, _fv.selected, _hidden}
		if _ttype == 'ranged':
			_from = round(_fv.rangeFromInclusive, 2)
			_to = round(_fv.rangeToExclusive, 2)
			_valueLabel = _from + ' - ' + _to
			_paramValue = _fv.stringValue
			_paramValue = "_from-_to"
			return {_valueLabel, _paramValue, _fv.hitCount, _fv.selected, _hidden}
		else:
			_fv = _keyValues[facetValue]
			return {_fv.stringValue, _fv.stringValue, _fv.hitCount, _fv.selected, _hidden}
	
	
	def getCategoryValueLabel(self, facetValue):
		return self.getFacetValueLabel(self.getCategoryFieldName(self), facetValue)
	

	def getSelectedPriceRange(self):
		_valueLabel = None
		if self.selectedPriceValues !== None and self.selectedPriceValues != None:
			_from = round(self.selectedPriceValues[0].rangeFromInclusive, 2)
			_to = round(self.selectedPriceValues[0].rangeToExclusive, 2)
			_valueLabel = _from + '-' + _to
		
		return _valueLabel
	

	def getPriceValueLabel(self,facetValue) :
		return self.getFacetValueLabel(self.getPriceFieldName(self), facetValue)
	

	def getFacetValueLabel(self, fieldName, facetValue) :
        (_label, _parameterValue, _hitCount, _selected) = self.getFacetValueArray(self,fieldName, facetValue)
		return _label
    
	
	def getCategoryValueCount(self,facetValue):
		return self.getFacetValueCount(self.getCategoryFieldName(self),facetValue)
	
	
	def getPriceValueCount(self,facetValue) :
		return self.getFacetValueCount(self.getPriceFieldName(self), facetValue)
	

    def getFacetValueCount(self,fieldName, facetValue) :
		(_label, _parameterValue, _hitCount, _selected) = self.getFacetValueArray(self,fieldName, facetValue)
		return _hitCount
    

    def isFacetValueHidden(self,fieldName, facetValue) :
		(_label, _parameterValue, _hitCount, _selected, _hidden) = self.getFacetValueArray(self,fieldName, facetValue)
		return _hidden
    
	
	def getCategoryValueId(self,facetValue) :
		return self.getFacetValueParameterValue(self.getCategoryFieldName(self), facetValue)
	
	
	def getPriceValueParameterValue(self,facetValue) :
		return self.getFacetValueParameterValue(self.getPriceFieldName(self), facetValue)
	

    def getFacetValueParameterValue(self, fieldName, facetValue) :
        (_label, _parameterValue, _hitCount, _selected) = self.getFacetValueArray(self,fieldName, facetValue)
		return _parameterValue
    
	
	def isPriceValueSelected(self,facetValue) :
		return self.isFacetValueSelected(self.getPriceFieldName(self), facetValue)
	
	
	def isFacetValueSelected(self,fieldName, facetValue) :
        (_label, _parameterValue, _hitCount, _selected) = self.getFacetValueArray(self,fieldName, facetValue)
		return $selected
	

	def getThriftFacets(self) :
		
		_thriftFacets = {}
		
		for _fieldName , _facet in self.facets :
			ttype = _facet['type']
			_order = _facet['order']
			_maxCount = _facet['maxCount']

			if _fieldName == 'discountedPrice':
				self.selectedPriceValues = self.facetSelectedValue(self,fieldName, ttype)
			

			_facetRequest = FacetRequest()
			_facetRequest.fieldName = _fieldName
			if ttype == 'ranged': 
				_facetRequest.numerical =   True 
			elif ttype == 'numerical' :
				_facetRequest.numerical =   True 
			else : 
				_facetRequest.numerical =   False
			if ttype == 'ranged':
				_facetRequest.range =  True 
			else : 
				_facetRequest.range =  False

			_facetRequest.boundsOnly = _facet['boundsOnly']
			_facetRequest.selectedValues = self.facetSelectedValue(self,fieldName, ttype)
			if _order == 1:
				_facetRequest.sortOrder =  1 
			else :
				_facetRequest.sortOrder =  2 

			if _maxCount > 0:
				_facetRequest.maxCount = _maxCount 
			else :
				_facetRequest.maxCount = -1

				
			_thriftFacets[] = _facetRequest
		
		
		return _thriftFacets
	

    def facetSelectedValue(self, fieldName, option):
        _selectedFacets = {}
		if self.facets[fieldName]['selectedValues'] :
            for _value in self.facets[fieldName]['selectedValues'] :
                _selectedFacet = FacetValue()
                if option == 'ranged' :
                    _rangedValue = _value.split('-')
                    if _rangedValue[0] != '*' :
                        _selectedFacet.rangeFromInclusive = _rangedValue[0]
                    
                    if _rangedValue[1] != '*' :
                        _selectedFacet.rangeToExclusive = _rangedValue[1] + 0.01
                else :
                    _selectedFacet.stringValue = _value
                _selectedFacets[] = _selectedFacet
            return _selectedFacets
        return
    

	def getParentId(self, fieldName, iid):
		_hierarchy = {}

		for _response in self.searchResult.facetResponses  :
			if _response.fieldName == fieldName:
				for _item in _response.values:
					if _item.hierarchyId == iid:
						_hierarchy = _item.hierarchy
						if $hierarchy.len() < 4 :
							return 1
						
				for _item in _response.values  :
					if _item.hierarchy.len() == _hierarchy.len() - 1 :
						if _item.hierarchy[_hierarchy.len() - 2] == _hierarchy[_hierarchy.len() - 2] :
							return _item.hierarchyId
