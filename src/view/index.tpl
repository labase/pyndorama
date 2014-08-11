<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><!--

############################################################
Pyndorama - Educational game creation - Pyany branch
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
        <meta charset="UTF-8">
        <title>Pyndorama</title>
        <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
        <link rel="shortcut icon" href="view/favicon.ico" type="image/x-icon" />
        <link rel="stylesheet" type="text/css" href="view/theme.css">
        <style>
        .hidden_display { display :none;}
        </style>
        <script type="text/javascript" src="https://dl.dropboxusercontent.com/u/1751704/labase/lib/brython.js"></script>
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
                def conf(self, question):
                    return confirm(question)
                def aler(self, question):
                    return alert(question)
                def prom(self, question):
                    return prompt(question)
            print(doc.cookie)
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

            <div id="text" class="text">
                <img src="http://dl.dropboxusercontent.com/u/1751704/labase/pyndorama/jeppetoc.png" width="500px"/>
            </div>
            <div id="illumini" class="illumini">
                <em>Come andò che maestro Ciliegia, falegname, trovò un
pezzo di legno, che piangeva e rideva come un bambino.</em><br/><br/><br/>
C’era una volta...<br/><br/>
– Un re! – diranno subito i miei piccoli lettori.
No, ragazzi, avete sbagliato. C’era una volta un pezzo
di legno.<br/><br/>
Non era un legno di lusso, ma un semplice pezzo da
catasta, di quelli che d’inverno si mettono nelle stufe e
nei caminetti per accendere il fuoco e per riscaldare le
stanze.<br/><br/>
Non so come andasse, ma il fatto gli è che un bel
giorno questo pezzo di legno capitò nella bottega di un
vecchio falegname, il quale aveva nome mastr’Antonio,
se non che tutti lo chiamavano maestro Ciliegia, per via
della punta del suo naso, che era sempre lustra e
paonazza, come una ciliegia matura.<br/><br/>
Appena maestro Ciliegia ebbe visto quel pezzo di
legno, si rallegrò tutto e dandosi una fregatina di mani
per la contentezza, borbottò a mezza voce:<br/><br/>
– Questo legno è capitato a tempo: voglio servirmene
per fare una gamba di tavolino.</div>

        </div>
        <!-- -->
    </body>
</html>
