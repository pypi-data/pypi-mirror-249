from sympy import symbols, IndexedBase, Identity, cos, Inverse, tensorcontraction, permutedims, tensorproduct
from sympy.codegen.array_utils import (CodegenArrayContraction,
                                       CodegenArrayTensorProduct, CodegenArrayDiagonal,
                                       CodegenArrayPermuteDims, CodegenArrayElementwiseAdd,
                                       _codegen_array_parse, _recognize_matrix_expression, _RecognizeMatOp,
                                       _RecognizeMatMulLines, _unfold_recognized_expr,
                                       parse_indexed_expression, recognize_matrix_expression,
                                       parse_matrix_expression, nest_permutation)
from sympy import MatrixSymbol, Sum
from sympy.combinatorics import Permutation
from sympy.functions.special.tensor_functions import KroneckerDelta
from sympy.matrices.expressions.diagonal import DiagMatrix
from sympy.matrices import Trace, MatAdd, MatMul, Transpose
from sympy.testing.pytest import raises
import random


A, B = symbols("A B", cls=IndexedBase)
i, j, k, l, m, n = symbols("i j k l m n")

M = MatrixSymbol("M", k, k)
N = MatrixSymbol("N", k, k)
P = MatrixSymbol("P", k, k)
Q = MatrixSymbol("Q", k, k)


def test_codegen_array_contraction_construction():
    cg = CodegenArrayContraction(A)
    assert cg == A

    s = Sum(A[i]*B[i], (i, 0, 3))
    cg = parse_indexed_expression(s)
    assert cg == CodegenArrayContraction(CodegenArrayTensorProduct(A, B), (0, 1))

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, B), (1, 0))
    assert cg == CodegenArrayContraction(CodegenArrayTensorProduct(A, B), (0, 1))

    expr = M*N
    result = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (1, 2))
    assert parse_matrix_expression(expr) == result
    elem = expr[i, j]
    assert parse_indexed_expression(elem) == result

    expr = M*N*M
    result = CodegenArrayContraction(CodegenArrayTensorProduct(M, N, M), (1, 2), (3, 4))
    assert parse_matrix_expression(expr) == result
    elem = expr[i, j]
    result = CodegenArrayContraction(CodegenArrayTensorProduct(M, M, N), (1, 4), (2, 5))
    cg = parse_indexed_expression(elem)
    cg = cg.sort_args_by_name()
    assert cg == result


def test_codegen_array_contraction_indices_types():

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (0, 1))
    indtup = cg._get_contraction_tuples()
    assert indtup == [[(0, 0), (0, 1)]]
    assert cg._contraction_tuples_to_contraction_indices(cg.expr, indtup) == [(0, 1)]

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (1, 2))
    indtup = cg._get_contraction_tuples()
    assert indtup == [[(0, 1), (1, 0)]]
    assert cg._contraction_tuples_to_contraction_indices(cg.expr, indtup) == [(1, 2)]

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M, M, N), (1, 4), (2, 5))
    indtup = cg._get_contraction_tuples()
    assert indtup == [[(0, 0), (1, 1)], [(0, 1), (2, 0)]]
    assert cg._contraction_tuples_to_contraction_indices(cg.expr, indtup) == [(0, 3), (1, 4)]


def test_codegen_array_recognize_matrix_mul_lines():

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M), (0, 1))
    assert recognize_matrix_expression(cg) == Trace(M)

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (0, 1), (2, 3))
    assert recognize_matrix_expression(cg) == Trace(M)*Trace(N)

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (0, 3), (1, 2))
    assert recognize_matrix_expression(cg) == Trace(M*N)

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (0, 2), (1, 3))
    assert recognize_matrix_expression(cg) == Trace(M*N.T)

    cg = parse_indexed_expression((M*N*P)[i,j])
    assert recognize_matrix_expression(cg) == M*N*P
    cg = parse_matrix_expression(M*N*P)
    assert recognize_matrix_expression(cg) == M*N*P

    cg = parse_indexed_expression((M*N.T*P)[i,j])
    assert recognize_matrix_expression(cg) == M*N.T*P
    cg = parse_matrix_expression(M*N.T*P)
    assert recognize_matrix_expression(cg) == M*N.T*P

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(M,N,P,Q), (1, 2), (5, 6))
    assert recognize_matrix_expression(cg) == [M*N, P*Q]

    expr = -2*M*N
    elem = expr[i, j]
    cg = parse_indexed_expression(elem)
    assert recognize_matrix_expression(cg) == -2*M*N


