from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'etlassist is a python package supporting ETL operations'
LONG_DESCRIPTION = 'etlassist can be used with general python and the functions used can also be extended as UDF for the databricks opertaions.'

# Setting up
setup(
    name="etlassist",
    version=VERSION,
    author="Gokul Kumar Jayaram",
    author_email="<gokulkumar.jayaram@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['lxml'],
    keywords=['python', 'etlassist', 'packaging' , 'etl operations' , 'databricks'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)