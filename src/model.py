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
THETHING = None


class Thing:
    """A commom element for every other element."""
    ALL_THINGS = {}
    INVENTORY = {}

    def __init__(self, o_id=None):
        self.o_id = o_id or len(Thing.ALL_THINGS)
        self.items = []

    def create(self, part=None, o_id=None, **kwargs):
        """Fabricate a given part. """
        self.o_part = part
        o_id = o_id or len(Thing.ALL_THINGS)
        try:
            a_thing = Thing.INVENTORY[part](o_id=o_id)
            a_thing.create(part=part, o_id=o_id, **kwargs)
            Thing.ALL_THINGS.append(a_thing)
            a_thing._add_properties(**kwargs)
            self._do_create(a_thing)
        except Exception:
            print ("error creating %s id = %s" % (part, o_id))

    def append(self, item):
        """Append this thing to this container. """
        self.items.append(item)

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        site({argument: getattr(self, argument)
              for argument in dir(self) if argument.startswith("o_")})

    def _do_create(self, a_thing):
        """Finish thing creation. """
        pass

    def _add_properties(self, **kwargs):
        """Finish thing creation. """
        [setattr(self, argument, value)
         for argument, value in kwargs.items() if argument.startswith("o_")]


class Locus(Thing):
    """A place where things happen."""

    def __init__(self, o_id=None):
        Thing.__init__(self, o_id)

    def _do_create(self, a_thing):
        """Finish thing creation. """
        self.container = Thing.ALL_THINGS.setdefault(self.o_con, THETHING)
        Thing.ALL_THINGS[self.o_con] = self
        self.container.append(self)

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        Thing.deploy(site=site, **kwargs)
        [item.deploy(site=site, **kwargs) for item in self.items]
        site({argument: getattr(self, argument)
              for argument in dir(self) if argument.startswith("o_")})


def init():
    global THETHING
    THETHING = Thing()
    Thing.INVENTORY.update(dict(Locus=Locus, TheThing=THETHING))

