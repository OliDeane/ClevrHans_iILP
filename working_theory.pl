:-consult("aleph_input/hans_aleph.bk").

true_class(A,Ex) :-
     contains(B,A), has_color(B,gray), has_size(B,large),
    Ex = [contains(B,A), has_color(B,gray), has_size(B,large)].

