"""
############################################################
Pyndorama - Model
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/10
:Status: This is a "work in progress"
:Revision: 0.1.1
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Game model comprising of Loci and Actors
"""


class Thing:
    """A commom element for every other element."""
    ALL_THINGS = []

    def __init__(self, obj_id):
        self.obj_id = obj_id

    def create(self, part=None):
        """Fabricate a given part. """
        pass


class Locus:
    """A place where things happen."""
    ALL_THINGS = []

    def __init__(self, obj_id):
        self.obj_id = obj_id
