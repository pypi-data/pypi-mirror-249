import _pymovex3


def debug(d):
    _pymovex3.debug(d)


def connect(*args, **kwargs):
    return _pymovex3.connect(*args, **kwargs)


def fquery(cmd, fieldMap, outputFields=()):
    return _pymovex3.fquery(cmd, fieldMap, outputFields)


def fquery_single(cmd, fieldMap, outputFields=()):
    return _pymovex3.fquery_single(cmd, fieldMap, outputFields)


def close(*args, **kwargs):
    return _pymovex3.close(*args, **kwargs)


def query(cmd, args):
    ffargs = []
    for value, length in args:
        ffargs.append(("%%-%ss" % length) % value)
    fargs = "".join(ffargs)
    query = "%-15s%s" % (cmd, fargs)
    return _pymovex3.query(query)


def rawquery(query):
    return _pymovex3.query(query)


def maxrec(num):
    query("SetLstMaxRec", ((num, 11),))
