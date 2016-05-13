#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime         import datetime, timedelta
from core.api         import Api
import local


def explore(request):
    api = Api(request)

    genre = request.GET.get('genre')
    sort  = request.GET.get('sort', 'popular')

    params          = { 'api_key':local.API_KEY, 'language':request.LANGUAGE_CODE }
    params_discover = {}

    if genre:
        try:
            genre = int(genre)
        except Exception as e:
            err = e

        params_discover['with_genres'] = genre


    if sort == 'popular':
        params_discover['sort_by']          = 'popularity.desc'
        params_discover['release_date.lte'] = datetime.today()

    elif sort == 'top_rated':
        params_discover['sort_by']          = 'vote_average.desc'
        params_discover['release_date.lte'] = datetime.today()
        params_discover['vote_count.gte']   = 100

    elif sort == 'last_releases':
        params_discover['sort_by']                  = 'popularity.desc' #'release_date.desc'
        params_discover['primary_release_date.lte'] = datetime.today()
        params_discover['primary_release_date.gte'] = datetime.today() - timedelta(days=30)
        #params_discover['vote_count.gte']   = 1

    elif sort == 'upcomming':
        params_discover['sort_by']                  = 'popularity.desc' #'release_date.desc'
        params_discover['primary_release_date.lte'] = datetime.today() + timedelta(days=30)
        params_discover['primary_release_date.gte'] = datetime.today()
        #params_discover['vote_count.gte']           = 1

    elif sort == 'revenue':
        params_discover['sort_by']          = 'revenue.desc'
        params_discover['release_date.lte'] = datetime.today()


    params_discover.update(params)
    result = api.get(local.API_URL_DISCOVER, params_discover)
    items  = result.get('results', [])


    # Converte a data para datetime e retorna o ano
    if items:
        try:
            for item in items:
                item['year'] = datetime.strptime(item.get('release_date'), '%Y-%m-%d').year
        except Exception as e:
            #pass
            raise Exception(e)


    # Retornar o generos
    genres = api.get(local.API_URL_GENRES, params)


    context = {
        'app'   : 'explore',

        'genre' : genre,
        'sort'  : sort,

        'genres': genres.get('genres'),

        'items'      : items,
        'total_items': result.get('total_results'),
        'total_pages': result.get('total_pages'),
    }
    return render(request, 'explore.html', context)
