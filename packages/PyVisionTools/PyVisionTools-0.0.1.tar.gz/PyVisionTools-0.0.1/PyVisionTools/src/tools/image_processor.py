import io
import math
from typing import List, Tuple
import urllib.request
import struct
import array

class ImageProcessor:
    def __init__(self):
        pass

    def open_image_from_url(self, image_url):
        try:
            with urllib.request.urlopen(image_url) as response:
                width, height = struct.unpack("<LL", response.read(8))

                pixels = array.array("B", response.read())

            return width, height, pixels
        except Exception as e:
            print(f"Error opening image from URL: {e}")
            return None

    def process_image(self, width, height, pixels, grayscale=False):
        try:
            if grayscale:
                pixels = self.convert_to_grayscale(width, height, pixels)


            return width, height, pixels
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def save_image_to_bytes(self, width, height, pixels):
        try:
            bmp_header = struct.pack("<ccLLL", b'B', b'M', 54 + len(pixels), 0, 54)

            image_bytes = array.array("B", bmp_header)
            image_bytes.extend(pixels)

            return image_bytes.tobytes()
        except Exception as e:
            print(f"Error saving image to bytes: {e}")
            return None

    def convert_to_grayscale(self, width, height, pixels):
        for i in range(0, len(pixels), 3):
            gray_value = int(0.299 * pixels[i] + 0.587 * pixels[i + 1] + 0.114 * pixels[i + 2])
            pixels[i], pixels[i + 1], pixels[i + 2] = gray_value, gray_value, gray_value

        return pixels

def resize_image(self, width, height, pixels, new_width, new_height):
  try:
      resized_pixels = array.array("B")

      for y in range(new_height):
          for x in range(new_width):
              source_x = int(x / new_width * width)
              source_y = int(y / new_height * height)

              pixel_index = (source_y * width + source_x) * 3
              resized_pixels.extend(pixels[pixel_index:pixel_index + 3])

      return new_width, new_height, resized_pixels
  except Exception as e:
      print(f"Error resizing image: {e}")
      return None

def rotate_image(self, angle):
  rotated_data = self.rotate_array(self.data, angle)
  self.data = rotated_data

def rotate_array(self, image_data, angle) -> List[List[Tuple[int, int, int]]]:
  rad_angle = math.radians(angle)
  cos_angle = math.cos(rad_angle)
  sin_angle = math.sin(rad_angle)

  rotated_data = [
      [
          (
              round(x * cos_angle - y * sin_angle),
              round(x * sin_angle + y * cos_angle),
              z
          )
          for x, y, z in row
      ]
      for row in image_data
  ]

  return rotated_data

def crop_image(self, width, height, pixels, left, top, right, bottom):
  try:
      cropped_width = right - left
      cropped_height = bottom - top
      cropped_pixels = array.array("B")

      for y in range(top, bottom):
          for x in range(left, right):
              pixel_index = (y * width + x) * 3
              cropped_pixels.extend(pixels[pixel_index:pixel_index + 3])

      return cropped_width, cropped_height, cropped_pixels
  except Exception as e:
      print(f"Error cropping image: {e}")
      return None