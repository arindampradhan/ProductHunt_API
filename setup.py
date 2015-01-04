try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '1.0.0'

setup(
    name='ProductHunt',
    version=version,
    install_requires=['BeautifulSoup4>=4.3.1', 'requests'],
    author='Arindam Pradhan',
    author_email='arindampradhan10@gmail.com',
    packages=['ph'],
    license='MIT License',
    description='Python API for Product Hunt.',
    long_description='Unofficial Python API for Product Hunt. Usage: https://github.com/arindampradhan/ProductHunt_API.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)