def test_codegen_array_flatten():

    # Flatten nested CodegenArrayTensorProduct objects:
    expr1 = CodegenArrayTensorProduct(M, N)
    expr2 = CodegenArrayTensorProduct(P, Q)
    expr = CodegenArrayTensorProduct(expr1, expr2)
    assert expr == CodegenArrayTensorProduct(M, N, P, Q)
    assert expr.args == (M, N, P, Q)

    # Flatten mixed CodegenArrayTensorProduct and CodegenArrayContraction objects:
    cg1 = CodegenArrayContraction(expr1, (1, 2))
    cg2 = CodegenArrayContraction(expr2, (0, 3))

    expr = CodegenArrayTensorProduct(cg1, cg2)
    assert expr == CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (1, 2), (4, 7))

    expr = CodegenArrayTensorProduct(M, cg1)
    assert expr == CodegenArrayContraction(CodegenArrayTensorProduct(M, M, N), (3, 4))

    # Flatten nested CodegenArrayContraction objects:
    cgnested = CodegenArrayContraction(cg1, (0, 1))
    assert cgnested == CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (0, 3), (1, 2))

    cgnested = CodegenArrayContraction(CodegenArrayTensorProduct(cg1, cg2), (0, 3))
    assert cgnested == CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 6), (1, 2), (4, 7))

    cg3 = CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (1, 3), (2, 4))
    cgnested = CodegenArrayContraction(cg3, (0, 1))
    assert cgnested == CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 5), (1, 3), (2, 4))

    cgnested = CodegenArrayContraction(cg3, (0, 3), (1, 2))
    assert cgnested == CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 7), (1, 3), (2, 4), (5, 6))

    cg4 = CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (1, 5), (3, 7))
    cgnested = CodegenArrayContraction(cg4, (0, 1))
    assert cgnested == CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 2), (1, 5), (3, 7))

    cgnested = CodegenArrayContraction(cg4, (0, 1), (2, 3))
    assert cgnested == CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 2), (1, 5), (3, 7), (4, 6))

    cg = CodegenArrayDiagonal(cg4)
    assert cg == cg4
    assert isinstance(cg, type(cg4))

    # Flatten nested CodegenArrayDiagonal objects:
    cg1 = CodegenArrayDiagonal(expr1, (1, 2))
    cg2 = CodegenArrayDiagonal(expr2, (0, 3))
    cg3 = CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P, Q), (1, 3), (2, 4))
    cg4 = CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P, Q), (1, 5), (3, 7))

    cgnested = CodegenArrayDiagonal(cg1, (0, 1))
    assert cgnested == CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N), (1, 2), (0, 3))

    cgnested = CodegenArrayDiagonal(cg3, (1, 2))
    assert cgnested == CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P, Q), (1, 3), (2, 4), (5, 6))

    cgnested = CodegenArrayDiagonal(cg4, (1, 2))
    assert cgnested == CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P, Q), (1, 5), (3, 7), (2, 4))


def test_codegen_array_parse():
    expr = M[i, j]
    assert _codegen_array_parse(expr) == (M, (i, j))
    expr = M[i, j]*N[k, l]
    assert _codegen_array_parse(expr) == (CodegenArrayTensorProduct(M, N), (i, j, k, l))
    expr = M[i, j]*N[j, k]
    assert _codegen_array_parse(expr) == (CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N), (1, 2)), (i, k, j))
    expr = Sum(M[i, j]*N[j, k], (j, 0, k-1))
    assert _codegen_array_parse(expr) == (CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (1, 2)), (i, k))
    expr = M[i, j] + N[i, j]
    assert _codegen_array_parse(expr) == (CodegenArrayElementwiseAdd(M, N), (i, j))
    expr = M[i, j] + N[j, i]
    assert _codegen_array_parse(expr) == (CodegenArrayElementwiseAdd(M, CodegenArrayPermuteDims(N, Permutation([1,0]))), (i, j))
    expr = M[i, j] + M[j, i]
    assert _codegen_array_parse(expr) == (CodegenArrayElementwiseAdd(M, CodegenArrayPermuteDims(M, Permutation([1,0]))), (i, j))
    expr = (M*N*P)[i, j]
    assert _codegen_array_parse(expr) == (CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P), (1, 2), (3, 4)), (i, j))
    expr = expr.function  # Disregard summation in previous expression
    ret1, ret2 =  _codegen_array_parse(expr)
    assert ret1 == CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P), (1, 2), (3, 4))
    assert str(ret2) == "(i, j, _i_1, _i_2)"
    expr = KroneckerDelta(i, j)*M[i, k]
    assert _codegen_array_parse(expr) == (M, ({i, j}, k))
    expr = KroneckerDelta(i, j)*KroneckerDelta(j, k)*M[i, l]
    assert _codegen_array_parse(expr) == (M, ({i, j, k}, l))
    expr = KroneckerDelta(j, k)*(M[i, j]*N[k, l] + N[i, j]*M[k, l])
    assert _codegen_array_parse(expr) == (CodegenArrayDiagonal(CodegenArrayElementwiseAdd(
            CodegenArrayTensorProduct(M, N),
            CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), Permutation(0, 2)(1, 3))
        ), (1, 2)), (i, l, frozenset({j, k})))
    expr = KroneckerDelta(j, m)*KroneckerDelta(m, k)*(M[i, j]*N[k, l] + N[i, j]*M[k, l])
    assert _codegen_array_parse(expr) == (CodegenArrayDiagonal(CodegenArrayElementwiseAdd(
            CodegenArrayTensorProduct(M, N),
            CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), Permutation(0, 2)(1, 3))
        ), (1, 2)), (i, l, frozenset({j, m, k})))
    expr = KroneckerDelta(i, j)*KroneckerDelta(j, k)*KroneckerDelta(k,m)*M[i, 0]*KroneckerDelta(m, n)
    assert _codegen_array_parse(expr) == (M, ({i,j,k,m,n}, 0))
    expr = M[i, i]
    assert _codegen_array_parse(expr) == (CodegenArrayDiagonal(M, (0, 1)), (i,))


