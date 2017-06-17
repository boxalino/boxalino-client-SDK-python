class BxFilter:

	_fieldName= None
	_values= None
	_negative = None
	
	_hierarchyId = None
	_hierarchy = None
	_rangeFrom = None
	_rangeTo = None
	
	def __init__(self, fieldName, values=[], negative = False):
		self.fieldName = fieldName
		self.values = values
		self.negative = negative
	
	
	def getFieldName(self):
		return self.fieldName
	
	
	def getValues(self) :
		return self.values
	
	
	def isNegative(self) :
		return self.negative
	
	
	def getHierarchyId() :
		return self.hierarchyId
	
	
	def setHierarchyId(hierarchyId) :
		self.hierarchyId = hierarchyId
	
	
	def getHierarchy(self) :
		return self.hierarchy
	
	
	def setHierarchy(self, hierarchy) :
		self.hierarchy = hierarchy
	
	
	def getRangeFrom(self) :
		return self.rangeFrom
	
	
	def setRangeFrom(self, rangeFrom): 
		self.rangeFrom = rangeFrom
	
	
	def getRangeTo(self) :
		return self.rangeTo
	
	
	def setRangeTo(self, rangeTo) :
		self.rangeTo = rangeTo
	
	
	def getThriftFilter(self) :
		_filter = Filter()
		_filter.fieldName = self.fieldName
		_filter.negative = self.negative
		_filter.stringValues = self.values
		if self.hierarchyId!=None:
			_filter.hierarchyId = self.hierarchyId
		
		if self.hierarchy!=None:
			_filter.hierarchy = self.hierarchy
		
		if self.rangeFrom!=None:
			_filter.rangeFrom = self.rangeFrom
		
		if self.rangeTo!=None:
			_filter.rangeTo = self.rangeTo
		return _filter
	