:-consult('aleph_input/hans_aleph.bk').

true_class(A,Ex) :-
     contains(B,A), has_shape(B,cylinder), contains(C,A), has_shape(C,cube), contains(B,A), has_shape(B,cylinder), contains(C,A), has_shape(C,cube), has_color(C,gray),
    Ex = [contains(B,A), has_shape(B,cylinder), contains(C,A), has_shape(C,cube), contains(B,A), has_shape(B,cylinder), contains(C,A), has_shape(C,cube), has_color(C,gray)].

