% Cyrrent theory:
% true_class(A) :- contains(B,A), has_education(B,masters), has_coverage(B,premium), has_marital_status(B,married).


hypothesis(Head,Body) :- Head = true_class(_), Body = (contains(_,_), has_coverage(_,_), has_marital_status(_,_), has_claim_reason(_,_), useless_feature(_,_)).


new_clause_list([_,_|NCL], NCL).
new_clause([NewClause|_], NewClause ). 

reduce_clause(BodyList, NewClause) :- new_clause_list(BodyList, NCL), new_clause(NCL, NewClause).
current_term([_,CurrentTerm|_], CurrentTerm).
insertAtEnd(X,Y,Z) :- append(Y,[X],Z).
check_for_vars([_,B|_]) :- var(B).
list_to_term([Functor|List], Term) :-
    Term =.. [Functor | List].

debug_test(Body, Lst, Output, BodyList) :- Body =.. BodyList.
var_test([_,B|_]) :- var(B).
clause2list(Body , Lst, Output, BodyList) :- Body =.. BodyList, check_for_vars(BodyList), reverse(Lst,Output).
clause2list(Body, Lst, Output, ClauseOutput) :- Body =.. BodyList, 
                    reduce_clause(BodyList, NewClause), 
                    current_term(BodyList, CurrentTerm),
                    insertAtEnd(CurrentTerm, Lst, Lst1),
                    clause2list(NewClause, Lst1, Output, ClauseOutput).

bodyList(Body, FinalList) :- clause2list(Body,[],Output, Clause), list_to_term(Clause, Term), insertAtEnd(Term,Output,FinalList).
constraint(List) :- hypothesis(_,Body), bodyList(Body, List), !, member(contains(_,_), List).

hypothesis(Head,Body,_) :- Head = true_class(A), Body = (contains(B,A), has_shape(B,cylinder), 
                            has_size(B,large), contains(C,A), has_shape(C,cube), left_of(B,C,A)).

% hypothesis(Head,Body,_) :- Head = true_class(A), Body = (contains(_,_,_)).






% false :- hypothesis(_,Body,_), bodyList(Body, List), !, \+ member(has_claim_reason(_,_), List).

/*

clause2list(Body , Lst, Output, BodyList) :- Body =.. BodyList, length(Lst, Len), Len > 2, reverse(Lst,Output).

clause2list(Body, Lst, Output, ClauseOutput) :- Body =.. BodyList, 
                    reduce_clause(BodyList, NewClause), 
                    current_term(BodyList, CurrentTerm),
                    insertAtEnd(CurrentTerm, Lst, Lst1),
                    clause2list(NewClause, Lst1, Output, ClauseOutput).

tester(NewClause, CurrentTerm) :- hypothesis(Head,Body), 
                    Body =.. BodyList, 
                    get_new_clause_list(BodyList, NCL), get_new_clause(NCL, NewClause), 
                    get_current_term(BodyList, CurrentTerm).

*/

% hypothesis(H,B), B =.. C, D = [X,Y|Rest], Rest =..

