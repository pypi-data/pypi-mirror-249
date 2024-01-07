from setuptools import setup

setup(
    name='paperplots',
    version='0.1.0',    
    description='Camera ready machine learning plots with a Tensorboard-like API',
    url='https://github.com/anishhdiwan/paperplots',
    author='Anish Abhijit Diwan',
    author_email='A.A.Diwan@student.tudelft.nl',
    license='MIT',
    packages=['paperplots'],
    install_requires=['matplotlib',
                      'numpy',                    
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.0',
    ],
)