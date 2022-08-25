:-consult("aleph_input/hans_aleph.bk").

true_class(A,Ex) :-
     contains(B,A), has_shape(B,cylinder), has_size(B,large), contains(C,A), has_shape(C,cube),
    Ex = [contains(B,A), has_shape(B,cylinder), has_size(B,large), contains(C,A), has_shape(C,cube)].

