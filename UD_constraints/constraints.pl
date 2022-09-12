new_clause_list([_,_|NCL], NCL).
new_clause([NewClause|_], NewClause ). 

reduce_clause(BodyList, NewClause) :- new_clause_list(BodyList, NCL), new_clause(NCL, NewClause).
current_term([_,CurrentTerm|_], CurrentTerm).
insertAtEnd(X,Y,Z) :- append(Y,[X],Z).
check_for_vars([_,B,_]) :- var(B).
list_to_term([Functor|List], Term) :-
    Term =.. [Functor | List].

clause2list(Body , Lst, Output, BodyList) :- Body =.. BodyList, check_for_vars(BodyList), reverse(Lst,Output).
clause2list(Body, Lst, Output, ClauseOutput) :- Body =.. BodyList, 
                    reduce_clause(BodyList, NewClause), 
                    current_term(BodyList, CurrentTerm),
                    insertAtEnd(CurrentTerm, Lst, Lst1),
                    clause2list(NewClause, Lst1, Output, ClauseOutput).