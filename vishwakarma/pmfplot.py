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
import string
from datetime import datetime
from IPython.display import Image

class pmfplot:
    ''' This class generates visualizations for discrete distributions '''

    def __init__(self):
        # setup the API endpoint to be called
        self.url = 'http://www.diagram.ai/api/vishwakarma/'
        self.endpoint = 'pmfplot'
        # default width of image to be displayed
        self.width = 600

    def bernoulli(k, p, width=600):
        '''
        Visualization for a Bernoulli distribution
        Args:
            k, p (float): parameters to a Bernoulli distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='bernoulli', k=k, p=p)

    def binomial(n, k, p, width=600):
        '''
        Visualization for a Binomial distribution
        Args:
            n, k, p (float): parameters to a Binomial distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='binomial', n=n, k=k, p=p)

    def geometric(n, p, width=600):
        '''
        Visualization for a Geometric distribution
        Args:
            n, p (float): parameters to a Geometric distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='geometric', n=n, p=p)

    def poisson(mu, e, x, width=600):
        '''
        Visualization for a Poisson distribution
        Args:
            mu, sigma (float): parameters to a Poisson distribution
        Returns:
            image (IPython.display.Image): The image that can be displayed inline in a Jupyter notebook
        '''
        self.width = width
        return call_post(dist='poisson', mu=mu, e=e, x=x)

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