def test_codegen_array_diagonal():
    cg = CodegenArrayDiagonal(M, (1, 0))
    assert cg == CodegenArrayDiagonal(M, (0, 1))

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P), (4, 1), (2, 0))
    assert cg == CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P), (1, 4), (0, 2))


def test_codegen_recognize_matrix_expression():

    expr = CodegenArrayElementwiseAdd(M, CodegenArrayPermuteDims(M, [1, 0]))
    rec = _recognize_matrix_expression(expr)
    assert rec == _RecognizeMatOp(MatAdd, [M, _RecognizeMatOp(Transpose, [M])])
    assert _unfold_recognized_expr(rec) == M + Transpose(M)

    expr = M[i,j] + N[i,j]
    p1, p2 = _codegen_array_parse(expr)
    rec = _recognize_matrix_expression(p1)
    assert rec == _RecognizeMatOp(MatAdd, [M, N])
    assert _unfold_recognized_expr(rec) == M + N

    expr = M[i,j] + N[j,i]
    p1, p2 = _codegen_array_parse(expr)
    rec = _recognize_matrix_expression(p1)
    assert rec == _RecognizeMatOp(MatAdd, [M, _RecognizeMatOp(Transpose, [N])])
    assert _unfold_recognized_expr(rec) == M + N.T

    expr = M[i,j]*N[k,l] + N[i,j]*M[k,l]
    p1, p2 = _codegen_array_parse(expr)
    rec = _recognize_matrix_expression(p1)
    assert rec == _RecognizeMatOp(MatAdd, [_RecognizeMatMulLines([M, N]), _RecognizeMatMulLines([N, M])])
    #assert _unfold_recognized_expr(rec) == TensorProduct(M, N) + TensorProduct(N, M) maybe?

    expr = (M*N*P)[i, j]
    p1, p2 = _codegen_array_parse(expr)
    rec = _recognize_matrix_expression(p1)
    assert rec == _RecognizeMatMulLines([_RecognizeMatOp(MatMul, [M, N, P])])
    assert _unfold_recognized_expr(rec) == M*N*P

    expr = Sum(M[i,j]*(N*P)[j,m], (j, 0, k-1))
    p1, p2 = _codegen_array_parse(expr)
    rec = _recognize_matrix_expression(p1)
    assert rec == _RecognizeMatOp(MatMul, [M, N, P])
    assert _unfold_recognized_expr(rec) == M*N*P

    expr = Sum((P[j, m] + P[m, j])*(M[i,j]*N[m,n] + N[i,j]*M[m,n]), (j, 0, k-1), (m, 0, k-1))
    p1, p2 = _codegen_array_parse(expr)
    rec = _recognize_matrix_expression(p1)
    assert rec == _RecognizeMatOp(MatAdd, [
        _RecognizeMatOp(MatMul, [M, _RecognizeMatOp(MatAdd, [P, _RecognizeMatOp(Transpose, [P])]), N]),
        _RecognizeMatOp(MatMul, [N, _RecognizeMatOp(MatAdd, [P, _RecognizeMatOp(Transpose, [P])]), M])
        ])
    assert _unfold_recognized_expr(rec) == M*(P + P.T)*N + N*(P + P.T)*M


