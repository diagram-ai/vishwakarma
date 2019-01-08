# -*- coding: utf-8 -*-
'''Build visualization for discrete distributions

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


def pmfplot(dist, width=600, **kwargs):
    '''Build visualization for discrete distributions

    Args:
        dist (str): The discrete distribution that needs to be visualized
                    ['bernoulli', 'binomial', 'geometric', 'poisson']
        width (int): Width of the image in px (default 600)
        **kwargs: dist == 'bernoulli': 'k' & 'p'
                  dist == 'binomial': 'n', 'k' & 'p'
                  dist == 'geometric': 'n' & 'p'
                  dist == 'poisson': 'mu', 'e' & 'x'

    Returns:
        Image: The image that can be displayed inline in a Jupyter notebook
    '''
    if dist == 'bernoulli':
        if 'k' in kwargs:
            _k = kwargs.get('k')
        else:
            raise ValueError('Missing argument \'k\'\nUsage: pmfplot(dist=\'bernoulli\', k=<val>, p=<val>)')
        if 'p' in kwargs:
            _p = kwargs.get('p')
        else:
            raise ValueError('Missing argument \'p\'\nUsage: pmfplot(dist=\'bernoulli\', k=<val>, p=<val>')
        return _call_post(dist, _k, _p)
    elif dist == 'binomial':
        if 'n' in kwargs:
            _n = kwargs.get('n')
        else:
            raise ValueError('Missing argument \'n\'\nUsage: pmfplot(dist=\'binomial\', n=<val>, k=<val>, p=<val>)')
        if 'k' in kwargs:
            _k = kwargs.get('k')
        else:
            raise ValueError('Missing argument \'k\'\nUsage: pmfplot(dist=\'binomial\', n=<val>, k=<val>, p=<val>)')
        if 'p' in kwargs:
            _p = kwargs.get('p')
        else:
            raise ValueError('Missing argument \'p\'\nUsage: pmfplot(dist=\'binomial\', n=<val>, k=<val>, p=<val>')
        return _call_post(dist, _n, _k, _p)
    elif dist == 'geometric':
        if 'n' in kwargs:
            _n = kwargs.get('n')
        else:
            raise ValueError('Missing argument \'n\'\nUsage: pmfplot(dist=\'geometric\', n=<val>, p=<val>)')
        if 'p' in kwargs:
            _p = kwargs.get('p')
        else:
            raise ValueError('Missing argument \'p\'\nUsage: pmfplot(dist=\'geometric\', n=<val>, p=<val>')
        return _call_post(dist, _n, _p)
    elif dist == 'poisson':
        if 'mu' in kwargs:
            _mu = kwargs.get('mu')
        else:
            raise ValueError('Missing argument \'mu\'\nUsage: pmfplot(dist=\'poisson\', mu=<val>, e=<val>, x=<val>')
        if 'e' in kwargs:
            _e = kwargs.get('e')
        else:
            raise ValueError('Missing argument \'e\'\nUsage: pmfplot(dist=\'poisson\', mu=<val>, e=<val>, x=<val>')
        if 'x' in kwargs:
            _x = kwargs.get('x')
        else:
            raise ValueError('Missing argument \'x\'\nUsage: pmfplot(dist=\'poisson\', mu=<val>, e=<val>, x=<val>')
        return _call_post(dist, _mu, _e, _x)
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

            url = 'http://www.diagram.ai/api/vishwakarma/pmfplot'
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
