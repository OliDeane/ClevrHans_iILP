:- modeh(1, true_class(+example)).

:- modeb(*, contains(-oid, +example)).
:- modeb(*, has_shape(+oid, #shape)).
:- modeb(*, has_material(+oid, #material)).
:- modeb(*, has_color(+oid, #color)).
:- modeb(*, has_size(+oid, #size)).
:- modeb(*, left_of(+oid, +oid, +example)).
:- modeb(*, right_of(+oid, +oid, +example)).

:- determination(true_class/1, contains/2).
:- determination(true_class/1, has_shape/2).
:- determination(true_class/1, has_material/2).
:- determination(true_class/1, has_color/2).
:- determination(true_class/1, has_size/2).
:- determination(true_class/1, left_of/3).
:- determination(true_class/1, right_of/3).

:- set(i,4).
:- set(verbosity,0).
:- set(minpos,3).
:- set(noise,10).
:- set(clauselength, 20).
:- consult('hans_aleph_XY.bk').