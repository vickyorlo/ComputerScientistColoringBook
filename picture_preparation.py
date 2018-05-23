import os
import cv2
import random

from multiprocessing import Pool, cpu_count
from shutil import rmtree
from unidecode import unidecode


class PicturePreparation(object):

    def __init__(self, workers=1):
        self.workers = workers if workers else cpu_count()

    @staticmethod
    def prepare_images(path_to_source, path_to_destination, filename):
        """
        Saves each frame of a movie as a list of consecutive frames
        """

        if not os.path.exists('{}/{}'.format(path_to_destination,filename)):
            os.mkdir('{}/{}'.format(path_to_destination,filename))

        video = cv2.VideoCapture(os.path.join(path_to_source, filename))
        success = True
        index = 0
        while success:
            success, image = video.read()

            if success:
                resized = cv2.resize(image, (int(256), int(256)))
                cv2.imwrite("{}/{}/{}.png".format(path_to_destination,filename, index), resized)
            index += 1

        video.release()

    def process_all_movies(self, path_to_training, path_to_testing):
        # if os.path.exists('frames_from_movies'):
        #     rmtree('frames_from_movies')
        #     rmtree('test')

        if not os.path.exists('training_frames'):
            os.mkdir('training_frames')

        if not os.path.exists('testing_frames'):
            os.mkdir('testing_frames')

        files_in_training = os.listdir(path_to_training)

        os.chdir(path_to_training)
        [os.rename(filename, unidecode(filename)) for filename in files_in_training]
        os.chdir("..")
        os.listdir(path_to_training)

        function_input = [(path_to_training,'training_frames', filename) for filename in files_in_training if not 
                            os.path.exists('{}/{}'.format('training_frames',filename))]

        with Pool(processes=self.workers) as pool:
            pool.starmap_async(PicturePreparation.prepare_images, function_input)
            pool.close()
            pool.join()


        files_in_testing = os.listdir(path_to_testing)

        os.chdir(path_to_testing)
        [os.rename(filename, unidecode(filename)) for filename in files_in_testing]
        os.chdir("..")
        os.listdir(path_to_testing)

        function_input = [(path_to_testing,'testing_frames', filename) for filename in files_in_testing if not 
                            os.path.exists('{}/{}'.format('testing_frames',filename))]

        with Pool(processes=self.workers) as pool:
            pool.starmap_async(PicturePreparation.prepare_images, function_input)
            pool.close()
            pool.join()


if __name__ == "__main__":
    pp = PicturePreparation(workers=8)
    pp.process_all_movies('filmy','filmy2')
    