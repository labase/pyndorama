#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Memit - Main
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/05/24
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from datetime import datetime
from bottle import route, view, run, get, post, static_file, template, request
import bottle
import os
from couchdb import Server
import database
DIR = os.path.dirname(__file__)+'/'
ADM, HEA, PEC, PHA, END = 'adm1n head peca fase fim'.split()

@route('/')
@view(DIR+'meme')
def main():
    try:
        doc_id, doc_rev = database.DRECORD.save({'type': 'Memit', 'date': str(datetime.now())})

        return dict(doc_id = doc_id)
    except Exception:
        return "Error in Database %s"%doc_id
        pass

@get('/<filename:re:.*\.html>')
def html(filename):
    return static_file(filename, root='src')

@get('/<filename:re:.*\.js>')
def javascript(filename):
    return static_file(filename, root='libs')

@get('/<filename:re:.*\.py>')
def python(filename):
    return static_file(filename, root='src')

@get('/<filename:re:.*\.png>')
def imagepng(filename):
    return static_file(filename, root='studio/memit')

@post('/record/head')
def record_head():
    try:
        json = request.json
        record_id = json.keys()[0]
        record = database.DRECORD[record_id]
        record[record_id][HEA]=json[record_id]
        record[record_id][PEC]=[]
        record[record_id][PHA]=[]
        return record
    except Exception:
        return "Cabeçalho não foi gravado %s"%request.json

@post('/record/piece')
def record_piece():
    try:
        json = request.json
        record_id = json.keys()[0]
        record = database.DRECORD[record_id]
        record[record_id][PEC] +=[json[record_id]]
        return record
    except Exception:
        return "Movimento de peça não foi gravado %s"%request.json


@post('/record/phase')
def record_phase():
    try:
        json = request.json
        record_id = json.keys()[0]
        record = database.DRECORD[record_id]
        record[record_id][PHA] +=[json[record_id]]
        return record
    except Exception:
        return "Movimento de peça não foi gravado %s"%request.json

@post('/record/end')
def record_end():
    try:
        json = request.json
        record_id = json.keys()[0]
        record = database.DRECORD[record_id]
        record[record_id][END] =json[record_id]
        return record
    except Exception:
        return "Fim de jogo não foi gravado %s"%request.json


if __name__ == "__main__":
    run(server='gunicorn', host='0.0.0.0', port=int(os.environ.get("PORT", 8080)), debug=True, workers=1)

app = bottle.default_app()
