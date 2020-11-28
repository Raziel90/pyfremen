from setuptools import setup

setup(
    name='pyfremen',
    version='0.1',
    description='Fast Python implementation of the FreMEn model',
    long_description='Fast Python implementation of the FreMEn model implemented in https://github.com/gestom/fremen'
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Time series analysis',
      ],
    url='http://github.com/Raziel90/pyfremen',
    author='Claudio Coppola',
    author_email='claudiocoppola90@gmail.com',
    license='MIT',
    packages=['fremen'],
    install_requires=['numpy']
    zip_safe=False
)