def test_codegen_array_shape():
    expr = CodegenArrayTensorProduct(M, N, P, Q)
    assert expr.shape == (k, k, k, k, k, k, k, k)
    Z = MatrixSymbol("Z", m, n)
    expr = CodegenArrayTensorProduct(M, Z)
    assert expr.shape == (k, k, m, n)
    expr2 = CodegenArrayContraction(expr, (0, 1))
    assert expr2.shape == (m, n)
    expr2 = CodegenArrayDiagonal(expr, (0, 1))
    assert expr2.shape == (m, n, k)
    exprp = CodegenArrayPermuteDims(expr, [2, 1, 3, 0])
    assert exprp.shape == (m, k, n, k)
    expr3 = CodegenArrayTensorProduct(N, Z)
    expr2 = CodegenArrayElementwiseAdd(expr, expr3)
    assert expr2.shape == (k, k, m, n)

    # Contraction along axes with discordant dimensions:
    raises(ValueError, lambda: CodegenArrayContraction(expr, (1, 2)))
    # Also diagonal needs the same dimensions:
    raises(ValueError, lambda: CodegenArrayDiagonal(expr, (1, 2)))
    # Diagonal requires at least to axes to compute the diagonal:
    raises(ValueError, lambda: CodegenArrayDiagonal(expr, (1,)))


def test_codegen_array_parse_out_of_bounds():

    expr = Sum(M[i, i], (i, 0, 4))
    raises(ValueError, lambda: parse_indexed_expression(expr))
    expr = Sum(M[i, i], (i, 0, k))
    raises(ValueError, lambda: parse_indexed_expression(expr))
    expr = Sum(M[i, i], (i, 1, k-1))
    raises(ValueError, lambda: parse_indexed_expression(expr))

    expr = Sum(M[i, j]*N[j,m], (j, 0, 4))
    raises(ValueError, lambda: parse_indexed_expression(expr))
    expr = Sum(M[i, j]*N[j,m], (j, 0, k))
    raises(ValueError, lambda: parse_indexed_expression(expr))
    expr = Sum(M[i, j]*N[j,m], (j, 1, k-1))
    raises(ValueError, lambda: parse_indexed_expression(expr))


def test_codegen_permutedims_sink():

    cg = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), [0, 1, 3, 2], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == CodegenArrayTensorProduct(M, CodegenArrayPermuteDims(N, [1, 0]))
    assert recognize_matrix_expression(sunk) == [M, N.T]

    cg = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), [1, 0, 3, 2], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == CodegenArrayTensorProduct(CodegenArrayPermuteDims(M, [1, 0]), CodegenArrayPermuteDims(N, [1, 0]))
    assert recognize_matrix_expression(sunk) == [M.T, N.T]

    cg = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), [3, 2, 1, 0], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == CodegenArrayTensorProduct(CodegenArrayPermuteDims(N, [1, 0]), CodegenArrayPermuteDims(M, [1, 0]))
    assert recognize_matrix_expression(sunk) == [N.T, M.T]

    cg = CodegenArrayPermuteDims(CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (1, 2)), [1, 0], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == CodegenArrayContraction(CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), [[0, 3]]), (1, 2))

    cg = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), [1, 0, 3, 2], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == CodegenArrayTensorProduct(CodegenArrayPermuteDims(M, [1, 0]), CodegenArrayPermuteDims(N, [1, 0]))

    cg = CodegenArrayPermuteDims(CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P), (1, 2), (3, 4)), [1, 0], nest_permutation=False)
    sunk = nest_permutation(cg)
    assert sunk == CodegenArrayContraction(CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N, P), [[0, 5]]), (1, 2), (3, 4))


def test_parsing_of_matrix_expressions():

    expr = M*N
    assert parse_matrix_expression(expr) == CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (1, 2))

    expr = Transpose(M)
    assert parse_matrix_expression(expr) == CodegenArrayPermuteDims(M, [1, 0])

    expr = M*Transpose(N)
    assert parse_matrix_expression(expr) == CodegenArrayContraction(CodegenArrayTensorProduct(M, CodegenArrayPermuteDims(N, [1, 0])), (1, 2))

    expr = 3*M*N
    res = parse_matrix_expression(expr)
    rexpr = recognize_matrix_expression(res)
    assert expr == rexpr

    expr = 3*M + N*M.T*M + 4*k*N
    res = parse_matrix_expression(expr)
    rexpr = recognize_matrix_expression(res)
    assert expr == rexpr

    expr = Inverse(M)*N
    rexpr = recognize_matrix_expression(parse_matrix_expression(expr))
    assert expr == rexpr

    expr = M**2
    rexpr = recognize_matrix_expression(parse_matrix_expression(expr))
    assert expr == rexpr

    expr = M*(2*N + 3*M)
    res = parse_matrix_expression(expr)
    rexpr = recognize_matrix_expression(res)
    assert expr.expand() == rexpr.doit()

    expr = Trace(M)
    result = CodegenArrayContraction(M, (0, 1))
    assert parse_matrix_expression(expr) == result


