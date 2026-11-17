import tempfile
import unittest
from pathlib import Path

from tablecheck.reader import InputError, read_csv


class ReaderTests(unittest.TestCase):
    def read(self, content):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.csv"
            path.write_bytes(content)
            return read_csv(path)

    def test_bom_quotes_newlines_and_crlf(self):
        self.assertEqual(self.read(b'\xef\xbb\xbfname,note\r\nA,"x,y\nnext"\r\n'),
                         (["name", "note"], [["A", "x,y\nnext"]]))

    def test_bad_inputs(self):
        for content in (b"", b"a,a\n", b"a, a\n", b" ,b\n", b"a,b\n1\n",
                        b'a\n"unterminated', b"a\n\xff", b"a\n\x00", b"a\n\n"):
            with self.subTest(content=content), self.assertRaises(InputError):
                self.read(content)

    def test_header_only(self):
        self.assertEqual(self.read(b"a,b\n"), (["a", "b"], []))
