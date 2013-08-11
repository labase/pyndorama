"""
############################################################
Pyndorama - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/08/11 $
:Status: This is a "work in progress"
:Revision: $Revision: 0.2 $
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Educational game construction.
"""
REPO = "/studio/%s"
IMG = 'http://j.mp/aegadian_sea'
SHIP = 'view/Trireme_1.png'


class Visual:
    """ Builder creating SVG elements and placeholder groups. :ref:`visual`
    """
    def __init__(self, doc, svg, html, ajax, win):
        self.doc, self.svg, self.html, self.ajax, self.win = doc, svg, html, ajax, win
        print(1)
        #args = win.location.search[1:]
        #self.args = {k: v for k, v in [c.split('=') for c in args.split('&')]}
        self.doc_id = doc["doc_id"]

        self.book = doc["book"]
        self.text = doc["text"]
        self.subtext = doc["subtext"]
        self.illumini = doc["illumini"]

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

    def build_ship(self, place):
        return self.gui.img(place=place, width=20, src=SHIP)

    def build_cell(self, place, name):
        S = 10
        SS = 9
        x, y = 1100 - 120 + (name % 50) * S, 100 + (name // 50) * S
        #stl = dict(position="absolute", width="%dpx" % SS, height="%dpx" % SS,
        #           opacity=0.5, top=y, left=x, backgroundColor="navajowhite")
        #cell = self.html.DIV(style=stl)
        #place <= cell
        return self.gui.div(
            place=place, o_position="absolute", o_width="%dpx" % SS, o_height="%dpx" % SS,
            o_opacity=0.5, o_top=y, o_left=x, o_backgroundColor="navajowhite")

    def build_convoy(self, convoy, size):
        fleet = self.gui.div(place=self.subtext, Class="fleet")
        self.ships = [self.build_ship(fleet) for ship in range(size)]
        return fleet

    def build_book(self, gui):
        self.gui = gui
        gui.iframe(place=self.text, width=450, height=600, Class="frame",
                   frameBorder=0, src="view/battle.html")
        gui.img(place=self.illumini, width=500, src=IMG)
        self.fleet = [self.build_convoy(convoy, 4) for convoy in range(6)]
        self.grid = [self.build_cell(self.book, name) for name in range(50*38)]


class Gui:
    """ Builder creating HTML, SVG elements and placeholder groups. :ref:`visual`
    """
    def __init__(self, doc, svg, html, ajax, win):
        self.doc, self.svg, self.html = doc, svg, html
        self.ajax, self.win = ajax, win
        self.main = doc["base"]

    def _locate(self, place, element):
        locus = place if place else self.main
        locus <= element
        return element

    def _filter(self, args):
        #print(args)
        return {k[2:]: value for k, value in args.items() if "o_" in k}

    def div(self, place=None, Class=None, **kwargs):
        #print(self._filter(kwargs))
        return self._locate(place, self.html.DIV(
            Class=Class, style=self._filter(kwargs)))

    def iframe(
        self, place=None, width=10, height=10, Class="frame",
            frameBorder=0, src="", **kwarg):
        """Html iframe."""
        return self._locate(place, self.html.IFRAME(
            width=width, height=height, Class=Class,
            frameBorder=frameBorder, src=src))

    def img(
            self, place=None, width=None, height=None, Class=None, src="", **k):
        """Html image. """
        return self._locate(place, self.html.IMG(
            width=width, height=height, Class=Class, src=src))
