#!/usr/bin/env python
# -*- coding: utf-8 -*-


def template(request):

    return {
        'URL_CURRENT'   : request.get_full_path(),
        'URL_POSTER'    : '//image.tmdb.org/t/p/w154', #w92
        'URL_POSTER_BIG': '//image.tmdb.org/t/p/w500',
        'URL_BACKDROP'  : '//image.tmdb.org/t/p/w1280',
        'URL_IMG_ERROR' : '//placehold.it/150x225&text=Sem+imagem',

        'URL_IMDB_MOVIE': 'http://www.imdb.com/title/',
    }