def test_special_matrices():
    a = MatrixSymbol("a", k, 1)
    b = MatrixSymbol("b", k, 1)

    expr = a.T*b
    elem = expr[0, 0]
    cg = parse_indexed_expression(elem)
    assert cg == CodegenArrayContraction(CodegenArrayTensorProduct(a, b), (0, 2))
    assert recognize_matrix_expression(cg) == a.T*b


def test_push_indices_up_and_down():

    indices = list(range(12))

    contr_diag_indices = [(0, 6), (2, 8)]
    assert CodegenArrayContraction._push_indices_down(contr_diag_indices, indices) == (1, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15)
    assert CodegenArrayContraction._push_indices_up(contr_diag_indices, indices) == (None, 0, None, 1, 2, 3, None, 4, None, 5, 6, 7)

    assert CodegenArrayDiagonal._push_indices_down(contr_diag_indices, indices, 10) == (1, 3, 4, 5, 7, 9, (0, 6), (2, 8), None, None, None, None)
    assert CodegenArrayDiagonal._push_indices_up(contr_diag_indices, indices, 10) == (6, 0, 7, 1, 2, 3, 6, 4, 7, 5, None, None)

    contr_diag_indices = [(1, 2), (7, 8)]
    assert CodegenArrayContraction._push_indices_down(contr_diag_indices, indices) == (0, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15)
    assert CodegenArrayContraction._push_indices_up(contr_diag_indices, indices) == (0, None, None, 1, 2, 3, 4, None, None, 5, 6, 7)

    assert CodegenArrayDiagonal._push_indices_down(contr_diag_indices, indices, 10) == (0, 3, 4, 5, 6, 9, (1, 2), (7, 8), None, None, None, None)
    assert CodegenArrayDiagonal._push_indices_up(contr_diag_indices, indices, 10) == (0, 6, 6, 1, 2, 3, 4, 7, 7, 5, None, None)


