from __future__ import absolute_import, print_function

import unittest

import numpy as np

from weighted_levenshtein import dam_lev, lev, osa


class TestClev(unittest.TestCase):

    def setUp(self):
        self.iw = np.ones(128, dtype=np.float64)
        self.dw = np.ones(128, dtype=np.float64)
        self.sw = np.ones((128, 128), dtype=np.float64)
        self.tw = np.ones((128, 128), dtype=np.float64)

    def _lev(self, x, y, sc=float('inf')):
        return lev(x, y, self.iw, self.dw, self.sw, sc)

    def _osa(self, x, y, sc=float('inf')):
        return osa(x, y, self.iw, self.dw, self.sw, self.tw, sc)

    def _dl(self, x, y, sc=float('inf')):
        return dam_lev(x, y, self.iw, self.dw, self.sw, self.tw, sc)

    def test_lev(self):
        self.assertEqual(self._lev('1234', '1234'), 0.0)
        self.assertEqual(self._lev('', '1234'), 4.0)
        self.assertEqual(self._lev('1234', ''), 4.0)
        self.assertEqual(self._lev('', ''), 0.0)
        self.assertEqual(self._lev('1234', '12'), 2.0)
        self.assertEqual(self._lev('1234', '14'), 2.0)
        self.assertEqual(self._lev('1111', '1'), 3.0)

    def test_lev_insert(self):
        self.iw[ord('a')] = 5
        self.assertEqual(self._lev('', 'a'), 5.0)
        self.assertEqual(self._lev('a', ''), 1.0)
        self.assertEqual(self._lev('', 'aa'), 10.0)
        self.assertEqual(self._lev('a', 'aa'), 5.0)
        self.assertEqual(self._lev('aa', 'a'), 1.0)
        self.assertEqual(self._lev('asdf', 'asdf'), 0.0)
        self.assertEqual(self._lev('xyz', 'abc'), 3.0)
        self.assertEqual(self._lev('xyz', 'axyz'), 5.0)
        self.assertEqual(self._lev('x', 'ax'), 5.0)

    def test_lev_delete(self):
        self.dw[ord('z')] = 7.5
        self.assertEqual(self._lev('', 'z'), 1.0)
        self.assertEqual(self._lev('z', ''), 7.5)
        self.assertEqual(self._lev('xyz', 'zzxz'), 3.0)
        self.assertEqual(self._lev('zzxzzz', 'xyz'), 18.0)

    def test_lev_substitute(self):
        self.sw[ord('a'), ord('z')] = 1.2
        self.sw[ord('z'), ord('a')] = 0.1
        self.assertEqual(self._lev('a', 'z'), 1.2)
        self.assertEqual(self._lev('z', 'a'), 0.1)
        self.assertEqual(self._lev('a', ''), 1)
        self.assertEqual(self._lev('', 'a'), 1)
        self.assertEqual(self._lev('asdf', 'zzzz'), 4.2)
        self.assertEqual(self._lev('asdf', 'zz'), 4.0)
        self.assertEqual(self._lev('asdf', 'zsdf'), 1.2)
        self.assertEqual(self._lev('zsdf', 'asdf'), 0.1)

    def test_osa(self):
        self.assertEqual(self._osa('1234', '1234'), 0.0)
        self.assertEqual(self._osa('', '1234'), 4.0)
        self.assertEqual(self._osa('1234', ''), 4.0)
        self.assertEqual(self._osa('', ''), 0.0)
        self.assertEqual(self._osa('1234', '12'), 2.0)
        self.assertEqual(self._osa('1234', '14'), 2.0)
        self.assertEqual(self._osa('1111', '1'), 3.0)

    def test_osa_insert(self):
        self.iw[ord('a')] = 5
        self.assertEqual(self._osa('', 'a'), 5.0)
        self.assertEqual(self._osa('a', ''), 1.0)
        self.assertEqual(self._osa('', 'aa'), 10.0)
        self.assertEqual(self._osa('a', 'aa'), 5.0)
        self.assertEqual(self._osa('aa', 'a'), 1.0)
        self.assertEqual(self._osa('asdf', 'asdf'), 0.0)
        self.assertEqual(self._osa('xyz', 'abc'), 3.0)
        self.assertEqual(self._osa('xyz', 'axyz'), 5.0)
        self.assertEqual(self._osa('x', 'ax'), 5.0)

    def test_osa_delete(self):
        self.dw[ord('z')] = 7.5
        self.assertEqual(self._osa('', 'z'), 1.0)
        self.assertEqual(self._osa('z', ''), 7.5)
        self.assertEqual(self._osa('xyz', 'zzxz'), 3.0)
        self.assertEqual(self._osa('zzxzzz', 'xyz'), 18.0)

    def test_osa_substitute(self):
        self.sw[ord('a'), ord('z')] = 1.2
        self.sw[ord('z'), ord('a')] = 0.1
        self.assertEqual(self._osa('a', 'z'), 1.2)
        self.assertEqual(self._osa('z', 'a'), 0.1)
        self.assertEqual(self._osa('a', ''), 1)
        self.assertEqual(self._osa('', 'a'), 1)
        self.assertEqual(self._osa('asdf', 'zzzz'), 4.2)
        self.assertEqual(self._osa('asdf', 'zz'), 4.0)
        self.assertEqual(self._osa('asdf', 'zsdf'), 1.2)
        self.assertEqual(self._osa('zsdf', 'asdf'), 0.1)

    def test_osa_transpose(self):
        self.tw[ord('a'), ord('z')] = 1.5
        self.tw[ord('z'), ord('a')] = 0.5
        self.assertEqual(self._osa('az', 'za'), 1.5)
        self.assertEqual(self._osa('za', 'az'), 0.5)
        self.assertEqual(self._osa('az', 'zfa'), 3)
        self.assertEqual(self._osa('azza', 'zaaz'), 2)
        self.assertEqual(self._osa('zaaz', 'azza'), 2)
        self.assertEqual(self._osa('azbza', 'zabaz'), 2)
        self.assertEqual(self._osa('zabaz', 'azbza'), 2)
        self.assertEqual(self._osa('azxza', 'zayaz'), 3)
        self.assertEqual(self._osa('zaxaz', 'azyza'), 3)

    def test_dl(self):
        self.assertEqual(self._dl('', ''), 0)
        self.assertEqual(self._dl('', 'a'), 1)
        self.assertEqual(self._dl('a', ''), 1)
        self.assertEqual(self._dl('a', 'b'), 1)
        self.assertEqual(self._dl('a', 'ab'), 1)
        self.assertEqual(self._dl('ab', 'ba'), 1)
        self.assertEqual(self._dl('ab', 'bca'), 2)
        self.assertEqual(self._dl('bca', 'ab'), 2)
        self.assertEqual(self._dl('ab', 'bdca'), 3)
        self.assertEqual(self._dl('bdca', 'ab'), 3)

    def test_dl_transpose(self):
        self.iw[ord('c')] = 1.9
        self.assertEqual(self._dl('ab', 'bca'), 2.9)
        self.assertEqual(self._dl('ab', 'bdca'), 3.9)
        self.assertEqual(self._dl('bca', 'ab'), 2)

    def test_dl_transpose2(self):
        self.dw[ord('c')] = 1.9
        self.assertEqual(self._dl('bca', 'ab'), 2.9)
        self.assertEqual(self._dl('bdca', 'ab'), 3.9)
        self.assertEqual(self._dl('ab', 'bca'), 2)

    def test_dl_transpose3(self):
        self.tw[ord('a'), ord('b')] = 1.5
        self.assertEqual(self._dl('ab', 'bca'), 2.5)
        self.assertEqual(self._dl('bca', 'ab'), 2)

    def test_dl_transpose4(self):
        self.tw[ord('b'), ord('a')] = 1.5
        self.assertEqual(self._dl('ab', 'bca'), 2)
        self.assertEqual(self._dl('bca', 'ab'), 2.5)

    def test_lev_cutoff(self):
        self.assertEqual(self._lev('1234', '1234', 1.0), 0.0)
        self.assertEqual(self._lev('', '1234', 2.0), 2.0)
        self.assertEqual(self._lev('1234', '', 2.0), 2.0)
        self.assertEqual(self._lev('', '', 1.0), 0.0)
        self.assertEqual(self._lev('1234', '12', 3.0), 2.0)
        self.assertEqual(self._lev('1234', '14', 1.5), 1.5)
        self.assertEqual(self._lev('1111', '1', 2.5), 2.5)

    def test_osa_cutoff(self):
        self.assertEqual(self._osa('1234', '1234', 1.0), 0.0)
        self.assertEqual(self._osa('', '1234', 2.0), 2.0)
        self.assertEqual(self._osa('1234', '', 2.0), 2.0)
        self.assertEqual(self._osa('', '', 0.5), 0.0)
        self.assertEqual(self._osa('1234', '12', 2.5), 2.0)
        self.assertEqual(self._osa('1234', '14', 1.5), 1.5)
        self.assertEqual(self._osa('1111', '1', 2.0), 2.0)

    def test_dl_cutoff(self):
        self.assertEqual(self._dl('', '', 1), 0)
        self.assertEqual(self._dl('', 'a', 2), 1)
        self.assertEqual(self._dl('a', '', 2), 1)
        self.assertEqual(self._dl('a', 'b', 0.5), 0.5)
        self.assertEqual(self._dl('a', 'ab', 0.5), 0.5)
        self.assertEqual(self._dl('ab', 'ba', 1.5), 1)
        self.assertEqual(self._dl('ab', 'bca', 1.5), 1.5)
        self.assertEqual(self._dl('bca', 'ab', 3.0), 2)
        self.assertEqual(self._dl('ab', 'bdca', 2.5), 2.5)
        self.assertEqual(self._dl('bdca', 'ab', 3.5), 3)


