:-consult('extract_terms.pl').

hypothesis(Head,Body) :- Head = true_class(A), Body = (contains(B,A), has_shape(B,cylinder), has_size(B,large), contains(C,A), 
has_shape(C,cube)).




% get the variable name by extracting it from contains/2

var(contains(Var_name,_),Var_name).
extract_var([A,B|_],Var_name) :- var(B,Var_name).
quick(B) :- hypothesis(H,B), B =.. L, extract_var(L,Var_name). 

tester :- 
   hypothesis(_,Body), 
   term_string(Body, BodyString), 
   (\+ sub_atom(BodyString,_,_,_,'has_claim_reason') ;
   sub_atom(BodyString,_,_,_,'has_marital_status')).


/*
Below is various attempts at converting clauses to lists, 
*/

transform([A], A):- A=..[_].
%transform([A,B], (A,B)):- B=..[_].
%transform([A,B,C|Tail], L):- L=..[',',A,T],transform([B,C|Tail], T).

%haystack_needle(H,N) :- H==N.
%haystack_needle(H,N) :- compound(H),arg(_,H,A),haystack_needle(A,N).

needle_haystack(N,H) :- N==H.
needle_haystack(N,H) :- H=..[_|As],member(A,As),needle_haystack(N,A).

makeList(Y,F) :-
append(Y,[],X),
F = X.

term_subterm_n(T, S, N) :-
   bagof(t, term_subterm(T,S), Ts),
   length(Ts, N).

term_subterm(T, T).
term_subterm(T, S) :-
   compound(T),
   T =.. [_|Es],
   member(E, Es),
   term_subterm(E, S).

/*
Below extracts sub-terms from terms. Problem - it still uses the =.. method which does not work well with 
terms without functors. So you need to explore more - how can this work with the actual body clause provided
by hypothesis/2. 
*/

exterm(T, M, E) :-
    T =.. [F|As],
    select(E, As, Bs),
    M =.. [F|Bs],
    E = contains(_,_).

/* 
User options:
1) Add a condition.
2) Delete a condition.
3) Modify a value.
4) Modify an operator.
1-2 can be done with the existing exclusion - inclusion constraint.
3-4 require access to the actual terms.
*/

% Evaluates to fales if the hypothesis body is permissable. 

hypothesis(Head,Body,L) :- Head = (true_class(_,_)), Body = (has_education(_,masters),
                        has_claim_reason(_,scratch_dent), has_occupation(_,sales)), L = 2.

add_condition :- hypothesis(_,Body,_), bodyList(Body, BodyList), !, 
    member(has_education(_,masters), BodyList), 
    member(has_claim_reason(_,scratch_dent),BodyList),
    \+ member(has_occupation(_,sales), BodyList).

delete_condition :- hypothesis(_,Body,_), bodyList(Body, BodyList), !, 
    member(has_education(_,masters), BodyList), 
    member(has_claim_reason(_,scratch_dent),BodyList),
    \+ member(has_occupation(_,sales), BodyList).

% Pruning
%prune((_:-Body)) :- violates_constraints(Body).
%violates_constraints(Body) :- bodyList(Body, BodyList), !, member(has_education(_,_), BodyList).

/* Have a look at this later on - for bodytoList predicate
clause_body_list(Clause, Body) :-
    clause(Clause, Elements),
    clause_body_list_aux(Elements, Body).

clause_body_list_aux(Elements, [BodyPart|BodyRest]) :-
    Elements =.. [_, E | T],
    (   T = []
    ->  BodyPart = E,
        BodyRest = []
    ;   [ClauseRest] = T,
        true(BodyPart) = E,
        clause_body_list_aux(ClauseRest, BodyRest)
    ).
*/