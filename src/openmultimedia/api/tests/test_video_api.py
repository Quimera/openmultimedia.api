# -*- coding: utf-8 -*-

import json
import unittest2 as unittest
import urllib

from copy import deepcopy

from zope.component import getUtility
from zope.component import getMultiAdapter

from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser

from Products.CMFCore.utils import getToolByName

from openmultimedia.api.interfaces import IVideoAPI

from openmultimedia.api.testing import INTEGRATION_TESTING
#from openmultimedia.api.testing import setupTestContent

class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pc = getToolByName(self.portal, 'portal_catalog')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.video_api = getUtility(IVideoAPI)

        self.test_url = ("http://multimedia.tlsur.net/api/clip/vallejo-"
                         "el-conflicto-debe-resolverse-con-los-"
                         "estudiantes/?detalle=completo")

    def test_get_json(self):
        results = self.video_api.get_json(self.test_url)
        self.assertIs(type(results), dict)
        results = self.video_api.get_json("http://www.google.com")
        self.assertIs(results, None)

    def test_get_widgets(self):
        today = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                          'cmswidgets/cmswidgets.html?widget=mas_vistos'
                          '&amp;tiempo=dia'),
                 'title': u'Most seen today'}
        week = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                          'cmswidgets/cmswidgets.html?widget=mas_vistos'
                          '&amp;tiempo=semana'),
                 'title': u'Most seen this week'}
        month = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                          'cmswidgets/cmswidgets.html?widget=mas_vistos'
                          '&amp;tiempo=mes'),
                 'title': u'Most seen this month'}
        year = {'url': (u'http://multimedia.telesurtv.net/media/video/'
                          'cmswidgets/cmswidgets.html?widget=mas_vistos'
                          '&amp;tiempo=ano'),
                 'title': u'Most seen this year'}

        results = self.video_api.get_videos_most_seen_widgets(['today'])

        self.assertIn(today, results)
        self.assertNotIn(week, results)
        self.assertNotIn(month, results)
        self.assertNotIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['today',
                                                               'week'])

        self.assertIn(today, results)
        self.assertIn(week, results)
        self.assertNotIn(month, results)
        self.assertNotIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['today',
                                                               'week',
                                                               'month'])

        self.assertIn(today, results)
        self.assertIn(week, results)
        self.assertIn(month, results)
        self.assertNotIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['today',
                                                               'week',
                                                               'month',
                                                               'year'])

        self.assertIn(today, results)
        self.assertIn(week, results)
        self.assertIn(month, results)
        self.assertIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['week',
                                                               'month',
                                                               'year'])

        self.assertNotIn(today, results)
        self.assertIn(week, results)
        self.assertIn(month, results)
        self.assertIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['month',
                                                               'year'])

        self.assertNotIn(today, results)
        self.assertNotIn(week, results)
        self.assertIn(month, results)
        self.assertIn(year, results)

        results = self.video_api.get_videos_most_seen_widgets(['year'])

        self.assertNotIn(today, results)
        self.assertNotIn(week, results)
        self.assertNotIn(month, results)
        self.assertIn(year, results)

    def test_get_video_widget_url(self):
        results = self.video_api.get_video_widget_url(self.test_url)

        self.assertEqual(results, (u"http://multimedia.telesurtv.net/"
                                    "player/insertar.js?archivo=clips/"
                                    "telesur-video-2011-10-14-201605224901"
                                    ".mp4&amp;width=400"))

    def test_get_video_thumb(self):
        results = self.video_api.get_video_thumb(self.test_url)
        self.assertEqual(results, (u"http://media.tlsur.net/cache/10/f9/"
                                    "10f910a49e6a261276f90d920063eede.jpg"))

    def test_get_section_last_videos(self):

        url = ("http://multimedia.telesurtv.net/media/video/cmswidgets/videos"
               ".html?widget=ultimos_seccion&amp;seccion_plone=")

        categories_list = ['latinoamerica', 'vuelta-al-mundo', 'deportes',
                           'ciencia', 'cultura', 'salud', 'tecnologia']

        for i in categories_list:
            result = self.video_api.get_latest_from_section_video_widget(i)
            self.assertEqual(result, url+i)

    def test_get_basic_clip_list(self):

        result = self.video_api.get_basic_clip_list()
        self.assertEqual(result,
                         (u'http://multimedia.tlsur.net/api/clip/?'
                           'detalle=basico'))

        result = self.video_api.get_basic_clip_list(limit=10)
        self.assertEqual(result,
                         (u'http://multimedia.tlsur.net/api/clip/?'
                           'limit=10&detalle=basico'))

        result = self.video_api.get_basic_clip_list(offset=10, limit=10)
        self.assertEqual(result,
                         (u'http://multimedia.tlsur.net/api/clip/?'
                           'limit=10&detalle=basico&offset=10'))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
