"""
############################################################
Pyndorama - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/09/13 $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1.7 $
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Visual module with HTML5 factory and declarative builder.
"""
ACTIV = "https://activufrj.nce.ufrj.br"
SOURCE = 'mansao'
SCENE = ACTIV + '/rest/studio/%s?size=G'
TIMEOUT = 5  # seconds
GROUP = 'EICA'
REPO = "/studio/%s"
IMG = 'http://j.mp/aegadian_sea'
SHIP = 'view/Trireme_1.png'
MENUPX = "https://dl.dropboxusercontent.com/u/1751704/labase/pyndorama/%s.png"
MENULIST = ACTIV + '/rest/studio/%s?type=%d'
MENUITEM = ACTIV + '/rest/studio/%s?size=N'
EICA = ["EICA/1_1c.jpg", "EICA/1_2c.jpg", "EICA/2_1c.jpg",
        "EICA/3_1c.jpg", "EICA/3_2.png", "EICA/4_2c.jpg"]
EICAP = ["jeppeto/bule0.png", "jeppeto/vaso0.png", "jeppeto/anfora.png",
         "jeppeto/agave.png", "jeppeto/moita.png", "jeppeto/palmeira.png"]
E_MENU = lambda item, ck="act_rubber": dict(
    o_Id=item, o_src=MENUITEM % item, s_padding='2px', o_click=ck, o_title=item)
STUDIO = "https://activufrj.nce.ufrj.br/studio/EICA/%s?disp=inline&size=N"
MENU_DEFAULT = ['ad_objeto', 'ad_cenario', 'wiki', 'navegar']
MENU_PROP = ['apagar', 'configurar', 'pular']
MENU_BALAO = ['apagar', 'configurar', 'editar', 'pular']
MENU_TEXT = ['balao']
DEFAULT = [
]


