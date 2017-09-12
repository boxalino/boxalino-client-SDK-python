from p13n import ttypes
class BxSortFields:

	sorts = {}

	def __init__(self, field=None, reverse=False ) :

		if field!= None:
			self.push(field, reverse)
		


	def push(self, field, reverse=False):

		self.sorts[field] = reverse

	def getSortFields(self):

		return self.sorts.keys()

	
	def isFieldReverse(self, field):
		try:
			if self.sorts[field] != None :
				return True;
		except IndexError:
			return False
	
	
	def getThriftSortFields(self) :
		sortFields = {}
		for field  in self.getSortFields():
			sortFields.update(ttypes.SortField({'fieldName' : field,'reverse' : self.isFieldReverse(field)}))
		
		return sortFields
	