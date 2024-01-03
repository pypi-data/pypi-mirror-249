# coding=utf8
r"""
DetAutomaton generators

AUTHORS:

- Paul Mercat (2018)- I2M AMU Aix-Marseille Universite - initial version
- Dominique Benielli (2018) Labex Archimede - I2M -
  AMU Aix-Marseille Universite - Integration in -SageMath

"""

# *****************************************************************************
#       Copyright (C) 2018 Paul Mercat <paul.mercat@univ-amu.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
# *****************************************************************************
from __future__ import division, print_function, absolute_import

from badic.cautomata import DetAutomaton
from sage.misc.prandom import randint, random


class DetAutomatonGenerators(object):
    """
    This class permits to generate various usefull DetAutomata.

    EXAMPLES::

        #. DetAutomaton recognizing every words over a given alphabet
        sage: from badic.cautomata_generators import *
        sage: dag.AnyWord(['a','b'])
        DetAutomaton with 1 state and an alphabet of 2 letters

        #. DetAutomaton recognizing every letters of a given alphabet
        sage: from badic.cautomata_generators import *
        sage: dag.AnyLetter(['a','b'])
        DetAutomaton with 2 states and an alphabet of 2 letters

        #. DetAutomaton whose language is a single word
        sage: from badic.cautomata_generators import *
        sage: dag.Word(['a','b','a'])
        DetAutomaton with 4 states and an alphabet of 2 letters

        #. DetAutomaton with a given alphabet, recognizing the empty word
        sage: from badic.cautomata_generators import *
        sage: dag.EmptyWord(['a','b'])
        DetAutomaton with 1 state and an alphabet of 2 letters

        #. random DetAutomaton
        sage: from badic.cautomata_generators import *
        sage: dag.Random()      # random
        DetAutomaton with 244 states and an alphabet of 183 letters
    """

    def EmptyAutomaton(self, A, S, keep_labels=True):
        """
        Generate a DetAutomaton with a given language and given set of states.

        INPUT:

        - ``A`` - list -- alphabet of the result

        - ``S`` - list -- states of the result

        - ``keep_labels`` - bool (default: ``True``) -- if True keep the list of labels (i.e. the list S)

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.EmptyAutomaton([0,1], ['a', 'b'])
            DetAutomaton with 2 states and an alphabet of 2 letters

        """
        a = DetAutomaton(None)
        return a.new_empty_automaton(A, S, keep_labels)

    def AnyLetter(self, A, A2=None):
        """
        Generate a DetAutomaton recognizing every letter of the alphabet A.

        INPUT:

        - ``A`` -- the result recognize every letter of this alphabet

        - ``A2`` (default: ``None``) -- alphabet of the result (must contain A)

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.AnyLetter(['a', 'b'])
            DetAutomaton with 2 states and an alphabet of 2 letters

            sage: dag.AnyLetter(['a', 'b'], ['a', 0, 'b', 1])
            DetAutomaton with 2 states and an alphabet of 4 letters

        TESTS::

            sage: from badic.cautomata_generators import *
            sage: dag.AnyLetter(['a', 'b'], [0,1])
            Traceback (most recent call last):
            ...
            ValueError: A label of a transition is not in the alphabet [0, 1]
        """
        return DetAutomaton([(0, 1, i) for i in A], A=A2, i=0, final_states=[1])

    def AnyWord(self, A, A2=None):
        """
        Generate a DetAutomaton recognizing every words over the alphabet A.

        INPUT:

        - ``A`` -- the result recognize every word over this alphabet

        - ``A2`` (default: ``None``) -- alphabet of the result (must contain A)

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.AnyWord(['a', 'b'])
            DetAutomaton with 1 state and an alphabet of 2 letters

            sage: dag.AnyWord(['a', 'b'], ['a', 0, 'b', 1])
            DetAutomaton with 1 state and an alphabet of 4 letters

        TESTS::

            sage: from badic.cautomata_generators import *
            sage: dag.AnyWord(['a', 'b'], [0,1])
            Traceback (most recent call last):
            ...
            ValueError: A label of a transition is not in the alphabet [0, 1]
        """
        return DetAutomaton([(0, 0, i) for i in A], A=A2, i=0, final_states=[0])

    def Empty(self, A):
        """
        Generate a DetAutomaton recognizing the empty language over the alphabet A.

        INPUT:

        - ``A`` -- alphabet of the result

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.Empty(['a', 'b'])
            DetAutomaton with 0 state and an alphabet of 2 letters
        """
        return DetAutomaton([], A=A)

    def EmptyWord(self, A):
        """
        Generate a DetAutomaton recognizing the empty word and having the alphabet A.

        INPUT:

        - ``A`` -- alphabet of the result

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.EmptyWord(['a', 'b'])
            DetAutomaton with 1 state and an alphabet of 2 letters
        """
        return DetAutomaton([], S=[0], i=0, final_states=[0], A=A)

    def Word(self, w, A=None):
        """
        Generate a DetAutomaton recognizing the word w.

        INPUT:

        - ``w`` -- the result recognize this word

        - ``A`` (default: ``None``) -- alphabet of the result (must contain the letters of w)

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.Word("ab")
            DetAutomaton with 3 states and an alphabet of 2 letters

            sage: dag.Word("ab", ['a', 0, 'b', 1])
            DetAutomaton with 3 states and an alphabet of 4 letters

        TESTS::

            sage: from badic.cautomata_generators import *
            sage: dag.Word(['a', 'b'], [0,1])
            Traceback (most recent call last):
            ...
            ValueError: A label of a transition is not in the alphabet [0, 1]
        """
        return DetAutomaton(
            [(i, i + 1, j) for i, j in enumerate(w)], A=A, i=0, final_states=[len(w)])

    def Union(self, la, A=None, verb=False):
        """
        Generate the minimal DetAutomaton recognizing the union of languages

        INPUT:

        - ``la`` -- list of DetAutomata

        - ``A`` (default: ``None``) -- alphabet of the result (must contain the letters of w)

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.Union([dag.Word("hello"), dag.EmptyWord(list("hleo"))])
            DetAutomaton with 6 states and an alphabet of 4 letters
        """
        if A is None:
            # find the alphabet
            A = set()
            for a in la:
                A = A.union(a.alphabet)
            A = list(A)
        if verb:
            print("A=%s" % A)
        r = []
        ls = [a.initial_state for a in la]
        to_see = [(0,ls)]
        seen = dict()
        seen[tuple(ls)] = 0
        cs = 1 # current state
        for a in la:
            if a.initial_state != -1 and a.is_final(a.initial_state):
                lf = [0]
                break
        else:
            lf = []
        s1 = set([-1])
        while len(to_see) > 0:
            if verb:
                print("to_see = %s" % to_see, flush=True)
            c,ls = to_see.pop()
            for l in A:
                ls2 = [a.succc(i, l) for (a,i) in zip(la,ls)]
                if set(ls2) != s1:
                    if tuple(ls2) in seen:
                        r.append((c,l,seen[tuple(ls2)]))
                    else:
                        # add new state
                        r.append((c,l,cs))
                        to_see.append((cs,ls2))
                        for a,s in zip(la,ls2):
                            if s != -1 and a.is_final(s):
                                lf.append(cs)
                        seen[tuple(ls2)] = cs
                        cs += 1
        return DetAutomaton(r, i=0, final_states=lf, avoidDiGraph=True).minimize()

    def Words(self, lw, A=None):
        """
        Generate a DetAutomaton recognizing the set of words

        INPUT:

        - ``lw`` -- list of words

        - ``A`` (default: ``None``) -- alphabet of the result (must contain the letters of w)

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.Words(["arbre", "artichaud", "art"])
            DetAutomaton with 12 states and an alphabet of 10 letters

        TESTS::

            sage: from badic.cautomata_generators import *
            sage: dag.Words([['a', 'b']], [0,1])
            Traceback (most recent call last):
            ...
            ValueError: A label of a transition is not in the alphabet [0, 1]
        """
        if A is None:
            # find the alphabet
            A = set()
            for w in lw:
                for l in w:
                    A.add(l)
            A = list(A)
        return self.Union([self.Word(w, A=A) for w in lw], A=A)

    def Random(self, n=None, A=None, density_edges=None,
               density_finals=None, verb=False):
        """
        Generate a random DetAutomaton.

        INPUT:

        - ``n`` - int (default: ``None``) -- the number of states

        - ``A`` (default: ``None``) -- alphabet of the result

        - ``density_edges`` (default: ``None``) -- the density of the transitions among all possible transitions

        - ``density_finals`` (default: ``None``) -- the density of final states among all states

        - ``verb`` - bool (default: ``False``) -- print informations for debugging

        OUTPUT:

        A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic.cautomata_generators import *
            sage: dag.Random()      # random
            DetAutomaton with 401 states and an alphabet of 836 letters

            sage: dag.Random(3, ['a','b'])
            DetAutomaton with 3 states and an alphabet of 2 letters

        """
        if density_edges is None:
            density_edges = random()
        if density_finals is None:
            density_finals = random()
        if n is None:
            n = randint(2, 1000)
        if A is None:
            if random() < .5:
                A = list('abcdefghijklmnopqrstuvwxyz')[:randint(0, 25)]
            else:
                A = list(range(1, randint(1, 1000)))
        if verb:
            print("Random automaton with %s states, density of leaving edges %s, density of final states %s and alphabet %s" % (n, density_edges, density_finals, A))
        L = []
        for i in range(n):
            for j in range(len(A)):
                if random() < density_edges:
                    L.append((i, randint(0, n - 1), A[j]))
        if verb:
            print(L)
        F = []
        for i in range(n):
            if random() < density_finals:
                F.append(i)
        if verb:
            print("final states %s" % F)
        return DetAutomaton(L, A=A, S=range(n), i=randint(0,n-1), final_states=F)

    def MatricesGraph(self, lm):
        r"""
        Return the continued fraction algorithm defined as a matrices graph with one state and matrices lm.

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.MatricesGraph([identity_matrix(3)])
            DetAutomaton with 1 state and an alphabet of 1 letter
        """
        for m in lm:
            m.set_immutable()
        return DetAutomaton([(0, m, 0) for m in lm], i=0, avoidDiGraph=True)

    def GeneralAlgo(self, l):
        r"""
        Return the continued fraction algorithm defined as a graph with transitions 0 --m,D--> 0, with only one state 0.

        INPUT:

        - ``l`` - list - a list of couples of matrices (m,D), where m is a square invertible matrix,
                            and D is a convex projective polyhedron whose vertices are columns of D

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.GeneralAlgo([(identity_matrix(3),identity_matrix(3))])
            DetAutomaton with 1 state and an alphabet of 1 letter
        """
        for m, D in l:
            m.set_immutable()
            D.set_immutable()
        return DetAutomaton([(0, (m, D), 0) for m, D in l], i=0, avoidDiGraph=True)

    def Brun(self, d = 3):
        r"""
        Return the Brun continued fraction algorithm as a graph label by matrices m,D, where D is the domain where we do m^(-1).

        INPUT:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.Brun()
            DetAutomaton with 1 state and an alphabet of 6 letters

        """
        from sage.matrix.constructor import matrix
        from sage.matrix.special import identity_matrix
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        D = matrix([[0 for _ in range(i)] + [1 for _ in range(d - i)] for i in range(d)])
        m = identity_matrix(d)
        m[0,1] = 1
        lm = []
        ld = []
        for s in SymmetricGroup(d):
            ld.append(s.matrix().inverse() * D * s.matrix())
            lm.append(s.matrix().inverse() * m * s.matrix())
        return self.GeneralAlgo(list(zip(lm,ld)))

    def ArnouxRauzyPoincare(self):
        r"""
        Return the Arnoux-Rauzy-Poincaré continued fraction algorithm as a graph label by matrices m,D, where D is the domain where we do m^(-1).

        INPUT:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.ArnouxRauzyPoincare()
            DetAutomaton with 1 state and an alphabet of 9 letters
        """
        from sage.matrix.constructor import matrix
        from .cautomata import simplex_density
        lm = [matrix([[1, 1, 1], [0, 1, 0], [0, 0, 1]]),\
              matrix([[1, 0, 0], [1, 1, 1], [0, 0, 1]]),\
              matrix([[1, 0, 0], [0, 1, 0], [1, 1, 1]]),\
              matrix([[1, 0, 0], [1, 1, 0], [1, 1, 1]]),\
              matrix([[1, 0, 0], [1, 1, 1], [1, 0, 1]]),\
              matrix([[1, 1, 0], [0, 1, 0], [1, 1, 1]]),\
              matrix([[1, 1, 1], [0, 1, 0], [0, 1, 1]]),\
              matrix([[1, 0, 1], [1, 1, 1], [0, 0, 1]]),\
              matrix([[1, 1, 1], [0, 1, 1], [0, 0, 1]])]
        ld = [matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),\
              matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),\
              matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),\
              matrix([[1, 0, 1], [0, 1, 0], [0, 0, 1]]),\
              matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),\
              matrix([[1, 0, 0], [0, 1, 1], [0, 0, 1]]),\
              matrix([[1, 0, 0], [1, 1, 0], [0, 0, 1]]),\
              matrix([[1, 0, 0], [0, 1, 0], [0, 1, 1]]),\
              matrix([[1, 0, 0], [0, 1, 0], [1, 0, 1]])]
        ld = [m*d for (m,d) in zip(lm,ld)]
        return self.GeneralAlgo(list(zip(lm,ld)))

    def CassaigneWinLose(self):
        r"""
        Return the Cassaigne continued fraction algorithm as a win-lose graph.

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.CassaigneWinLose()
            DetAutomaton with 3 states and an alphabet of 3 letters
        """
        return DetAutomaton([(0,1,1),(0,2,2),(1,0,0),(1,2,2),(2,0,0),(2,1,1)])

    def Cassaigne(self, d=3):
        r"""
        Return the Cassaigne continued fraction algorithm as a matrices graph.

        INPUT:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.Cassaigne()
            DetAutomaton with 1 state and an alphabet of 2 letters
        """
        from sage.matrix.constructor import matrix
        from sage.rings.integer_ring import ZZ
        if d == 3:
            lm = [matrix([[1,1,0],[0,0,1],[0,1,0]]), matrix([[0,1,0],[1,0,0],[0,1,1]])]
        else:
            def z(n):
                return [0 for _ in range(n)]
            lm = [ matrix([[0,0,1]+z(d-3), [-1,1]+z(d-2)]\
                         +[z(i)+[1]+z(d-i-1) for i in range(3,d)]+[[1]+z(d-1)]),\
                   matrix([[1,-1]+z(d-2), [0,0,1]+z(d-3)]\
                         +[z(i)+[1]+z(d-i-1) for i in range(3,d)]+[[0,1]+z(d-2)]) ]
            lm = [matrix(m.inverse(), ring=ZZ) for m in lm]
        return self.MatricesGraph(lm)

    def Reverse(self):
        r"""
        Return the Reverse continued fraction algorithm as a matrices graph.

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.Reverse()
            DetAutomaton with 1 state and an alphabet of 4 letters
        """
        from sage.matrix.constructor import matrix
        lm = [matrix([[1,1,1],[0,1,0],[0,0,1]]), matrix([[1,0,0],[1,1,1],[0,0,1]]), matrix([[1,0,0],[0,1,0],[1,1,1]]), matrix([[0,1,1],[1,0,1],[1,1,0]])]
        return self.MatricesGraph(lm)

    def Poincare(self, d=3):
        r"""
        Return the Poincare continued fraction algorithm as a matrices graph.

        INPUT:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.Poincare()
            DetAutomaton with 1 state and an alphabet of 6 letters
        """
        from sage.matrix.constructor import matrix
        from sage.matrix.special import identity_matrix
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        m = identity_matrix(d)
        for i in range(d):
            for j in range(i):
                m[i,j] = 1
        lm = []
        G = SymmetricGroup(range(d))
        for g in G:
            gm = g.matrix()
            lm.append(gm*m*gm.inverse())
        return self.MatricesGraph(lm)

    def FullySubstractive(self, d=3):
        r"""
        Return the Fully substractive continued fraction algorithm as a win-lose graph.

        INPUT:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.FullySubstractive()
            DetAutomaton with 1 state and an alphabet of 3 letters
        """
        return DetAutomaton([(0,i,0) for i in range(d)], avoidDiGraph=True)

    def Selmer(self, d=3):
        r"""
        Return the Selmer continued fraction algorithm as a graph label by matrices m,D, where D is the domain where we do m^(-1).

        INPUT:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.Selmer()
            DetAutomaton with 1 state and an alphabet of 6 letters

        """
        from sage.matrix.constructor import matrix
        from sage.matrix.special import identity_matrix
        from sage.groups.perm_gps.permgroup_named import SymmetricGroup
        D = matrix([[0 for _ in range(i)] + [1 for _ in range(d-i)] for i in range(d)])
        m = identity_matrix(d)
        m[0,2] = 1
        lm = []
        ld = []
        for s in SymmetricGroup(d):
            ld.append(s.matrix().inverse()*D*s.matrix())
            lm.append(s.matrix().inverse()*m*s.matrix())
        return self.GeneralAlgo(list(zip(lm,ld)))

    def ArnouxRauzy(self, d=3):
        r"""
        Return the Arnoux-Rauzy continued fraction algorithm as a matrices graph.

        Input:

            - ``d`` - int (default: ``3``) - number of coordinates

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.ArnouxRauzy()
            DetAutomaton with 1 state and an alphabet of 3 letters
            sage: dag.ArnouxRauzy(4)
            DetAutomaton with 1 state and an alphabet of 4 letters
        """
        from sage.matrix.constructor import matrix
        from sage.matrix.special import identity_matrix
        lm = []
        for i in range(d):
            m = identity_matrix(d)
            for j in range(d):
                m[i,j] = 1
            m.set_immutable()
            lm.append(m)
        return self.MatricesGraph(lm)

    def JacobiPerron(self):
        r"""
        Return a slower version of the Jacobi-Perron continued fraction algorithm
        (i.e. (x,y,z) ---> (y - [y/x]x, z - [z/x]x, x), where [.] denote the floor), 
        as a general algo, i.e. a graph label by matrices m,D, where D is the domain where we do m^(-1).

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.JacobiPerron()
            DetAutomaton with 1 state and an alphabet of 5 letters

            # convertion to a matrices graph
            sage: dag.JacobiPerron().matrices_graph()
            DetAutomaton with 4 states and an alphabet of 11 letters

            # matrices graph with only two vertices up to conjugacy
            sage: am = dag.JacobiPerron().matrices_graph()
            sage: amm = am.sub_automaton(max(am.strongly_connected_components(), key=lambda x:len(x)))
            sage: amm
            DetAutomaton with 2 states and an alphabet of 11 letters

        """
        from sage.matrix.constructor import matrix
        L = [[matrix([[1,0,0],[1,1,0],[0,0,1]]), matrix([[1,0,1],[1,1,1],[0,0,1]])],
             [matrix([[1,0,0],[1,1,0],[1,0,1]]), matrix([[1,0,0],[1,1,0],[1,0,1]])],
             [matrix([[1,0,0],[0,1,0],[1,0,1]]), matrix([[1,1,0],[0,1,0],[1,1,1]])],
             [matrix([[0,0,1],[1,0,0],[0,1,0]]), matrix([[1,1,1],[0,1,1],[0,0,1]])],
             [matrix([[0,0,1],[1,0,0],[0,1,0]]), matrix([[1,1,1],[0,1,0],[0,1,1]])]]
             #(matrix([[0,0,1],[1,0,0],[0,1,0]]), matrix([[1,1,1,1],[0,1,1,0],[0,0,1,1]]))])
        L[3][0] = L[3][0]*L[2][0] # accelerate in order to have a simpler matrices graph
        L[4][0] = L[4][0]*L[1][0]
        return self.GeneralAlgo(L)

    def SymmetricJacobiPerron(self):
        r"""
        Return a slower version of the symmetric Jacobi-Perron continued fraction algorithm
        (i.e. subtract as many time as possible the smallest coordinate to the other ones),
        as a graph label by matrices m,D, where D is the domain where we do m^(-1).

        OUTPUT:
            A :class:`DetAutomaton`

        EXAMPLES::

            sage: from badic import *
            sage: dag.SymmetricJacobiPerron()
            DetAutomaton with 1 state and an alphabet of 15 letters

            # convertion to a matrices graph
            sage: dag.SymmetricJacobiPerron().general_algo_to_matrices().minimize()
            DetAutomaton with 4 states and an alphabet of 26 letters

            # matrices graph with only two vertices up to conjugacy
            sage: am = dag.SymmetricJacobiPerron().general_algo_to_matrices()
            sage: amm = am.sub_automaton(max(am.strongly_connected_components(), key=lambda x:len(x)))
            sage: amm.minimize()
            DetAutomaton with 2 states and an alphabet of 26 letters

        """
        from sage.matrix.constructor import matrix
        l = [(matrix([[1, 0, 0], [1, 1, 0], [1, 0, 1]]), matrix([[1, 0, 0], [2, 1, 0], [2, 0, 1]])), \
             (matrix([[1, 0, 0], [1, 1, 0], [1, 0, 1]]), matrix([[1, 1, 1], [1, 2, 1], [2, 2, 1]])), \
             (matrix([[1, 0, 0], [1, 1, 0], [1, 0, 1]]), matrix([[1, 1, 1], [1, 2, 2], [1, 2, 1]])), \
             (matrix([[1, 0, 0], [0, 1, 0], [1, 0, 1]]), matrix([[1, 1, 0], [1, 2, 0], [2, 2, 1]])), \
             (matrix([[1, 0, 0], [1, 1, 0], [0, 0, 1]]), matrix([[1, 0, 1], [2, 1, 2], [1, 0, 2]]))]
        p0 = matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        p = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        l2 = []
        for i in range(3):
            for m,D in l:
                l2.append((p*m*p.inverse(), p*D*p.inverse()))
            p *= p0
        return self.GeneralAlgo(l2)

    def L(self, x):
        r"""
        Compute an DetAutomaton whose limit set is the interval [(x:1), (1:0)]

        INPUT:
            - x -- a quadratic number
        
        OUTPUT:
            A DetAutomaton.
        """
        from sage.rings.qqbar import AlgebraicField,AA
        QQbar = AlgebraicField()
        x = QQbar(x)
        if x.minpoly().degree() > 2:
            raise ValueError("L(x) can be computed only for a quadratic number x ! Here x={}".format(x))
        if x not in AA:
            raise ValueError("x={} must be a real quadratic number".format(x))
        L = []
        v = (x/(1+x),1/(1+x))
        d = dict()
        d[v] = 0
        stop = False
        while not stop:
            #print("v={}".format(v))
            if v[0] < v[1]:
                i = 1
                v2 = (v[0],v[1]-v[0])
            else:
                i = 0
                v2 = (v[0] - v[1], v[1])
            v2 = (v2[0]/sum(v2), v2[1] / sum(v2))
            if v2 not in d:
                d[v2] = len(d)
            else:
                stop = True
            L.append((d[v],i,d[v2]))
            v = v2
        for (i,j,k) in L:
            if j == 1:
                L.append((i, 0, len(d)))
        for i in range(2):
            L.append((len(d), i, len(d)))
        return DetAutomaton(L, i=0, avoidDiGraph=True)

    def winlose_from_set_of_quadratic_numbers(self, l):
        r"""
        Give a win-lose graph whose invariant density is a rational fraction
        where the quadratic numbers of the given list appear.

        INPUT:

            - l -- a list of quadratic numbers

        OUTPUT:
            A DetAutomaton.
        """
        l = list(l)
        if len(l)%2 != 0:
            if 0 in l:
                l.remove(0)
            else:
                l.append(0)
        l.sort()
        #print(l)
        a = dag.Empty([0,1])
        for i in range(len(l)//2):
            a = a.union(self.L(l[2*i]).intersection(self.L(l[2*i+1]).complementary()))
        return a.mirror().determinize().minimize()


# Easy access to the automaton generators:
dag = DetAutomatonGenerators()
