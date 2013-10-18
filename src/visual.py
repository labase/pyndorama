"""
############################################################
Pyndorama - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/09/13 $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1.8 $
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Visual module with HTML5 factory and declarative builder.
0.1.8 Load save remote
"""
ACTIV = "https://activufrj.nce.ufrj.br"
SCENE = ACTIV + '/rest/studio/%s?size=G'
TIMEOUT = 1  # seconds
GROUP = 'EICA'
REPO = "/studio/%s"
MENUPX = "https://dl.dropboxusercontent.com/u/1751704/labase/pyndorama/%s.png"
EXTRA = "https://dl.dropboxusercontent.com/u/1751704/labase/pyndorama/%s"
MARKER = "extra/marcador.png"
MENULIST = ACTIV + '/rest/studio/%s?type=%d'
MENUITEM = ACTIV + '/rest/studio/%s?size=N'
EICA = ["EICA/1_1c.jpg", "EICA/1_2c.jpg", "EICA/2_1c.jpg",
        "EICA/3_1c.jpg", "EICA/3_2.png", "EICA/4_2c.jpg"]
EICAP = ["jeppeto/Lutroforo.png", "jeppeto/Pacote.png", "jeppeto/Pote_com_bico_-_Frente.png",
         "jeppeto/Ciprestes.png", "jeppeto/Gramineas.png", "jeppeto/Herbacea.png"]
E_MENU = lambda item, ck="act_rubber": dict(
    o_Id=item, o_src=MENUITEM % item, s_padding='2px', o_click=ck, o_title=item)
STUDIO = "https://activufrj.nce.ufrj.br/rest/studio/%s?type=%d"
STORAGE = "https://activufrj.nce.ufrj.br/storage/%s/%s/__persist__"
MENU_DEFAULT = ['ad_objeto', 'ad_cenario', 'wiki', 'navegar', 'jeppeto']
MENU_PROP = ['apagar', 'configurar', 'pular', 'esconder', 'mostrar']
MENU_BALAO = ['apagar', 'configurar', 'editar', 'pular', 'esconder', 'mostrar']
MENU_TEXT = ['balao']
DEFAULT = [
]
MENU_JEPPETO = ['salvar', 'apagar_jogo']
JEPPETOAPP, JEPPETO, LGM, NGM = "jeppeto", "__J_E_P_P_E_T_O__", 'LOAD_GAME', 'NEW_GAME'
LOADPAGE = '/rest/wiki/%s/%s'
SAVEPAGE = '/rest/wiki/edit/%s/%s'
NEWPAGE = '/wiki/newpage/%s?folder=%s'
#GAMELIST = STORAGE % JEPPETO
NEWPAGE = STORAGE
SAVEPAGE = LOADPAGE = STORAGE
GAMELIST = LOADPAGE % (JEPPETOAPP, JEPPETO)
SAVEGAMELIST = SAVEPAGE % (JEPPETOAPP, JEPPETO)


class Builder:
    """ Builder creating model elements and rendering with gui components. :ref:`builder`
    """
    def __init__(self, gui, model):
        self.doc, self.json, self.html = gui.DOC, gui.JSON, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.model = model
        self.props, self.scenes = EICAP, EICA
        self.xsrf = ''
        self.properties, self.folder = 'jeppeto', ''
        self.nmenu = self.rmenu = self.args = self.pmenu = self.smenu = self.gui = None
        self.wenu = self.jenu = self.tenu = self.omenu = self.mmenu = self.umenu = None
        if 'xsrf' in self.doc.cookie:
            self.xsrf = {key: value for key, value in [cook.split('=')
                         for cook in self.doc.cookie.split('; ') if 'xsrf' in cook]}['_xsrf']
            print('xsrf', self.xsrf)

    def process_arguments(self, gui):

        def set_prop(value):
            self.props = self.json.loads(value)['result']
            self.pmenu = Menu(self.gui, 'ad_objeto', menu=self.props, prefix=MENUITEM, command='', extra=[MARKER])
            print('set_prop', self.props)

        def set_scene(value):
            self.scene = self.json.loads(value)['result']
            self.smenu = Menu(self.gui, 'ad_cenario', menu=self.scenes, prefix=MENUITEM, command='')
            print('set_scene', self.scene)

        args = self.win.location.search
        if '=' in args:
            self.args = {k: v for k, v in [c.split('=') for c in args[1:].split('&')]}
            props = self.properties = self.args.setdefault('props', 'jeppeto')
            self.folder = self.args.setdefault('folder', '')
            scenes = self.args.setdefault('scenes', 'EICA')
            self.gui.send(STUDIO % (props, 1), record=set_prop, method="GET")
            self.gui.send(STUDIO % (scenes, 2), record=set_scene, method="GET")
            print(self.args, props, STUDIO % (props, 1))
            if 'game' in self.args:
                gui.start_a_game(self.args['game'])
            else:
                gui.show_front_menu()
        else:
            gui.show_front_menu()

    def build_deploy(self, descriptor):
        [self.model.employ(**description) for description in descriptor]

    def build_menus(self):
        self.rmenu = Menu(self.gui, '__ROOT__', menu=MENU_DEFAULT, event="contextmenu")
        self.gui.doc.oncontextmenu = self.gui.screen_context
        self.pmenu = not self.pmenu and Menu(
            self.gui, 'ad_objeto', menu=self.props, prefix=MENUITEM, command='', extra=[MARKER])
        self.smenu = not self.smenu and Menu(self.gui, 'ad_cenario', menu=self.scenes, prefix=MENUITEM, command='')
        self.nmenu = Menu(self.gui, 'navegar', menu=self.scenes, prefix=MENUITEM, command='')
        self.umenu = Menu(self.gui, 'pular', menu=self.scenes, prefix=MENUITEM, command='')
        self.mmenu = Menu(self.gui, 'mostrar', menu=self.scenes, prefix=MENUITEM, command='')
        self.omenu = Menu(self.gui, 'ob_ctx', menu=MENU_PROP, activate=True)
        self.tenu = Menu(self.gui, 'tx_ctx', menu=MENU_BALAO, activate=True)
        self.jenu = Menu(self.gui, 'jeppeto', menu=MENU_JEPPETO, activate=True)
        self.wenu = Menu(self.gui, 'wiki', menu=MENU_TEXT, activate=True)

    def build_all(self, gui):
        self.gui = gui
        self.gui.control = self.model
        self.build_deploy(DEFAULT)
        self.process_arguments(gui)
        self.gui.xsrf = self.xsrf
        self.gui.properties = self.properties
        self.gui.folder = self.folder
        self.build_menus()
        print(self.model.items)
        self.model.deploy(self.gui.employ)


