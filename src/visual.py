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
REPO = "/studio/%s"
IMG = 'http://j.mp/aegadian_sea'
SHIP = 'view/Trireme_1.png'
MENU = "https://dl.dropboxusercontent.com/u/1751704/labase/pyndorama/%s.png"
DEFAULT = [
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
    dict(o_part='Dragger', o_Id='13161200990060', o_gcomp="drag", o_place='13081200990040',
         o_drop='13081200990020'),
    #dict(o_part='Grid', o_Id=13081200990050, o_gcomp={'0': 'img'}, o_width=30,
    #     o_place='13081200990030',  o_src={'0': SHIP}, o_mapper='0000')
]


class Builder:
    """ Builder creating model elements and rendering with gui components. :ref:`builder`
    """
    def __init__(self, gui, model):
        self.doc, self.svg, self.html = gui.DOC, gui.SVG, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.model = model
        #args = win.location.search[1:]
        #self.args = {k: v for k, v in [c.split('=') for c in args.split('&')]}

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
        self.build_deploy(DEFAULT)
        print(self.model.items)
        self.model.deploy(self.gui.employ)


class Gui:
    """Factory returning HTML, SVG elements and placeholder groups. :ref:`gui`
    """
    def __init__(self, gui):
        self.doc, self.svg, self.html = gui.DOC, gui.SVG, gui.HTML
        self.ajax, self.win, self.time = gui.AJAX, gui.WIN, gui.TIME
        self.main = self.doc["base"]
        self.doc.oncontextmenu = self._menu
        self.build_menu()
        self.rubber_start = self.build_rubberband()
        self.deliverables = dict(div=self.div, iframe=self.iframe, img=self.img,
                                 drag=self.build_dragndrop)

    def employ(self, o_gcomp=None, o_place=None, **kwargs):
        place = self.doc
        print ('employ', o_place, o_gcomp)
        try:
            place = self.doc[o_place]
        except Exception:
            print('place rejected:', o_place)
        self.deliverables[o_gcomp](o_place=place, **kwargs)

    def build_menu(self):
        def close(ev):
            self.menu.style.display = 'none'

        def rubber(ev):
            self.menu.style.display = 'none'
            self.doc["book"].bind('mousedown', self.rubber_start)

        self.menu = self.div(
            self.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display='none', s_border='1px solid #d0d0d0')
        self.img(self.menu, o_src=MENU % 'ad_objeto', s_padding='2px').onclick = rubber
        self.img(self.menu, o_src=MENU % 'ad_cenario', s_padding='2px').onclick = close

    def build_dragndrop(self, o_place, o_drop, **kwargs):
        def start(ev):
            print(ev, ev.data, ev.target.id)
            ev.data['text'] = ev.target.id
            # permitir que o objeto arrastado seja movido
            ev.data.effectAllowed = 'move'

        def drag_over(ev):
            ev.target.style.cursor = "pointer"

        def drop_over(ev):
            #ev.data.dropEffect = 'move'
            ev.preventDefault()

        def drop(ev):
            src_id = ev.data['text']
            elt = self.doc[src_id]
            self.doc[kwargs['action'](src_id)] <= elt
        print('drag', o_drop, o_place)
        draggable, droppable = o_place, self.doc[o_drop]
        draggable.draggable, draggable.onmousedown = True, start
        draggable.onmouseover = drag_over
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
            self.doc.unbind('mouseup', stop)  # , stop)
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
            #alert('menu')
            self.menu.style.display = 'block'
            return False

    def _locate(self, place, element):
        locus = place if place else self.main
        locus <= element
        return element

    def _filter(self, args):
        #print(args)
        return {k[2:]: value for k, value in args.items() if k[:2] in "s_"}

    def div(self, o_place=None, o_Id=None, o_Class='deafault', **kwargs):
        print(kwargs, self._filter(kwargs))
        return self._locate(o_place, self.html.DIV(
            Id=o_Id, Class=o_Class, style=self._filter(kwargs)))

    def iframe(
        self, o_place=None, o_width=10, o_height=10, o_Id=None, o_Class="frame",
            o_frameBorder=0, o_src="", **kwarg):
        """Html iframe."""
        return self._locate(o_place, self.html.IFRAME(
            Id=o_Id, width=o_width, height=o_height, Class=o_Class,
            frameBorder=o_frameBorder, src=o_src))

    def img(
            self, o_place=None, o_src="", o_width='',
            o_height='', o_Id='', o_Class='deafault', **kwargs):
        """Html image. """
        return self._locate(o_place, self.html.IMG(
            Id=o_Id, width=o_width, height=o_height, Class=o_Class,
            src=o_src, style=self._filter(kwargs)))
