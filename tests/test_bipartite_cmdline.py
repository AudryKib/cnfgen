import pytest

from cnfformula.graphs import bipartite_sets
from cnfgen.graph_cmdline import BipartiteGraphHelper

from cnfgen.cmdline import CLIParser, CLIError


def get_bipartite(args):
    parser = CLIParser()
    BipartiteGraphHelper.setup_command_line(parser)
    args = parser.parse_args(args)
    return BipartiteGraphHelper.obtain_graph(args)


def test_bp():
    G = get_bipartite(["--bp", "10", "9", "0.5"])

    assert G.order() == 19

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 9


def test_bm():
    G = get_bipartite(["--bm", "10", "9", "15"])

    assert G.order() == 19
    assert G.size() == 15

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 9


def test_bd():
    G = get_bipartite(["--bd", "20", "13", "3"])

    assert G.order() == 33
    assert G.size() == 60

    left, right = bipartite_sets(G)

    assert len(left) == 20
    assert len(right) == 13

    for v in left:
        assert G.degree(v) == 3


def test_bregular():
    G = get_bipartite(["--bregular", "10", "8", "4"])

    assert G.order() == 18
    assert G.size() == 40

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 8

    for v in left:
        assert G.degree(v) == 4

    for v in right:
        assert G.degree(v) == 5


def test_bregular_fail():
    with pytest.raises(CLIError):
        get_bipartite(["--bregular", "10", "6", "4"])


def test_bshift_empty():

    G = get_bipartite(["--bshift", "10", "9"])
    assert G.order() == 19
    assert G.size() == 0

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 9

    for v in left:
        assert G.degree(v) == 0


def test_bshift_1248():

    G = get_bipartite(["--bshift", "10", "10", "1", "2", "4", "8"])
    assert G.order() == 20
    assert G.size() == 40

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 10

    for v in left:
        assert G.degree(v) == 4

    for v in right:
        assert G.degree(v) == 4


def test_bshift_1248bis():

    G = get_bipartite(["--bshift", "13", "10", "1", "2", "4", "8"])
    assert G.order() == 23
    assert G.size() == 52

    left, right = bipartite_sets(G)

    assert len(left) == 13
    assert len(right) == 10

    for v in left:
        assert G.degree(v) == 4

    for v in right:
        assert G.degree(v) >= 4


def test_bcomplete():
    G = get_bipartite(["--bcomplete", "10", "9"])

    assert G.order() == 19
    assert G.size() == 90

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 9

    for v in left:
        assert G.degree(v) == 9

    for v in right:
        assert G.degree(v) == 10


def test_already_complete():
    with pytest.raises(ValueError):
        get_bipartite(["--bcomplete", "10", "9", "--addedges", "1"])


def test_empty_to_complete():
    G = get_bipartite(["--bp", "10", "9", "0", "--addedges", "90"])

    assert G.order() == 19
    assert G.size() == 90

    left, right = bipartite_sets(G)

    assert len(left) == 10
    assert len(right) == 9

    for v in left:
        assert G.degree(v) == 9

    for v in right:
        assert G.degree(v) == 10


def test_addedges():
    G = get_bipartite(["--bm", "10", "9", "15", "--addedges", "10"])

    assert G.order() == 19
    assert G.size() == 25


def test_too_large_left():
    with pytest.raises(ValueError):
        get_bipartite(["--bcomplete", "10", "9", "--plantbiclique", "11", "9"])


def test_too_large_right():
    with pytest.raises(ValueError):
        get_bipartite(
            ["--bcomplete", "10", "9", "--plantbiclique", "10", "10"])


def test_already_complete_plant():
    G = get_bipartite(["--bcomplete", "10", "9", "--plantbiclique", "5", "4"])

    assert G.order() == 19
    assert G.size() == 90


def test_plant_bcomplete():
    G = get_bipartite(["--bp", "10", "9", "0", "--plantbiclique", "10", "9"])

    assert G.order() == 19
    assert G.size() == 90


def test_add_plant():
    G = get_bipartite(["--bm", "10", "9", "15", "--plantbiclique", "5", "4"])

    assert G.order() == 19
    assert 20 <= G.size() <= 35