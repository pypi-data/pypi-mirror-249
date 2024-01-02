from setuptools import setup, find_packages

setup(
    name='ElectricalWireSizes',
    version='0.1.31',
    url='https://electricalwiresizes.org/',
    project_urls={
        'Documentation': 'https://pyews.readthedocs.io/',
        'Source': 'https://github.com/jacometoss/PyEWS',
        'Funding': 'https://ko-fi.com/jacometoss',
        'Forum': 'https://k-denveloper.blogspot.com/',
        'Bug Tracker': 'https://github.com/jacometoss/PyEWS/issues',
        'Course': 'https://electricalwiresizes/courses',
    },    
    license='GPL-3.0',
    author='Marco Polo Jacome Toss',
    author_email='jacometoss@outlook.com',
    description='Module for dimensioning copper electrical conductors, feeder conductor and branch circuits ',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['electrical', 'conductor', 'size', 'electricalwiresizes','nom-001-sede-2012','branch','feeder','ElectricalWireSizes'],
    packages=find_packages(include=["electricalwiresizes"]),
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.5',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Utilities ',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    setup_requires=['wheel'],
    extras_require={
        'wheel': ['wheel']
    } 
)

