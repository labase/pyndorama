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
from operator import __setitem__
from ossaudiodev import control_labels
import unittest
import model
import json
from visual import Builder
from visual import Gui, LOADPAGE, SAVEPAGE, NEWPAGE, GAMELIST, SAVEGAMELIST, JEPPETO
from defer import return_value
from mock import MagicMock, ANY
#ITEM = 'it3m'

LOAD = LOADPAGE % ('jeppeto', '_JPT_Jeppeto_1')


class TestPyndoramaControl(unittest.TestCase):

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
                self['adm1n'].update(kwargs)
                return 'adm1n', 1

        self.control = model.init()
        self.br = Brython()
        self.br.dumps = json.dumps
        self.br.loads = json.loads
        self.app = Gui(self.br)
        self.app.menuX = self.app.menuY = 1
        self.builder = Builder(self.br, self.control)
        self.builder.build_all(self.app)
        self.gui = _Gui()
        self.gui['adm1n'] = {}
        Gui.REV = {}
        self.control.ALL_THINGS = model.Thing.ALL_THINGS = {}
        self.control.items = []

    def _action_load(self):
        """load an action."""
        self.employ = MagicMock()
        self.control.activate(self.employ, **L0)
        self.control.activate(self.employ, **AM)
        #self.gui['adm1n'] = {}
        #self.control.activate(self.employ, **JEP0["JAC"])

    def _add_locus(self):
        """ adds a new locus."""
        self.br.id, self.app.game = 'idEica01', '_JPT_g0'
        self.app.storage = dict(_JPT__JPT_g0=json.dumps([LR]))

        def eff(**kw):
            assert 2424 in kw, 'but not in %s' % kw
        self.br.DIV = MagicMock(name='div', side_effect=eff)
        self.builder.jenu.ad_cenario(self.br, self.br)

    def _add_baloon(self):
        """ adds a new baloon."""
        mock_prop = self.mp = MagicMock(name='prop')
        mock_prop.bind = MagicMock(name='prop_bind', side_effect=lambda ev, hook: hook(mock_prop))
        self.control.current = self.control  # MagicMock(name='curr')  # self.br
        mock_shape = self.app.shape = MagicMock(name='shape')
        self.mc_doc = self.app.doc = MagicMock(name='doc')  # self.br
        #mc_doc.__getitem__ = MagicMock(name='doc_set', return_value=mock_prop)
        self.app.doc.__getitem__ = MagicMock(name='doc_set', side_effect=lambda x: self.mp)
        mock_store = self.app.storage = MagicMock(name='store')
        mock_store_get = self.app.storage.__getitem__ = MagicMock(name='store_get', return_value="[]")
        mock_store_set = self.app.storage.__setitem__ = MagicMock(name='store_set')
        self.br.id, self.br.o_Id, self.app.game = 'idEica01', 'idEica01', '_JPT_g0'

        def eff(**kw):
            bv, ks = set(BALOON.values()), set(kw.values())
            assert bv < ks, 'but %s not in %s' % (bv, ks)
            activate(**kw)
        self.the_div = MagicMock(name='div')
        self.the_div.html = "Lorem isum"
        self.app.div = MagicMock(name='div_call', side_effect=lambda *a, **x: self.the_div)  # , side_effect=eff)
        #activate, self.app.control.activate = self.app.control.activate, MagicMock(name='act', side_effect=eff)

    def _result_test(self, the_item, container=None, app_op=None, item_id='o1_balao', savdict={}, extra=[]):
        container = container or self.control.items
        assert len(container) >= 1, 'but ALL_THINGS is %s ' % container
        assert item_id in the_item.o_Id, 'but item id is %s but given is %s ' % (the_item.o_Id, item_id)
        #assert self.app.control.activate.assert_any_called()
        app_op = app_op or self.app.div
        if savdict != {}:
            app_op.assert_any_called()
            bv, ks = set(savdict.values()), set(app_op.call_args[1].values())
            assert bv < ks, 'but %s not in %s' % (bv, ks)
        #container = self.app.control.items
        self.app.doc.__getitem__.assert_any_called()
        self.app.storage.__getitem__.assert_any_call('_JPT__JPT_g0')
        self.app.storage.__setitem__.assert_any_call('_JPT__JPT_g0', ANY)
        bv, ks = set(list(savdict.values())+extra), self.app.storage.__setitem__.call_args[0][1]
        assert bv < set(json.loads(ks)[0].values()), 'but %s not in %s' % (bv, set(json.loads(ks)[0].values()))
        #assert False, 'but mc was %s' % self.mp.mock_calls
        savargs = {}
        saver = MagicMock(name='saver', side_effect=lambda **kw: savargs.update(kw))
        the_item.deploy(saver)
        bv, ks = set(savdict.values()), set(savargs.values())
        assert bv < ks, 'but %s not in %s' % (bv, savargs)

    def test_add_baloon(self):
        """test adds a new baloon."""
        self._add_baloon()
        self.builder.mmenu.menu_balao(self.br, self.br)
        self.mp.bind.assert_called_once_with('click', ANY)
        self._result_test(the_item=self.app.control.items[0], savdict=BALSAV)

    def test_add_jump(self):
        """test adds a jump action."""
        self._add_baloon()
        self._action_load()
        self.app.obj_id = 'o1_EICA/1_1c.jpg'
        self.app.act = MagicMock(name='mock_act')
        self.builder.mmenu.pular(self.br, self.br)
        #self.app.act.assert_any_call()
        item_id = 'o1_o1_EICA/1_1c.jpg'
        jump = self.control.ALL_THINGS[item_id]
        self._result_test(the_item=jump, container=model.Thing.ALL_THINGS, app_op=self.app.act,
                          item_id=item_id, savdict=JUMP)

    def test_add_hide(self):
        """test adds a hide action."""
        self._add_baloon()
        self._action_load()
        self.app.obj_id = 'o1_EICA/1_1c.jpg'
        self.app.shape = MagicMock(name='mock_act')
        self.builder.mmenu.menu_esconder(self.br, self.br)
        #self.app.act.assert_any_call()
        item_id = 'o1_jeppeto/ampu.png'
        #assert False, 'items %s things %s' % (self.control.items[0].items[0], self.control.ALL_THINGS)
        jump = self.control.items[0].items[0]
        self._result_test(the_item=jump, container=model.Thing.ALL_THINGS, app_op=self.app.shape, item_id=item_id,
                          extra=['o1_EICA/1_1c.jpg', '0.1', 'Holder', 'jeppeto/ampu.png',
                                 'shape', 'absolute', 'DoShape', 'o1_jeppeto/ampu.png'])

    def test_save_action(self):
        """test saves a jump action."""
        self._add_baloon()
        self._action_load()
        #assert False,'self.control.ALL_THINGS.keys() %s' % self.control.ALL_THINGS.keys()
        place = 'o1_jeppeto/ampu.png'
        self.app.obj_id = place
        #self.app.obj_id = 'o1_pl_Eica01'
        self.app.act = MagicMock(name='mock_act')
        self.app.save = MagicMock(name='mock_save')
        self.builder.mmenu.pular(self.br, self.br)
        #self.app.act.assert_any_call()
        #jump = self.control.ALL_THINGS['o1_Eica01']
        calls = [{'o1_'+place},{'o1_jeppeto/ampu.png'},{'o1_EICA/1_1c.jpg'}]
        def save(o_Id= '',**kwargs):
            _id = calls.pop()
            assert _id == set([o_Id]), 'but id %s was not %s' % (_id, set([o_Id]))

        employ = MagicMock(name='mock_save', side_effect=save)
        self.control.deploy(employ)
        #employ.assert_any_call(ANY)
        employ_calls = employ.call_args_list
        #self.app.act.assert_any_call()
        #self.app.save.assert_called_once_with()
        assert self.control.current.o_Id =='o1_EICA/1_1c.jpg', 'but current id was %s' % self.control.current.o_Id
        #assert employ_calls == '', 'but employ_calls was %s' % str(employ_calls)

    def test_edit_baloon(self):
        """test edit an existing baloon."""
        self._add_baloon()
        self.the_div.html = "Sic Amet"
        self.builder.mmenu.menu_balao(self.br, self.br)
        self.mp = MagicMock(name='edit_prop')
        self.mp.html = "Sic Amet"
        self.mp.id = 'o1_balao'
        self.builder.mmenu.menu_editar(self.br, self.br)
        self.mp.bind.assert_called_once_with('click', ANY)
        baloon=self.app.control.items[0]
        self._result_test(the_item=baloon, container=self.app.control.items,
                          item_id='o1_balao', savdict=BALSAV, extra=["Sic Amet"] )

    def test_add_locus(self):
        """test adds a new locus."""
        self._add_locus()
        assert 'o1_Eica01' in self.br.DIV.call_args[1]['Id'], self.br.DIV.call_args[1]['Id']
        loci = self.control.items
        assert len(loci) == 1, 'but items was %s' % loci
        assert loci[0].o_Id == 'o1_Eica01', 'but id was %s' % loci[0].o_Id

    def _add_object(self):
        """adds a new holder object."""
        self._add_locus()
        self.br.id, self.app.game = 'idEica01', '_JPT_g0'
        self.app.storage = dict(_JPT__JPT_g0=json.dumps([LR]))

        def eff(**kw):
            assert 2424 in kw, 'but not in %s' % kw
        self.br.IMG = MagicMock(name='img', side_effect=eff)
        act, self.control.activate = self.control.activate, MagicMock(name='act')
        self.control.activate.side_effect = lambda **kw: act(**kw)
        self.builder.jenu.ad_objeto(self.br, self.br)

    def test_add_object(self):
        """test adds a new holder object."""
        self._add_object()
        self.control.activate.assert_called_any()
        #self.br.IMG.assert_called_once_with()
        loci = self.control.items
        assert len(loci) == 1, 'but items was %s' % loci
        assert loci[0].o_Id == 'o1_Eica01', 'but id was %s' % loci[0].o_Id
        assert loci[0].items[0].o_Id == 'o2_Eica01', 'but id was %s' % loci[0].items[0].o_Id
        assert 'o2_Eica01' in self.br.IMG.call_args[1]['Id'], 'but call id was %s' % self.br.IMG.call_args[1]['Id']

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

    def test_remove_game(self):
        """remove a game locally and from remote server."""
        self.app.alert = MagicMock(name='alert')
        self.app.confirm = MagicMock(name='confirm', return_value=True)
        self.app.send = MagicMock(name='send', side_effect=lambda a,b,c,d,e: b('1 2 3'))
        self.app.remote_games = 'Jeppeto_0 Jeppeto_1 Jeppeto_2'.split()
        self.app.game = 'Jeppeto_0'
        self.builder.mmenu.menu_apagar_jogo(self.br, self.br)
        #self.app.remote_delete('Jeppeto_0')
        self.app.confirm.assert_called_once_with('Tem certeza que quer remover completamente Jeppeto_0 ?')
        self.app.send.assert_called_once_with(SAVEGAMELIST, ANY, ANY, ANY,'POST' )
        self.app.alert.assert_called_once_with('Arquivo Jeppeto_0 completamente removido com sucesso')
        bv, ks = set(['Jeppeto_1', 'Jeppeto_2']), json.loads(self.app.send.call_args[0][3]['value'])
        assert bv == set(ks), 'but %s not same as %s' % (bv, ks)
        self.app.confirm = MagicMock(name='newconfirm')
        self.app.remote_delete('NoNo')
        self.app.confirm.assert_called_once_with('Tem certeza que quer remover completamente NoNo ?')
        self.app.alert.assert_called_once_with('Arquivo Jeppeto_0 completamente removido com sucesso')

    def test_remote_load(self):
        """test load from remote server."""

        def store(x, y):
            assert x == '_JPT_Jeppeto_1', 'but storage was %s %s' % (x, y)
        self._remote_load()
        self.br.status, self.br.text = 200, json.dumps(dict(status=0, value=JP0))
        #self.app.load('_JPT_g0')
        self.app.storage = MagicMock(name="storage")
        self.app.storage.__setitem__ = MagicMock(name="setitem")  # , side_effect=store)
        self.app.storage.__getitem__ = MagicMock(name="setitem", return_value="[\"Jeppeto_0\"]")
        self.br['_JPT_Jeppeto_1'] = JP0
        self.app.load('Jeppeto_1')
        assert self.br.on_complete
        self.br.open.assert_called_once_with('GET', LOAD, True)
        self.br.send.assert_called_once_with({})
        assert self.app.remote_games == [], 'but remote_games was %s' % self.app.remote_games
        self.app.storage.__setitem__.assert_called_with(JEPPETO, '["Jeppeto_1", "Jeppeto_0"]')
        self.app.storage.__setitem__.assert_any_call('_JPT_Jeppeto_1', ANY)

    def test_no_remote_local_load(self):
        """test load from local on remote server denial."""
        self._remote_load()
        self.app.storage = dict(_JPT_Jeppeto_1=json.dumps([LR]))
        self.br.status, self.br.text = 404, json.dumps(dict(status=0, value=[LR]))
        self.app.load('Jeppeto_1')
        assert self.br.on_complete
        self.br.open.assert_called_once_with('GET', LOAD, True)
        self.br.send.assert_called_once_with({})

    def nest_action_execute(self):  # todo: fix this test
        """test execute an action."""
        self._action_load()
        self.gui['adm1n'] = {}
        self.control.activate(o_emp=self.gui.employ, o_Id="o1_jeppeto/ampu.png", o_cmd='DoExecute')
        assert False, 'no admin in %s' % self.gui['adm1n']
        assert self.gui['adm1n']["o_Id"] == "o1_EICA/1_1c.jpg", 'no admin in %s' % self.gui['adm1n']
        assert self.gui['adm1n']["o_gcomp"] == "up", 'no admin in %s' % self.gui['adm1n']

    def test_save_remote(self):
        """test save remote."""
        #Url = 'https://activufrj.nce.ufrj.br/storage/jeppeto/_JPT_Jeppeto_0/__persist__'
        Urle = SAVEPAGE % ('jeppeto', '_JPT_Jeppeto_0')  # '/rest/wiki/edit/jeppeto/_JPT_Jeppeto_0'
        Url = GAMELIST  # '/rest/wiki/edit/activlets/__J_E_P_P_E_T_O__'
        conts = ['', '[]', '["Jeppeto_0"]']
        urls = [Urle, NEWPAGE % ('jeppeto', '_JPT_Jeppeto_0'), Url]  # '/wiki/newpage/jeppeto?folder=', Url]
        import json

        def store_effect(key, value):
            assert 'o_gcomp' in value, 'but value was %s' % value

        def send_effect(url, func, funcb, value, tx=0):
            expected = urls.pop()
            assert expected == url, 'but url was %s against %s' % (url, expected)
            val = [L0, AM]
            expect_cont = conts.pop()
            if len(value['value']) > 20:
                value = json.loads(value['value'])
                #assert False, 'val, value %s %s' % (value, val)
                assert val[0] == value[0], 'but value was %s -AND- %s' % (value, val[0])
            else:
                assert value['value'] == expect_cont, \
                    'but value conteudo was %s against %s' % (value['value'], conts)
            func('um texto')
        self._action_load()
        self.app.game = "Jeppeto_0"
        self.app.games = ["Jeppeto_1"]
        self.app.json = self.br
        self.br.dumps = lambda x: json.dumps(x)
        self.app.storage = MagicMock(name='store', side_effect=store_effect)
        send = self.app.send = MagicMock(name='send', side_effect=send_effect)
        self.app.remote_save()
        send.assert_any_call(ANY, ANY, ANY, ANY, "POST")
        self.app.storage.__setitem__.assert_any_call(ANY, ANY)
        expected_count = 2
        assert send.call_count == expected_count, 'but send count was %s' % send.call_count

    def test_Menu_cenario(self):
        """test add a new scene."""
        #Url = 'https://activufrj.nce.ufrj.br/storage/jeppeto/_JPT_Jeppeto_0/__persist__'
        import json

        self.app.json = self.br
        self.br.id = 'jeppeto/thing'
        self.br.dumps = MagicMock(name='dumps')  # lambda x: json.dumps(x)
        self.br.loads = lambda x: json.loads(x)
        self.app.game = "jeppeto_0"
        self.app.storage = MagicMock(name='store')
        self.app.storage.__getitem__ = MagicMock(name='storeget', return_value="[]")
        self.builder.jenu.ad_cenario(self.br, None)
        self.br.dumps.assert_called_once()  # _with(0)
        assert self.control.items[0].o_gcomp == 'div', 'but items gcomp was %s' % self.control.items[0].o_gcomp

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
    dict(s_top=0, s_left=0, o_gcomp='div', s_background='url(https://activufrj.nce.ufrj.br/rest/studio/EICA/1_1c.jpg?size=G) no-repeat',
         s_width=1100, o_placeid='book', o_item='EICA/1_1c.jpg', o_part='Locus', s_height=800, s_position='absolute',
         s_backgroundSize='100% 100%', o_Id='o1_EICA/1_1c.jpg'),
    dict(s_top=187, s_left=444, o_gcomp='img', s_float='left', o_placeid='o1_EICA/1_1c.jpg', o_item='jeppeto/ampu.png',
         o_part='Holder', s_position='absolute', o_title='jeppeto/ampu.png',
         o_src='https: //activufrj.nce.ufrj.br/rest/studio/jeppeto/ampu.png?size=G', o_Id='o1_jeppeto/ampu.png'),
    dict(o_act='DoUp', o_gcomp='act', o_placeid='o1_EICA/1_1c.jpg', o_item='Eica01', o_part='Action',
         o_acomp='up', o_Id='o1_o1_EICA/1_1c.jpg')]