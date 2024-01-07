# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openjpeg', 'openjpeg.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24,<2.0']

entry_points = \
{'pylibjpeg.jpeg_2000_decoders': ['openjpeg = openjpeg:decode'],
 'pylibjpeg.pixel_data_decoders': ['1.2.840.10008.1.2.4.201 = '
                                   'openjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.202 = '
                                   'openjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.203 = '
                                   'openjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.90 = '
                                   'openjpeg:decode_pixel_data',
                                   '1.2.840.10008.1.2.4.91 = '
                                   'openjpeg:decode_pixel_data']}

setup_kwargs = {
    'name': 'pylibjpeg-openjpeg',
    'version': '2.0.0',
    'description': 'A Python wrapper for openjpeg, with a focus on use as a plugin for for pylibjpeg',
    'long_description': '<p align="center">\n<a href="https://github.com/pydicom/pylibjpeg-openjpeg/actions?query=workflow%3Aunit-tests"><img alt="Build status" src="https://github.com/pydicom/pylibjpeg-openjpeg/workflows/unit-tests/badge.svg"></a>\n<a href="https://codecov.io/gh/pydicom/pylibjpeg-openjpeg"><img alt="Test coverage" src="https://codecov.io/gh/pydicom/pylibjpeg-openjpeg/branch/main/graph/badge.svg"></a>\n<a href="https://pypi.org/project/pylibjpeg-openjpeg/"><img alt="PyPI versions" src="https://img.shields.io/pypi/v/pylibjpeg-openjpeg"></a>\n<a href="https://www.python.org/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/pylibjpeg-openjpeg"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n\n## pylibjpeg-openjpeg\n\nA Python 3.8+ wrapper for\n[openjpeg](https://github.com/uclouvain/openjpeg), with a focus on use as a plugin for [pylibjpeg](http://github.com/pydicom/pylibjpeg).\n\nLinux, OSX and Windows are all supported.\n\n### Installation\n#### Dependencies\n[NumPy](http://numpy.org)\n\n#### Installing the current release\n```bash\npython -m pip install -U pylibjpeg-openjpeg\n```\n\n#### Installing the development version\n\nMake sure [Python](https://www.python.org/), [Git](https://git-scm.com/) and [CMake](https://cmake.org/) are installed. For Windows, you also need to install\n[Microsoft\'s C++ Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16).\n```bash\ngit clone --recurse-submodules https://github.com/pydicom/pylibjpeg-openjpeg\npython -m pip install pylibjpeg-openjpeg\n```\n\n\n### Supported JPEG Formats\n#### Decoding\n\n| ISO/IEC Standard | ITU Equivalent | JPEG Format |\n| --- | --- | --- |\n| [15444-1](https://www.iso.org/standard/78321.html) | [T.800](https://www.itu.int/rec/T-REC-T.800/en) | [JPEG 2000](https://jpeg.org/jpeg2000/) |\n\n#### Encoding\nEncoding of JPEG 2000 images is not currently supported\n\n\n### Transfer Syntaxes\n| UID | Description |\n| --- | --- |\n| 1.2.840.10008.1.2.4.90 | JPEG 2000 Image Compression (Lossless Only) |\n| 1.2.840.10008.1.2.4.91 | JPEG 2000 Image Compression |\n| 1.2.840.10008.1.2.4.201 | High-Throughput JPEG 2000 Image Compression (Lossless Only) |\n| 1.2.840.10008.1.2.4.202 | High-Throughput JPEG 2000 with RPCL Options Image Compression (Lossless Only) |\n| 1.2.840.10008.1.2.4.203 | High-Throughput JPEG 2000 Image Compression |\n\n\n### Usage\n#### With pylibjpeg and pydicom\n\n```python\nfrom pydicom import dcmread\nfrom pydicom.data import get_testdata_file\n\nds = dcmread(get_testdata_file(\'JPEG2000.dcm\'))\narr = ds.pixel_array\n```\n\n#### Standalone JPEG decoding\n\nYou can also decode JPEG 2000 images to a [numpy ndarray][1]:\n\n[1]: https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html\n\n```python\nfrom openjpeg import decode\n\nwith open(\'filename.j2k\', \'rb\') as f:\n    # Returns a numpy array\n    arr = decode(f)\n\n# Or simply...\narr = decode(\'filename.j2k\')\n```\n',
    'author': 'pylibjpeg-openjpeg contributors',
    'author_email': 'None',
    'maintainer': 'scaramallion',
    'maintainer_email': 'scaramallion@users.noreply.github.com',
    'url': 'https://github.com/pydicom/pylibjpeg-openjpeg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
