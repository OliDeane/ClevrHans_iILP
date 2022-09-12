:- consult('extract_terms.pl').

hypothesis(Head,Body) :- Head = true_class(_), 
    Body = (contains(_,_), has_education(_,masters), 
    has_claim_reason(_,scratch_dent), has_occupation(_,accountant)).


body_preds((A,B,C,D), [A,B,C,D]).

/*
Below is a working 'add condition' constraint - we just need to be mindful of the body_preds solution. That is our bottleneck here. 
Works if: we have an occupation feature which is not included in the final theory when initially trained with the dataset.\
But when we include this condition, the occupation feature is included despite giving a slightly worse performance on the train set. 
Declarative Description: if there is a claim_reason(,B,scratch_dent) and education(b, masters) then there has to be has_occupation(_,sales).

Need to consider that we change the signs around when used as actual constraint for Aleph.
*/

present_condition(BodyList) :- member(has_claim_reason(_,scratch_dent),BodyList),
    member(has_education(_,masters), BodyList),
    member(has_occupation(_,sales), BodyList). 

absent_condition(BodyList) :- \+ member(has_education(_,masters), BodyList) ; 
    \+ member(has_claim_reason(_,scratch_dent), BodyList).

add_condition :- hypothesis(_,Body), 
    bodyList(Body, BodyList), 
    \+ (present_condition(BodyList) ; absent_condition(BodyList)). 

long_constraint :- hypothesis(_,Body), 
    body_preds(Body, BodyList), 
    ((member(has_claim_reason(_,scratch_dent),BodyList), member(has_education(_,masters), BodyList), member(has_occupation(_,sales), BodyList)) ;
    (\+ member(has_education(_,masters), BodyList), \+ member(has_claim_reason(_,scratch_dent), BodyList))). 

/*
Delete condition. This will constrain the program to only produce theories that do not contain the occupation feature (when the has_education
and has_claim_reason are in the theory). Test this again to make sure that it is actually working correctly.
Declarative description: if a rulke contains has_education and has_claim_reason(_,scratch_dent) then it cannot contain occupation(_,sales). Otherwise, it's permissable.
*/

del_hypothesis(Head,Body) :- Head = true_class(_), 
    Body = (contains(_,_), has_education(_,masters), has_claim_reason(_,scratch_dent)).

del_body_preds((A,B,C), [A,B,C]).

delete_condition :- del_hypothesis(_,Body), 

    del_body_preds(Body, BodyList), 

    ((member(has_education(_,masters), BodyList), member(has_claim_reason(_,scratch_dent), BodyList), \+ member(has_occupation(_,sales), BodyList)) ;

    (\+ member(has_education(_,masters), BodyList), \+ member(has_claim_reason(_,scratch_dent), BodyList), \+ member(has_occupation(_,sales), BodyList)) ; 

    (member(has_education(_,masters), BodyList) ; member(has_claim_reason(_,scratch_dent), BodyList), member(has_occupation(_,sales), BodyList))).
    



%del_hypothesis(_,Body), del_body_preds(Body, BodyList), \
%(member(has_education(_,masters),BodyList) ;  member(has_claim_reason(_,scratch_dent), BodyList), member(has_occupation(_,sales), BodyList))