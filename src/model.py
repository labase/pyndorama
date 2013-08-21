"""
############################################################
Pyndorama - Model
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/15
:Status: This is a "work in progress"
:Revision: 0.3
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

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        for item in self.items:
            item.deploy(employ=employ, **kwargs)

    def visit(self, visiting):
        """Visit across the structure. """
        for item in self.items:
            visiting(item)

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
        self.o_part, kwargs['o_Id'] = self.__class__.__name__, o_Id
        self._add_properties(**kwargs)

    def append(self, item):
        """Append this item to the master container. """
        return THETHING

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        #print(self.o_place, self.o_width)
        employ(**{argument: getattr(self, argument)
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
        self.container = container.append(self)
        #print("""Finish thing creation. """, container, self.o_place, self.container, self)

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        employ(**{argument: getattr(self, argument)
                  for argument in dir(self) if argument[:2] in "o_ s_"})
        for item in self.items:
            item.deploy(employ=employ, **kwargs)


class Grid(Locus):
    """A mapped grid with sub elements."""

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        #print ("Thing init:", fab, part, o_Id)
        kwargs['o_gcomp'] = 'div'
        self.create(fab=fab, part=part, o_Id=o_Id, **kwargs)
        self.items, kwargs['o_place'], kwargs['o_gcomp'] = [], o_Id, 'div'
        grid, invent = kwargs.pop('o_grid')
        args = {key[1:]: value for key, value in kwargs.items() if key[:3] in "go_ gs_ "}
        objid, args['o_place'], obj = o_Id, o_Id, self  # kwargs  # .items()
        #return
        self.items = [
            invent[ckey].update(args) or Thing.INVENTORY[invent[ckey]['o_part']](
                o_Id=objid+str(i), **invent[ckey]) for i, ckey in enumerate(grid)]

    def ___do_create(self):
        """Finish thing creation. """
        self.container = Thing.ALL_THINGS.setdefault(
            self.o_place, THETHING).append(self)


class Dragger(Holder):
    """A drag decorator."""
    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        Holder.__init__(self, o_Id=o_Id)
        dropper, dragger, self.kwargs = kwargs['o_drop'], kwargs['o_place'], kwargs
        self.dropper = Thing.ALL_THINGS[dropper]
        self.dragger = Thing.ALL_THINGS[dragger]
        self.dropper.receive = self.receive
        self.dragger.visit(self.visiting)
        kwargs['action'] = self.dropper.receive
        self._add_properties(**kwargs)
        THETHING.append(self)

    def visiting(self, visited):
        visited.enter = self.enter

    def receive(self, guest_id):
        return Thing.ALL_THINGS[guest_id].enter(self.dropper)

    def enter(self, host):
        self.container = host
        return self.o_Id


def init():
    global THETHING
    THETHING = Thing()
    Thing.INVENTORY.update(dict(Locus=Locus, Holder=Holder, TheThing=THETHING,
                                Grid=Grid, Dragger=Dragger))
    #print (Thing.INVENTORY, Thing.ALL_THINGS)
    return THETHING