def test_recognize_diagonalized_vectors():

    a = MatrixSymbol("a", k, 1)
    b = MatrixSymbol("b", k, 1)
    A = MatrixSymbol("A", k, k)
    B = MatrixSymbol("B", k, k)
    C = MatrixSymbol("C", k, k)
    X = MatrixSymbol("X", k, k)
    x = MatrixSymbol("x", k, 1)
    I1 = Identity(1)
    I = Identity(k)

    # Check matrix recognition over trivial dimensions:

    cg = CodegenArrayTensorProduct(a, b)
    assert recognize_matrix_expression(cg) == a*b.T

    cg = CodegenArrayTensorProduct(I1, a, b)
    assert recognize_matrix_expression(cg) == a*I1*b.T

    # Recognize trace inside a tensor product:

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, B, C), (0, 3), (1, 2))
    assert recognize_matrix_expression(cg) == Trace(A*B)*C

    # Transform diagonal operator to contraction:

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(A, a), (1, 2))
    assert cg.transform_to_product() == CodegenArrayContraction(CodegenArrayTensorProduct(A, DiagMatrix(a)), (1, 2))
    assert recognize_matrix_expression(cg) == A*DiagMatrix(a)

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(a, b), (0, 2))
    assert cg.transform_to_product() == CodegenArrayContraction(CodegenArrayTensorProduct(DiagMatrix(a), b), (0, 2))
    assert recognize_matrix_expression(cg).doit() == DiagMatrix(a)*b

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(A, a), (0, 2))
    assert cg.transform_to_product() == CodegenArrayContraction(CodegenArrayTensorProduct(A, DiagMatrix(a)), (0, 2))
    assert recognize_matrix_expression(cg) == A.T*DiagMatrix(a)

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(I, x, I1), (0, 2), (3, 5))
    assert cg.transform_to_product() == CodegenArrayContraction(CodegenArrayTensorProduct(I, DiagMatrix(x), I1), (0, 2))

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(I, x, A, B), (1, 2), (5, 6))
    assert cg.transform_to_product() == CodegenArrayDiagonal(CodegenArrayContraction(CodegenArrayTensorProduct(I, DiagMatrix(x), A, B), (1, 2)), (3, 4))

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(x, I1), (1, 2))
    assert isinstance(cg, CodegenArrayDiagonal)
    assert cg.diagonal_indices == ((1, 2),)
    assert recognize_matrix_expression(cg) == x

    cg = CodegenArrayDiagonal(CodegenArrayTensorProduct(x, I), (0, 2))
    assert cg.transform_to_product() == CodegenArrayContraction(CodegenArrayTensorProduct(DiagMatrix(x), I), (0, 2))
    assert recognize_matrix_expression(cg).doit() == DiagMatrix(x)

    raises(ValueError, lambda: CodegenArrayDiagonal(x, (1,)))

    # Ignore identity matrices with contractions:

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(I, A, I, I), (0, 2), (1, 3), (5, 7))
    assert cg.split_multiple_contractions() == cg
    assert recognize_matrix_expression(cg) == Trace(A)*I

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(Trace(A) * I, I, I), (1, 5), (3, 4))
    assert cg.split_multiple_contractions() == cg
    assert recognize_matrix_expression(cg).doit() == Trace(A)*I

    # Add DiagMatrix when required:

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, a), (1, 2))
    assert cg.split_multiple_contractions() == cg
    assert recognize_matrix_expression(cg) == A*a

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, a, B), (1, 2, 4))
    assert cg.split_multiple_contractions() == CodegenArrayContraction(CodegenArrayTensorProduct(A, DiagMatrix(a), B), (1, 2), (3, 4))
    assert recognize_matrix_expression(cg) == A*DiagMatrix(a)*B

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, a, B), (0, 2, 4))
    assert cg.split_multiple_contractions() == CodegenArrayContraction(CodegenArrayTensorProduct(A, DiagMatrix(a), B), (0, 2), (3, 4))
    assert recognize_matrix_expression(cg) == A.T*DiagMatrix(a)*B

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, a, b, a.T, B), (0, 2, 4, 7, 9))
    assert cg.split_multiple_contractions() == CodegenArrayContraction(CodegenArrayTensorProduct(A, DiagMatrix(a), DiagMatrix(b),
                                                                                                 DiagMatrix(a), B),
                                                                       (0, 2), (3, 4), (5, 7), (6, 9))
    assert recognize_matrix_expression(cg).doit() == A.T*DiagMatrix(a)*DiagMatrix(b)*DiagMatrix(a)*B.T

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(I1, I1, I1), (1, 2, 4))
    assert cg.split_multiple_contractions() == CodegenArrayContraction(CodegenArrayTensorProduct(I1, I1, I1), (1, 2), (3, 4))
    assert recognize_matrix_expression(cg).doit() == Identity(1)

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(I, I, I, I, A), (1, 2, 8), (5, 6, 9))
    assert recognize_matrix_expression(cg.split_multiple_contractions()).doit() == A

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, a, C, a, B), (1, 2, 4), (5, 6, 8))
    expected = CodegenArrayContraction(CodegenArrayTensorProduct(DiagMatrix(a), DiagMatrix(a), C, A, B), (0, 4), (1, 7), (2, 5), (3, 8))
    assert cg.split_multiple_contractions() == expected
    assert recognize_matrix_expression(cg).doit() == A*DiagMatrix(a)*C*DiagMatrix(a)*B

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(a, I1, b, I1, (a.T*b).applyfunc(cos)), (1, 2, 8), (5, 6, 9))
    assert cg.split_multiple_contractions().dummy_eq(CodegenArrayContraction(CodegenArrayTensorProduct((a.T * b).applyfunc(cos), I1, I1, a, b), (0, 2), (1, 4), (3, 7), (5, 9)))
    assert recognize_matrix_expression(cg).doit().dummy_eq(MatMul(a, (a.T*b).applyfunc(cos), b.T))

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A.T, a, b, b.T, (A*X*b).applyfunc(cos)), (1, 2, 8), (5, 6, 9))
    assert cg.split_multiple_contractions().dummy_eq(CodegenArrayContraction(CodegenArrayTensorProduct(DiagMatrix(a), (A*X*b).applyfunc(cos), A.T, b, b.T), (0, 2), (1, 5), (3, 7, 8)))
    # assert recognize_matrix_expression(cg)

    # Check no overlap of lines:

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(A, a, C, a, B), (1, 2, 4), (5, 6, 8), (3, 7))
    assert cg.split_multiple_contractions() == cg

    cg = CodegenArrayContraction(CodegenArrayTensorProduct(a, b, A), (0, 2, 4), (1, 3))
    assert cg.split_multiple_contractions() == cg


