#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib    import messages
from django.utils.http import urlencode
from urllib2           import Request, urlopen, URLError
import json


class Api(object):

    def __init__(self, request):
        self.request = request


    def get(self, url, params):
        result  = {}
        request = Request('%s?%s' % (url, urlencode(params)), headers={'Accept':'application/json'})

        try:
            f        = urlopen(request)
            response = f.read()
            f.close()

            result = json.loads(response)

        except Exception as e:
            messages.warning(self.request, e)

        return result