class TestClevUsingDefaultValues(unittest.TestCase):

    def test_lev(self):
        self.assertEqual(lev('1234', '1234'), 0.0)
        self.assertEqual(lev('', '1234'), 4.0)
        self.assertEqual(lev('1234', ''), 4.0)
        self.assertEqual(lev('', ''), 0.0)
        self.assertEqual(lev('1234', '12'), 2.0)
        self.assertEqual(lev('1234', '14'), 2.0)
        self.assertEqual(lev('1111', '1'), 3.0)

    def test_osa(self):
        self.assertEqual(osa('1234', '1234'), 0.0)
        self.assertEqual(osa('', '1234'), 4.0)
        self.assertEqual(osa('1234', ''), 4.0)
        self.assertEqual(osa('', ''), 0.0)
        self.assertEqual(osa('1234', '12'), 2.0)
        self.assertEqual(osa('1234', '14'), 2.0)
        self.assertEqual(osa('1111', '1'), 3.0)

    def test_dl(self):
        self.assertEqual(dam_lev('', ''), 0)
        self.assertEqual(dam_lev('', 'a'), 1)
        self.assertEqual(dam_lev('a', ''), 1)
        self.assertEqual(dam_lev('a', 'b'), 1)
        self.assertEqual(dam_lev('a', 'ab'), 1)
        self.assertEqual(dam_lev('ab', 'ba'), 1)
        self.assertEqual(dam_lev('ab', 'bca'), 2)
        self.assertEqual(dam_lev('bca', 'ab'), 2)
        self.assertEqual(dam_lev('ab', 'bdca'), 3)
        self.assertEqual(dam_lev('bdca', 'ab'), 3)


