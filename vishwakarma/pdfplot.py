# -*- coding: utf-8 -*-
'''Build visualization for continuous distributions

Example:

Attributes:

Todo:

'''
import requests
import tempfile
import os
import string
from datetime import datetime
from IPython.display import Image


def pdfplot(dist, width=600, **kwargs):
    '''Build visualization for continuous distributions

    Args:
        dist (str): The continuous distribution that needs to be visualized
                    ['uniform', 'gaussian', 'exponential', 'gamma']
        width (int): Width of the image in px (default 600)
        **kwargs: dist == 'uniform': 'a' & 'b'
                  dist == 'gaussian': 'mu' & 'sigma'
                  dist == 'exponential': 'lambda'
                  dist == 'gamma': 'alpha' & 'beta'

    Returns:
        Image: The image that can be displayed inline in a Jupyter notebook
    '''
    if dist == 'uniform':
        if 'a' in kwargs:
            _a = kwargs.get('a')
        else:
            raise ValueError('Missing argument \'a\'\nUsage: pdfplot(dist=\'uniform\', a=<val>, b=<val>)')
        if 'b' in kwargs:
            _b = kwargs.get('b')
        else:
            raise ValueError('Missing argument \'b\'\nUsage: pdfplot(dist=\'uniform\', a=<val>, b=<val>')
        return _call_post(dist, _a, _b)
    elif dist == 'gaussian':
        if 'mu' in kwargs:
            _mu = kwargs.get('mu')
        else:
            raise ValueError('Missing argument \'mu\'\nUsage: pdfplot(dist=\'gaussian\', mu=<val>, sigma=<val>')
        if 'sigma' in kwargs:
            _sigma = kwargs.get('sigma')
        else:
            raise ValueError('Missing argument \'sigma\'\nUsage: pdfplot(dist=\'gaussian\', mu=<val>, sigma=<val>')
        return _call_post(dist, _mu, _sigma)
    elif dist == 'exponential':
        if 'lambda' in kwargs:
            _lambda = kwargs.get('lambda')
        else:
            raise ValueError('Missing argument \'lambda\'\nUsage: pdfplot(dist=\'exponential\', lambda=<val>')
        return _call_post(dist, _lambda)
    elif dist == 'gamma':
        if 'alpha' in kwargs:
            _alpha = kwargs.get('alpha')
        else:
            raise ValueError('Missing argument \'alpha\'\nUsage: pdfplot(dist=\'gamma\', alpha=<val>, beta=<val>')
        if 'beta' in kwargs:
            _beta = kwargs.get('beta')
        else:
            raise ValueError('Missing argument \'beta\'\nUsage: pdfplot(dist=\'gamma\', alpha=<val>, beta=<val>')
        return _call_post(dist, _alpha, _beta)
    else:
        raise ValueError('Unsupported value for argument \'dist\'')

    def _call_post(**kwargs):
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

            url = 'http://www.diagram.ai/api/vishwakarma/pdfplot'
            resp = requests.post(url, data=kwargs)

            if(resp.ok):
                # get the image file and write it to temp dir
                if resp.headers.get('Content-Disposition'):
                    open(tmp_file_name, 'wb').write(resp.content)

                    # now return this image as an Image object displayable in
                    # the jupyter notebook
                    return Image(filename=tmp_file_name, width=width)
            else:
                raise Exception(resp.raise_for_status())

        finally:
            # cleanup the temp directory
            shutil.rmtree(tmp_dir_name, ignore_errors=True)
