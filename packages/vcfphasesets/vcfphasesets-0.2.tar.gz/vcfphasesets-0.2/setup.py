from setuptools import setup

setup(name='vcfphasesets',
    version='0.2',
    description='A python library to extract phase sets from a vcf file using pysam.',
    url='http://github.com/LUMC/vcfphasesets',
    author='Mark Santcroos',
    author_email='m.a.santcroos@lumc.nl',
    license='MIT',
    packages=['vcfphasesets'],
    zip_safe=False,
    install_requires=[
        'natsort',
        'pysam',
    ],
)
