#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts         import render, redirect
from django.utils.translation import ugettext as _
from datetime                 import datetime
from core.api                 import Api
import local


def home(request):
    api = Api(request)

    categories = (
        {'name':_('Last Releases'), 'api':local.API_URL_LAST,     'link':'last_releases'},
        {'name':_('Upcoming'),      'api':local.API_URL_UPCOMING, 'link':'upcomming'},
        {'name':_('Popular'),       'api':local.API_URL_POPULAR,  'link':'popular'},
        {'name':_('Top Rated'),     'api':local.API_URL_TOPRATED, 'link':'top_rated'},
    )

    params = {
        'api_key' : local.API_KEY,
        'language': request.LANGUAGE_CODE
    }

    featured = None

    for category in categories:
        result = api.get(category['api'], params)
        items  = result.get('results', [])

        for item in items:
            try:
                item['year'] = datetime.strptime(item.get('release_date'), '%Y-%m-%d').year
            except Exception as e:
                # pass
                raise Exception(e)

        category['items'] = items

        if category['link'] == 'popular':
            featured = items[:5]



    context = {
        'app': 'home',

        'featured'  : featured,
        'categories': categories,
    }

    return render(request, 'home.html', context)
