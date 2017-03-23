# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

'''
css = Bundle(
    'libs/semantic/dist/semantic.min.css',
    'css/style.css','css/reset.css',
    filters='cssmin',
    output='public/css/common.css'
)
'''
css = Bundle(
    'libs/semantic/dist/semantic.min.css',
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'libs/jQuery/dist/jquery.js',
    'libs/semantic/dist/semantic.min.js',
    'js/plugins.js','js/main.js','js/modernizr.js',
    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
