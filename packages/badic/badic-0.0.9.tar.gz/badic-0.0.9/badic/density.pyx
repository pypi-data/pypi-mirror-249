# coding=utf8
"""
Density


AUTHORS:

- Paul Mercat (2013)- I2M AMU Aix-Marseille Universite - initial version

REFERENCES:

"""

# *****************************************************************************
#	   Copyright (C) 2014 Paul Mercat <paul.mercat@univ-amu.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#	This code is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#	General Public License for more details.
#
#  The full text of the GPL is available at:
#
#				  http://www.gnu.org/licenses/
# *****************************************************************************
from __future__ import division, print_function, absolute_import

from sage.matrix.special import identity_matrix
from sage.modules.free_module_element import vector
from sage.matrix.constructor import matrix
#from sage.modules.free_module_element import zero_vector

from .cautomata cimport DetAutomaton

def simplex_density (m, x=None, ring=None, det=None):
	r"""
	Return the density function associated to the simplex m.

	INPUT:

		- ``m`` - matrix defining a simplex

		- ``x`` - list (default: ``None``) -- list of variables used 

		- ``ring`` - ring (default: ``None``) - ring used to express the result

		- ``det`` - number (default: ``None``) - absolute value of the determinant of m (in order to avoid its re-calculation if m is complicated)

	OUTPUT:
		A symbolic expressions.

	EXAMPLES::
		sage: from badic.cautomata import simplex_density
		sage: m = matrix([[0,1,1],[1,0,1],[1,1,0]])
		sage: simplex_density(m)
		2/((x0 + x1)*(x0 + x2)*(x1 + x2))

	"""
	from sage.modules.free_module_element import vector
	n = m.ncols()
	if x is None:
		from sage.calculus.var import var
		x = []
		for i in range(n):
			x.append(var("x" + str(i)))
	x = vector(x)
	if m.is_zero():
		d = zero_density(n, x)
	else:
		from sage.misc.misc_c import prod
		if det is None:
			det = abs(m.det())
		if ring is not None:
			d = ring(det)/(prod([vector([ring(t) for t in c])*x for c in m.columns()])) # factorial(n)
		else:
			d = det/(prod([c*x for c in m.columns()])) # factorial(n)
	return d
	#from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
	#from sage.rings.fraction_field import FractionField
	#K = FractionField(PolynomialRing(ring, list(x)))
	#return K(d)

def simplify_polyhedron(m):
	"""
	Renormalize the columns of the matrix in order to have as much as integer coefficients as possible.

	INPUT:

		- ``m`` - matrix

	OUTPUT:
		A matrix.

	EXAMPLES::

		sage: from badic.density import simplify_polyhedron
		sage: m = matrix([[1/2,1/3],[1/2, 2/3]])
		sage: simplify_polyhedron(m)
		[1 1]
		[1 2]

	"""
	from sage.rings.rational_field import QQ
	from sage.arith.functions import lcm
	from sage.matrix.special import diagonal_matrix
	lg = []
	for C in m.columns():
		g = 1
		for c in C:
			if c in QQ:
				g = lcm(g,QQ(c).denominator())
		lg.append(g)
	m = m*diagonal_matrix(lg)
	m.set_immutable()
	return m

def split_polyhedron(P):
	r"""
	Decompose a polyhedron into a quasi-disjoint union of simplicies.
	Return square matrices whose columns are the vertices of the simplicies.
	"""
	from sage.structure.element import is_Matrix
	from sage.geometry.polyhedron.all import Polyhedron
	if is_Matrix(P):
		if P.is_zero():
			return [P]
		P = Polyhedron([c/sum(c) for c in P.columns()])
	#print("P = %s" % P)
	d = P.dimension()
	if len(P.vertices()) <= d+1:
		return [simplify_polyhedron(matrix(P.vertices()).transpose())]
	# find a vertex to remove
	g = P.graph()
	for v in g:
		E = g.neighbors(v)
		if len(E) == d:
			#print("E = %s, v = %s" % (E,v))
			V = list(P.vertices())
			V.remove(v)
			#print(V)
			Q = simplify_polyhedron(matrix(E+[v]).transpose())
			l = split_polyhedron(Polyhedron(V))
			l.append(Q)
			return l
	raise RuntimeError("Sorry, I was unable to split this polyhedron into simplicies.")

