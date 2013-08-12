"""
############################################################
Pyndorama - Model
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/12
:Status: This is a "work in progress"
:Revision: 0.1.2
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Game model comprising of Loci and Actors
"""
THETHING = None


class Thing:
    """A commom element for every other element."""
    ALL_THINGS = {}
    INVENTORY = {}

    def __init__(self, fab=None, part=None, o_id=None, **kwargs):
        self.create(fab=fab, part=part, o_id=o_id, **kwargs)

    def create(self, fab=None, part=None, o_id=None, **kwargs):
        """Fabricate and return a given part."""
        self.o_id = o_id or len(Thing.ALL_THINGS)
        self.items = []
        self.o_part = part
        (fab or self).register(o_id or 130812999999, self)
        self._add_properties(**kwargs)
        self._do_create()

    def employ(self, part=None, o_id=None, **kwargs):
        """Fabricate and locate a given part."""
        try:
            thing_class = Thing.INVENTORY[part](o_id=o_id)
            thing_class(fab=self, part=part, o_id=o_id, **kwargs)
        except Exception:
            print ("error creating %s id = %s" % (part, o_id))

    def register(self, oid, entry):
        """Append an entry to this resgistry. """
        Thing.ALL_THINGS[oid] = entry

    def append(self, item):
        """Append this thing to this container. """
        self.items.append(item)
        return self

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        site({argument: getattr(self, argument)
              for argument in dir(self) if argument.startswith("o_")})

    def _do_create(self):
        """Finish thing creation. """
        pass

    def _add_properties(self, **kwargs):
        """Finish thing creation. """
        [setattr(self, argument, value)
         for argument, value in kwargs.items() if argument.startswith("o_")]


class Holder(Thing):
    """A paceholder for gui positioning scaffolding."""

    def __init__(self, fab=None, part=None, o_id=None, **kwargs):
        fab.register(o_id, self)

    def append(self, item):
        """Append this item to the master container. """
        return THETHING


class Locus(Thing):
    """A place where things happen."""

    #def __init__(self, fab=None, part=None, o_id=None, **kwargs):
    #    Thing.__init__(self, o_id)

    def _do_create(self):
        """Finish thing creation. """
        container = Thing.ALL_THINGS.setdefault(self.o_con, THETHING)
        #Thing.ALL_THINGS[self.o_con] = self
        self.container = container.append(self)

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        Thing.deploy(site=site, **kwargs)
        [item.deploy(site=site, **kwargs) for item in self.items]
        site({argument: getattr(self, argument)
              for argument in dir(self) if argument.startswith("o_")})


def init():
    global THETHING
    THETHING = Thing()
    Thing.INVENTORY.update(dict(Locus=Locus, Holder=Holder, TheThing=THETHING))
    print (Thing.INVENTORY, Thing.ALL_THINGS)
    return THETHING

