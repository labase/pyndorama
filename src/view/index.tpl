<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><!--

############################################################
Pyndorama - Educational game creation
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/31
:Status: This is a "work in progress"
:Revision: 0.1.1
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
-->
<html>
    <head>
        <meta charset="iso-8859-1">
        <title>Pyndorama</title>
        <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
        <link rel="shortcut icon" href="view/favicon.ico" type="image/x-icon" />
        <link rel="stylesheet" type="text/css" href="view/theme.css">
        <style>
        .hidden_display { display :none;}
        </style>
        <script type="text/javascript" src="http://dl.dropboxusercontent.com/u/1751704/labase/lib/brython.js"></script>
        <script type="text/python" src="control.py">
        </script>
        <script type="text/python">
            from local_storage import storage
            import json
            import svg
            import html
            import time
            class Brython:
                DOC, SVG, HTML, AJAX, WIN = doc, svg, html, ajax, win
                STORAGE, JSON, TIME = storage, json, time
            main(Brython)
        </script>
    </head>
    <body onLoad="brython(1)" class="main">
        <div id="doc_id" class="hidden_display">{{ doc_id }}</div>
        <div id="base" class="base"></div>
        <div id="propbox" draggable="true"
             style="position: absolute; background-color: white; opacity: 0.3"></div>
        <div id="propsize" draggable="true"
             style="position: absolute; background-color: black; opacity: 0.4"></div>
        <!-- -->
        <div id="book" class="book">
            <div id="text" class="text"></div>
            <div id="illumini" class="illumini"></div>
            <div id="subtext" class="subtext">
                <div id="f0" class="fleet" style= "float: left; margin: 10px;"></div>
                <div id="f1" class="fleet" style= "float: left; margin: 10px;"></div>
                <div id="f2" class="fleet" style= "float: left; margin: 10px;"></div>
                <div id="f3" class="fleet" style= "float: left; margin: 10px;"></div>
                <div id="f4" class="fleet" style= "float: left; margin: 10px;"></div>
                <div id="f5" class="fleet" style= "float: left; margin: 10px;"></div>
            </div>

        </div>
        <!-- -->
    </body>
</html>
