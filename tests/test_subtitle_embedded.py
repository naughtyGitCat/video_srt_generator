# 20240313
import unittest
from utils.file import subtitle_embedded


class TestSubtitleEmbedded(unittest.TestCase):

    def test_no_embedded(self):
        self.assertFalse(subtitle_embedded("/root/ffmpeg/test/mkv"))

    def test_embedded(self):
        pass
