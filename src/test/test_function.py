#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Functional Test - Go trhough server
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/05
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
import unittest
import model
import json
from visual import Builder
from visual import Gui, LOADPAGE, SAVEPAGE, NEWPAGE, GAMELIST, SAVEGAMELIST, JEPPETO
from mock import MagicMock, ANY
from json import dumps, loads
from webmain import application
from webtest import TestApp
import database
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

LOAD = LOADPAGE % ('jeppeto', '_JPT_Jeppeto_1')
ED, EL = {}, []


class TestPyndoramaFunctional(unittest.TestCase):

    def setUp(self):

        class Brython(dict):
            def __init__(self):
                dict.__init__({})
                self.DOC, self.SVG, self.HTML, self.AJAX = [self]*4
                self.doc = dict(base=self)
                self['base'] = self['book'] = self
                self.cookie = '_xsrf=123456; '
                self.WIN, self.STORAGE, self.JSON, self.TIME = [self]*4
                self.__getitem__ = self.DIV = self.div = self.IMG = self.nop
                self.div = self.img = self.deploy = self.employ = self.nop
                self.show_front_menu = self.screen_context = self.nop
                self.aler = self.prom = self.conf = self.nop
                self.offsetLeft = self.offsetTop = self.menuX = self.menuY = 1
                self.Id = self.search = ''
                self.location = self.target = self
                self.aargs = self.items = self.evs = []

            def __le__(self, other):
                """
                shades brython append operator
                """
                pass

            def activate(self, **kwargs):
                self.aargs = kwargs

            def bind(self, ev, hook):
                self.evs.append(hook)
                return self

            def nop(self, *args, **kwargs):
                return self

            def __call__(self, *args, **kwargs):
                return self

        class _Gui(dict):

            def employ(self, **kwargs):
                print('setUp employ')
                #self['adm1n'].update(kwargs)
                return 'adm1n', 1

        def send(url, record=lambda text: None, terr=lambda text, y='': None, data=ED, method="POST"):
            if method == "POST":
                requisition = self.serv.post(url, data)
            else:
                requisition = self.serv.get(url)
                print("requisition", type(requisition.body))

            if  "200" in requisition.status or requisition.status == 0 and requisition.body:
                print ("send status %s body: %s" % (requisition.status, requisition.body))
                record(requisition.body)
            else:
                print ("send error %s : %s" % (requisition.status, requisition.body))
                terr("error %s" % requisition.status, requisition)

        self.control = model.init()
        self.br = Brython()
        self.br.dumps = json.dumps
        self.br.loads = json.loads
        self.app = Gui(self.br)
        self.app._locate = self.app._filter = MagicMock(name='locate')
        self.app.menuX = self.app.menuY = 1
        self.builder = Builder(self.br, self.control)
        self.builder.build_all(self.app)
        self.gui = _Gui()
        self.gui['adm1n'] = {}
        Gui.REV = {}
        self.control.ALL_THINGS = model.Thing.ALL_THINGS = {}
        self.control.items = []
        # Server setup
        self.app.send = send
        self.serv = TestApp(application)
        database.GRECORD = database.Banco(lambda: TinyDB(storage=MemoryStorage))
        database.GRECORD["j_e_p_p_e_t_o__"] = []
        database.GRECORD["_JPT_Jeppeto_0"] = JSON_LOADER

    def _action_load(self):
        """load an action."""
        self.employ = MagicMock()
        self.control.activate(self.employ, **L0)
        self.control.activate(self.employ, **AM)
        #self.gui['adm1n'] = {}
        #self.control.activate(self.employ, **JEP0["JAC"])

    def nest_action_load(self):  # todo: fix this test
        """test load an action."""
        COMP = [dict(AM), dict(L0)]
        [i.update(o_place=None) for i in COMP]

        def eff(**kwargs):
            cmpr = COMP.pop()
            assert kwargs == cmpr, 'but action were %s -AND- %s' % (kwargs, cmpr)

        self._action_load()
        print('self.control', self.control)
        self.employ.side_effect = eff
        self.employ.assert_called_once()
        #assert self.gui['adm1n']["o_Id"] == "o1_jeppeto/ampu.png", 'no admin in %s' % self.gui['adm1n']
        things = {'o1_jeppeto/ampu.png', 'o1_EICA/1_1c.jpg', 'o1_o1_EICA/1_1c.jpg'}
        assert things <= set(self.control.ALL_THINGS.keys()), self.control.ALL_THINGS.keys()
        assert len(self.control.items) == 1, 'Not one member in items %s' % self.control.items
        assert self.control.current.o_Id == 'o1_EICA/1_1c.jpg', 'Not current locus %s' % self.control.current.o_Id
        register_value = MagicMock(side_effect=lambda **k: eff(**k))
        #COMP = AM
        self.control.deploy(register_value)
        register_value.assert_called_once()
        pass

    def _remote_load(self):
        """fixture for loading from remote server."""
        self.br.on_complete = lambda x: None
        self.br.text = '{"status": 0, "value": "[\"GamesInteligentesII\",\"Jeppeto_1\",\"Jeppeto_0\"]"}'

        def do_call():
            self.br.on_complete(self.br)
        self.br.set_timeout = self.br.set_header = MagicMock()
        self.br.open = MagicMock(name='open')
        self.br.send = MagicMock(name='send', side_effect=lambda x: do_call())
        self.app.ajax = lambda: self.br  # MagicMock()

    def nest_remove_game(self):
        """remove a game locally and from remote server."""
        self.app.alert = MagicMock(name='alert')
        self.app.confirm = MagicMock(name='confirm', return_value=True)
        self.app.send = MagicMock(name='send', side_effect=lambda a, b, c, d, e: b('1 2 3'))
        self.app.remote_games = 'Jeppeto_0 Jeppeto_1 Jeppeto_2'.split()
        self.app.game = 'Jeppeto_0'
        self.builder.mmenu.menu_apagar_jogo(self.br, self.br)
        #self.app.remote_delete('Jeppeto_0')
        self.app.confirm.assert_called_once_with('Tem certeza que quer remover completamente Jeppeto_0 ?')
        self.app.send.assert_called_once_with(SAVEGAMELIST, ANY, ANY, ANY, 'POST')
        self.app.alert.assert_called_once_with('Arquivo Jeppeto_0 completamente removido com sucesso')
        bv, ks = {'Jeppeto_1', 'Jeppeto_2'}, json.loads(self.app.send.call_args[0][3]['value'])
        assert bv == set(ks), 'but %s not same as %s' % (bv, ks)
        self.app.confirm = MagicMock(name='newconfirm')
        self.app.remote_delete('NoNo')
        self.app.confirm.assert_called_once_with('Tem certeza que quer remover completamente NoNo ?')
        self.app.alert.assert_called_once_with('Arquivo Jeppeto_0 completamente removido com sucesso')

    def test_remote_load(self):
        """test load from remote server."""
        self.app.storage = MagicMock(name="storage")
        self.app.storage.__setitem__ = MagicMock(name="setitem")  # , side_effect=store)
        self.app.storage.__getitem__ = MagicMock(name="getitem", return_value="[\"Jeppeto_0\"]")
        self.app.doc = MagicMock(name="doc")
        self.app.doc.__setitem__ = MagicMock(name="docsetitem")  # , side_effect=store)
        self.app.doc.__getitem__ = MagicMock(name="docgetitem", return_value=self.app.doc)
        self.app.load('Jeppeto_0')

    def nest_remote_load(self):
        """test load from remote server."""

        def store(x, y):
            assert x == '_JPT_Jeppeto_1', 'but storage was %s %s' % (x, y)
        self._remote_load()
        self.br.status, self.br.text = 200, json.dumps(dict(status=0, value=JP0))
        #self.app.load('_JPT_g0')
        self.app.storage = MagicMock(name="storage")
        self.app.storage.__setitem__ = MagicMock(name="setitem")  # , side_effect=store)
        self.app.storage.__getitem__ = MagicMock(name="setitem", return_value="[\"Jeppeto_0\"]")
        self.br['_JPT_Jeppeto_0'] = JP0
        self._save_remote()
        self.app.load('Jeppeto_0')
        assert self.br.on_complete
        self.br.open.assert_called_once_with('GET', LOAD, True)
        self.br.send.assert_called_once_with({})
        assert self.app.remote_games == [], 'but remote_games was %s' % self.app.remote_games
        self.app.storage.__setitem__.assert_called_with(JEPPETO, '["Jeppeto_1", "Jeppeto_0"]')
        self.app.storage.__setitem__.assert_any_call('_JPT_Jeppeto_1', ANY)

    def nest_no_remote_local_load(self):
        """test load from local on remote server denial."""
        self._remote_load()
        self.app.storage = dict(_JPT_Jeppeto_1=json.dumps([LR]))
        self.br.status, self.br.text = 404, json.dumps(dict(status=0, value=[LR]))
        self.app.load('Jeppeto_1')
        assert self.br.on_complete
        self.br.open.assert_called_once_with('GET', LOAD, True)
        self.br.send.assert_called_once_with({})

    def _save_remote(self):
        """save remote."""
        Urle = SAVEPAGE % ('jeppeto', '_JPT_Jeppeto_0')  # '/rest/wiki/edit/jeppeto/_JPT_Jeppeto_0'
        Url = GAMELIST  # '/rest/wiki/edit/activlets/__J_E_P_P_E_T_O__'
        conts = ['', '[]', '["Jeppeto_0"]']
        urls = [Urle, NEWPAGE % ('jeppeto', '_JPT_Jeppeto_0'), Url]  # '/wiki/newpage/jeppeto?folder=', Url]
        import json

        def store_effect(key, value):
            assert 'o_gcomp' in value, 'but value was %s' % value
        self._action_load()
        self.app.game = "Jeppeto_0"
        self.app.games = ["Jeppeto_1"]
        self.app.json = self.br
        self.br.dumps = lambda x: json.dumps(x)
        self.app.storage = MagicMock(name='store', side_effect=store_effect)
        self.app.remote_save()

    def nest_save_remote(self):
        """test save remote."""
        self._save_remote()
        self.app.storage.__setitem__.assert_any_call(ANY, ANY)
        assert self.app.game in database.GRECORD["j_e_p_p_e_t_o__"],\
            "game %s not in database: %s " % (self.app.game, database.GRECORD["j_e_p_p_e_t_o__"])
        assert "EICA/1_1c.jpg" in dumps(database.GRECORD["_JPT_Jeppeto_0"]),\
            "game %s not in database: %s " % (self.app.game, database.GRECORD["_JPT_Jeppeto_0"][0])

    def nest_game_start(self):
        """test show start screen."""
        event = MagicMock(name='event')
        div_eff = MagicMock(name='div_effect')
        self.br = MagicMock(name='gui')
        self.br.__le__ = MagicMock()
        self.br.JSON.loads = lambda x=0: ['a_game']
        self.app = Gui(self.br)
        ids = [
            0, '__ROOT__', 'ad_objeto', 'ad_cenario', 'navegar', 'pular', 'mostrar',
            'ob_ctx', 'tx_ctx', 'jeppeto', 'wiki', '_JPT_a_game', '_JPT_jpt_0', '_JPT_g'
        ]

        def side_effect(a, b, c, d, e):
            assert a == GAMELIST, 'but url was %s' % a
            assert e == "GET"
            assert d == {'_xsrf': '', 'value': []}, 'but data was %s' % d
            #assert d == {'_xsrf': '', 'conteudo': '[]'}, 'but data was %s' % d
            self.app.games = ['jpt_0', 'g']

        def div_effect(a=0, b=0, c=0, s_top=0, s_display=0, s_left=0, s_width=0,
                       s_position=0, s_border=0, o_Id=0, s_color=0, s_fontSize=0,
                       s_fontFamily=0):
            assert o_Id in ids, 'but id was %s' % o_Id
            return div_eff
        #self.app._remote_load = MagicMock(name='rl', side_effect=side_effect)
        self.app.send = MagicMock(name='send', side_effect=side_effect)
        self.app.div = MagicMock(name='div', side_effect=div_effect)
        self.app.img = MagicMock(name='img')
        self.builder = Builder(self.br, self.control)
        self.builder.build_all(self.app)
        self.app.start(event)
        self.app.send.assert_called_once()
        self.app.div.assert_called_any()

