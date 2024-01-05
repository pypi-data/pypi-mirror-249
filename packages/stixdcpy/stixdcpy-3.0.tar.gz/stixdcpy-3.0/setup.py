from setuptools import setup, find_packages

setup(
    name='stixdcpy',
    description='STIX data center APIs and data analysis tools',
    version='3.0',
    author='Hualin Xiao',
    author_email='hualin.xiao@fhnw.ch',
    long_description=open('README.md').read(),
    install_requires=['numpy', 'requests', 'python-dateutil', 'ipython',
                      'astropy', 'matplotlib','tqdm','pandas','joblib', 'roentgen', 'simplejson', 'sunpy','wget'],
    long_description_content_type='text/markdown',
    #packages=find_packages(where='stixdcpy'),
    url='https://github.com/i4ds/stixdcpy',
    packages=['stixdcpy'],
    python_requires='>=3.7'
)