def polyhedra_intersection(m1,m2):
	"""
	Determine the intersection of the polyhedra given by matrices.
	"""
	from sage.geometry.polyhedron.all import Polyhedron
	p1 = Polyhedron(rays=m1.columns())
	p2 = Polyhedron(rays=m2.columns())
	return matrix((p1.intersection(p2)).rays()).transpose()

def is_positive(v):
	r"""
	Test if a vector is non-negative.
	"""
	for t in v:
		if t < 0:
			return False
	return True

def is_in (v, m):
	r"""
	Test if the vector v is in the polyhedron m, given by a matrix (columns are vertices).
	"""
	lm = split_polyhedron(m)
	for m in lm:
		if is_positive(m.inverse()*vector(v)):
			return True
	return False

def polyhedron_density (P, x=None, ring=None):
	r"""
	Compute the density function of the polyhedron.

	INPUT:

		- ``m`` - matrix defining a polyhedron (columns are vertices)

		- ``x`` - list (default: ``None``) -- list of variables used 

		- ``ring`` - ring (default: ``None``) - ring used to express the result

	OUTPUT:
		A symbolic expressions.

	EXAMPLES::
		sage: from badic import *
		sage: m = matrix([[0,1,1],[1,0,1],[1,1,0]])
		sage: polyhedron_density(m)
		2/((x0 + x1)*(x0 + x2)*(x1 + x2))

	"""
	lm = split_polyhedron(P)
	s = 0
	for m in lm:
		s += simplex_density(m, x=x, ring=ring)
	return s

def zero_density (n=None, x=None, ring=None):
	r"""
	Return the zero density function.

	INPUT:

		- ``n`` - int (default: ``None``) - number of variables (used if x is None)

		- ``x`` - list (default: ``None``) -- list of variables used 

		- ``ring`` - ring (default: ``None``) - ring used to express the result

	OUTPUT:
		A symbolic expressions.

	EXAMPLES::
		sage: from badic.density import zero_density
		sage: zero_density(2)
		0
		sage: z = zero_density(2, ring=QQ); z
		0
		sage: z.parent()
		Fraction Field of Multivariate Polynomial Ring in x0, x1 over Rational Field
	"""
	if x is None:
		from sage.calculus.var import var
		x = []
		if n is None:
			raise ValueError("You must precise the variables x, or the number of variables n")
		for i in range(n):
			x.append(var("x" + str(i)))
	x = vector(x)
	from sage.misc.misc_c import prod
	if ring is None:
		return 0*prod(x)
	from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
	from sage.rings.fraction_field import FractionField
	K = FractionField(PolynomialRing(ring, list(x)))
	return K(0)

class Domain:
	"""
	Describe a domain as a union of m R_+^d for m in a rational language.
	"""
	def __init__ (self, a):
		self.a = a
		self.type = "domain"
	
	def __repr__ (self):
		return "Union of m R_+^d for m recognized by a %s" % self.a
	
	def _latex_(self):
		txt = r"\biguplus_{m \in L} m \mathbb{R}_+^%s, \text{ where $L$ is recognized by a %s}" % (self.a.alphabet[0].nrows(), self.a)
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def simplify(self):
		"""
		Does nothing: return itself.
		"""
		return self

def Decompose(d0, D0):
	"""
	Decompose the language d0 as a union of m*D0 for m in a regular language.
	"""
	# decompose d0 as A*D0
	# find state whose language is D0
	i0 = d0.initial_state
	for i in range(d0.n_states):
		d0.set_initial_state(i)
		if d0.has_same_language_as(D0):
			break
	else:
		raise ValueError("Could not find state with language D0")
	d0.set_initial_state(i0)
	print(i)
	r = d0.copy()
	# set this state as the unique final state
	r.set_final_states([i])
	# remove outgoing edges from this state
	for j in range(d0.n_letters):
		r.set_succ(i,j,-1)
	# minimize and return the result
	return Domain(r.prune().minimize())