def test_nested_permutations():

    cg = CodegenArrayPermuteDims(CodegenArrayPermuteDims(M, (1, 0)), (1, 0))
    assert cg == M

    times = 3
    plist1 = [list(range(6)) for i in range(times)]
    plist2 = [list(range(6)) for i in range(times)]

    for i in range(times):
        random.shuffle(plist1[i])
        random.shuffle(plist2[i])

    plist1.append([2, 5, 4, 1, 0, 3])
    plist2.append([3, 5, 0, 4, 1, 2])

    plist1.append([2, 5, 4, 0, 3, 1])
    plist2.append([3, 0, 5, 1, 2, 4])

    plist1.append([5, 4, 2, 0, 3, 1])
    plist2.append([4, 5, 0, 2, 3, 1])

    Me = M.subs(k, 3).as_explicit()
    Ne = N.subs(k, 3).as_explicit()
    Pe = P.subs(k, 3).as_explicit()
    cge = tensorproduct(Me, Ne, Pe)

    for permutation_array1, permutation_array2 in zip(plist1, plist2):
        p1 = Permutation(permutation_array1)
        p2 = Permutation(permutation_array2)

        cg = CodegenArrayPermuteDims(
            CodegenArrayPermuteDims(
                CodegenArrayTensorProduct(M, N, P),
                p1),
            p2
        )
        result = CodegenArrayPermuteDims(
            CodegenArrayTensorProduct(M, N, P),
            p2*p1
        )
        assert cg == result

        # Check that `permutedims` behaves the same way with explicit-component arrays:
        result1 = permutedims(permutedims(cge, p1), p2)
        result2 = permutedims(cge, p2*p1)
        assert result1 == result2


def test_contraction_permutation_mix():

    Me = M.subs(k, 3).as_explicit()
    Ne = N.subs(k, 3).as_explicit()

    cg1 = CodegenArrayContraction(CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), Permutation([0, 2, 1, 3])), (2, 3))
    cg2 = CodegenArrayContraction(CodegenArrayTensorProduct(M, N), (1, 3))
    assert cg1 == cg2
    assert recognize_matrix_expression(cg2) == M*N.T
    cge1 = tensorcontraction(permutedims(tensorproduct(Me, Ne), Permutation([0, 2, 1, 3])), (2, 3))
    cge2 = tensorcontraction(tensorproduct(Me, Ne), (1, 3))
    assert cge1 == cge2

    cg1 = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N), Permutation([0, 1, 3, 2]))
    cg2 = CodegenArrayTensorProduct(M, CodegenArrayPermuteDims(N, Permutation([1, 0])))
    assert cg1 == cg2
    assert recognize_matrix_expression(cg1) == [M, N.T]
    assert recognize_matrix_expression(cg2) == [M, N.T]

    cg1 = CodegenArrayContraction(
        CodegenArrayPermuteDims(
            CodegenArrayTensorProduct(M, N, P, Q), Permutation([0, 2, 3, 1, 4, 5, 7, 6])),
        (1, 2), (3, 5)
    )
    cg2 = CodegenArrayContraction(
        CodegenArrayTensorProduct(M, N, P, CodegenArrayPermuteDims(Q, Permutation([1, 0]))),
        (1, 5), (2, 3)
    )
    assert cg1 == cg2
    assert recognize_matrix_expression(cg1) == [M*P.T*Trace(N), Q.T]
    assert recognize_matrix_expression(cg2) == [M*P.T*Trace(N), Q.T]

    cg1 = CodegenArrayContraction(
        CodegenArrayPermuteDims(
            CodegenArrayTensorProduct(M, N, P, Q), Permutation([1, 0, 4, 6, 2, 7, 5, 3])),
        (0, 1), (2, 6), (3, 7)
    )
    cg2 = CodegenArrayPermuteDims(
        CodegenArrayContraction(
            CodegenArrayTensorProduct(M, P, Q, N),
            (0, 1), (2, 3), (4, 7)),
        [1, 0]
    )
    assert cg1 == cg2

    cg1 = CodegenArrayContraction(
        CodegenArrayPermuteDims(
            CodegenArrayTensorProduct(M, N, P, Q), Permutation([1, 0, 4, 6, 7, 2, 5, 3])),
        (0, 1), (2, 6), (3, 7)
    )
    cg2 = CodegenArrayPermuteDims(
        CodegenArrayContraction(
            CodegenArrayTensorProduct(CodegenArrayPermuteDims(M, [1, 0]), N, P, Q),
            (0, 1), (3, 6), (4, 5)
        ),
        Permutation([1, 0])
    )
    assert cg1 == cg2


