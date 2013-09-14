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
ITEM = 'it3m'


class TestPyndoramaControl(unittest.TestCase):

    def setUp(self):
        class _Gui(dict):

            def employ(self, **kwargs):
                print('setUp employ')
                self['adm1n'].update(kwargs)
                return 'adm1n', 0001

        self.control = model.init()
        self.gui = _Gui()
        self.gui['adm1n'] = {}

    def _action_load(self):
        """load an action."""
        self.control.activate(self.gui.employ, place=self.gui, **JEP0["E1"])
        self.control.activate(self.gui.employ, place=self.gui, **JEP0["JAM"])
        self.gui['adm1n'] = {}
        self.control.activate(self.gui.employ, place=self.gui, **JEP0["JAC"])

    def test_action_load(self):
        """test load an action."""
        self._action_load()
        assert self.gui['adm1n']["o_Id"] == "o1_jeppeto/ampu.png", 'no admin in %s' % self.gui['adm1n']
        pass

    def test_action_execute(self):
        """test execute an action."""
        self._action_load()
        self.gui['adm1n'] = {}
        self.control.activate(o_emp=self.gui.employ, o_Id="o1_jeppeto/ampu.png", o_cmd='DoExecute')
        assert self.gui['adm1n']["o_Id"] == "o1_EICA/1_1c.jpg", 'no admin in %s' % self.gui['adm1n']
        assert self.gui['adm1n']["o_gcomp"] == "up", 'no admin in %s' % self.gui['adm1n']

if __name__ == '__main__':
    unittest.main()

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
