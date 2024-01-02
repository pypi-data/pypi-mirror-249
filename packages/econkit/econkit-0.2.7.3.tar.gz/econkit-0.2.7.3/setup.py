from setuptools import setup, find_packages

setup(
    name='econkit',
    version='0.2.7.3',
    packages=find_packages(),
    description='Advanced Econometric Analysis Tools',
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    long_description_content_type='text/markdown',
    author='Stefanos Stavrianos',
    author_email='contact@stefanstavrianos.eu',
    url='https://www.stefanstavrianos.eu/',
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'yfinance',
        'matplotlib'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ]
)