class TestClevUsingNonPositiveCutoff(unittest.TestCase):

    def test_cutoff(self):
        self.assertEqual(lev('1234', '1234', score_cutoff=0), 0.0)
        self.assertEqual(lev('1234', '123', score_cutoff=0), 0.0)
        self.assertEqual(lev('', '1234', score_cutoff=-1.0), -1.0)
        self.assertEqual(osa('1234', '1234', score_cutoff=0), 0.0)
        self.assertEqual(osa('1234', '123', score_cutoff=0), 0.0)
        self.assertEqual(osa('1234', '1234', score_cutoff=-1.0), -1.0)
        self.assertEqual(dam_lev('', '', score_cutoff=0.0), 0.0)
        self.assertEqual(dam_lev('a', '', score_cutoff=0.0), 0.0)
        self.assertEqual(dam_lev('', 'a', score_cutoff=-1.0), -1.0)


class TestClevFasterWithCutoff(unittest.TestCase):

    def test_lev_performance(self):
        import time

        iterations = 100

        str1 = 'asdlajhfsdfjlsd' * 100
        str2 = 'uxcmtrocvbihirt' * 100

        start_time = time.time()

        for _ in range(iterations):
            lev(str1, str2, score_cutoff=5.0)

        time_with_cutoff = time.time() - start_time

        start_time = time.time()

        for _ in range(iterations):
            lev(str1, str2)
        
        time_without_cutoff = time.time() - start_time

        # At least 10x faster
        self.assertLess(time_with_cutoff, time_without_cutoff / 10)