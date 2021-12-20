from challenge import Challenge
import numpy as np
import scipy.ndimage as ndimage

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Initialise result
        result = list()

        # Load data from path
        with open(path) as infile:
            # Load data
            enhancement_image, image = infile.read().split('\n\n')
            # Load enhancement image
            enhancement_image = np.asarray(list(
                enhancement_image.replace('\n', '')
            ))

            # Load image
            image = np.asarray([list(row) for row in image.split('\n') if row])

        # Return result
        return enhancement_image, image

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Unpack data
        enhancement_image, image = data

        # Perform enhancement
        image = self.enhance(enhancement_image, image)
        image = self.enhance(enhancement_image, image,
            zeros = enhancement_image[0] == "."
        )

        # Count number of lit pixels
        return np.sum(image == '#')


    def part_2(self, data):
        # Unpack data
        enhancement_image, image = data

        for i in range(50):
            image = self.enhance(
                enhancement_image,
                image,
                zeros = (enhancement_image[0] == "." or i&1 == 0),
            )

        # Count number of lit pixels
        return np.sum(image == '#')

    ########################################################################
    #                             Apply filter                             #
    ########################################################################

    def enhance(self, enhancement_image, image, zeros=True):
        # Transform to boolean array
        image = (image == '#').astype(bool)

        # Enhance image
        if zeros:
            large = np.zeros((image.shape[0]+4, image.shape[1]+4), dtype=bool)
        else:
            large = np.ones((image.shape[0]+4, image.shape[1]+4), dtype=bool)

        large[2:-2, 2:-2] = image

        # Initialise large image
        squares = np.lib.stride_tricks.sliding_window_view(large, (3, 3))
        squares = squares.reshape((image.shape[0] + 2, image.shape[1] + 2, -1))

        # Transform squares to indices
        indices = np.zeros((image.shape[0] + 2, image.shape[1] + 2), dtype=int)
        for index in range(squares.shape[-1]):
            indices += squares[:,:,index] << (8-index)

        # Get image
        image = enhancement_image[indices]

        # Return new image
        return image
