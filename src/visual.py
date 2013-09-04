"""
############################################################
Pyndorama - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/08/31 $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1.6 $
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
EICAP = ["jeppeto/ampu.png", "jeppeto/ampulheta.png", "jeppeto/astrolabio.png",
         "jeppeto/Astrolabio.png", "jeppeto/astrolabiobserv.png"]
E_MENU = lambda item, ck="act_rubber": dict(
    o_Id=item, o_src=MENUITEM % item, s_padding='2px', o_click=ck, o_title=item)
STUDIO = "https://activufrj.nce.ufrj.br/studio/EICA/%s?disp=inline&size=N"
#NO_MENU_DEFAULT = [dict(o_src=MENU % 'ad_objeto', s_padding='2px', o_click="props"),
#                dict(o_src=MENU % 'ad_cenario', s_padding='2px', o_click="scenes")]
MENU_DEFAULT = ['ad_objeto', 'ad_cenario', 'navegar']
DEFAULT = [
]
NODEFAULT = [
    dict(o_part='Locus', o_Id='13081200990010', o_gcomp='iframe', o_place='text',
         o_width=450, o_height=600,
         o_Class="frame", o_frameBorder=0, o_src="view/battle.html"),
    dict(o_part='Locus', o_Id='13081200990020', o_gcomp='img', o_place='illumini',
         o_width=500, o_src=IMG),
    dict(o_part='Locus', o_Id='13081200990030', o_gcomp='div', o_place='subtext',
         o_Class="fleet"),
    dict(o_part='Grid', o_Id='13081200990040', go_width=30, o_place='13081200990030',
         gs_backgroundColor='white', s_width=140,
         o_grid=["0000", {"0": dict(o_part='Holder', o_gcomp="img", o_src=SHIP)}]),
    dict(o_part='Grid', o_Id='13081200990050', go_width=30, o_place='13081200990030',
         gs_backgroundColor='navajowhite', s_width=120,
         o_grid=["0000", {"0": dict(o_part='Holder', o_gcomp="img", o_src=SHIP)}]),
    #dict(o_part='Dragger', o_Id='13161200990060', o_gcomp="drag", o_place='13081200990040',
    #     o_drop='13081200990020'),
    #dict(o_part='Inventary', o_Id=13082300990010, o_gcomp={'0': 'img'}, o_width=30,
    #     o_place='13081200990030',  o_src={'0': SHIP}, o_mapper='0000')
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
                 command='gomenu', prefix=MENUPX, event="click"):
        self.gui, self.item, self.prefix = gui, originator, prefix
        self.command, self.prefix = command, prefix
        self.originator = originator
        self.book = self.gui.doc["book"]
        menu and self.build_menu(menu)

    def build_item(self, item):
        #print('build_item', self.prefix, item)
        pr = self.prefix % item
        kwargs = dict(o_Id=item, o_src=pr, s_padding='2px', o_title=item)
        menu_item = self.gui.img(self.menu, **kwargs)
        menu_item.bind("click", self.click)
        return menu_item

    def build_menu(self, menu=MENU_DEFAULT, display="none"):
        #print ("build_menu:", self.gui.div)
        self.menu = Menu.MENU[self.originator] = self.gui.div(
            self.gui.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display=display, s_border='1px solid #d0d0d0', o_Id=self.item)
        #print ('build_menu', [self.comm[kwargs['o_click']] for kwargs in menu])
        [self.build_item(item) for item in menu]
        return self.menu

    def click(self, event):
        event.stopPropagation()
        event.preventDefault()
        self.menu.style.display = 'none'
        #print('click:', event.target.id, self.menu.Id, self.prefix, self.originator, self.item)
        obj = event.target.id in Menu.MENU and Menu.MENU[event.target.id] or self
        self.activate(self.command or self.item, event, obj)

    def contextmenu(self, ev):
        if True:  # ev.button == 2:
            ev.stopPropagation()
            ev.preventDefault()
            print('self menu:', self.menu, self.gui.win.pageXOffset, self.gui.win.pageYOffset)
            self.menu.style.display = 'block'
            self.menu.style.left = self.gui.menuX = ev.clientX + self.gui.win.pageXOffset
            self.menu.style.top = self.gui.menuY = ev.clientY + self.gui.win.pageYOffset
            return False

    def make_id(self, targ_id):
        oid = Gui.REV[targ_id] = Gui.REV.setdefault(targ_id, 0) + 1
        return "o%d_" % oid + targ_id

    def activate(self, command, ev, menu):
        print('activate', command, getattr(self, command))
        getattr(self, command)(ev, menu)

    def gomenu(self, ev, menu):
        menu.style.display = 'block'
        menu.style.left = self.gui.menuX
        menu.style.top = self.gui.menuY

    def latemenu(self, ev, menu):
        menu.style.display = 'block'
        menu.style.left = self.gui.menuX
        menu.style.top = self.gui.menuY

    def navegar(self, ev, menu):
        oid = ev.target.id
        kwargs = dict(
            o_emp=self.gui.div, o_cmd="DoUp", o_part="Locus", o_Id=oid
        )
        self.gui.control.activate(**kwargs)

    def ad_cenario(self, ev, menu):
        oid = self.make_id(ev.target.id)
        kwargs = dict(
            o_emp=self.gui.div, o_cmd="DoAdd", o_part="Locus", o_Id=oid,
            s_background='url(%s) no-repeat' % (SCENE % ev.target.id),
            s_width=1100, s_height=800, s_top=0, o_gcomp="div", o_place=self.book,
            s_backgroundSize="100% 100%", s_left=0, s_position='absolute'
        )
        self.gui.control.activate(**kwargs)
        self.gui.save(kwargs)

    def ad_objeto(self, ev, menu):
        offx, offy, tid = self.book.offsetLeft, self.book.offsetTop, ev.target.id
        oid = self.make_id(ev.target.id)
        self.gui.img(
            self.book, o_src=SCENE % ev.target.id, o_Id=oid,
            s_position='absolute', s_float='left', s_top=self.gui.menuY-offy,
            s_left=self.gui.menuX-offx, o_title=tid).onclick = self.gui.sel_prop


class GuiDraw(object):
    """Factory returning HTML, SVG elements and placeholder groups. :ref:`gui`
    """
    def _locate(self, place, element, kwargs=[]):
        #print(kwargs)
        if 's_backgroundSize' in kwargs:
            element.style.backgroundSize = kwargs['s_backgroundSize']
        locus = place if place else self.main
        locus <= element
        return element

    def _filter(self, args):
        #print(args)
        return {k[2:]: value for k, value in args.items() if k[:2] in "s_"}

    def div(self, o_place=None, o_Id=None, o_Class='deafault', **kwargs):
        #print(kwargs, self._filter(kwargs))
        return self._locate(o_place, self.html.DIV(
            Id=o_Id, Class=o_Class, style=self._filter(kwargs)), kwargs)

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
            title=o_title, src=o_src, style=self._filter(kwargs)))
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
        self.lst = self.div(self.book, s_position='absolute', s_left=220,
                            s_top=510, s_width=300, s_display='none')
        #self.comm = dict(act_rubber=self.act_rubber, scenes=self.scenes, props=self.props)
        self.rubber_start = self.build_rubberband()
        self.img(
            self.book, MENUPX[:-4] % 'fundo.jpg', 1100, 800,
            s_position='absolute', s_left=0)
        self.img(self.book, o_Id=LGM, s_left=120, **KWA).onclick = self.start
        self.img(self.book, o_Id=NGM, s_left=530, **KWA).onclick = self.start
        self.deliverables = dict(div=self.div, iframe=self.iframe, img=self.img,
                                 drag=self.build_drag, drop=self.build_drop)

    def load(self, cmd=None):
        def render(o_gcomp, o_place, **kwargs):
            self.control.activate(
                self.deliverables[o_gcomp], o_place=self.doc[o_place], **kwargs)

        commands = self.json.loads(self.storage['_JPT_' + (cmd or self.game)])
        #print('load:', self.control, commands)
        [render(**kwargs) for kwargs in commands]

    def save(self, cmd):
        cmd['o_place'] = cmd.pop('o_place').id
        self.storage['_JPT_'+self.game] = self.json.dumps(
            self.json.loads(self.storage['_JPT_'+self.game]) + [cmd])

    def start(self, ev):
        lst = self.lst

        def nameit(ev):
            self.game = ev.target.id[5:]
            #print('nameit', self.game)
            lst.style.display = 'none'
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

    def employ(self, o_gcomp=None, o_place=None, **kwargs):
        place = self.doc
        print ('employ', o_place, o_gcomp, kwargs)
        try:
            place = self.doc[o_place]
        except Exception:
            print('place rejected:', o_place)
        self.deliverables[o_gcomp](o_place=place, **kwargs)

    def sel_prop(self, ev):
        prop = self.doc[ev.target.id]
        prop_box = self.doc["propbox"]
        prop_size = self.doc["propsize"]

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
            print(ev, ev.data, ev.target.id, self.offx, self.offy)
            ev.data['text'] = ev.target.id
            ev.stopPropagation()
            # permitir que o objeto arrastado seja movido
            ev.data.effectAllowed = 'move'

        def dropmove(ev):
            offx, offy = self.book.offsetLeft, self.book.offsetTop
            self.book <= prop
            prop.style.left, prop.style.top = ev.x - offx-self.offx, ev.y - offy - self.offy
            self.book.unbind('drop')
            prop_box.style.left = -90000
            prop_size.style.left = -90000
            ev.preventDefault()

        def dropsize(ev):
            ev.preventDefault()
            ev.stopPropagation()
            self.book.unbind('drop')
            offx, offy = self.book.offsetLeft, self.book.offsetTop
            self.book <= prop
            cx = prop_box.offsetLeft + prop_box.offsetWidth // 2
            cy = prop_box.offsetTop + prop_box.offsetHeight // 2
            w, h = abs(ev.x - offx - cx), abs(ev.y - offy - cy)
            x, y = cx - w, cy - h
            #w, h = abs(ev.x - cx), abs(y - cy)
            prop_box.style.left = -90000
            prop_size.style.left = -90000
            print('dropsize', x, y, w, h)
            prop.style.left, prop.style.top, prop.style.width, prop.style.height = x, y, 2*w, 2*h
            prop_box.unbind('dragstart', dragstart)
            prop_size.unbind('dragstart', sizestart)

        def dragover(ev):
            #print(ev, ev.x, ev.y)
            ev.data.effectAllowed = 'move'
            ev.preventDefault()
        x, y, w, h, s = prop.offsetLeft, prop.offsetTop, prop.offsetWidth, prop.offsetHeight, 10
        print (ev.target.id, x, y, w, h)
        #prop.unbind('click')
        prop_box.bind('dragstart', dragstart)
        prop_box.style.left, prop_box.style.top, prop_box.style.width, prop_box.style.height = x, y, w, h
        self.book <= prop_box
        prop_size.bind('dragstart', sizestart)
        prop_size.style.left, prop_size.style.top, prop_size.style.width, prop_size.style.height = x-5, y-5, s, s
        self.book <= prop_size
        self.book.bind('dragover', dragover)
        prop.style.left, prop.style.top = 0, 0
        prop_box <= prop
        #self.div(self.book, s_width=w, s_height=h, s_top=y, s_left=x, s_position='absolute',
        #         s_backgroundColor="white")  # , s_opacity=0.5)

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
