"""
############################################################
Pyndorama - Model
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/09/13
:Status: This is a "work in progress"
:Revision: 0.1.5
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Game model comprising of Loci and Actors
0.1.4 Add commands for game action
0.1.5 Add selectable action to holder
"""
THETHING = None


class Thing:
    """A commom element for every other element."""
    ALL_THINGS = {}
    INVENTORY = {}
    CONTROL = {}

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        self.items = []
        #print ("Thing init:", fab, part, o_Id)
        self.create(fab=fab, part=part, o_Id=o_Id, **kwargs)
        self.container = self.o_part = self.o_Id = self.current = None

    def create(self, fab=None, part=None, o_Id=None, **kwargs):
        """Fabricate and return a given part."""
        #print ("create:", fab, part, o_Id, kwargs, self)
        self.o_part, kwargs['o_Id'] = self.__class__.__name__, o_Id
        self.o_Id = o_Id or len(Thing.ALL_THINGS)
        self.o_part = part
        (fab or self).register(o_Id or 13081299999999, self)
        self._add_properties(**kwargs)
        self._do_create()

    def activate(self, o_emp=None, o_cmd="DoAdd", o_part=None, o_Id=None, o_place=None, **kwargs):
        """Activate a given command."""
        try:
            kwargs['o_place'] = o_place
            #print("activate:", o_emp, o_cmd, o_part, o_Id, o_place, kwargs)
            thing_class = Thing.CONTROL[o_cmd]
            return thing_class(o_emp, fab=self, o_part=o_part, o_Id=o_Id, **kwargs)
        except Exception:
            print("error activating %s id = %s, place %s" % (o_part, o_Id, o_place))

    def employ(self, o_part=None, o_Id=None, **kwargs):
        """Fabricate and locate a given part."""
        #print ("employ:", o_part, o_Id, kwargs)
        try:
            thing_class = Thing.INVENTORY[o_part]
            return thing_class(fab=self, part=o_part, o_Id=o_Id, **kwargs)
        except Exception:
            print("error creating %s id = %s" % (o_part, o_Id))

    def register(self, oid, entry):
        """Append an entry to this resgistry. """
        Thing.ALL_THINGS[oid] = entry

    def remove(self, item):
        """Remove this thing from this container. """
        self.items.remove(item)
        return self

    def append(self, item):
        """Append this thing to this container. """
        self.items.append(item)
        return self

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        for item in self.items:
            item.deploy(employ=employ, **kwargs)

    def shape(self, o_Id, **kwargs):
        """Set member as current. """
        shaped = Thing.ALL_THINGS[o_Id]
        shaped._add_properties(**kwargs)
        return shaped

    def delete(self, o_Id, employ):
        """Set member as current. """
        deleted = Thing.ALL_THINGS[o_Id]
        deleted.deploy(employ)
        oid = deleted.o_placeid if hasattr(deleted, "o_placeid") else deleted.o_place.Id
        Thing.ALL_THINGS[oid].remove(deleted)
        del Thing.ALL_THINGS[o_Id]
        return self.current

    def up(self, o_Id):
        """Set member as current. """
        self.current = Thing.ALL_THINGS[o_Id]
        return self.current

    def list(self, employ=None, kind='Locus', **kwargs):
        """List member. """
        [employ(**{argument: getattr(item, argument)
                   for argument in dir(item) if argument[:2] in "o_ s_"})
         for item in Thing.ALL_THINGS.values() if item.o_part == kind]

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
    """A placeholder for gui positioning scaffolding."""

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        self.items = []
        if 'o_place' not in kwargs or not kwargs['o_place']:
            kwargs['o_placeid'] = THETHING.current.o_Id
        THETHING.current.append(self)
        self.o_part, kwargs['o_Id'] = self.__class__.__name__, o_Id
        (fab or self).register(o_Id, self)
        self._add_properties(**kwargs)

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        employ(**{argument: getattr(self, argument)
                  for argument in dir(self) if argument[:2] in "o_ s_"})

    def execute(self, employ=None, **kwargs):
        """Execute a given action. """
        [item.execute(employ=employ, **kwargs) for item in self.items]


class Action(Holder):
    """A placeholder describing an action to be executed by a holder."""

    def __init__(self, fab=None, part=None, o_Id=None, o_placeid=None, **kwargs):
        Thing.ALL_THINGS[o_placeid].append(self)
        kwargs.update(o_part=self.__class__.__name__, o_Id=o_Id, o_placeid=o_placeid)
        (fab or self).register(o_Id, self)
        self._add_properties(**kwargs)

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        args = {argument: getattr(self, argument)
                for argument in dir(self) if argument[:2] in "o_ s_"}
        args.update(o_Id=self.o_placeid)
        #print("Action deploy", args)
        employ(**args)

    def execute(self, employ=None, **kwargs):
        """Execute a given action. """
        args = {argument: getattr(self, argument)
                for argument in dir(self) if argument[:2] in "o_ s_"}
        args.update(o_cmd=self.o_act, o_gcomp=self.o_acomp, o_Id=self.o_item)
        #employ(**args)
        THETHING.activate(employ, **args)


