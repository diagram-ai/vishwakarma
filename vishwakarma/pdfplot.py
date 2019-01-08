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
import string
from datetime import datetime
from IPython.display import Image

class pdfplot:
    ''' This class generates visualizations for continuous distributions '''

    def __init__(self):
        # setup the API endpoint to be called
        self.url = 'http://www.diagram.ai/api/vishwakarma/'
        self.endpoint = 'pdfplot'
        # default width of image to be displayed
        self.width = 600

    def uniform(a, b, width=600):
        '''
        Visualization for a Uniform distribution
        Args:
            a, b (float): parameters to a Uniform distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='uniform', a=a, b=b)

    def gaussian(mu, sigma, width=600):
        '''
        Visualization for a Gaussian distribution
        Args:
            mu, sigma (float): parameters to a Gaussian distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='gaussian', mu=mu, sigma=sigma)

    def exponential(lambda, width=600):
        '''
        Visualization for an Exponential distribution
        Args:
            lambda (float): parameters to an Exponential distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='exponential', lambda=lambda)

    def gamma(alpha, beta, width=600):
        '''
        Visualization for a Gamma distribution
        Args:
            alpha, beta (float): parameters to a Gamma distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='gamma', alpha=alpha, beta=beta)

    def call_post(**kwargs):
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
            resp = requests.post(self.url+self.endpoint, data=kwargs)

            if(resp.ok):
                # get the image file and write it to temp dir
                if resp.headers.get('Content-Disposition'):
                    open(tmp_file_name, 'wb').write(resp.content)

                    # now return this image as an Image object displayable in a Jupyter notebook
                    return Image(filename=tmp_file_name, width=self.width)
            else:
                raise Exception(resp.raise_for_status(), kwargs)
        finally:
            # cleanup the temp directory
            shutil.rmtree(tmp_dir_name, ignore_errors=True)
