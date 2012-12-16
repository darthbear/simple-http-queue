from setuptools import setup

setup(
    name='simple-http-queue',
    version='0.1.0',
    description='Simple HTTP queue implemented using Python, SQLite3 and Tornado',
    keywords='queue http sqlite python tornado',
    license='New BSD License',
    author="Francois Dang Ngoc",
    author_email='francois.dangngoc@gmail.com',
    url='http://github.com/darthbear/simple-http-queue/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    packages=[
        'simple_http_queue',
    ],
    install_requires=[
        'tornado',
        'sqlite3',
    ],
)
