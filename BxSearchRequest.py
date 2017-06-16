import BxRequest
class BxSearchRequest(BxRequest.BxSearchRequest):

	def __init__(self, language, queryText, max=10, choiceId=None):
		if choiceId == None
			choiceId = 'search'
		
		super(Instructor, self).__init__(language, choiceId, max,0 )
		self.setQueryText(queryText);
	