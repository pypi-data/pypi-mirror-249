from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='paperplots',
    version='0.2.0',    
    description='Camera ready machine learning plots with a Tensorboard-like API',
    long_description=long_description,
    long_description_content_type='text/markdown',
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