def decompose (d0, la, minimize=True, verb=False):
	"""
	Decompose the language d0 as the prefix closure of a disjoint union of W_a a for a in la.
	Raise an error if it is not possible.

	- d0 - DetAutomaton -- the language to decompose

	- la - list of DetAutomaton -- list of languages

	- minimize - bool (default: ``True``) - if False, automata are assumed minimized and pruned.

	- verb - bool (default: ``False``) - if True, print informations

	"""
	d00 = d0
	if minimize:
		# make sure that every automaton of la is pruned and minimal
		la = [a.prune().minimize() for a in la]
		# idem for d0
		d0 = d0.prune().minimize()
	else:
		d0 = d0.copy()
	# find state whose language is D0
	i0 = d0.initial_state
	d = [[] for _ in la]
	empty = True
	for i in range(d0.n_states):
		d0.set_initial_state(i)
		dm = d0.prune().minimize()
		for k,a in enumerate(la):
			if dm.has_same_language_as(a):
				d[k] = [i]
				empty = False
	if verb:
		print("d = %s" % d)
	if empty:
		raise ValueError("The language cannot be decomposed with the given list of languages.")
	for s in d:
		for i in s:
			# disconnect every outgoing edges from i
			for j in range(d0.n_letters):
				d0.set_succ(i,j,-1)
	d0.set_initial_state(i0)
	#return d0
	lW = []
	for s in d:
		d0.set_final_states(s)
		lW.append(d0.prune().minimize())
	# check
	r = DetAutomaton([], A=d0.alphabet)
	for W,a in zip(lW, la):
		r = r.union(W.concat(a))
	if not r.prefix_closure().has_same_language_as(d00):
		if verb > 0:
			print("Verification failed.")
		raise ValueError("The language cannot be decomposed with the given list of languages.")
	elif verb > 0:
		print("Verification ok.")
	#
	return lW

class InfUnion:
	"""
	Describe a domain as an infinite union over integers: union of m^n E, where E is another expression.
	
	EXAMPLES::
		sage: from badic import *
		sage: a = DetAutomaton([(0,0,0),(0,1,1),(1,1,2),(2,0,2),(2,1,2)],i=0,avoidDiGraph=True)
		sage: a = a.mirror().determinize()
		sage: a.domains_polyhedra()
		[[1 0]
		 [2 1] positive cone on 2 coordinates,
		 [1 1]
		 [0 1] Union of [1 1]
		 [0 1]^j [1 0]
		 [2 1] positive cone on 2 coordinates for j in N,
		 [1 1]
		 [1 2] positive cone on 2 coordinates,
		 [1 1]
		 [0 1] Union of [1 1]
		 [0 1]^j [1 1]
		 [1 2] positive cone on 2 coordinates for j in N]
	"""
	def __init__ (self, m, e, varname):
		from sage.calculus.var import var
		#print("inf union %s (*) %s" % (m,varname))
		self.m = m
		self.e = e
		self.varname = var(varname)
		self.type = "infunion"
	
	def __repr__ (self):
		if self.e.need_par():
			return "Union of %s^%s ( %s ) for %s in N" % (self.m, self.varname, self.e, self.varname)
		else:
			return "Union of %s^%s %s for %s in N" % (self.m, self.varname, self.e, self.varname)
	
	def _latex_(self):
		from sage.misc.latex import latex
		if self.e.need_par():
			txt = r"\biguplus_{%s \in \mathbb{N}} %s^%s \left( %s \right)" % (self.varname, latex(self.m), self.varname, latex(self.e))
		else:
			txt = r"\biguplus_{%s \in \mathbb{N}} %s^%s %s" % (self.varname, latex(self.m), self.varname, latex(self.e))
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def need_par(self):
		"""
		Determine if this expression needs parentheses when writen inside something.
		"""
		return False

	def is_finite(self):
		return False
	
	def simplify(self):
		return InfUnion(self.m, self.e.simplify(), self.varname)

