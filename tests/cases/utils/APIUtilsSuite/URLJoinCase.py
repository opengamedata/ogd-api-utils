# import libraries
import unittest
from unittest import TestCase
# import ogd libraries.
from ogd.common.utils.Logger import Logger
# import locals
from src.ogd.apis.utils.APIUtils import urljoin

class URLJoinCase(TestCase):
    """Test case for the `urljoin` utility function.

    This is one of those weird cases where we've actually got standalone functions.
    They each get a 'case' for calling in a number of different ways.

    :param TestCase: _description_
    :type TestCase: _type_
    """
    def test_noslashes_noscheme(self):
        base = "ogd-services.fielddaylab.wisc.edu"
        loc  = "app.wsgi/path/to/endpoint"
        self.assertEqual(urljoin(base=base, url=loc), f"{base}/{loc}")

    def test_baseslash_noscheme(self):
        base = "ogd-services.fielddaylab.wisc.edu/"
        loc  = "app.wsgi/path/to/endpoint"
        self.assertEqual(urljoin(base=base, url=loc), f"{base[:-1]}/{loc}")

    def test_urlslash_noscheme(self):
        base = "ogd-services.fielddaylab.wisc.edu"
        loc  = "/app.wsgi/path/to/endpoint"
        self.assertEqual(urljoin(base=base, url=loc), f"{base}/{loc[1:]}")

    def test_bothslash_noscheme(self):
        base = "ogd-services.fielddaylab.wisc.edu/"
        loc  = "/app.wsgi/path/to/endpoint"
        self.assertEqual(urljoin(base=base, url=loc), f"{base[:-1]}/{loc[1:]}")
