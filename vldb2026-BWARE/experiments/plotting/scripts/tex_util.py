import os
import numpy as np

numprint = "\\numprint{"
end = "}"


def float3(f):
    return '\\numprint{' + "{0:0.3f}".format(f) + "}"


def float2(f):
    return '\\numprint{' + "{0:0.2f}".format(f) + "}"


def float1(f):
    return '\\numprint{' + "{0:0.1f}".format(f) + "}"


def integer(f):
    return '\\numprint{' + "{0:0.0f}".format(f) + "}"


def makeBytes(v):
    if v > 1000000000:
        vf = v / 1000000000.0
        return "{0}{1:0.2f}{2} GB".format(numprint, vf, end)
    elif v > 1000000:
        vf = v / 1000000.0
        return "{0}{1:0.2f}{2} MB".format(numprint, vf, end)
    elif v > 1000:
        vf = v / 1000.0
        return "{0}{1:0.2f}{2} KB".format(numprint, vf, end)
    else:
        return "{0}{1}{2} B".format(numprint, v, end)


def formatRatio(v):
    if v > 100:
        return "{0}{1:0.0f}{2}".format(numprint, v, end)
    elif v > 10:
        return "{0}{1:0.1f}{2}".format(numprint, v, end)
    else:
        return "{0}{1:0.2f}{2}".format(numprint, v, end)


def make_tex_table(data):
    s = ""
    idx = 0
    for x in data:
        for y in x:
            s += y + " &\t"
        s = s[:-2] + " \\\\\n"
        idx += 1
    return s
