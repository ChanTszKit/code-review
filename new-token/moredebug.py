def dict_tail(d, n=10, offset=0):
    return {k:d[k] for k in list(d)[-n-offset:len(d)-offset]}