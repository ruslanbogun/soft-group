class A(type):
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(D, B):
    pass


class F(C):
    pass


class G(C):
    pass


class H(F, E, G):
    pass


# L[H] = [H] + merge(L[F], L[E], L[G], [F, E, G])
# L[G] = [G] + merge(L[C], [C])
# L[F] = [F] + merge(L[C], [C])
# L[E] = [E] + merge(L[D], L[B], [D, B])
# L[D] = [D] + merge(L[B], [B])
# L[C] = [C] + merge(L[A], [A]) = [C, A]
# L[B] = [B] + merge(L[A], [A]) = [B, A]

print(H.__mro__)
