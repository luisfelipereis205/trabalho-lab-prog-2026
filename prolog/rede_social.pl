/* O arquivo principal em Prolog que vai conter a base de conhecimento (fatos de amizade), as regras de inferência de conexões indiretas e o predicado findall/3 para gerar as sugestões. */


/* Descrição: Este arquivo contém a base de conhecimento que representa as amizades entre pessoas, bem como as regras para inferir conexões indiretas e gerar sugestões de amizade com base nessas conexões.*/


/* Conexões diretas */
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