def test_permute_tensor_product():
    cg1 = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N, P, Q), Permutation([2, 3, 1, 0, 5, 4, 6, 7]))
    cg2 = CodegenArrayTensorProduct(N, CodegenArrayPermuteDims(M, [1, 0]),
                                    CodegenArrayPermuteDims(P, [1, 0]), Q)
    assert cg1 == cg2

    # TODO: reverse operation starting with `CodegenArrayPermuteDims` and getting down to `bb`...
    cg1 = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N, P, Q), Permutation([2, 3, 4, 5, 0, 1, 6, 7]))
    cg2 = CodegenArrayTensorProduct(N, P, M, Q)
    assert cg1 == cg2

    cg1 = CodegenArrayPermuteDims(CodegenArrayTensorProduct(M, N, P, Q), Permutation([2, 3, 4, 6, 5, 7, 0, 1]))
    assert cg1.expr == CodegenArrayTensorProduct(N, P, Q, M)
    assert cg1.permutation == Permutation([0, 1, 2, 4, 3, 5, 6, 7])

    cg1 = CodegenArrayContraction(
        CodegenArrayPermuteDims(
            CodegenArrayTensorProduct(N, Q, Q, M),
            [2, 1, 5, 4, 0, 3, 6, 7]),
        [1, 2, 6])
    cg2 = CodegenArrayPermuteDims(CodegenArrayContraction(CodegenArrayTensorProduct(Q, Q, N, M), (3, 5, 6)), [0, 2, 3, 1, 4])
    assert cg1 == cg2

    cg1 = CodegenArrayContraction(
        CodegenArrayContraction(
            CodegenArrayContraction(
                CodegenArrayContraction(
                    CodegenArrayPermuteDims(
                        CodegenArrayTensorProduct(N, Q, Q, M),
                        [2, 1, 5, 4, 0, 3, 6, 7]),
                    [1, 2, 6]),
                [1, 3, 4]),
            [1]),
        [0])
    cg2 = CodegenArrayContraction(CodegenArrayTensorProduct(M, N, Q, Q), (0, 3, 5), (1, 4, 7), (2,), (6,))
    assert cg1 == cg2


def test_normalize_diagonal_permutedims():
    tp = CodegenArrayTensorProduct(M, Q, N, P)
    expr = CodegenArrayDiagonal(
        CodegenArrayPermuteDims(tp, [0, 1, 2, 4, 7, 6, 3, 5]), (2, 4, 5), (6, 7),
        (0, 3))
    result = CodegenArrayDiagonal(tp, (2, 6, 7), (3, 5), (0, 4))
    assert expr == result

    tp = CodegenArrayTensorProduct(M, N, P, Q)
    expr = CodegenArrayDiagonal(CodegenArrayPermuteDims(tp, [0, 5, 2, 4, 1, 6, 3, 7]), (1, 2, 6), (3, 4))
    result = CodegenArrayDiagonal(CodegenArrayTensorProduct(M, P, N, Q), (3, 4, 5), (1, 2))
    assert expr == result


def test_normalize_diagonal_contraction():
    tp = CodegenArrayTensorProduct(M, N, P, Q)
    expr = CodegenArrayContraction(CodegenArrayDiagonal(tp, (1, 3, 4)), (0, 3))
    result = CodegenArrayDiagonal(CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 6)), (0, 2, 3))
    assert expr == result

    expr = CodegenArrayContraction(CodegenArrayDiagonal(tp, (0, 1, 2, 3, 7)), (1, 2, 3))
    result = CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 1, 2, 3, 5, 6, 7))
    assert expr == result

    expr = CodegenArrayContraction(CodegenArrayDiagonal(tp, (0, 2, 6, 7)), (1, 2, 3))
    result = CodegenArrayDiagonal(CodegenArrayContraction(tp, (3, 4, 5)), (0, 2, 3, 4))
    assert expr == result

    td = CodegenArrayDiagonal(CodegenArrayTensorProduct(M, N, P, Q), (0, 3))
    expr = CodegenArrayContraction(td, (2, 1), (0, 4, 6, 5, 3))
    result = CodegenArrayContraction(CodegenArrayTensorProduct(M, N, P, Q), (0, 1, 3, 5, 6, 7), (2, 4))
    assert expr == result
