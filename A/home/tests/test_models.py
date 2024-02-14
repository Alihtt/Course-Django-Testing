from django.test import TestCase
from home.models import Writer
from model_bakery import baker


class TestWriterModel(TestCase):
    def setUp(self):
        """Run before methods"""
        self.writer = baker.make(Writer, first_name='ali', last_name='ht')

    def test_writer_str(self):
        self.assertEqual(str(self.writer), 'ali ht')
