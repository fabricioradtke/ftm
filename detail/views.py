#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from datetime         import datetime, time
from core.api         import Api
import local


def detail(request, id):
    api = Api(request)

    params = {
        'api_key'           : local.API_KEY,
        'language'          : request.LANGUAGE_CODE,
        'append_to_response': 'videos,images,similar'
    }
    item = api.get(local.API_URL_MOVIE % id, params)

    if item:
        # Passar o release_date para datetime
        try:
            item['release_date_dt'] = datetime.strptime(item.get('release_date'), '%Y-%m-%d').date()
        except Exception as e:
            pass

        # Passar o runtime para datetime
        runtime = item.get('runtime')

        if type(runtime) == int:
            ttime = runtime / 60, runtime % 60
            item['runtime_dt'] = time(ttime[0], ttime[1])

        # Passar o release_date dos sililares para datetime
        similars = item.get('similar', {}).get('results', [])

        for similar in similars:
            try:
                similar['year'] = datetime.strptime(similar.get('release_date'), '%Y-%m-%d').year
            except Exception as e:
                #pass
                raise Exception(e)


    context = {
        'app' : 'detail',

        'item': item,
    }
    return render(request, 'detail.html', context)