class Union:
	"""
	Describe a domain as a finite union of other expressions.
	"""
	def __init__ (self, l):
		"""
		l is an array of couples (m, e) where m is a matrix and e is an expression
		"""
		#print("union %s" % [m for m,_ in l])
		self.l = l
		self.type = "union"
	
	def __repr__ (self):
		txt = ""
		for i,(m,e) in enumerate(self.l):
			if i > 0:
				txt += " union "
			if e.need_par():
				txt += "%s ( %s )" % (m, e)
			else:
				txt += "%s %s" % (m, e)
		return txt
	
	def _latex_(self):
		from sage.misc.latex import latex
		txt = ""
		for i,(m,e) in enumerate(self.l):
			if i > 0:
				txt += r" \cup "
			if e.need_par():
				txt += r"%s \left( %s \right)" % (latex(m), latex(e))
			else:
				txt += "%s %s" % (latex(m), latex(e))
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def need_par(self):
		"""
		Determine if this union needs parentheses when writen inside something.
		"""
		return len(self.l) > 1

	def is_finite(self):
		for _,e in self.l:
			if not e.is_finite():
				return False
		return True

	def simplify(self):
		l = []
		for (m,e) in self.l:
			e = e.simplify()
			if e.type == "union":
				for (m2,e2) in e.l:
					l.append((m*m2, e2))
			elif len(self.l) == 1 and e.type == "poscone" and m.is_permutation_of(identity_matrix(m.ncols())):
				return PosCone(m.ncols())
			else:
				l.append((m, e))
		return Union(l)

class PosCone:
	"""
	Positive cone.
	
	EXAMPLES::
		sage: from badic.density import PosCone
		sage: PosCone(3)
		positive cone on 3 coordinates
		sage: latex(PosCone(2))
		\mathbb{R}_+^2
		
	"""
	def __init__ (self, d):
		#print("pos cone %s" % d)
		self.d = d
		self.type = "poscone"
	
	def __repr__ (self):
		return "positive cone on %s coordinates" % self.d
	
	def _latex_(self):
		txt = r"\mathbb{R}_+^%s" % (self.d)
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def need_par(self):
		"""
		Determine if this expression needs parentheses when writen inside something.
		"""
		return False

	def is_finite(self):
		"""
		Return always True.
		"""
		return True

	def simplify(self):
		"""
		Does nothing: return itself.
		"""
		return self

class ZeroVect:
	"""
	Singleton zero vector.
	
	EXAMPLES::
		sage: from badic.density import ZeroVect
		sage: z = ZeroVect(3)
		sage: z
		{0}
		sage: latex(z)
		\{0_{\mathbb{R}^3}\}
		
	"""
	def __init__ (self, d):
		#print("pos cone %s" % d)
		self.d = d
		self.type = "zero"
	
	def __repr__ (self):
		return "{0}"
	
	def _latex_(self):
		txt = r"\{0_{\mathbb{R}^%d}\}" % (self.d)
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def need_par(self):
		"""
		Determine if this expression needs parentheses when writen inside something.
		"""
		return False

	def is_finite(self):
		"""
		Return always True.
		"""
		return True

	def simplify(self):
		"""
		Does nothing: return itself.
		"""
		return self

class Formulae:
	"""
	Describe a domain as an expression with union over integers and finite unions.
	"""
	def __init__ (self, e):
		self.e = e
		self.type = "formulae"
	
	def __repr__ (self):
		return str(self.e)
	
	def _latex_(self):
		from sage.misc.latex import latex
		return latex(self.e)

	def is_finite(self):
		return self.e.is_finite()

	def matrices(self):
		return self.e.matrices()

	def simplify(self):
		return Formulae(self.e.simplify())

