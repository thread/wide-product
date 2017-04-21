import io

from setuptools import setup, find_packages


with io.open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='wide-product',
    version='0.0.1',
    url='https://github.com/thread/wide-product',
    description="Wide (partial Khatri-Rao) sparse matrix product",
    long_description=long_description,

    author="Thread Tech",
    author_email="tech@thread.com",

    keywords=(
        'numpy',
        'scipy',
        'matrix',
        'sparse',
        'khatri-rao',
        'product',
        'science',
        'feature',
        'courgette',
    ),
    license='MIT',

    zip_safe=False,

    packages=find_packages(),
    cffi_modules=['build_wide.py:ffibuilder'],

    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries',
    ),

    install_requires=(
        'numpy',
        'scipy',
    ),

    setup_requires=(
        'cffi >=1.10',
    ),

    tests_require=(
        'pytest',
        'hypothesis',
    ),
)
