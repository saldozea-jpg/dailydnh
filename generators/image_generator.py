import random
import string
import os

class ImageGenerator:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

    def generate_random_image(self):
        # Create an image with random pixels
        return [[random.randint(0, 255) for _ in range(self.width)] for _ in range(self.height)]

    def save_image(self, image, filename):
        with open(filename, 'w') as f:
            for row in image:
                f.write(' '.join(str(pixel) for pixel in row) + '\n')

# Example usage
if __name__ == '__main__':
    generator = ImageGenerator()
    img = generator.generate_random_image()
    generator.save_image(img, 'random_image.txt')