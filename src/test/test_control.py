#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Teste
############################################################

:Author: *Carlo E. T. Oliveira*
:Author: *Erica Nogueira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/10
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
import unittest
import model
from visual import Builder
from visual import Gui
from mock import MagicMock, ANY
ITEM = 'it3m'


class Matcher:
    def __init__(self, **matcher):
        self.matcher = matcher

    def __eq__(self, other):
        print('matcher', other)
        return other == self.matcher


class TestPyndoramaControl(unittest.TestCase):

    def setUp(self):

        class Brython:
            def __init__(self):
                self.DOC, self.SVG, self.HTML, self.AJAX = [self]*4
                self.doc = self
                self.cookie = '_xsrf=123456; '
                self.WIN, self.STORAGE, self.JSON, self.TIME = [self]*4
                self.__getitem__ = self.DIV = self.div = self.IMG = self.nop
                self.div = self.img = self.deploy = self.employ = self.nop
                self.show_front_menu = self.screen_context = self.nop
                self.menuX = self.menuY = 0
                self.Id = self.search = ''
                self.location = self.target = self
                self.items = self.evs = []

            def activate(self, **kwargs):
                self.aargs = kwargs

            def bind(self, ev, hook):
                self.evs.append(hook)
                return self
                return self

            def nop(self, *args, **kwargs):
                return self

        class _Gui(dict):

            def employ(self, **kwargs):
                print('setUp employ')
                self['adm1n'].update(kwargs)
                return 'adm1n', 0001

        self.control = model.init()
        self.br = Brython()
        self.app = Gui(self.br)
        self.builder = Builder(self.br, self.control)
        self.builder.build_all(self.app)
        self.gui = _Gui()
        self.gui['adm1n'] = {}

    def _action_load(self):
        """load an action."""
        self.employ = MagicMock()
        self.control.activate(self.employ, **L0)
        self.control.activate(self.gui.employ, **AM)
        self.gui['adm1n'] = {}
        self.control.activate(self.gui.employ, **JEP0["JAC"])

    def test_action_load(self):
        """test load an action."""
        self._action_load()
        print ('self.control', self.control)
        self.employ.assert_called_once_with(**L0)
        assert self.gui['adm1n']["o_Id"] == "o1_jeppeto/ampu.png", 'no admin in %s' % self.gui['adm1n']
        things = {'o1_jeppeto/ampu.png', 'o1_EICA/1_1c.jpg', 'o1_o1_EICA/1_1c.jpg'}
        assert things <= set(self.control.ALL_THINGS.keys()), self.control.ALL_THINGS.keys()
        assert len(self.control.items) == 1, 'Not one member in items %s' % self.control.items
        assert self.control.current.o_Id == 'o1_EICA/1_1c.jpg', 'Not current locus %s' % self.control.current.o_Id
        register_value = MagicMock()
        self.control.deploy(register_value)
        register_value.assert_called_with(**AM)
        pass

    def _nest_action_baloon(self):
        """test baloon action."""
        self._action_load()
        self.br.stopPropagation = self.br.preventDefault = self.br.nop
        self.br.style = self.br.win = self.br
        self.br.display = self.br.clientX = self.br.clientY = 0
        self.br.pageXOffset = self.br.pageYOffset = 0
        self.br.offsetTop = self.br.offsetLeft = 0
        self.br.id = 'm_balao'
        self.br.oncontextmenu(self.br)
        self.br.evs[0](self.br)
        self.control.employ = MagicMock()
        #self.control.employ.assert_called_once_with(1,2)
        assert self.br.aargs["o_Id"] == "o1_balao", 'no balao in %s' % self.br.aargs
        pass

    def test_action_execute(self):
        """test execute an action."""
        self._action_load()
        self.gui['adm1n'] = {}
        self.control.activate(o_emp=self.gui.employ, o_Id="o1_jeppeto/ampu.png", o_cmd='DoExecute')
        assert self.gui['adm1n']["o_Id"] == "o1_EICA/1_1c.jpg", 'no admin in %s' % self.gui['adm1n']
        assert self.gui['adm1n']["o_gcomp"] == "up", 'no admin in %s' % self.gui['adm1n']

    def test_save_remote(self):
        """test save remote."""
        self._action_load()
        self.app.game = "Jeppeto_0"
        self.app.json = self.br
        self.br.dumps = lambda x: str(x)
        self.app.storage = MagicMock(name='store')
        self.app.send = MagicMock(name='send')
        self.builder.jenu.menu_salvar(None, None)
        value = dict(_xsrf='123456', value='[%s, %s]' % (str(L0), str(AM)))
        url = 'https://activufrj.nce.ufrj.br/storage/jeppeto/_JPT_Jeppeto_0/__persist__'
        self.app.send.assert_called_once_with(url, ANY, ANY, value)

    def test_game_start(self):
        """test show start screen."""
        event = MagicMock(name='event')
        div_eff = MagicMock(name='div_effect')
        self.br = MagicMock(name='gui')
        self.br.JSON.loads = lambda x=0: ['a_game']
        self.app = Gui(self.br)
        ids = [
            0, '__ROOT__', 'ad_objeto', 'ad_cenario', 'navegar', 'pular', 'mostrar',
            'ob_ctx', 'tx_ctx', 'jeppeto', 'wiki', '_JPT_a_game', '_JPT_jpt_0', '_JPT_g'
        ]

        def side_effect(a, b, c, d, e):
            assert a == URLJEPPETO, 'but url was %s' % a
            assert e == "GET"
            assert d == {'_xsrf': '', 'value': []}, 'but data was %s' % d
            self.app.games = ['jpt_0', 'g']

        def div_effect(a=0, b=0, c=0, s_top=0, s_display=0, s_left=0, s_width=0,
                       s_position=0, s_border=0, o_Id=0, s_color=0, s_fontSize=0,
                       s_fontFamily=0):
            assert o_Id in ids, 'but id was %s' % o_Id
            return div_eff
        #self.app._remote_load = MagicMock(name='rl', side_effect=side_effect)
        self.app.send = MagicMock(name='send', side_effect=side_effect)
        self.app.div = MagicMock(name='div', side_effect=div_effect)
        self.builder = Builder(self.br, self.control)
        self.builder.build_all(self.app)
        self.app.start(event)
        self.app.send.assert_called_once()
        self.app.div.assert_called()

if __name__ == '__main__':
    unittest.main()
URLJEPPETO = 'https://activufrj.nce.ufrj.br/storage/jeppeto/__J_E_P_P_E_T_O__/__persist__'
L0 = dict(s_top=0, s_left=0, o_gcomp='div',
          s_background='url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_1c.jpg?size=G) no-repeat',
          s_width=1100, o_placeid='book', o_item='EICA/1_1c.jpg', o_part='Locus', s_height=800,
          s_position='absolute', s_backgroundSize='100% 100%', o_place=None, o_Id='o1_EICA/1_1c.jpg')
AM = dict(s_top=187, s_left=444, s_float='left', o_gcomp='img', o_placeid='o1_EICA/1_1c.jpg',
          o_item='jeppeto/ampu.png', o_part='Holder', o_place=None, s_position='absolute',
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
