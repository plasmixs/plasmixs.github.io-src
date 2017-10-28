#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Ramesh D'
SITENAME = 'Plasmixs'
SITEURL = 'http://plasmixs.github.io'
TIMEZONE = 'Asia/Calcutta'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_RSS = 'feeds/all.rss.xml'

# Social widget
SOCIAL = (('rss', 'http://plasmixs.github.io/feeds/all.rss.xml'),)

DEFAULT_PAGINATION = 10

OUTPUT_PATH = '/Mysite/plasmixs.github.io'

THEME = '/Mysite/themes/pelican-bootstrap3'
BOOTSTRAP_FLUID = True
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

PLUGIN_PATHS = ['/Mysite/plugins']
PLUGINS = ['tag_cloud', 'related_posts', 'tipue_search', 'summary', 'sitemap', 'i18n_subsites']

DIRECT_TEMPLATES = ['index', 'archives', 'search']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

DISPLAY_CATEGORIES_ON_MENU=False

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = [".git"]

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

NEWEST_FIRST_ARCHIVES = True

DISQUS_SITENAME = "plasmixs"
DISQUS_NO_ID = True

GOOGLE_ANALYTICS = 'UA-76217567-1'

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

CC_LICENSE="CC-BY"

