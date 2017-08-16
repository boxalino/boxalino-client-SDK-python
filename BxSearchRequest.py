from BxRequest import *
class BxSearchRequest(BxRequest):

	def __init__(self, language, queryText, max=10, choiceId=None):
		if choiceId == None:
			choiceId = 'search'

		#BxRequest.__init__(language, choiceId, max,0 )
		BxRequest.setQueryText(queryText);
	