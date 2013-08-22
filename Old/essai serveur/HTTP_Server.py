#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import time

TIMEOUT = 60			# timeout en seconde
class Serveur(Resource):
    def render_POST(self, request):
        print "requete POST :",request.args
        return str(request.args)
			
    def render_GET(self, request):
        print request.args
        return str(request.args)
			
			
root = Resource()
root.putChild("coinche", Serveur())
factory = Site(root)
reactor.listenTCP(8080, factory)
reactor.run()
