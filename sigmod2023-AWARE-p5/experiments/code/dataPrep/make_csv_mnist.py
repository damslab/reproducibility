
import argparse
import array
import functools
import gzip
import operator
import os
import struct
import tempfile

import numpy as np

# see https://github.com/datapythonista/mnist/blob/master/mnist/__init__.py for original implementation


class IdxDecodeError(ValueError):
    """Raised when an invalid idx file is parsed."""
    pass


def parse_idx(fd):
    """Parse an IDX file, and return it as a np array.
    Parameters
    ----------
    fd : file
        File descriptor of the IDX file to parse
    endian : str
        Byte order of the IDX file. See [1] for available options
    Returns
    -------
    data : np.ndarray
        np array with the dimensions and the data in the IDX file
    1. https://docs.python.org/3/library/struct.html
        #byte-order-size-and-alignment
    """
    DATA_TYPES = {0x08: 'B',  # unsigned byte
                  0x09: 'b',  # signed byte
                  0x0b: 'h',  # short (2 bytes)
                  0x0c: 'i',  # int (4 bytes)
                  0x0d: 'f',  # float (4 bytes)
                  0x0e: 'd'}  # double (8 bytes)

    header = fd.read(4)
    if len(header) != 4:
        raise IdxDecodeError('Invalid IDX file, '
                             'file empty or does not contain a full header.')

    zeros, data_type, num_dimensions = struct.unpack('>HBB', header)

    if zeros != 0:
        raise IdxDecodeError('Invalid IDX file, '
                             'file must start with two zero bytes. '
                             'Found 0x%02x' % zeros)

    try:
        data_type = DATA_TYPES[data_type]
    except KeyError:
        raise IdxDecodeError('Unknown data type '
                             '0x%02x in IDX file' % data_type)

    dimension_sizes = struct.unpack('>' + 'I' * num_dimensions,
                                    fd.read(4 * num_dimensions))

    data = array.array(data_type, fd.read())
    data.byteswap()  # looks like array.array reads data as little endian

    expected_items = functools.reduce(operator.mul, dimension_sizes)
    if len(data) != expected_items:
        raise IdxDecodeError('IDX file has wrong number of items. '
                             'Expected: %d. Found: %d' % (expected_items,
                                                          len(data)))

    return np.array(data).reshape(dimension_sizes)


def parse_mnist_file(fname):
    """Download the IDX file named fname from the URL specified in dataset_url
    and return it as a np array.
    Parameters
    ----------
    fname : str
        File name to parse
    Returns
    -------
    data : np.ndarray
        np array with the dimensions and the data in the IDX file
    """
    with open(fname, 'rb') as fd:
        return parse_idx(fd)


def save_csv_images(fname, csvName):
    data = parse_mnist_file(fname)
    print(data.shape)
    data = data.reshape((data.shape[0], 28*28))
    np.savetxt(csvName, data, delimiter=',', fmt='%d')


def save_csv_labels(fname, csvName):
    data = parse_mnist_file(fname)
    print(data.shape)
    # data = data.reshape((data.shape[0], 28*28))
    np.savetxt(csvName, data, delimiter=',', fmt='%d')


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', required=True, type=str)
parser.add_argument('-o', '--output', required=True, type=str)
parser.add_argument('-i', '--image', type=bool, default=False)
args = parser.parse_args()

if args.image:
    save_csv_images(args.data, args.output)
else:
    save_csv_labels(args.data, args.output)
