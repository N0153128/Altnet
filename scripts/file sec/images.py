from PIL import Image
import os
import unittest


'''

- large image files must be truncated to the maximum size of 1080p
- images smaller than 1080p can be ignored
- all images must contain a watermark
- image size cannot be larger than 8MB
- images can be as small as 16x16px

'''


class ImageTest(unittest.TestCase):

    @staticmethod
    def resolution_validator(picture):
        # this method ensures that the image is not larger than (1920 x 1080)
        max_size = (1920, 1080)
        with Image.open(picture) as img:
            if img.height <= max_size[0] or img.height <= max_size[1]:
                return True
            else:
                return False

    def test_resolution(self, picture):
        self.assertEqual(self.resolution_validator(picture), True, 'Resolution')

    @staticmethod
    def format_validator(picture):
        # this method ensures that the given file is an image
        with Image.open(picture) as img:
            if img.format == 'PNG' or img.format == 'JPEG':
                return True
            else:
                return False

    def test_format(self, picture):
        self.assertEqual(self.format_validator(picture), True, 'Format')

    @staticmethod
    def size_validator(picture):
        # this method ensures that the given image's size does not exceed 8MB
        if os.stat(picture).file_stats.st_size / 1024 * 1024 <= 8:
            return True
        else:
            return False

    def test_size(self, picture):
        self.assertEqual(self.size_validator(picture), True, 'Size')

    @staticmethod
    def main_validator():
        # runs a series of tests in order to ensure that the image corresponds to the standard
        unittest.main()


def watermarker(picture):
    # this method applies a watermark to the given image
    pass