class Builder:
    """ Builder creating model elements and rendering with gui components. :ref:`builder`
    """
    def __init__(self, gui, model):
        self.doc, self.svg, self.html = gui.DOC, gui.SVG, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.model = model
        args = self.win.location.search
        if '=' in args:
            self.args = {k: v for k, v in [c.split('=') for c in args[1:].split('&')]}
            print(self.args)

    def _on_sent(self, req):
        if req.status == 200 or req.status == 0:
            self.doc["result"].html = req.text
        else:
            self.doc["result"].html = "error "+req.text

    def send(self, data, url):
        req = self.ajax()
        #req.on_complete = on_complete
        #req.set_timeout(timeout,err_msg)
        req.open('POST', url, True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send(data)

    def build_deploy(self, descriptor):
        [self.model.employ(**description) for description in descriptor]

    def build_menus(self):
        self.rmenu = Menu(self.gui, '__ROOT__', menu=MENU_DEFAULT, event="contextmenu")
        self.gui.doc.oncontextmenu = self.rmenu.contextmenu
        self.pmenu = Menu(self.gui, 'ad_objeto', menu=EICAP, prefix=MENUITEM, command='')
        self.smenu = Menu(self.gui, 'ad_cenario', menu=EICA, prefix=MENUITEM, command='')
        self.nmenu = Menu(self.gui, 'navegar', menu=EICA, prefix=MENUITEM, command='')
        self.umenu = Menu(self.gui, 'pular', menu=EICA, prefix=MENUITEM, command='')
        self.omenu = Menu(self.gui, 'ob_ctx', menu=MENU_PROP, activate=True)
        self.tenu = Menu(self.gui, 'tx_ctx', menu=MENU_BALAO, activate=True)
        self.wenu = Menu(self.gui, 'wiki', menu=MENU_TEXT, activate=True)

    def build_all(self, gui):
        self.gui = gui
        self.gui.control = self.model
        self.build_deploy(DEFAULT)
        self.build_menus()
        print(self.model.items)
        self.model.deploy(self.gui.employ)


class Menu(object):
    """Menu hierarchy builder with flyweight menuitem. :ref:`menu`
    """
    MENU = {}

    def __init__(self, gui, originator, menu=None,
                 command='menu_', prefix=MENUPX, event="click", activate=False):
        self.gui, self.item, self.prefix = gui, originator, prefix
        self.command, self.prefix, self.activated = command, prefix, activate
        self.originator = originator
        self.book = self.gui.doc["book"]
        self.menu_ad_cenario = self.menu___ROOT__ = self.menu_ad_objeto = self.menu_ad
        self.menu_wiki = self.menu_ad
        menu and self.build_menu(menu)

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

    def build_menu(self, menu=MENU_DEFAULT, display="none"):
        #print ("build_menu:", self.gui.div)
        Menu.MENU[self.originator] = self
        self.menu = self.gui.div(
            self.gui.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display=display, s_border='1px solid #d0d0d0', o_Id=self.item)
        #print ('build_menu', [self.comm[kwargs['o_click']] for kwargs in menu])
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
        #print('click:', menu_id, self.command + item, self.menu.Id, self.prefix)  # , self.item, item)
        self.activate(self.command + item, event, obj)

    def contextmenu(self, ev):
        if True:  # ev.button == 2:
            ev.stopPropagation()
            ev.preventDefault()
            #print('self menu:', self.menu, self.gui.win.pageXOffset, self.gui.win.pageYOffset)
            self.menu.style.display = 'block'
            self.menu.style.left = self.gui.menuX = ev.clientX + self.gui.win.pageXOffset
            self.menu.style.top = self.gui.menuY = ev.clientY + self.gui.win.pageYOffset
            self.gui.context_obj_id = ev.target.id[2:]
            return False

    def make_id(self, targ_id):
        oid = Gui.REV[targ_id] = Gui.REV.setdefault(targ_id, 0) + 1
        return ("o%d_" % oid) + targ_id

    def activate(self, command, ev, menu):
        #print('activate', command, ev.target.id, getattr(self, command))
        getattr(self, command)(ev, menu)

    def menu_ad(self, ev, menu):
        menu = menu.menu
        menu.style.display = 'block'
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
            s_left=prop.offsetLeft, s_top=prop.offsetTop)
        self._editar(ev, prop, kwargs)

    def _editar(self, ev, prop, kwargs):
        prop_box = self.gui.doc["propbox"]
        prop_size = self.gui.doc["propsize"]
        prop_size.style.backgroundColor = 'green'
        prop.style.backgroundColor = 'white'

        def _dropend(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop

            prop_size.style.backgroundColor = 'black'
            ev.preventDefault()
            ev.stopPropagation()
            kwargs.update(o_text=prop.html)
            print('_dropend', kwargs)
            self.gui.save(kwargs)
            self.gui.control.activate(**kwargs)
            prop.style.backgroundColor = 'transparent'
            prop_box.style.left = -90000
            prop_size.style.left = -90000
            prop.contentEditable = "false"

        x, y, w, h, s = prop.offsetLeft, prop.offsetTop, prop.offsetWidth, prop.offsetHeight, 10
        pboxs, psizes = prop_box.style, prop_size.style
        prop_size.bind('click', _dropend)
        psizes.left, psizes.top, psizes.width, psizes.height = x-5, y-5, s, s
        self.gui.book <= prop_size
        prop.contentEditable = "true"

    def menu_apagar(self, ev, menu):
        def delete(o_item, o_Id, **kwargs):
            #print('thumb', self.prefix, kwargs)
            self.gui.doc[o_Id].style.display = 'none'
            kwargs.update(o_cmd='DoDel', o_Id=o_Id, o_gcomp='delete')
            self.gui.save(kwargs)
        self.gui.control.activate(
            o_emp=delete, o_Id=self.gui.obj_id, o_cmd='DoDel')

    def menu_pular(self, ev, menu):
        def thumb(o_item, o_Id, **kwargs):
            #print('thumb', self.prefix, kwargs)
            self.activated = False
            self.build_item(o_Id, MENUITEM % o_item, menu)
        pane = menu.menu
        while (pane.hasChildNodes()):
            pane.removeChild(pane.lastChild)
        self.gui.control.activate(o_emp=thumb, o_cmd='DoList')
        pane.style.display = 'block'
        pane.style.left = self.gui.menuX
        pane.style.top = self.gui.menuY

    def menu_navegar(self, ev, menu):
        def thumb(o_item, o_Id, **kwargs):
            #print('thumb', self.prefix, kwargs)
            #item = '/'.join(o_src[:-7].split('/')[:-2])
            self.build_item(o_Id, MENUITEM % o_item, menu)
        pane = menu.menu
        while (pane.hasChildNodes()):
            pane.removeChild(pane.lastChild)
        self.gui.control.activate(o_emp=thumb, o_cmd='DoList')
        pane.style.display = 'block'
        pane.style.left = self.gui.menuX
        pane.style.top = self.gui.menuY

    def navegar(self, ev, menu):
        def up(o_Id, **kwargs):
            #print('up', self.prefix, o_Id)
            #item = '/'.join(o_src[:-7].split('/')[:-2])
            self.gui._locate(self.book, self.gui.doc[o_Id])
        kwargs = dict(
            o_emp=up, o_cmd="DoUp", o_part="Locus", o_Id=ev.target.id[2:]
        )
        self.gui.control.activate(**kwargs)

    def pular(self, ev, menu):
        def jump(o_Id, **kwargs):
            self.gui.doc[o_Id].onclick = self.gui.action

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
        kwargs = dict(
            o_emp=prop, o_cmd="DoAdd", o_part="Holder", o_gcomp="sprite",
            o_item=tid, o_src=SCENE % tid, o_Id=oid,
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
                self._editar(ev, prop, kwargs)
                #prop.oncontextmenu = self.gui.text_context  # gui.sel_prop
                #t.text = 'Lorem Ipsum'
                #self.gui.save(kwargs)
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
        #prop = self.gui.div(**kwargs)
        #prop = self.gui.doc[self.gui.obj_id]
        #kwargs = dict(
        #    o_emp=self.gui.shape, o_cmd='DoShape', o_Id=prop.id, o_gcomp='shape',
        #    s_left=prop.offsetLeft, s_top=prop.offsetTop)
        pass


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
        shaper.left, shaper.top = kwargs['s_left'], kwargs['s_top']
        print('shape', o_Id, shaper, shaper.left, kwargs)
        if ('s_width' in kwargs) or ('s_height' in kwargs):
            shaper.width, shaper.height = kwargs['s_width'], kwargs['s_height']
        if 'o_text' in kwargs:
            self.doc[o_Id].html = kwargs['o_text']

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
JEPPETO, LGM, NGM = "__J_E_P_P_E_T_O__", 'LOAD_GAME', 'NEW_GAME'
KWA = dict(s_position='absolute', s_opacity=0.1, s_top=180,
           o_src=MENUPX % 'drawing', o_width=400, o_height=400)


class Gui(GuiDraw):
    """Deal with incoming html events. :ref:`gui_event`
    """
    REV = {}

    def __init__(self, gui):
        self.doc, self.svg, self.html = gui.DOC, gui.SVG, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.storage, self.json = gui.STORAGE, gui.JSON
        self.main = self.doc["base"]
        self.book = self.doc["book"]
        #self.comm = dict(act_rubber=self.act_rubber, scenes=self.scenes, props=self.props)
        self.rubber_start = self.build_rubberband()
        self.start_div = self.div(self.book)
        self.lst = self.div(self.start_div, s_position='absolute', s_left=220,
                            s_top=510, s_width=300, s_display='none')
        self.img(
            self.start_div, MENUPX[:-4] % 'fundo.jpg', 1100, 800,
            s_position='absolute', s_left=0)
        self.img(self.start_div, o_Id=LGM, s_left=120, **KWA).onclick = self.start
        self.img(self.start_div, o_Id=NGM, s_left=530, **KWA).onclick = self.start
        self.deliverables = dict(
            div=self.div, iframe=self.iframe, sprite=self.sprite, text=self.text,
            drag=self.build_drag, drop=self.build_drop, shape=self.shape,
            up=self.up,  delete=self.delete, act=self.act)

    def object_context(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.obj_id = ev.target.id
        menu = Menu.MENU['ob_ctx'].menu
        menu.style.display = 'block'
        menu.style.left = self.menuX = ev.clientX + self.win.pageXOffset
        menu.style.top = self.menuY = ev.clientY + self.win.pageYOffset

    def text_context(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.obj_id = ev.target.id
        menu = Menu.MENU['tx_ctx'].menu
        menu.style.display = 'block'
        menu.style.left = self.menuX = ev.clientX + self.win.pageXOffset
        menu.style.top = self.menuY = ev.clientY + self.win.pageYOffset

    def action(self, event):
        self.control.activate(o_emp=self.employ, o_Id=event.target.id, o_cmd='DoExecute')

    def text(self, cmd=None, **kwargs):
        self.div(**kwargs).oncontextmenu = self.text_context  # gui.sel_prop

    def sprite(self, cmd=None, **kwargs):
        self.img(**kwargs).oncontextmenu = self.object_context  # gui.sel_prop

    def load(self, cmd=None):
        def render(o_gcomp, **kwargs):
            targ_id = kwargs['o_Id'].split('_')[1]
            if 'o_placeid' in kwargs:
                placeid = kwargs['o_placeid']
                place = self.doc[placeid]
                kwargs.update(o_place=place)
            Gui.REV[targ_id] = Gui.REV.setdefault(targ_id, 0) + 1
            self.control.activate(
                self.deliverables[o_gcomp], **kwargs)

        commands = self.json.loads(self.storage['_JPT_' + (cmd or self.game)])
        print('load:', self.control, self.storage['_JPT_' + (cmd or self.game)])
        [render(**kwargs) for kwargs in commands]

    def save(self, cmd):
        if (not 'o_placeid' in cmd) and 'o_place' in cmd and cmd['o_place']:
            cmd['o_placeid'] = cmd.pop('o_place').id
        elif 'o_place' in cmd:
            cmd.pop('o_place')
        #print('save,', cmd)
        self.storage['_JPT_'+self.game] = self.json.dumps(
            self.json.loads(self.storage['_JPT_'+self.game]) + [cmd])

    def start(self, ev):
        lst = self.lst

        def nameit(ev):
            self.game = ev.target.id[5:]
            #print('nameit', self.game)
            self.start_div.style.display = 'none'
            self.doc["illumini"].style.display = "none"
            self.doc["text"].style.display = "none"
            self.load()
        self.book <= lst

        if JEPPETO not in self.storage:
            self.storage[JEPPETO] = self.json.dumps([])
        games = self.json.loads(self.storage[JEPPETO])
        #print (games, len(games))
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
        req = self.ajax()
        req.on_complete = response
        req.set_timeout(TIMEOUT, response)
        req.open('GET', url, True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send()

    def employ(self, o_gcomp=None, o_placeid=None, **kwargs):
        place = kwargs.pop('o_place') or self.doc
        try:
            place = self.doc[o_placeid]
        except Exception:
            print('place rejected:', o_placeid, o_gcomp, kwargs)
        print ('employ', place, o_placeid, o_gcomp, kwargs)
        self.deliverables[o_gcomp](o_place=place, **kwargs)

    def sel_prop(self, ev):
        prop = self.doc[ev.target.id]
        prop_box = self.doc["propbox"]
        prop_size = self.doc["propsize"]
        prop_place = prop.parentNode

        def dragstart(ev):
            prop_box.unbind('dragstart', dragstart)
            prop_size.unbind('dragstart', sizestart)
            self.book.bind('drop', dropmove)
            _start(ev)

        def sizestart(ev):
            self.book.bind('drop', dropsize)
            _start(ev)

        def _start(ev):
            self.offx = ev.x - self.book.offsetLeft - prop_box.offsetLeft
            self.offy = ev.y - self.book.offsetTop - prop_box.offsetTop
            #print(ev, ev.data, ev.target.id, self.offx, self.offy)
            ev.data['text'] = ev.target.id
            ev.stopPropagation()
            # permitir que o objeto arrastado seja movido
            ev.data.effectAllowed = 'move'

        def dropmove(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop
            kwargs = dict(
                o_cmd='DoShape', o_Id=prop.id, o_gcomp='shape',
                s_left=ev.x-offx-self.offx, s_top=ev.y-offy-self.offy)
            _dropend(ev, kwargs)

        def _dropend(ev, kwargs):
            prop_place <= prop
            ev.preventDefault()
            ev.stopPropagation()
            self.book.unbind('drop')
            self.save(kwargs)
            self.control.activate(self.shape, **kwargs)
            prop_box.style.left = -90000
            prop_size.style.left = -90000

        def dropsize(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop
            cx = prop_box.offsetLeft + prop_box.offsetWidth // 2
            cy = prop_box.offsetTop + prop_box.offsetHeight // 2
            w, h = abs(ev.x - offx - cx), abs(ev.y - offy - cy)
            x, y = cx - w, cy - h
            kwargs = dict(
                o_cmd='DoShape', o_Id=prop.id, o_gcomp='shape',
                s_left=x, s_top=y, s_width=2*w, s_height=2*h)
            _dropend(ev, kwargs)

        def dragover(ev):
            #print(ev, ev.x, ev.y)
            ev.data.effectAllowed = 'move'
            ev.preventDefault()
        x, y, w, h, s = prop.offsetLeft, prop.offsetTop, prop.offsetWidth, prop.offsetHeight, 10
        #print ('GUi.sel_prop', ev.target.id, x, y, w, h)
        #prop.unbind('click')
        prop_box.bind('dragstart', dragstart)
        pboxs, psizes = prop_box.style, prop_size.style
        pboxs.left, pboxs.top, pboxs.width, prop_box.style.height = x, y, w, h
        self.book <= prop_box
        prop_size.bind('dragstart', sizestart)
        psizes.left, psizes.top, psizes.width, psizes.height = x-5, y-5, s, s
        self.book <= prop_size
        self.book.bind('dragover', dragover)
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
