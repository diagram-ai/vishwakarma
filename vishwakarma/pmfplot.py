# -*- coding: utf-8 -*-
'''
Build visualizations for discrete distributions
    [Bernoulli, Binomial, Geometric, Poisson]

Example:
    from vishwakarma import pmfplot
    pmfplot.bernoulli(k, p)

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


class pmfplot:
    ''' This class generates visualizations for discrete distributions '''

    # setup the API endpoint to be called
    _url = 'http://api.diagram.ai/vishwakarma/'
    _endpoint = 'pmfplot/'
    # default width of image to be displayed
    _width = 600

    @classmethod
    def bernoulli(cls, k, p):
        '''
        Visualization for a Bernoulli distribution
        Args:
            k, p (float): parameters to a Bernoulli distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if k not in (0,1):
            raise ValueError('For a Bernoulli distribution, k should always be either 0 or 1.')
        if not 0 <= p <= 1:
            raise ValueError('For a Bernoulli distribution, p should always be between 0 and 1.')
        return cls._call_post(dist='bernoulli', k=k, p=p)

    @classmethod
    def binomial(cls, k, n, p):
        '''
        Visualization for a Binomial distribution
        Args:
            k, n, p (float): parameters to a Binomial distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if not isinstance(k, int):
            raise ValueError('For a Binomial distribution, k should always be an integer.')
        if not isinstance(n, int):
            raise ValueError('For a Binomial distribution, n should always be an integer.')
        if n < 0:
            raise ValueError('For a Binomial distribution, n should be greater than or equal to zero.')
        if not 0 <= k <= n:
            raise ValueError('For a Binomial distribution, k should always be between 0 and n.')
        if not 0 <= p <= 1:
            raise ValueError('For a Binomial distribution, p should always be between 0 and 1.')
        return cls._call_post(dist='binomial', k=k, n=n, p=p)

    @classmethod
    def geometric(cls, n, p):
        '''
        Visualization for a Geometric distribution
        Args:
            n, p (float): parameters to a Geometric distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if not isinstance(n, int):
            raise ValueError('For a Geometric distribution, n should always be an integer.')
        if n < 0:
            raise ValueError('For a Geometric distribution, n should be greater than or equal to zero.')
        if not 0 <= p <= 1:
            raise ValueError('For a Geometric distribution, p should always be between 0 and 1.')
        return cls._call_post(dist='geometric', n=n, p=p)

    @classmethod
    def poisson(cls, mu, x):
        '''
        Visualization for a Poisson distribution
        Args:
            mu, x (float): parameters to a Poisson distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        if not isinstance(x, int):
            raise ValueError('For a Poisson distribution, x should always be an integer.')
        if x < 0:
            raise ValueError('For a Poisson distribution, x should be greater than or equal to zero.')
        if mu <= 0:
            raise ValueError('For a Poisson distribution, mu should be greater than zero.')
        return cls._call_post(dist='poisson', mu=mu, x=x)

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
