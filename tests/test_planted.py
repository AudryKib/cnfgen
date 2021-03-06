import pytest

from cnfgen.cnf import CNF
from cnfgen import RandomKCNF

from tests.utils import assertCnfEqual


def test_not_planted():
    F = RandomKCNF(4, 10, 20, seed=2311)
    G = RandomKCNF(4, 10, 20, seed=2311, planted_assignments=[])
    assertCnfEqual(F, G)


def test_one():
    assign = [{'x_1': True, 'x_2': False}]
    F = RandomKCNF(2, 2, 3, planted_assignments=assign)
    G = CNF([
        [(True, 'x_1'), (False, 'x_2')],
        [(False, 'x_1'), (False, 'x_2')],
        [(True, 'x_1'), (True, 'x_2')],
    ])
    assertCnfEqual(F, G)


def test_most():
    ass = [
        {
            'x_1': True,
            'x_2': False
        },
        {
            'x_1': False,
            'x_2': False
        },
        {
            'x_1': True,
            'x_2': True
        },
    ]
    F = RandomKCNF(2, 2, 1, planted_assignments=ass)
    G = CNF([[(True, 'x_1'), (False, 'x_2')]])
    assertCnfEqual(F, G)


def test_all():
    ass = [
        {
            'x_1': False,
            'x_2': True
        },
        {
            'x_1': True,
            'x_2': False
        },
        {
            'x_1': False,
            'x_2': False
        },
        {
            'x_1': True,
            'x_2': True
        },
    ]
    with pytest.raises(ValueError):
        RandomKCNF(2, 2, 1, planted_assignments=ass)
