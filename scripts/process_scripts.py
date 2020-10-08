#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Date : 6 octobre 2020
"""

import PIL
import os
import sys
from kraken import binarization
from bs4 import BeautifulSoup


def binarize(directory, extension, new_extension, new_directory) -> None:
    """Function that binarizes images in a directory and save the new files
    in an other directory.
    :param directory: path to the directory where the images are located.
    :type directory: str
    :param extension: images' extension.
    :type extension: str
    :param new_extension: binarized images extension
    :type new_extension: str
    :param new_directory: path to the directory where the binarized images will be saved.
    :type new_directory: str
    :return: none
    """
    for file in os.listdir(directory):
        if file.endswith(extension):
            try:
                binarized = binarization.nlbin(PIL.Image.open(os.path.join(directory, file)))
            except PIL.UnidentifiedImageError:
                print('--//--> %s' % sys.exc_info()[1])
                continue
            except IsADirectoryError:
                print('--//--> %s' % sys.exc_info()[1])
                continue
            binarized = binarization.nlbin(PIL.Image.open(os.path.join(directory, file)))
            filename = file.replace(extension, new_extension)
            binarized.save(os.path.join(new_directory, filename))
            print("------> {} binarized !".format(os.path.join(directory, filename)))


def training_data(txt, html, page) -> None:
    """Function that takes a transcription file and put each line in the
    <li> tag of a Kraken's output.html document.
    :param txt: path to the file containing a transcription (one page)
    :param html: path to the kraken output.html
    :param page: value of @id in the <section> tag (page_x)
    :return: none
    """
    data = {}
    lines = [line.strip() for line in open(txt, "r")]
    with open(html, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
    segments = soup.find_all("section", {"id": page})
    for key, values in zip(segments[0].find_all("li"), lines):
        if len(segments[0].find_all("li")) != len(lines):
            print("Error : segments ({}) and lines ({}) are not equals !".format(
                len(segments[0].find_all("li")), len(lines)))
            break
        else:
            data[key] = values
    for tag in data:
        tag.string = data[tag]
    result = soup.prettify()
    with open(html, "w") as doc:
        doc.write(result)


def rename_file(directory, new_name) -> None:
    """Function that renames a set of files.
    :param directory: path to the directory where the files are located.
    :param new_name: common part of the new filenames.
    :return: none
    """
    for file in os.listdir(directory):
        old_f = os.path.join("/Volumes/GENERO_TNAH/training_data/109a_output_directory", file)
        new_f = os.path.join("/Volumes/GENERO_TNAH/training_data", new_name + file)
        os.rename(old_f, new_f)
        print("-----> {} renamed in {}".format(old_f, new_f))
