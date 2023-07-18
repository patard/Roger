Encodeur/décodeur de messages enICCma                         {#mainpage}
============

Documentation that will appear on the main page

\date

\msc
a [label="Maître"],b [label="Esclave"];
---  [label="envoi de donnees"];
a->b [label="setData(...)"];
b=>b [label="register data"];
...;
---  [label="demande de donnees"];
a->b [label="data resquest(...)"];
b=>b [label="recover data"];
b->a [label="requested data"];
\endmsc


\n
---

# Liste des messages

1. \ref IDL_VERSION
