#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Teste
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/02
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
import unittest
from json import dumps, loads
from webmain import application
from webtest import TestApp
#from webob import Request, Response
import database
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class TestPyndo_Web(unittest.TestCase):
    GAMELIST = ['_JPT_game1', '_JPT_game2']
    STUDIO = "/rest/studio/%s?type=%d"
    GAMEBUILD = [dict(obj='img', o_x=1, o_y=2), dict(obj='img', o_x=3, o_y=4)]
    WEB_GAME = '/storage/jeppeto/persist__/%s' % '_JPT_game1'
    MENUITEM = '/irest/studio/%s?size=N'

    def setUp(self):
        database.DRECORD = database.Banco(lambda: TinyDB(storage=MemoryStorage))
        database.GRECORD = database.Banco(lambda: TinyDB(storage=MemoryStorage))
        database.GRECORD["j_e_p_p_e_t_o__"] = []
        self.app = TestApp(application)
        pass

    def test_main(self):
        """retorna o html do jeppeto."""
        result = self.app.get('/')
        #db = database.DRECORD['adm1n']
        #assert 'date'in db, 'no time in %s' % db
        assert result.status == '200 OK'
        assert '">umidqualquer</div>' in result.body, 'no admin in %s' % result.body
        pass

    def test_load_empty_game_list(self):
        """recupera lista de games vazia."""
        result = self.app.get('/storage/jeppeto/persist__/j_e_p_p_e_t_o__')
        assert result.status == '200 OK'
        assert ': []' in result.body, 'no empty list value in %s' % result.body

    def test_load_game_list(self):
        """recupera lista de games."""
        result = self._store_game_list()
        result = self.app.get('/storage/jeppeto/persist__/j_e_p_p_e_t_o__')
        assert result.status == '200 OK'
        assert TestPyndo_Web.GAMELIST[0] in result.body, 'no game in game list: %s' % result.body

    def test_load_prop_list(self):
        """recupera lista de props."""
        result = self.app.get(TestPyndo_Web.STUDIO % ('EICA', 1))
        assert result.status == '200 OK'
        assert 'Astro' in result.body, 'no prop in game list: %s' % result.body

    def test_load_scene_list(self):
        """recupera lista de cenários."""
        result = self.app.get(TestPyndo_Web.STUDIO % ('EICA', 2))
        assert result.status == '200 OK'
        assert 'TIAE' in result.body, 'no prop in game list: %s' % result.body

    def _store_game(self):
        """salva game construído."""
        data = dict(_xsrf=1234, value=dumps(TestPyndo_Web.GAMEBUILD))
        url = TestPyndo_Web.WEB_GAME
        return self.app.post(url, data)
        #return self.app.post_json(url, data)

    def _store_game_list(self):
        """salva lista de games GAMELIST."""
        data = dict(_xsrf=1234, value=dumps(TestPyndo_Web.GAMELIST))
        return self.app.post('/storage/jeppeto/persist__/j_e_p_p_e_t_o__', data)
        #return self.app.post_json('/storage/jeppeto/persist__/j_e_p_p_e_t_o__', data)

    def test_load_game(self):
        """recupera game construído."""
        result = self._store_game()
        url = TestPyndo_Web.WEB_GAME
        result = self.app.get(url)
        assert result.status == '200 OK'
        for gamebuild in ["\"%s\": %s" % it for it in TestPyndo_Web.GAMEBUILD[0].items()][0]:
            assert gamebuild in result.body, 'no gamebuild %s in retrieved game: %s' % (gamebuild, result.body)

    def test_store_game(self):
        """salva game construído."""
        result = self._store_game()
        assert result.status == '200 OK'
        try:
            gamelist = database.GRECORD[TestPyndo_Web.GAMELIST[0]]
        except IndexError as ie:
            assert False, ie
        assert TestPyndo_Web.GAMEBUILD[0] in gamelist, 'no games %s in game list: %s' % (result.body, gamelist)

    def test_store_game_list(self):
        """salva lista de games GAMELIST."""
        result = self._store_game_list()
        assert result.status == '200 OK'
        gamelist = database.GRECORD['j_e_p_p_e_t_o__']
        assert TestPyndo_Web.GAMELIST[0] in gamelist, 'no games %s in game list: %s' % (result.body, gamelist)

    def test_load_image(self):
        """recupera imagem."""
        image = loads(self.app.get(TestPyndo_Web.STUDIO % ('EICA', 1)).body)
        url = TestPyndo_Web.MENUITEM % image['value'][0]
        result = self.app.get(url)
        assert result.status == '200 OK'
        assert len(result.body) > 2000, 'no image in retrieved body: %s' % result.body


if __name__ == '__main__':
    unittest.main()
