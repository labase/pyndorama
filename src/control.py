"""
############################################################
Pyndorama - Principal
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/12
:Status: This is a "work in progress"
:Revision: 0.1.3
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Pyndorama is a game creator using drag and drop style and Python.
"""
from visual import Builder
from visual import Gui
import model


class Main:
    """Create the game using HTML5 gui builder. :ref:`builder`
    """
    def __init__(self, builder, gui):
        """Initializes builder and gui. """
        self.builder, self.gui = builder, gui

    def build_all(self, builder):
        """Build all game parts, rendering to the gui."""
        builder.build_all(self.gui)


def main(gui):
    print('Pyndorama 0.1.0')
    builder = Builder(gui, model.init())
    app = Main(builder, Gui(gui))
    app.build_all(builder)
