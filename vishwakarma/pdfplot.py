# -*- coding: utf-8 -*-
'''
Build visualizations for continuous distributions
    [Uniform, Gaussian, Exponential, Gamma]

Example:
    from vishwakarma import pdfplot
    pdfplot.gaussian(mu, sigma)

Attributes:

Todo:

'''
import requests
import tempfile
import os
import random
import shutil
import string
import datetime
from IPython.display import Image


class pdfplot:
    ''' This class generates visualizations for continuous distributions '''

    # setup the API endpoint to be called
    _url = 'http://api.diagram.ai/vishwakarma/'
    _endpoint = 'pdfplot/'
    # default width of image to be displayed
    _width = 600

    @classmethod
    def uniform(cls, a, b):
        '''
        Visualization for a Uniform distribution
        Args:
            a, b (int): parameters to a Uniform distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if not isinstance(a, int):
            raise ValueError('For a Uniform distribution, a should always be an integer.')
        if not isinstance(b, int):
            raise ValueError('For a Uniform distribution, b should always be an integer.')
        if b <= a:
            raise ValueError('For a Uniform distribution, b should always be greater than a.')
        return cls._call_post(dist='uniform', a=a, b=b)
            

    @classmethod
    def gaussian(cls, mu, sigma):
        '''
        Visualization for a Gaussian distribution
        Args:
            mu, sigma (float): parameters to a Gaussian distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if sigma <= 0:
            raise ValueError('For a Gaussian distribution, sigma should be greater than zero.')
        return cls._call_post(dist='gaussian', mu=mu, sigma=sigma)

    @classmethod
    def exponential(cls, lam):
        '''
        Visualization for an Exponential distribution
        Args:
            lam (float): parameter to an Exponential distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if lam <= 0:
            raise ValueError('For an Exponential distribution, lambda should be greater than zero.')
        return cls._call_post(dist='exponential', lam=lam)

    @classmethod
    def gamma(cls, alpha, beta):
        '''
        Visualization for a Gamma distribution
        Args:
            alpha, beta (float): parameters to a Gamma distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if alpha <= 0:
            raise ValueError('For a Gamma distribution, alpha should be greater than zero.')
        if beta <= 0:
            raise ValueError('For a Gamma distribution, beta should be greater than zero.')
        return cls._call_post(dist='gamma', alpha=alpha, beta=beta)

    @classmethod
    def _call_post(cls, **kwargs):
        '''
        Calls the API hosted on www.diagram.ai
        Args:
            kwargs: Name and parameters of the distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        Note:
            Internal function - not to be exposed
        '''
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

            # make the call ...
            resp = requests.post(cls._url + cls._endpoint, json=kwargs)

            if(resp.ok):
                # get the image file and write it to temp dir
                if resp.headers.get('Content-Type') == 'image/png':
                    open(tmp_file_name, 'wb').write(resp.content)
                    # now return this image as an Image object displayable in a
                    # Jupyter notebook
                    return Image(filename=tmp_file_name, width=cls._width)
            else:
                raise Exception(resp.raise_for_status())
        finally:
            # cleanup the temp directory
            shutil.rmtree(tmp_dir_name, ignore_errors=True)
