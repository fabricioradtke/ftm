#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime         import datetime
from core.api         import Api
import local


def search(request, query):
    api = Api(request)

    try:
        page = int(request.GET.get('p',    1))
        safe = int(request.GET.get('safe', 1))
    except Exception as e:
        raise Exception(e)

    params = {
        'api_key'      : local.API_KEY,
        'language'     : request.LANGUAGE_CODE,
        'page'         : page,
        'include_adult': False if safe else True,
        'query'        : query,
    }
    result = api.get(local.API_URL_SEARCH, params)
    items  = result.get('results', [])

    # Converte a data para datetime e retorna o ano
    for item in items:
        try:
            item['year'] = datetime.strptime(item.get('release_date'), '%Y-%m-%d').year
        except Exception as e:
            pass
            #raise Exception(e)


    context = {
        'app'   : 'search',

        'search': query,
        'page'  : page,
        'safe'  : safe,

        'items'      : result.get('results'),
        'total_items': result.get('total_results'),
        'total_pages': result.get('total_pages'),
    }
    return render(request, 'search.html', context)