if __name__ == '__main__':
    unittest.main()
JUMP = {'o_act': 'DoUp', 'o_gcomp': 'act', 'o_placeid': 'o1_EICA/1_1c.jpg', 'o_item': 'Eica01',
        'o_part': 'Action', 'o_acomp': 'up', 'o_Id': 'o1_EICA/1_1c.jpg'}
BALSAV = {'s_top': 0, 's_left': 0, 's_float': 'left', 'o_gcomp': 'text',
          's_width': 200, 'o_Id': 'o1_balao', 'o_item': 'balao', 's_height': 150, 'o_part': 'Holder',
          's_position': 'absolute', 'o_title': 'balao'}
BALOON = dict(o_text='Lorem Ipsum', s_top=0, s_left=0, o_gcomp='text', s_float='left',
              s_width=200, o_title='balao', o_item='balao', s_height=150, o_part='Holder',
              s_position='absolute', o_cmd='DoAdd', o_Id='o1_balao')
#URLJEPPETO = 'https://activufrj.nce.ufrj.br/storage/jeppeto/__J_E_P_P_E_T_O__/__persist__'
URLJEPPETO = '/rest/wiki/activlets/__J_E_P_P_E_T_O__'
JP0 = "[{\"o_Id\":\"o1_EICA/1_2c.jpg\",\"o_gcomp\":\"div\"}]"
JP1 = '"[{\"o_Id\":\"o1_EICA/1_2c.jpg\",\"o_gcomp\":\"div\",' + \
      '\"o_item\":\"EICA/1_2c.jpg\",\"o_part\":\"Locus\",\"s_background\":' + \
      '\"url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_2c.jpg?size=G) no-repeat\",' + \
      '\"s_backgroundSize\":\"100% 100%\",\"s_height\":800,\"s_left\":0,\"s_position\":\"absolute\",\"s_top\":0,' + \
      '\"s_width\":1100,\"o_placeid\":\"book\"}]"'
