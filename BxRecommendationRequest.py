import BxRequest
class BxRecommendationRequest(BxRequest):
    _language = None
    _choiceId = None
    _hitCount = None
    BxRequest.BxRequest(_language, _choiceId, _hitCount)