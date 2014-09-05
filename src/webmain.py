#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Main
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/10
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from datetime import datetime
from bottle import default_app, route, view, get, post, static_file, request, redirect
import bottle
import os
import database
import json
DIR = os.path.dirname(__file__)+'/'
IMG = DIR + "../img/"

#LIBS = DIR + '../libs/lib'
IMGS = DIR + 'view/'

DIR = os.path.dirname(__file__)+'/view/'
LAST = None
PEC = "jogada"
HEAD = "marco casa move tempo ponto valor".split()
FAKE = [{k: 10*i+j for j, k in enumerate(HEAD)} for i in range(4)]


def retrieve_data(req):
    jdata = req.json['value']
    print(jdata)
    return json.loads(jdata)


def retrieve_params(req):
    print('retrieve_params', req)
    doc_id = req.pop('doc_id')
    data = {k: req[k] for k in req}
    print(doc_id, data)
    return {doc_id: data}


@route('/')
@view(DIR+'index.tpl')
def main():
    try:
        #doc_id, doc_rev = database.DRECORD.save({'type': 'Pyndorama', 'date': str(datetime.now())})
        doc_id = "umidqualquer"
        return dict(doc_id=doc_id)
    except Exception:
        return "Error in Database %s" % str([r for r in database.DRECORD])
        pass


@route('/:game#.jpt#')
@view(DIR+'index.tpl')
def game(game):
    try:
        doc_id = database.DRECORD.save({'game': game, 'date': str(datetime.now())})
        return dict(doc_id=doc_id)
    except Exception:
        return "Error in Database %s" % str([r for r in database.DRECORD])
        pass

'''
@get('/<filename:re:.*\.html>')
def html(filename):
    return static_file(filename, root=DIR)

#
#@get('/<filename:re:.*\.js>')
#def javascript(filename):
#    print(filename, '../libs/lib')
#    return static_file(filename, root=LIBS)


@get('/<filename:re:.*\.py>')
def python(filename):
    return static_file(filename, root=DIR)



@get('/<filename:re:.*\.css>')
def stylecss(filename):
    print(filename, IMGS)
    return static_file(filename, root=DIR)
'''


@get('/record/getid')
def get_user_id_():
    global LAST
    gid = database.DRECORD.save({PEC: []})
    print('/record/getid', gid)
    LAST = gid
    return gid


@get('/pontos')
@view('resultado')
def score():
    try:
        record_id = LAST
        if record_id is None:
            raise Exception()
        print('resultado', record_id)
        record = database.DRECORD[record_id]
        record = record[PEC]
        print('record resultado:', record)
        return dict(user=record_id, result=record)
    except Exception:
        #return dict(user="FAKE", result=FAKE)
        fake = dict(user="FAKE", result=FAKE)
        #print('score', fake)
        return fake


@get('/irest/studio/:storename/:partype/<filename:re:.*\.(jpg|png|gif|ico)>')
def imagepng(storename, partype, filename):
    path = img = ""
    try:
        size = "n" if request.params['size'] == "N" else ""
        path = IMG + storename + "/%s%s" % (partype, size)
        if filename in os.listdir(path):
            #raise Exception(path)
            img = static_file(filename, root=path)
        else:
            raise IOError("Not found: %s in %s" % (filename, path))
        return img
    except Exception as ex:
        return dict(
            status=500, value=
            "img não foi recuperada %s" % str(request.params.values())
            + " dir: %s" % path + " name: %s/%s" % (storename, filename) + " exception : %s" % ex)


@post('/record/store')
def save():
    try:
        json = retrieve_params(request.params)
        record_id = json.keys()[0]
        record = database.DRECORD[record_id]
        score = json[record_id]
        print('record/store:', score, record)
        score["tempo"] = str(datetime.now())
        record[PEC] += [score]
        print('record score:', score, record)
        database.DRECORD[record_id] = record
        return record
    except Exception:
        return "Movimento de peça não foi gravado %s" % str(request.params)


@get('/rest/studio/<storename:re:[^/]+>')
def image_list(storename):
    path = ''
    try:
        sub_path = storename + "/%s" % request.params['type']
        path = IMG + sub_path
        files = ["%s/%s" % (sub_path, name) for name in os.listdir(path)]
        return dict(status=0, value=files)
    except Exception as ex:
        return dict(
            status=500, value=
            "dir não foi recuperado %s" % str(request.params.values())
            + " dir: %s" % path + " name: %s --" % storename + " exception : %s" % ex)


@post('/storage/jeppeto/jpersist__/<storename:re:.*>')
def jsonstore(storename):
    try:
        record = request.json
        database.GRECORD[storename] = record['value']
        return dict(status=0, value=record)
    except Exception as ex:
        return dict(
            status=500, value=
            "Game não foi salvo %s" % str(request.json)
            + " name: %s" % storename + " exception : %s" % ex + str(database.GRECORD))


@post('/storage/jeppeto/persist__/<storename:re:.*>')
def store(storename):
    try:
        record = json.loads(request.params["value"])
        database.GRECORD[storename] = record
        return dict(status=0, value=record)
    except Exception as ex:
        return dict(
            status=500, value=
            "Game não foi salvo %s" % str(request.json)
            + " name: %s" % storename + " exception : %s" % ex + str(database.GRECORD))


@get('/storage/jeppeto/persist__/<storename:re:.*>')
def load(storename):
    try:
        #record = database.GRECORD[storename]
        record = database.GRECORD[storename]
        return dict(status=0, value=record)
    except IndexError as ex:
        return dict(
            status=500, value=
            "Game não foi recuperado %s" % str(request.params.values())
            + " name: %s" % storename + " exception : %s" % ex + str(database.GRECORD))

#database.GRECORD["j_e_p_p_e_t__o"] = []

application = default_app()

if __name__ == "__main__":
    #run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True, workers=1)
    run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True, workers=1)
