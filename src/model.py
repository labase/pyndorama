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

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        self.items = []
        #print ("Thing init:", fab, part, o_Id)
        self.create(fab=fab, part=part, o_Id=o_Id, **kwargs)

    def create(self, fab=None, part=None, o_Id=None, **kwargs):
        """Fabricate and return a given part."""
        #print ("create:", fab, part, o_Id, kwargs, self)
        self.o_Id = o_Id or len(Thing.ALL_THINGS)
        self.o_part = part
        (fab or self).register(o_Id or 13081299999999, self)
        self._add_properties(**kwargs)
        self._do_create()

    def employ(self, o_part=None, o_Id=None, **kwargs):
        """Fabricate and locate a given part."""
        #print ("employ:", o_part, o_Id, kwargs)
        try:
            thing_class = Thing.INVENTORY[o_part]
            thing_class(fab=self, part=o_part, o_Id=o_Id, **kwargs)
        except Exception:
            print ("error creating %s id = %s" % (o_part, o_Id))

    def register(self, oid, entry):
        """Append an entry to this resgistry. """
        Thing.ALL_THINGS[oid] = entry

    def append(self, item):
        """Append this thing to this container. """
        self.items.append(item)
        return self

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        for item in self.items:
            item.deploy(site=site, **kwargs)

    def _do_create(self):
        """Finish thing creation. """
        pass

    def _add_properties(self, **kwargs):
        """Finish thing creation. """
        #print (kwargs)
        [setattr(self, argument, value)
         for argument, value in kwargs.items() if argument[:2] in "o_ s_"]


class Holder(Thing):
    """A paceholder for gui positioning scaffolding."""

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        kwargs['o_Id'] = o_Id
        self._add_properties(**kwargs)

    def append(self, item):
        """Append this item to the master container. """
        return THETHING

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        print(self.o_place, self.o_width)
        site(**{argument: getattr(self, argument)
                for argument in dir(self) if argument[:2] in "o_ s_"})


class Locus(Thing):
    """A place where things happen."""

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        self.items = []
        #print ("Thing init:", fab, part, o_Id)
        self.create(fab=fab, part=part, o_Id=o_Id, **kwargs)

    def _do_create(self):
        """Finish thing creation. """
        container = Thing.ALL_THINGS.setdefault(self.o_place, THETHING)
        #Thing.ALL_THINGS[self.o_place] = self
        self.container = container.append(self)
        #print("""Finish thing creation. """, container, self.o_place, self.container, self)

    def deploy(self, site=None, **kwargs):
        """Deploy this thing at a certain site. """
        site(**{argument: getattr(self, argument)
                for argument in dir(self) if argument[:2] in "o_ s_"})
        for item in self.items:
            item.deploy(site=site, **kwargs)


class Grid(Thing):
    """A place where things happen."""

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        self.items = []
        #print ("Thing init:", fab, part, o_Id)
        self.create(fab=fab, part=part, o_Id=o_Id, **kwargs)
        mapper, gcomp, src = [kwargs.pop(arg)
                              for arg in 'o_mapper o_gcomp o_src'. split()]
        objid, args = o_Id, kwargs
        self.items = [
            Holder(o_Id=objid+i, o_gcomp=gcomp[k], o_src=src[k], **args)
            for i, k in enumerate(mapper)]

    def _do_create(self):
        """Finish thing creation. """
        self.container = Thing.ALL_THINGS.setdefault(
            self.o_place, THETHING).append(self)


def init():
    global THETHING
    THETHING = Thing()
    Thing.INVENTORY.update(dict(Locus=Locus, Holder=Holder, TheThing=THETHING,
                                Grid=Grid))
    print (Thing.INVENTORY, Thing.ALL_THINGS)
    return THETHING