class Density:
	"""
	Describe a general density as a sum over a rational language.
	"""
	def __init__ (self, a):
		self.a = a
		self.type = "density"
	
	def __repr__ (self):
		return "Sum of |det(m)|/prod(m x) for m recognized by a %s" % self.a
	
	def _latex_(self):
		txt = r"\sum_{m \in L} \frac{\left|\det(m)\right|}{\Pi m x}, \text{ where $L$ is recognized by a %s}" % (self.a)
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

class ExplicitDensity:
	"""
	Describe a density by an explicit formulae.
	"""
	def __init__ (self, e):
		self.e = e
		self.type = "explicit density"
	
	def __repr__ (self):
		return self.e

	def _latex_(self):
		from sage.misc.latex import latex
		from sage.misc.latex import LatexExpr
		return LatexExpr(latex(self.e))

	def need_par(self):
		return False

class InfSum:
	"""
	Describe a density as an infinite sum over integers of other expressions.
	"""
	def __init__ (self, e, lvar):
		self.e = e
		self.lvar = lvar
		self.type = "infsum"
	
	def __repr__ (self):
		return "Sum of %s for %s in N" % (self.e, ', '.join([str(v) for v in self.lvar]))

	def _latex_(self):
		from sage.misc.latex import latex
		txt = r"\sum_{%s \in \mathbb{N}} %s" % (', '.join([str(v) for v in self.lvar]), latex(self.e))
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def need_par(self):
		return True

class Sum:
	"""
	Describe a density as a finite sum of other expressions.
	"""
	def __init__ (self, l):
		"""
		l is an array of expressions
		"""
		self.l = l
		self.type = "sum"
	
	def __repr__ (self):
		txt = ""
		for i,e in enumerate(self.l):
			if i > 0:
				txt += " + "
			if e.need_par():
				txt += "( %s )" % e
			else:
				txt += "%s" % e
		return txt

	def _latex_(self):
		from sage.misc.latex import latex
		txt = ""
		for i,e in enumerate(self.l):
			if i > 0:
				txt += " + "
			if e.need_par():
				txt += r"\left( %s \right)" % latex(e)
			else:
				txt += "%s" % latex(e)
		from sage.misc.latex import LatexExpr
		return LatexExpr(txt)

	def need_par(self):
		"""
		Determine if this union needs parentheses when writen inside something.
		"""
		return len(self.l) > 1

def is_loop_or_less (a, c):
	for i in c:
		if len([None for j in a.succs(i) if a.succ(i,j) in c]) > 1:
			return False
	return True

def loop (r, c, i):
	"""
	find successive labels from i in loop c
	"""
	#print("loop %s" % c)
	i0 = i
	res = [] # edges of the loop
	out = [] # edges leaving the cc
	while True:
		#print(i)
		out.append([])
		for j in r.succs(i):
			k = r.succ(i,j)
			if k in c:
				break
		else:
			return [],[]
		out[-1] += [(j2, r.succ(i,j2)) for j2 in r.succs(i) if j != j2]
		res.append(j)
		i = k
		if i == i0:
			return res, out

def decompose_domain(r, verb=False):
	"""
	Decompose a domain as unions over integers.
	"""
	cc = r.a.strongly_connected_components()
	A = r.a.alphabet
	varnames = ['a','b','c','d','e','f','g','h','n','k','p','q','i','j']
	
	def decompose_rec(i):
		A = r.a.alphabet
		if verb:
			print("decompose %s" % i)
		for c in cc:
			if i in c:
				l,out = loop(r.a, c, i)
				if verb:
					print("out = %s" % out)
				if len(l) > 0:
					# i is in a cycle: it gives a countable union
					if verb:
						print("sum")
					# compute matrix of the loop and outgoing edges
					m = identity_matrix(A[0].nrows())
					lm = []
					for j in l:
						lm.append(m)
						m *= A[j]
					if verb:
						print("loop matrix:")
						print(m)
					c = 0
					for l in out:
						c += len(l)
					#res = r"\sum_{n \in \mathbb{N}} %s^n" % latex(m)
					le = []
					for u,l in enumerate(out):
						if len(l) > 0:
							for (j,k) in l:
								#print((j,k))
								le.append((lm[u]*A[j], decompose_rec(k)))
					return InfUnion(m, Union(le), varnames.pop())
		# i is not in a cycle
		lj = r.a.succs(i)
		if len(lj) > 0:
			if verb:
				print("union")
			l = []
			for j in lj:
				l.append((A[j], decompose_rec(r.a.succ(i, j))))
			return Union(l)
		else:
			return PosCone(A[0].nrows())
	
	# Test if a domain is decomposable a unions over integers.
	for c in cc:
		if not is_loop_or_less(r.a, c):
			raise ValueError("Very complicated domains !")
	
	#recursively decompose r
	return Formulae(decompose_rec(r.a.initial_state))

