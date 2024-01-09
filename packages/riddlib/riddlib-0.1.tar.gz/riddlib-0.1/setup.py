from setuptools import find_packages, setup

classifiers = [
   'Development Status :: 5 - Production/Stable',
   'Intended Audience :: Education',
   'Operating System :: Microsoft :: Windows :: Windows 11',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3'
]

setup(
   name='riddlib',
   version='0.1',
   description= 'For Personal Use',
   author='Riddhiman',
   author_email='riddhimanadhikari2007@gmail.com',
   license='MIT',
   classifiers=classifiers,
   packages=find_packages(
    where='src',
    include=['mypackage'],
),
   install_requires=['']
)