LR = {r's_top': 0, r's_left': 0, r'o_gcomp': r'div',
      r's_background': r'url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_1c.jpg?size=G) no-repeat',
      r's_width': 1100, r'o_Id': r'o1_EICA/1_1c.jpg', r'o_item': r'EICA/1_1c.jpg', r'o_part': r'Locus',
      r's_height': 800, r's_position': r'absolute', r's_backgroundSize': r'100% 100%', r'o_placeid': r'book'}
L0 = dict(
    s_top=0, s_left=0, o_gcomp='div',
    s_background='url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_1c.jpg?size=G) no-repeat',
    s_width=1100, o_Id='o1_EICA/1_1c.jpg', o_item='EICA/1_1c.jpg', o_part='Locus', s_height=800,
    s_position='absolute', s_backgroundSize='100% 100%', o_placeid='book')
AM = dict(s_top=187, s_left=444, s_float='left', o_gcomp='img', o_placeid='o1_EICA/1_1c.jpg',
          o_item='jeppeto/ampu.png', o_part='Holder', s_position='absolute',
          o_title='jeppeto/ampu.png', o_src='https: //activufrj.nce.ufrj.br/rest/studio/jeppeto/ampu.png?size=G',
          o_Id='o1_jeppeto/ampu.png')
JEP0 = dict(
    E1={
        "o_cmd": "DoAdd", "o_part": "Locus", "o_Id": "o1_EICA/1_1c.jpg",
        "s_background": "url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_1c.jpg?size=G) no-repeat",
        "s_width": 1100, "s_height": 800, "s_top": 0, "o_gcomp": "div", "s_backgroundSize": "100% 100%",
        "s_left": 0, "s_position": "absolute", "o_item": "EICA/1_1c.jpg", "o_placeid": "book"},
    E2={"o_cmd": "DoAdd", "o_part": "Locus", "o_Id": "o1_EICA/2_1c.jpg",
        "s_background": "url(https://activufrj.nce.ufrj.br/rest/studio/EICA/2_1c.jpg?size=G) no-repeat",
        "s_width": 1100, "s_height": 800, "s_top": 0, "o_gcomp": "div", "s_backgroundSize": "100% 100%",
        "s_left": 0, "s_position": "absolute", "o_item": "EICA/2_1c.jpg", "o_placeid": "book"},
    JAM={"o_Id": "o1_jeppeto/ampu.png", "o_gcomp": "img",
         "o_item": "jeppeto/ampu.png", "o_part": "Holder", "o_placeid": "o1_EICA/2_1c.jpg",
         "o_src": "https: //activufrj.nce.ufrj.br/rest/studio/jeppeto/ampu.png?size=G",
         "o_title": "jeppeto/ampu.png", "s_float": "left", "s_left": 444,
         "s_position": "absolute", "s_top": 187, "o_cmd": "DoAdd"},
    JAC={"o_cmd": "DoAdd", "o_part": "Action", "o_Id": "o1_o1_EICA/1_1c.jpg", "o_gcomp": "act",
         "o_act": "DoUp", "o_acomp": "up", "o_item": "o1_EICA/1_1c.jpg", "o_placeid": "o1_jeppeto/ampu.png"}
)
JSON_LOADER = [
    dict(s_background='url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_1c.jpg?size=G) no-repeat',
         s_width=1100, o_placeid='book', o_item='EICA/1_1c.jpg', o_part='Locus', s_height=800, s_position='absolute',
         s_backgroundSize='100% 100%', s_top=0, s_left=0, o_gcomp='div', o_Id='o1_EICA/1_1c.jpg'),
    dict(s_top=187, s_left=444, o_gcomp='sprite', s_float='left', o_placeid='o1_EICA/1_1c.jpg', o_item='jeppeto/ampu.png',
         o_part='Holder', s_position='absolute', o_title='jeppeto/ampu.png',
         o_src='https: //activufrj.nce.ufrj.br/rest/studio/jeppeto/ampu.png?size=G', o_Id='o1_jeppeto/ampu.png'),
    dict(o_act='DoUp', o_gcomp='act', o_placeid='o1_EICA/1_1c.jpg', o_item='Eica01', o_part='Action',
         o_acomp='up', o_Id='o1_o1_EICA/1_1c.jpg')]