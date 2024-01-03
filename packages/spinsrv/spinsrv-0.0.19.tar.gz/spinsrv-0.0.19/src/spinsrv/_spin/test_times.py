from .times import now, python_time, time_from_python


def test_times():
    t = now()
    assert t == time_from_python(python_time(t))