class Locus(Thing):
    """A place where things happen."""

    def __init__(self, fab=None, part=None, o_Id=None, **kwargs):
        self.items = []
        #print ("Thing init:", fab, part, o_Id)
        self.create(fab=fab, part=part, o_Id=o_Id, **kwargs)

    def _do_create(self):
        """Finish thing creation. """
        container = THETHING  # Thing.ALL_THINGS.setdefault(self.o_place, THETHING)
        self.container = container.append(self)
        #print("""Finish thing creation. """, THETHING, self.o_place, self.container, self)

    def deploy(self, employ=None, **kwargs):
        """Deploy this thing at a certain site. """
        THETHING.current = self
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
        self.kwargs = {key: value for key, value in kwargs
                       if key in 'o_drop '}
        self.dropper = Thing.ALL_THINGS[dropper]
        self.dragger = Thing.ALL_THINGS[dragger]
        self.dropper.receive = self.receive
        self.dragger.visit(self.visiting)
        kwargs['action'] = self.dropper.receive
        self._add_properties(**kwargs)
        THETHING.append(self)

    def visiting(self, visited):
        visited._add_properties(**self.kwargs)
        visited.enter = self.enter

    def receive(self, guest_id):
        return Thing.ALL_THINGS[guest_id].enter(self.dropper)

    def enter(self, host):
        self.container = host
        return self.o_Id


class Command(Thing):
    """A commom element to any kind of action."""
    SCRIPT = []

    def __init__(self, employ, fab=THETHING, o_part=None, o_Id=None, **kwargs):
        Command.SCRIPT.append(self)
        #print ("Command init:", fab, o_part, o_Id, kwargs)
        self.execute(employ, fab=fab, part=o_part, o_Id=o_Id, **kwargs)

    def create(self, employ, fab=None, part=None, o_Id=None, **kwargs):
        """Fabricate and return a given part."""
        pass


class DoAdd(Command):
    """Add an element to another."""
    def __init__(self, employ, fab=THETHING, o_part=None, o_Id=None, **kwargs):
        Command.__init__(self, employ, fab=fab, o_part=o_part, o_Id=o_Id, **kwargs)

    def execute(self, employ, fab=None, part=None, o_Id=None, **kwargs):
        """Add an element and deploy a given part."""
        element = fab.employ(part, o_Id, **kwargs)
        #print ("DoAdd execute:", fab, part, o_Id, element, employ, kwargs)
        element.deploy(employ)


class DoExecute(Command):
    """Execute the command associated with this element."""
    def execute(self, employ, fab=None, part=None, o_Id=None, **kwargs):
        """Deploy the current element to the front."""
        #print('DoExecute:', o_Id, employ)
        Thing.ALL_THINGS[o_Id].execute(employ)


class DoUp(Command):
    """Set element as current."""
    def execute(self, employ, fab=None, part=None, o_Id=None, **kwargs):
        """Deploy the current element to the front."""
        #print('DoUp:', o_Id, employ)
        element = fab.up(o_Id)
        employ(o_Id=element.o_Id, **kwargs)
        #element.deploy(employ)


class DoShape(Command):
    """Shape current element."""
    def execute(self, employ, fab=None, part=None, o_Id=None, **kwargs):
        """Reshape current element."""
        #print('DoShape:', o_Id, employ)
        #kwargs.update(o_gcomp='shape')
        kwargs.pop('o_gcomp')
        element = fab.shape(o_Id, **kwargs)
        element.o_gcomp, old_gcomp = 'shape', kwargs.pop('o_gcomp')
        element.deploy(employ)
        element.o_gcomp = old_gcomp


class DoDel(Command):
    """Delete current element."""
    def execute(self, employ, fab=None, part=None, o_Id=None, **kwargs):
        """Delete current element."""
        #print ("DoDel execute:", fab, part, o_Id, kwargs)
        fab.delete(o_Id, employ)


class DoList(Command):
    """List elements from another element."""
    def execute(self, employ, fab=None, part=None, o_Id=None, o_kind=None, **kwargs):
        """Ask fabric to list all."""
        fab.list(employ, o_kind)


def init():
    global THETHING
    THETHING = Thing(o_Id='book')
    Thing.INVENTORY.update(
        Locus=Locus, Holder=Holder, TheThing=THETHING,
        Grid=Grid, Dragger=Dragger, Action=Action)
    Thing.CONTROL.update(
        DoAdd=DoAdd, DoList=DoList, DoUp=DoUp, DoDel=DoDel, DoShape=DoShape,
        DoExecute=DoExecute)
    #print (Thing.INVENTORY, Thing.ALL_THINGS)
    return THETHING
