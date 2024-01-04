from .__version__ import __version__
from functools import reduce


class KMP:
    """
    https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
    https://gist.github.com/m00nlight/daa6786cc503fde12a77
    """

    def partial(self, pattern):
        """Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def search(self, T, P):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in T
        """
        partial, ret, j = self.partial(P), [], 0

        for i in range(len(T)):
            while j > 0 and T[i] != P[j]:
                j = partial[j - 1]
            if T[i] == P[j]:
                j += 1
            if j == len(P):
                ret.append(i - (j - 1))
                j = partial[j - 1]

        return ret


def endianness_swap(buffer: bytes) -> bytes:
    """Swap the endianness of the buffer and return it

    Args:
        buffer (bytes): _description_

    Returns:
        bytes: _description_
    """
    buffer = bytearray(buffer)
    buffer[0::2], buffer[1::2] = buffer[1::2], buffer[0::2]
    return buffer
    # return reduce(lambda a, b: a + b, [buffer[i : i + bytecount][::-1] for i in range(0, len(buffer), bytecount)])
