from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Reference Playback'
LONG_DESCRIPTION = 'Automate test cases using api call in SimplifyQA'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="reference_playback", 
        version=VERSION,
        author="Vanshika Agarwal",
        author_email="vanshika.agarwal2703@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['automation', 'simplifyQA'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)