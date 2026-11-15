import datetime as dt, traceback, sys
import numpy as np, bokeh
from bokeh.models import ColumnDataSource
print("bokeh", bokeh.__version__, "numpy", np.__version__, "py", sys.version.split()[0])

def run(label, f):
    try:
        print(label, "->", repr(f()))
    except Exception as e:
        print(label, "-> RAISES", type(e).__name__, e)

def p1():
    s = ColumnDataSource(data=dict(a=[10, 11]))
    s.patch(dict(a=[(2, 100)]))
    return s.data
run("patch index == len (list)", p1)

def p2():
    s = ColumnDataSource(data=dict(a=np.array([10, 11])))
    s.patch(dict(a=[(2, 100)]))
    return s.data
run("patch index == len (ndarray)", p2)

def p3():
    s = ColumnDataSource(data=dict(a=[10, 11], b=[20, 21]))
    events = []
    s.on_change("data", lambda attr, old, new: events.append(attr))
    try:
        s.patch(dict(a=[(0, 99)], b=[(2, 100)]))
    except Exception as e:
        print("   raised", type(e).__name__, e)
    return dict(data=dict(s.data), change_events=events)
run("partial apply", p3)

def p4():
    s = ColumnDataSource(data=dict(foo=[np.zeros((2, 2))]))
    s.patch(dict(foo=[([1, 0, 0], 5)]))
    return s.data
run("multi-index ind_0 == len", p4)

def p5():
    s = ColumnDataSource(data=dict(a=[10, 11]))
    s.patch(dict(a=[(3, 100)]))
run("patch index == len+1 (control)", p5)

def p6():
    s = ColumnDataSource(data=dict(a=[10, 11]))
    s.patch(dict(a=[(np.int64(1), 100)]))
    return s.data
run("patch np.int64 index", p6)

def p7():
    from bokeh.util.serialization import convert_datetime_type
    from zoneinfo import ZoneInfo
    import pandas as pd
    d = dt.datetime(2020, 1, 1, tzinfo=ZoneInfo("America/New_York"))
    return convert_datetime_type(d), convert_datetime_type(pd.Timestamp(d))
run("tz-aware datetime vs Timestamp", p7)
