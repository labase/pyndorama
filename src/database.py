#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Main - Pyany branch
############################################################

:Author: *Carlo E. T. Oliveira*
:Author: *Erica Nogueira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/15
:Status: This is a "work in progress"
:Revision: 0.1.1
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from tinydb import TinyDB, where
#from tinydb.storages import MemoryStorage
from uuid import uuid1
from os.path import expanduser
HOME = expanduser("~")
#DBM = lambda :TinyDB(storage=MemoryStorage)
USER = 'ceto'
DBF = lambda: TinyDB('%s/dev/dbs/pdata.json' % HOME)
GBF = lambda: TinyDB('%s/dev/dbs/pgame.json' % HOME)


class Banco:
    def __init__(self, base=DBF):
        self.banco = base()

    def __setitem__(self, key, value):
        if self.banco.contains(where('key') == key):
            self.banco.update(dict(value=value), where('key') == key)
        else:
            self.banco.insert(dict(key=key, value=value))

    def __getitem__(self, key):
        #print ('Banco__getitem__', key, self.banco.contains(where('key') == key))
        record = self.banco.get(where('key') == key)
        if not isinstance(record, dict):
            raise IndexError("No such key as: %s" % key)
        return record['value']

    def save(self, value, key=None, **kwargs):
        key = key or str(uuid1())
        items = dict(key=key, value=value).update(**kwargs)
        self.banco.insert(items)
        return key


def tests():
    from tinydb.storages import MemoryStorage
    b = Banco(lambda: TinyDB(storage=MemoryStorage))
    b[1] = 2
    assert b[1] == 2, "falhou em recuperar b[1]: %s" % str(b[1])
    b[1] = 3
    assert b[1] == 3, "falhou em recuperar b[1]: %s" % str(b[1])
    c = b.save(4)
    assert b[c] == 4, "falhou em recuperar b[1]: %s" % str(b[c])
    b['j_e_p_p_e_t__'] = []
    assert b['j_e_p_p_e_t__o'] == [], "falhou em recuperar b[1]: %s" % str(b[c])

if __name__ == "__main__":
    tests()
else:
    DRECORD = Banco()
    GRECORD = Banco(GBF)
