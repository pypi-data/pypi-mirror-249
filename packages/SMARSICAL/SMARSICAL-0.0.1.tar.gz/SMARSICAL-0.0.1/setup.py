from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='SMARSICAL',
    version='0.0.1',
    description='RSI and SMA calculator',
    long_description=open('Readme.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Emre Efe Kurt',
    author_email='emre_efe_krt@hotmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords="CALCULATOR,RSI,SMA",
    packages=find_packages(),
    install_requires=['']
)