# compute density from description as unions

def formulae_to_matrices (f, det=False):
	if f.type == "zero":
		from sage.matrix.special import zero_matrix
		if det:
			return [(zero_matrix(f.d), 0, [])]
		else:
			return [(zero_matrix(f.d), [])]
	elif f.type == "domain":
		return f
	elif f.type == "formulae":
		return formulae_to_matrices(f.e, det=det)
	elif f.type == "union":
		res = []
		for m,e in f.l:
			if det:
				res += [(m*m2, abs(m.det())*det, lvar) for m2,det,lvar in formulae_to_matrices(e, det=True)]
			else:
				res += [(m*m2, lvar) for m2,lvar in formulae_to_matrices(e)]
		return res
	elif f.type == "infunion":
		n = f.varname()
		if det:
			return [((f.m**n)*m2, (abs(f.m.det())**n)*det, lvar+[n]) for m2,det,lvar in formulae_to_matrices(f.e, det=True)]
		else:
			return [((f.m**n)*m2, lvar+[n]) for m2,lvar in formulae_to_matrices(f.e)]
	elif f.type == "poscone":
		if det:
			return [(identity_matrix(f.d), 1, [])]
		else:
			return [(identity_matrix(f.d), [])]
	else:
		raise ValueError("type %s unknown" % f.type)

def matrices_to_density(lm, ring=None):
	try:
		if lm.type == "domain":
			return Density(lm.a)
	except:
		pass
	l = []
	s = zero_density(lm[0][0].nrows())
	for m,det,v in lm:
		if len(v) == 0:
			s += simplex_density(m, det=det, ring=ring)
		else:
			l.append(InfSum(simplex_density(m, det=det, ring=ring), v))
	if len(l) == 0:
		return s
	else:
		if s != 0:
			l.append(s)
		if len(l) == 1:
			return l[0]
		else:
			return Sum(l)

def domain_to_density(d, ring=None):
	return matrices_to_density(formulae_to_matrices(d, det=True), ring=ring)

def simplicies_density(lm, ring=None):
	f = 0
	for m,lvar in lm:
		f += simplex_density(m, ring=ring)
	return f

def is_total_mass_finite_two_letters (DetAutomaton a, verb=False):
	# look for state with loop 0 and 1
	for i in range(a.n_states):
		if a.a.e[i].f[0] == i and a.a.e[i].f[1] == i:
			break
	else:
		if verb:
			print("zero mass")
		return True
	a.set_final_states([i])
	a = a.prune()
	# look if 0^oo or 1^oo is recognized
	i = a.a.i
	seen = set([i])
	loop = True
	while True:
		#print("i = %s, seen = %s" % (i, seen))
		i = a.a.e[i].f[0]
		if i == -1:
			break
		if i in seen:
			if verb:
				print("infinite cycle with 0 found")
			return False
		seen.add(i)
	i = a.a.i
	seen = set([i])
	loop = True
	while True:
		i = a.a.e[i].f[1]
		if i == -1:
			break
		if i in seen:
			if verb:
				print("infinite cycle with 1 found")
			return False
		seen.add(i)
	return True

def is_total_mass_finite (d):
	raise NotImplementedError("Sorry, not implemented !")	
