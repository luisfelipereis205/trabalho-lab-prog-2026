/* O arquivo principal em Prolog que vai conter a base de conhecimento (fatos de amizade), as regras de inferência de conexões indiretas e o predicado findall/3 para gerar as sugestões. */


/* Descrição: Este arquivo contém a base de conhecimento que representa as amizades entre pessoas, bem como as regras para inferir conexões indiretas e gerar sugestões de amizade com base nessas conexões.*/


/* CONEXÕES DIRETAS */
/* Definimos quem é amigo de quem.*/
amigo_direto(ana, bruno).
amigo_direto(ana, carlos).
amigo_direto(bruno, daniela).
amigo_direto(carlos, eduardo).
amigo_direto(bruno, fernanda).
amigo_direto(daniela, gabriel).

/*regra que auxiliar garantindo que se A é amigo de B, então B também é amigo de A. */
amizade(X, Y) :- amigo_direto(X, Y).
amizade(X, Y) :- amigo_direto(Y, X).

/* CONEXÕES INDIRETAS */

amigo_de_amigo(X, Z) :-
    amizade(X, Y),
    amizade(Y, Z),
    X \== Z,
    \+ amizade(X, Z).


/* PREDICADO DE COLETA OBRIGATÓRIO
findall/3 para recolher todas as sugestões de amizade possíveis para um usuário,
 e list_to_set/2 para remover duplicatas que a recursão possa gerar.*/

sugestoes_conexao(Usuario, ListaSugestoes) :-
    findall(Candidato, amigo_de_amigo(Usuario, Candidato), ListaBruta),
    list_to_set(ListaBruta, ListaSugestoes).


/* GRAU DE SEPARAÇÃO*/ 
/* Descobre se existe um caminho de amizade entre X e Y (evitando ciclos)*/
caminho(X, Y, Caminho) :-
    caminho_aux(X, Y, [X], CaminhoRev),
    reverse(CaminhoRev, Caminho).

caminho_aux(X, X, Acumulador, Acumulador).
caminho_aux(X, Y, Acumulador, CaminhoFinal) :-
    amizade(X, Z),
    \+ member(Z, Acumulador),
    caminho_aux(Z, Y, [Z | Acumulador], CaminhoFinal).