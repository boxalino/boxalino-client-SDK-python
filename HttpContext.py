import time
class HttpContext:
    _VISITOR_COOKIE_TIME = 31536000
    sessionId= None
    profileId= None
    domain = None
    ip= None
    referer = None
    currentUrl = None
    htmlDebug = ""
    userAgent = ""

    def HttpContext(self, domain,userAgent,ip, referer, currentUrl) :
        self.sessionId = None
        self.profileId = None
        self.domain = domain
        self.userAgent = userAgent
        self.ip = ip
        self.referer = referer
        self.currentUrl = currentUrl


    def HttpContext( self, sessionId, profileId, domain, userAgent, ip, referer, currentUrl) :
        self.sessionId = sessionId
        self.profileId = profileId
        self.domain = domain
        self.userAgent = userAgent
        self.ip = ip
        self.referer = referer
        self.currentUrl = currentUrl


    def setSessionAndProfile(self,  sessionId, profileId) :
        self.sessionId = sessionId
        self.profileId = profileId

    def getSessionId(self, domain) :
        self.getSessionAndProfile(None, None, domain)
        return self.sessionId


    def getProfileId(self, domain) :
        self.getSessionAndProfile(None, None, domain)
        return self.profileId




    def getSessionAndProfile(self, sessionId, profileId, domain) :
        if sessionId != None :
            self.sessionId = sessionId

        if profileId != None :
            self.profileId = profileId

        if self.sessionId == None :
            self.sessionId = uniqid()

        if self.profileId == None :
            self.profileId = uniqid()

        return {self.sessionId, self.profileId}

    def getUserAgent(self):

        return self.userAgent

    def getIP(self):

        return self.ip

    def getReferer(self):

        return self.referer


    def getCurrentUrl(self):
        return self.currentUrl


    def responseWrite(self,write) :
        self.htmlDebug += write
        return self.htmlDebug


    def getHtmlDebug(self):

        return self.htmlDebug

    def uniqid(prefix=''):
        return prefix + hex(int(time()))[2:10] + hex(int(time() * 1000000) % 0x100000)[2:7]