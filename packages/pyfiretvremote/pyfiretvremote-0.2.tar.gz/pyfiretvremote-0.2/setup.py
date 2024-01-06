from setuptools import setup

version = '0.2'

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='pyfiretvremote',
    packages=['pyfiretvremote'],
    package_dir={'': 'src'},
    version=version,
    license='Apache 2.0',
    description='Remote control for FireTV',
    long_description=long_descr,
    long_description_content_type='text/markdown',
    author='foxy82',
    author_email='foxy82.github@gmail.com',
    url='https://github.com/designer-living/pyfiretvremote',
    download_url=f'https://github.com/designer-living/pyfiretvremote/archive/{version}.tar.gz',
    keywords=['FireTV', 'Remote'],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.10'
    ],
)
