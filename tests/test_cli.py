from scalecheck.cli import TIME_LIMIT, growth_exponent

SIZES = [100, 1000, 10000]


def test_time_limit_allows_sixty_seconds():
    assert TIME_LIMIT == 60


def test_linear_program_gives_exponent_of_one():
    times = [1.0, 10.0, 100.0]
    assert round(growth_exponent(SIZES, times), 2) == 1.0


def test_quadratic_program_gives_exponent_of_two():
    times = [1.0, 100.0, 10000.0]
    assert round(growth_exponent(SIZES, times), 2) == 2.0
