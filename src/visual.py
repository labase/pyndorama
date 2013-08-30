"""
############################################################
Pyndorama - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/08/16 $
:Status: This is a "work in progress"
:Revision: $Revision: 0.4 $
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
MENU = "https://dl.dropboxusercontent.com/u/1751704/labase/pyndorama/%s.png"
MENULIST = ACTIV + '/rest/studio/%s?type=%d'
MENUITEM = ACTIV + '/rest/studio/%s?size=N'
EICA = ["EICA/1_1c.jpg", "EICA/1_2c.jpg", "EICA/2_1c.jpg",
        "EICA/3_1c.jpg", "EICA/3_2.png", "EICA/4_2c.jpg"]
EICAP = ["jeppeto/ampu.png", "jeppeto/ampulheta.png", "jeppeto/astrolabio.png",
         "jeppeto/Astrolabio.png", "jeppeto/astrolabiobserv.png"]
E_MENU = lambda item, ck="act_rubber": dict(
    o_Id=item, o_src=MENUITEM % item, s_padding='2px', o_click=ck, o_title=item)
STUDIO = "https://activufrj.nce.ufrj.br/studio/EICA/%s?disp=inline&size=N"
MENU_DEFAULT = [dict(o_src=MENU % 'ad_objeto', s_padding='2px', o_click="props"),
                dict(o_src=MENU % 'ad_cenario', s_padding='2px', o_click="scenes")]
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

    def build_all(self, gui):
        self.gui = gui
        self.gui.control = self.model
        self.build_deploy(DEFAULT)
        print(self.model.items)
        self.model.deploy(self.gui.employ)


class Menu(object):
    MENU = {}

    def __init__(self, seed=MENU_DEFAULT):
        self.build_menu(seed)

    def build_menu(self, menu=MENU_DEFAULT, display="none"):
        _menu = self.div(
            self.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display=display, s_border='1px solid #d0d0d0')
        #print ('build_menu', [self.comm[kwargs['o_click']] for kwargs in menu])
        [self.img(_menu, **kwargs).bind(
            "click", getattr(self, kwargs['o_click'])) for kwargs in menu]
        return _menu

    def action(self, event):
        menu = Menu.MENU[event.target.id]
        self.menu.style.display = 'none'
        self.s_menu.style.display = 'block'
        self.s_menu.style.left = self.menuX
        self.s_menu.style.top = self.menuY

    def _menu(self, ev):
        if True:  # ev.button == 2:
            ev.stopPropagation()
            ev.preventDefault()
            #print('self menu:', self.menu)
            self.menu.style.display = 'block'
            self.menu.style.left = self.menuX = ev.clientX
            self.menu.style.top = self.menuY = ev.clientY
            return False


class GuiEvent:
    """Deal with incoming html events. :ref:`gui_event`
    """
    REV = {}

    def __init__(self, gui):
        self.doc, self.svg, self.html = gui.DOC, gui.SVG, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.main = self.doc["base"]
        self.book = self.doc["book"]
        self.comm = dict(act_rubber=self.act_rubber, scenes=self.scenes, props=self.props)
        self.menu = self.build_menu(display='none')
        self.s_menu = self.build_menu([E_MENU(item, ck="act_scene") for item in EICA])
        self.p_menu = self.build_menu([E_MENU(item, ck="act_prop") for item in EICAP])
        self.doc.oncontextmenu = self._menu
        self.rubber_start = self.build_rubberband()
        self.deliverables = dict(div=self.div, iframe=self.iframe, img=self.img,
                                 drag=self.build_drag, drop=self.build_drop)

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

    def make_id(self, targ_id):
        oid = Gui.REV[targ_id] = Gui.REV.setdefault(targ_id, 0) + 1
        return "o%d_" % oid + targ_id

    def act_scene(self, ev):
        self.s_menu.style.display = 'none'
        #self.img(
        #    self.book, o_src=SCENE % ev.target.id, o_width=1100, s_top=0,
        #    s_left=0, o_Id=self.make_id(ev.target.id), s_position='absolute')
        oid = self.make_id(ev.target.id)
        kwargs = dict(
            s_background='url(%s) no-repeat' % (SCENE % ev.target.id),
            s_width=1100, s_height=800, s_top=0, o_gcomp="div", o_place=self.book,
            s_backgroundSize="100% 100%", s_left=0, s_position='absolute'
        )
        #scene = self.div(
        #    self.book, o_Class="bookpage", o_Id=oid, **kwargs)
        #scene.style.backgroundSize = "100% 100%"
        self.control.activate(
            self.div, o_cmd="DoAdd", o_part="Locus", o_Id=oid, **kwargs)

    def act_prop(self, ev):
        self.p_menu.style.display = 'none'
        offx, offy, tid = self.book.offsetLeft, self.book.offsetTop, ev.target.id
        self.img(self.book, o_src=SCENE % ev.target.id, o_Id=self.make_id(tid),
                 s_position='absolute', s_float='left', s_top=self.menuY-offy,
                 s_left=self.menuX-offx, o_title=tid).onclick = self.sel_prop

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

    def scenes(self, ev):
        self.menu.style.display = 'none'
        self.s_menu.style.display = 'block'
        self.s_menu.style.left = self.menuX
        self.s_menu.style.top = self.menuY

    def props(self, ev):
        self.menuitem = ev.target.id
        self.menu.style.display = 'none'
        self.p_menu.style.left = self.menuX
        self.p_menu.style.top = self.menuY
        self.p_menu.style.display = 'block'

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

    def _menu(self, ev):
        if True:  # ev.button == 2:
            ev.stopPropagation()
            ev.preventDefault()
            #print('self menu:', self.menu)
            self.menu.style.display = 'block'
            self.menu.style.left = self.menuX = ev.clientX
            self.menu.style.top = self.menuY = ev.clientY
            return False


class Gui(GuiEvent):
    """Factory returning HTML, SVG elements and placeholder groups. :ref:`gui`
    """
    def build_menu(self, menu=MENU_DEFAULT, display="none"):
        _menu = self.div(
            self.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display=display, s_border='1px solid #d0d0d0')
        #print ('build_menu', [self.comm[kwargs['o_click']] for kwargs in menu])
        [self.img(_menu, **kwargs).bind(
            "click", getattr(self, kwargs['o_click'])) for kwargs in menu]
        return _menu

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
            self, o_place=None, o_src="", o_width='', o_title='', o_alt="",
            o_height='', o_Id='', o_Class='deafault', **kwargs):
        """Html image. """
        return self._locate(o_place, self.html.IMG(
            Id=o_Id, width=o_width, height=o_height, Class=o_Class, alt=o_alt,
            title=o_title, src=o_src, style=self._filter(kwargs)))