class Menu(object):
    """Menu hierarchy builder with flyweight menuitem. :ref:`menu`
    """
    MENU = {}

    def __init__(self, gui, originator, menu=None, command='menu_',
                 prefix=MENUPX, event="click", activate=False, extra=[]):
        self.gui, self.item, self.prefix = gui, originator, prefix
        self.command, self.prefix, self.activated = command, prefix, activate
        self.originator = originator
        self.book = self.gui.doc["book"]
        self.menu_ad_cenario = self.menu___ROOT__ = self.menu_ad_objeto = self.menu_ad
        self.menu_wiki = self.menu_jeppeto = self.menu_ad
        self.target, self.id, self.menu = self, '', None
        menu and self.build_menu(menu, extra=extra)

    def build_item(self, item, source, menu):
        #print('build_item', self.prefix, item, menu, menu.menu)
        #pr = self.prefix % item
        kwargs = dict(o_Id="m_"+item, o_src=source, s_padding='2px', o_title=item)
        menu_item = self.gui.img(menu.menu, **kwargs)
        menu_item.bind("click", menu.click)
        if self.activated and (item not in Menu.MENU):
            #print('activated', item, menu_item)
            Menu.MENU[item] = Menu(self.gui, item, command='submenu_')
        return menu_item

    def build_menu(self, menu=MENU_DEFAULT, display="none", extra=[]):
        #print ("build_menu:", self.gui.div)
        Menu.MENU[self.originator] = self
        self.menu = self.gui.div(
            self.gui.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display=display, s_border='1px solid #d0d0d0', o_Id=self.item)
        #print ('build_menu', [self.comm[kwargs['o_click']] for kwargs in menu])
        [self.build_item(item, EXTRA % item, self) for item in extra]
        [self.build_item(item, self.prefix % item, self) for item in menu]
        return self.menu

    def click(self, event):
        event.stopPropagation()
        event.preventDefault()
        self.menu.style.display = 'none'
        menu_id = event.target.id[2:]
        item = menu_id in Menu.MENU and menu_id or self.item
        obj = menu_id in Menu.MENU and Menu.MENU[menu_id] or self
        #self.activate(self.command or self.item, event, obj)
        print('click:', menu_id, self.command + item, self.menu.Id, self.prefix)  # , self.item, item)
        self.activate(self.command + item, event, obj)

    def make_id(self, targ_id):
        oid = Gui.REV[targ_id] = Gui.REV.setdefault(targ_id, 0) + 1
        return ("o%d_" % oid) + targ_id

    def activate(self, command, ev, menu):
        #print('activate', command, ev.target.id, getattr(self, command))
        getattr(self, command)(ev, menu)

    def menu_ad(self, ev, menu):
        ev.preventDefault()
        menu = menu.menu
        menu.style.display = 'block'
        self.gui.current_menu = menu
        menu.style.left = self.gui.menuX
        menu.style.top = self.gui.menuY

    def menu_ob_ctx(self, ev, menu):
        menu = menu.menu
        menu.style.display = 'none'
        menu.style.left = self.gui.menuX
        menu.style.top = self.gui.menuY

    def menu_configurar(self, ev, menu):
        self.target, self.id = self, self.gui.obj_id
        self.gui.sel_prop(self)

    def menu_editar(self, ev, menu):
        prop = self.gui.doc[self.gui.obj_id]
        kwargs = dict(
            o_emp=self.gui.shape, o_cmd='DoShape', o_Id=prop.id, o_gcomp='shape',
            s_left=prop.offsetLeft, s_top=prop.offsetTop, o_text=prop.html)
        self._editar(ev, prop, kwargs)

    def _editar(self, event, prop, kwargs):
        prop_box = self.gui.doc["propbox"]
        prop_size = self.gui.doc["propsize"]
        prop_size.style.backgroundColor = 'green'
        prop.style.backgroundColor = 'white'
        self.gui.action = lambda no: None
        self.gui.contextmenu = lambda x, y: None

        def _dropend(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop

            kwargs.update(o_text=prop.html)
            print('_dropend', kwargs)
            self.gui.save(kwargs)
            kwargs.update(o_cmd="DoShape", o_emp=self.gui.shape, o_gcomp='shape')
            self.gui.control.activate(**kwargs)
            _drop_final(ev)

        def _drop_final(ev):
            ev.preventDefault()
            ev.stopPropagation()
            prop.html = kwargs['o_text']
            prop_size.style.backgroundColor = 'black'
            prop_size.unbind('click')
            prop.style.backgroundColor = 'transparent'
            prop_box.style.left = -90000
            prop_size.style.left = -90000
            prop.contentEditable = "false"
            self.gui.action = self.gui._action
            self.gui.contextmenu = self.gui._contextmenu
            self.gui.revoke_action = lambda x=0: None

        self.gui.revoke_action = _drop_final
        x, y, w, h, s = prop.offsetLeft, prop.offsetTop, prop.offsetWidth, prop.offsetHeight, 20
        pboxs, psizes = prop_box.style, prop_size.style
        prop_size.unbind('click')
        prop_size.bind('click', _dropend)
        psizes.left, psizes.top, psizes.width, psizes.height = x+w-10, y+h-10, s, s
        self.gui.book <= prop_size
        prop.contentEditable = "true"
        prop.onclick = lambda ev: ev.stopPropagation()

    def menu_esconder(self, ev, menu):
        def delete(o_item, o_Id, **kwargs):
            #print('thumb', self.prefix, kwargs)
            self.gui.doc[o_Id].style.opacity = '0.1'
            kwargs.update(o_cmd='DoShape', o_Id=o_Id, o_gcomp='shape', s_opacity='0.1')
            self.gui.save(kwargs)
        self.gui.control.activate(
            o_emp=delete, o_Id=self.gui.obj_id, o_cmd='DoShape')

    def menu_apagar(self, ev, menu):
        def delete(o_item, o_Id, **kwargs):
            #print('thumb', self.prefix, kwargs)
            self.gui.doc[o_Id].style.display = 'none'
            kwargs.update(o_cmd='DoDel', o_Id=o_Id, o_gcomp='delete')
            self.gui.save(kwargs)
        self.gui.control.activate(
            o_emp=delete, o_Id=self.gui.obj_id, o_cmd='DoDel')

    def menu_apagar_jogo(self, ev, menu):
        self.gui.storage['_JPT_'+self.gui.game] = self.gui.json.dumps([])
        games = self.gui.json.loads(self.gui.storage[JEPPETO])
        games.pop(self.gui.game)
        self.gui.storage[JEPPETO] = games

    def menu_pular(self, ev, menu):
        self._sub_menu(ev, menu)

    def menu_mostrar(self, ev, menu):
        self._sub_menu(ev, menu, kind='Holder')

    def menu_navegar(self, ev, menu):
        self._sub_menu(ev, menu)

    def menu_salvar(self, ev, menu):
        self.gui.remote_save()

    def _sub_menu(self, ev, menu, kind='Locus', activated=False, command='DoList'):
        def thumb(o_item, o_Id, **kwargs):
            self.activated = activated
            item = (MENUITEM % o_item) if o_item[:5] not in 'extra/balao' else EXTRA % MARKER
            print('_sub_menuthumb', o_item, item, o_item[:5])
            self.build_item(o_Id, item, menu)
        pane = menu.menu
        while pane.hasChildNodes():
            pane.removeChild(pane.lastChild)
        self.gui.control.activate(o_emp=thumb, o_cmd=command, o_kind=kind)
        pane.style.display = 'block'
        self.gui.current_menu = pane
        pane.style.left = self.gui.menuX
        pane.style.top = self.gui.menuY

    def navegar(self, ev, menu):
        def up(o_Id, **kwargs):
            self.gui._locate(self.book, self.gui.doc[o_Id])
        kwargs = dict(
            o_emp=up, o_cmd="DoUp", o_part="Locus", o_Id=ev.target.id[2:]
        )
        self.gui.control.activate(**kwargs)

    def mostrar(self, ev, menu):
        menu_id = ev.target.id[2:]
        oid = self.make_id(menu_id)
        kwargs = dict(
            o_emp=self.gui.act, o_cmd="DoAdd", o_part="Action", o_Id=oid,
            o_gcomp='act', o_act='DoShape', o_acomp='shape', s_opacity='1.0',
            o_item=menu_id, o_placeid=self.gui.obj_id
        )
        self.gui.control.activate(**kwargs)
        self.gui.save(kwargs)

    def pular(self, ev, menu):
        menu_id = ev.target.id[2:]
        oid = self.make_id(menu_id)
        kwargs = dict(
            o_emp=self.gui.act, o_cmd="DoAdd", o_part="Action", o_Id=oid,
            o_gcomp='act', o_act='DoUp', o_acomp='up',
            o_item=menu_id, o_placeid=self.gui.obj_id
        )
        self.gui.control.activate(**kwargs)
        self.gui.save(kwargs)
        #print('pular', kwargs)

    def ad_cenario(self, ev, menu):
        menu_id = ev.target.id[2:]
        oid = self.make_id(menu_id)
        kwargs = dict(
            o_emp=self.gui.div, o_cmd="DoAdd", o_part="Locus", o_Id=oid,
            s_background='url(%s) no-repeat' % (SCENE % menu_id),
            s_width=1100, s_height=800, s_top=0, o_gcomp="div", o_place=self.book,
            s_backgroundSize="100% 100%", s_left=0, s_position='absolute',
            o_item=menu_id
        )
        self.gui.control.activate(**kwargs)
        self.gui.save(kwargs)

    def ad_objeto(self, ev, menu):
        def prop(o_place, **kwargs):
            try:
                kwargs.update(o_cmd="DoAdd")
                self.gui.img(**kwargs).oncontextmenu = self.gui.object_context  # gui.sel_prop
                self.gui.save(kwargs)
            except Exception:
                print('ad_objeto place rejected:', o_place, kwargs)
        offx, offy, tid = self.book.offsetLeft, self.book.offsetTop, ev.target.id[2:]
        oid = self.make_id(tid)
        img_source = 'extra/' in tid and EXTRA % tid or SCENE % tid
        kwargs = dict(
            o_emp=prop, o_cmd="DoAdd", o_part="Holder", o_gcomp="sprite",
            o_item=tid, o_src=img_source, o_Id=oid,
            s_position='absolute', s_float='left', s_top=self.gui.menuY-offy,
            s_left=self.gui.menuX-offx, o_title=tid)
        self.gui.control.activate(**kwargs)

    def wiki(self, ev, menu):
        def prop(o_place, **kwargs):
            try:
                kwargs.update(o_cmd="DoAdd")
                self.gui.img(**kwargs).onclick = self.gui.sel_prop
                self.gui.save(kwargs)
            except Exception:
                print('ad_objeto place rejected:', o_place, kwargs)
        offx, offy, tid = self.book.offsetLeft, self.book.offsetTop, ev.target.id[2:]
        oid = self.make_id(tid)
        kwargs = dict(
            o_emp=prop, o_cmd="DoAdd", o_part="Holder", o_gcomp="img",
            o_item=tid, o_src=SCENE % tid, o_Id=oid,
            s_position='absolute', s_float='left', s_top=self.gui.menuY-offy,
            s_left=self.gui.menuX-offx, o_title=tid)
        print('wiki', kwargs)
        self.gui.control.activate(**kwargs)

    def menu_balao(self, ev, menu):
        def _prop(o_place, **kwargs):
            try:
                kwargs.update(o_cmd="DoAdd", o_emp=self.gui.text)
                print("menu_balao prop", kwargs)
                prop = self.gui.div('OOOOOO', **kwargs)
                prop.oncontextmenu = self.gui.text_context
                self._editar(ev, prop, kwargs)
            except Exception:
                print('text baloon rejected:', kwargs)
        offx, offy, tid = self.book.offsetLeft, self.book.offsetTop, 'balao'
        oid = self.make_id(tid)
        kwargs = dict(
            o_emp=_prop, o_cmd="DoAdd", o_part="Holder", o_gcomp="text",
            s_width=200, s_height=150, o_item=tid, o_Id=oid,
            s_position='absolute', s_float='left', s_top=self.gui.menuY-offy,
            s_left=self.gui.menuX-offx, o_title=tid, o_text="Lorem Ipsum")
        self.gui.control.activate(**kwargs)


class GuiDraw(object):
    """Factory returning HTML, SVG elements and placeholder groups. :ref:`gui`
    """
    def _locate(self, place, element, o_placeid=None, **kwargs):
        #print('_locate', place, element, o_placeid, kwargs)
        if 's_backgroundSize' in kwargs:
            element.style.backgroundSize = kwargs['s_backgroundSize']
        if 'o_text' in kwargs:
            element.html = kwargs['o_text']
        locus = o_placeid and self.doc[o_placeid] or place
        locus <= element
        return element

    def _filter(self, args):
        #print(args)
        return {k[2:]: value for k, value in args.items() if k[:2] in "s_"}

    def act(self, o_Id, **kwargs):
        self.doc[o_Id].onclick = self.action

    def up(self, o_Id, **kwargs):
        print('up', kwargs)
        self._locate(self.book, self.doc[o_Id], **kwargs)

    def div(self, o_place=None, o_Id=None, o_Class='deafault', **kwargs):
        #print(kwargs, self._filter(kwargs))
        return self._locate(o_place, self.html.DIV(
            Id=o_Id, Class=o_Class, style=self._filter(kwargs)), **kwargs)

    def shape(self, o_place=None, o_Id=None, o_Class='deafault', **kwargs):
        shaper = self.doc[o_Id].style
        if ('s_left' in kwargs) and ('s_top' in kwargs):
            shaper.left, shaper.top = kwargs['s_left'], kwargs['s_top']
        #print('shape', o_Id, shaper, shaper.left, kwargs)
        if ('s_width' in kwargs) or ('s_height' in kwargs):
            shaper.width, shaper.height = kwargs['s_width'], kwargs['s_height']
        if 'o_text' in kwargs:
            self.doc[o_Id].html = kwargs['o_text']
        if 's_opacity' in kwargs:
            shaper.opacity = kwargs['s_opacity']

    def delete(self, o_place=None, o_Id=None, o_Class='deafault', **kwargs):
        print('delete', kwargs)
        place = o_place or self.doc[kwargs['o_placeid']]
        place.removeChild(self.doc[o_Id])

    def iframe(
        self, o_place=None, o_width=10, o_height=10, o_Id=None, o_Class="frame",
            o_frameBorder=0, o_src="", **kwarg):
        """Html iframe."""
        return self._locate(o_place, self.html.IFRAME(
            Id=o_Id, width=o_width, height=o_height, Class=o_Class,
            frameBorder=o_frameBorder, src=o_src))

    def img(
            self, o_place=None, o_src="", o_width='', o_height='', o_title='', o_alt="",
            o_Id='', o_Class='deafault', **kwargs):
        """Html image. """
        return self._locate(o_place, self.html.IMG(
            Id=o_Id, width=o_width, height=o_height, Class=o_Class, alt=o_alt,
            title=o_title, src=o_src, style=self._filter(kwargs)), **kwargs)
KWA = dict(s_position='absolute', s_opacity=0.1, s_top=180,
           o_src=MENUPX % 'drawing', o_width=400, o_height=400)

EL, ED = [], {}


class Gui(GuiDraw):
    """Deal with incoming html events. :ref:`gui_event`
    """
    REV = {}

    def __init__(self, gui):
        self.doc, self.svg, self.html = gui.DOC, gui.SVG, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.storage, self.json = gui.STORAGE, gui.JSON
        self.current_menu = self.menuX = self.menuY = self.obj_id = None
        self.main = self.doc["base"]
        self.book = self.doc["book"]
        #self.comm = dict(act_rubber=self.act_rubber, scenes=self.scenes, props=self.props)
        self.rubber_start = self.build_rubberband()
        self.deliverables = dict(
            div=self.div, iframe=self.iframe, sprite=self.sprite, text=self.text,
            drag=self.build_drag, drop=self.build_drop, shape=self.shape,
            up=self.up,  delete=self.delete, act=self.act)
        self.doc.onclick = self.revoke_menu
        self.action = self._action
        self.contextmenu = self._contextmenu
        self.context_obj_id = self.lst = self.start_div = self.revoke_action = lambda x=0: None
        self.status = self.game = self.xsrf = self.properties = self.folder = self.control = None
        self.games = []
        self.commands = {}
        self.offx = self.offy = 0

    def start_a_game(self, game):
        print('start a game')
        self.load(game)
        pass

    def show_front_menu(self):
        print('show_front_menu')
        self.start_div = self.div(self.book)
        self.lst = self.div(self.start_div, s_position='absolute', s_left=220,
                            s_top=510, s_width=300, s_display='none')
        self.img(
            self.start_div, MENUPX[:-4] % 'fundo.jpg', 1100, 800,
            s_position='absolute', s_left=0)
        self.img(self.start_div, o_Id=LGM, s_left=120, **KWA).onclick = self.start
        self.img(self.start_div, o_Id=NGM, s_left=530, **KWA).onclick = self.start

    def revoke_menu(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.revoke_action(ev)
        #print('revoke_menu', self.current_menu, ev.button)
        if self.current_menu and ev.button == 0:
            #print('revoke_menu', self.current_menu.Id)
            self.current_menu.style.display = 'none'

    def screen_context(self, ev):
        self.contextmenu(ev, Menu.MENU['__ROOT__'].menu)

    def _contextmenu(self, ev, menu):
        ev.stopPropagation()
        ev.preventDefault()
        self.current_menu = menu
        #print('self menu:', self.menu, self.gui.win.pageXOffset, self.gui.win.pageYOffset)
        menu.style.display = 'block'
        menu.style.left = self.menuX = ev.clientX + self.win.pageXOffset
        menu.style.top = self.menuY = ev.clientY + self.win.pageYOffset
        self.context_obj_id = ev.target.id[2:]
        self.obj_id = ev.target.id
        return False

    def object_context(self, ev):
        self.contextmenu(ev, Menu.MENU['ob_ctx'].menu)

    def text_context(self, ev):
        self.contextmenu(ev, Menu.MENU['tx_ctx'].menu)

    def _action(self, event):
        self.control.activate(o_emp=self.employ, o_Id=event.target.id, o_cmd='DoExecute')

    def text(self, cmd=None, **kwargs):
        self.div(**kwargs).oncontextmenu = self.text_context  # gui.sel_prop

    def sprite(self, cmd=None, **kwargs):
        self.img(**kwargs).oncontextmenu = self.object_context  # gui.sel_prop

    def load(self, cmd=None):
        game = '_JPT_' + (cmd or self.game)

        def not_read(x=0, text=1):
            self.commands = self.json.loads(self.storage[game])
            print('load not read:', x, text, game, self.commands, self.storage[game])
            for kwargs in self.commands:
                render(**kwargs)

        def read(text):
            commands = self.json.loads(text)
            print('load read:', commands, text)
            if commands['status'] != '0':
                return not_read()
            #self.commands = commands['result']
            cmds = self.commands = commands['conteudo']
            assert isinstance(cmds, list), 'was not list but %s' % type(cmds)
            #self.json.loads(commands['conteudo'])
            for kwargs in self.commands:
                render(**{str(k): v for k, v in kwargs.items()})

        def render(o_gcomp, **kwargs):
            targ_id = kwargs['o_Id'].split('_')[1]
            if 'o_placeid' in kwargs:
                placeid = kwargs['o_placeid']
                place = self.doc[placeid]
                kwargs.update(o_place=place)
            Gui.REV[targ_id] = Gui.REV.setdefault(targ_id, 0) + 1
            kwargs.update(o_gcomp=o_gcomp)
            self.control.activate(
                self.deliverables[o_gcomp], **kwargs)
        #self.send(STORAGE % game, read, not_read, method="GET")
        self.send(LOADPAGE % (self.properties, game), read, not_read, method="GET")

    def save(self, cmd):
        if (not 'o_placeid' in cmd) and 'o_place' in cmd and cmd['o_place']:
            cmd['o_placeid'] = cmd.pop('o_place').id
        elif 'o_place' in cmd:
            cmd.pop('o_place')
        #print('save,', cmd)
        'o_emp' in cmd and cmd.pop('o_emp')
        self.storage['_JPT_'+self.game] = self.json.dumps(
            self.json.loads(self.storage['_JPT_'+self.game]) + [cmd])

    def _remote_save(self, value=EL, url=SAVEGAMELIST, nome='new_game', go=lambda: None):
        #data = dict(_xsrf=self.xsrf, value=value)
        data = dict(_xsrf=self.xsrf, conteudo=self.json.dumps(value), nomepag=nome)

        def receipt(text, error="error"):
            go()
            print('remote save receipt error', text)

        def receive_list(text):
            go()
            print('remote save receipt', text.split()[0])
        self.send(url, receive_list, receipt, data, "POST")

    def remote_save(self):
        value = []

        def register_value(**kwargs):
            if (not 'o_placeid' in kwargs) and 'o_place' in kwargs and kwargs['o_place']:
                kwargs['o_placeid'] = kwargs.pop('o_place').id
            elif 'o_place' in kwargs:
                kwargs.pop('o_place')
            value.append(kwargs)

        def receipt(text=0, error="error"):
            print('menu_salva register_value receipt', text)
        self.control.deploy(register_value)
        value = self.json.dumps(value)
        #data = dict(_xsrf=self.xsrf, value=value)

        def save_page():
            data = dict(_xsrf=self.xsrf, conteudo=value)
            self.send(SAVEPAGE % (self.properties, '_JPT_'+self.game), receipt, receipt, data)
            print('menu_salva register_value', data)
        self.storage['_JPT_'+self.game] = value
        #self.gui.send(STORAGE % ('_JPT_'+self.gui.game), receipt, receipt, data)
        self._remote_save(self.games+['_JPT_'+self.game])
        #self._remote_save([], NEWPAGE % (self.properties, self.folder), '_JPT_'+self.game, save_page)
        self._remote_save([], NEWPAGE % (self.properties, JEPPETO), '_JPT_'+self.game, save_page)

    def send(self, url, record=lambda x: '', terr=lambda x, y=0: '', data=ED, method="POST"):
        def _on_sent(requisition):
            if requisition.status == 200 or requisition.status == 0 and requisition.text:
                record(requisition.text)
            else:
                terr("error %d" % requisition.status, requisition.text)
        req = self.ajax()
        req.on_complete = _on_sent
        req.set_timeout(TIMEOUT, terr)
        req.open(method, url, True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send(data)

    def start(self, ev):
        if JEPPETO not in self.storage:
            self.storage[JEPPETO] = self.json.dumps([])
        self.games = []
        #data = dict(_xsrf=self.xsrf, value=value)
        data = dict(_xsrf=self.xsrf, conteudo='[]')

        def receipt(text, error="error"):
            print('remote load receipt error', text)
            self._start(ev)

        def receive_list(text):
            games = self.json.loads(text)
            if games['status'] == 0:
                #self.games = games['result']
                self.games = self.json.loads(games['result']["conteudo"])
            else:
                print('sending empty game list', text)
                self.send(SAVEGAMELIST, receipt, receipt, data)
            print('remote load receive list', text, self.games)
            self._start(ev)
        self.send(GAMELIST, receive_list, receipt, data, 'GET')

    def _start(self, ev):
        lst = self.lst

        def nameit(event):
            self.game = event.target.id[5:]
            #print('nameit', self.game)
            self.start_div.style.display = 'none'
            self.doc["illumini"].style.display = "none"
            self.doc["text"].style.display = "none"
            self.load()
        self.book <= lst
        games = self.json.loads(self.storage[JEPPETO]) + self.games
        print('start', games, len(games))
        default_name, ask = 'Jeppeto_%d' % len(games), 'Nome do novo jogo'
        if (ev.target.id == 'NEW_GAME') or (len(games) < 1):
            self.game = self.win.prompt(ask, default_name) or default_name
            self.storage[JEPPETO] = self.json.dumps(games + [self.game])
            self.storage['_JPT_'+self.game] = self.json.dumps([])
            self.start_div.style.display = 'none'
            self.doc["illumini"].style.display = "none"
            self.doc["text"].style.display = "none"
        else:
            for game in games:
                inp = self.div(lst, o_Id='_JPT_'+game, s_color='seagreen',
                               s_fontFamily='Arial Black', s_fontSize=40)
                inp.text = game
                inp.style.fontFamily = 'Arial'
                inp.style.fontSize = '30px'
                inp.bind('click', nameit)
                lst <= inp
            lst.style.display = 'block'

    def receive(self, url, default, deliver):
        self.status = 555

        def response(req=self, default=default):
            data = (req.status == 200 or req.status == 0) and req.text or default
            deliver(data)
        requisition = self.ajax()
        requisition.on_complete = response
        requisition.set_timeout(TIMEOUT, response)
        requisition.open('GET', url, True)
        requisition.set_header('content-type', 'application/x-www-form-urlencoded')
        requisition.send()

    def employ(self, o_gcomp=None, o_placeid=None, **kwargs):
        place = kwargs.pop('o_place') or self.doc
        try:
            place = self.doc[o_placeid]
        except Exception:
            print('place rejected:', o_placeid, o_gcomp, kwargs)
        print('employ', place, o_placeid, o_gcomp, kwargs)
        self.deliverables[o_gcomp](o_place=place, **kwargs)

    def sel_prop(self, event):
        prop = self.doc[event.target.id]
        prop_box = self.doc["propbox"]
        prop_size = self.doc["propsize"]
        prop_place = prop.parentNode
        self.contextmenu = lambda ev, menu: None
        self.action = lambda ev: None

        def dragstart(ev):
            self.book.bind('drop', dropmove)
            self.book.bind('dragover', moveover)
            _start(ev)

        def sizestart(ev):
            self.book.bind('drop', dropsize)
            self.book.bind('dragover', dragover)
            _start(ev)

        def _start(ev):
            prop_box.unbind('dragstart', dragstart)
            prop_size.unbind('dragstart', sizestart)
            self.offx = ev.x - self.book.offsetLeft - prop_box.offsetLeft
            self.offy = ev.y - self.book.offsetTop - prop_box.offsetTop
            self.goX, self.goY = pboxs.left, pboxs.top
            #print(ev, ev.data, ev.target.id, self.offx, self.offy)
            ev.data['text'] = ev.target.id
            ev.stopPropagation()
            # permitir que o objeto arrastado seja movido
            ev.data.effectAllowed = 'move'
            self.revoke_action = lambda x=0: None

        def dropmove(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop
            self.goX, self.goY = ev.x-offx-self.offx, ev.y-offy-self.offy
            kwargs = dict(
                o_cmd='DoShape', o_Id=prop.id, o_gcomp='shape',
                s_left=ev.x-offx-self.offx, s_top=ev.y-offy-self.offy)
            _dropend(ev, kwargs)

        def _dropend(ev, kwargs):
            print('_dropend')
            self.save(kwargs)
            self.control.activate(self.shape, **kwargs)
            self.book.unbind('drop')
            _drop_final(ev)

        def _drop_final(ev):
            ev.preventDefault()
            ev.stopPropagation()
            self.book.unbind('dragover')
            prop_box.unbind('dragstart', dragstart)
            prop_size.unbind('dragstart', sizestart)
            prop_place <= prop
            prop.style.left, prop.style.top = self.goX, self.goY
            prop_box.style.left = -90000
            prop_size.style.left = -90000
            self.contextmenu = self._contextmenu
            self.action = self._action

        def dropsize(ev):
            x, y = prop_box.offsetLeft, prop_box.offsetTop
            w, h = _dragover(ev)
            kwargs = dict(
                o_cmd='DoShape', o_Id=prop.id, o_gcomp='shape',
                s_left=x, s_top=y, s_width=w, s_height=h)
            _dropend(ev, kwargs)

        def moveover(ev):
            ev.data.effectAllowed = 'move'
            ev.preventDefault()

        def dragover(ev):
            ev.data.effectAllowed = 'move'
            ev.preventDefault()
            w, h = _dragover(ev)

        def _dragover(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop
            w, h = ev.x - prop_box.offsetLeft - offx, ev.y - prop_box.offsetTop - offy
            prop_box.style.width = prop.style.width = w
            prop_box.style.height = prop.style.height = h
            return w, h
        self.revoke_action = _drop_final
        x, y, w, h, s = prop.offsetLeft, prop.offsetTop, prop.offsetWidth, prop.offsetHeight, 10
        #print ('GUi.sel_prop', ev.target.id, x, y, w, h)
        #prop.unbind('click')
        prop_box.bind('dragstart', dragstart)
        pboxs, psizes = prop_box.style, prop_size.style
        pboxs.left, pboxs.top, pboxs.width, prop_box.style.height = x, y, w, h
        self.book <= prop_box
        prop_size.bind('dragstart', sizestart)
        psizes.left, psizes.top, psizes.width, psizes.height = w+x-5, h+y-5, s, s
        self.book <= prop_size
        prop.style.left, prop.style.top = 0, 0
        prop_box <= prop

    def act_rubber(self, ev):
        print('menu:', ev)
        self.s_menu.style.display = 'none'
        self.p_menu.style.display = 'none'
        self.doc["book"].bind('mousedown', self.rubber_start)

    def build_drag(self, o_place, **kwargs):
        def start(ev):
            #print(ev, ev.data, ev.target.id)
            ev.data['text'] = ev.target.id
            # permitir que o objeto arrastado seja movido
            ev.data.effectAllowed = 'move'
        print('drag', o_place)
        draggable = o_place
        draggable.draggable, draggable.onmousedown = True, start
        #draggable.onmouseover = drag_over

    def build_drop(self, o_drop, **kwargs):
        def drop_over(ev):
            #ev.data.dropEffect = 'move'
            ev.preventDefault()

        def drop(ev):
            src_id = ev.data['text']
            elt = self.doc[src_id]
            self.doc[kwargs['action'](src_id)] <= elt
        print('drag', o_drop)
        droppable = self.doc[o_drop]
        droppable.onmouseover, droppable.onmouseup = drop_over, drop

    def build_rubberband(self):
        def start(ev):
            self.rubber.style.left = self.rbX = ev.clientX
            self.rubber.style.top = self.rbY = ev.clientY
            self.rubber.style.display = 'block'
            self.doc.onmouseup = stop
            self.doc["book"].bind('mousemove', drag)
            print(self.rbX, self.rbY)
            ev.stopPropagation()
            ev.preventDefault()
            return False

        def drag(ev):
            self.rubber.style.width = self.rbH = ev.clientX - self.rbX
            self.rubber.style.height = self.rbW = ev.clientY - self.rbY
            ev.stopPropagation()
            ev.preventDefault()
            return False
            #print(self.rbH)

        def stop(ev):
            print(self.rbH, self.rbW)
            self.doc["book"].unbind('mousedown')  # , start)
            self.doc["book"].unbind('mousemove')  # , drag)
            #self.doc.unbind('mouseup', stop)  # , stop)
            self.rubber.style.display = 'none'
            self.rubber.style.width = 2
            self.rubber.style.height = 2

        self.rubber = self.div(
            self.doc, s_position='absolute', s_top='50%', s_left='50%',
            marginLeft='-150px', marginTop='-100px', padding='10px', s_display='none',
            s_width='2px', s_height='2px', s_border='1px solid #d0d0d0')
        return start
