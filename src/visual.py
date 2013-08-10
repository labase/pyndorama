"""
############################################################
Pyndorama - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/07/16 $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
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
    def __init__(self, doc, svg, html, ajax):
        self.doc, self.svg, self.html, self.ajax = doc, svg, html, ajax
        print(1)
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
        shipyard = self.html.IMG(width=20, src=SHIP)
        place <= shipyard
        return shipyard

    def build_cell(self, place, name):
        S = 10
        SS = 9
        x, y = 1100 - 120 + (name % 50) * S, 100 + (name // 50) * S
        stl = dict(position="absolute", width="%dpx" % SS, height="%dpx" % SS,
                   opacity=0.5, top=y, left=x, backgroundColor="navajowhite")
        cell = self.html.DIV(style=stl)
        place <= cell
        return cell

    def build_convoy(self, convoy, size):
        #fleet = self.html.DIV(style="margin: 10px;")
        #fleet = self.html.DIV(margin = "20px", Float = "left",
        #    width = "%dpx"%40*size, position = "relative")
        #fleet_style = dict(width="%dpx" % 40 * size)
        fleet = self.html.DIV(Class="fleet")  # , style = fleet_style)
        #fleet = self.doc["f%d" % convoy]
        self.ships = [self.build_ship(fleet) for ship in range(size)]
        self.subtext <= fleet
        #self.book <= fleet
        return fleet

    def build_book(self):
        text = self.html.IFRAME(width=450, height=600, Class="frame",
                                frameBorder=0, src="view/battle.html")
        print(20)
        self.text <= text
        illumini = self.html.IMG(width=500, src=IMG)
        self.illumini <= illumini
        self.fleet = [self.build_convoy(convoy, 4) for convoy in range(6)]
        self.grid = [self.build_cell(self.book, name) for name in range(50*38)]
