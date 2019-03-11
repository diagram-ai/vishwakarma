# -*- coding: utf-8 -*-
'''Build visualization for a pgmpy model

Example:

Attributes:

Todo:

'''
import pgmpy
import jsonpickle
import pickle
import requests
import tempfile
import os
import random
import shutil
import string
import datetime
from IPython.display import Image


def pgmplot(obj, width=600):
    '''Build visualization for a pgmpy model

    Args:
        obj (pgmpy.models): The pgmpy model that needs to be visualized
        width (int): Width of the image in px (default 600)

    Returns:
        Image: The image that can be displayed inline in a Jupyter notebook
    '''
    # list of supported classes
    supp_classes = (pgmpy.models.BayesianModel,
                    pgmpy.models.NaiveBayes,
                    pgmpy.models.MarkovModel,
                    pgmpy.models.FactorGraph,
                    pgmpy.models.DynamicBayesianNetwork)

    if isinstance(obj, supp_classes):
        tmp_dir_name = ''
        try:
            # create a temp directory & temp file
            tmp_dir_name = tempfile.mkdtemp()
            # generate a tmp file name (excluding file extension)
            epoch = datetime.datetime.now().strftime('%s')
            tmp_file_name = ''.join(
                [random.choice(string.ascii_letters + string.digits) for n in range(8)])
            tmp_file_name = os.path.join(
                tmp_dir_name, tmp_file_name + epoch + '.png')
            tmp_pkl_file_name = os.path.join(
                tmp_dir_name, tmp_file_name + epoch + '.pkl')

            # serialize the object
            data = pickle.dumps(obj)

            url = 'http://api.diagram.ai/vishwakarma/pgmplot/'

            resp = requests.post(url,data=data,
                    headers={'Content-Type': 'application/octet-stream'})

            if(resp.ok):
                # get the image file and write it to temp dir
                if resp.headers.get('Content-Type') == 'image/png':
                    open(tmp_file_name, 'wb').write(resp.content)
                    # now return this image as an Image object displayable in
                    # the jupyter notebook
                    return Image(filename=tmp_file_name, width=width)
            else:
                raise Exception(resp.raise_for_status())

        finally:
            # cleanup the temp directory
            shutil.rmtree(tmp_dir_name, ignore_errors=True)

    else:
        raise TypeError(
            'Expected pgmpy modely; unsupported object type: ' +
            type(obj))
