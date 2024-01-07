from setuptools import setup, find_packages


setup(
    name="AbdoDataPrepKit",
    version='0.1',
    author="abdelrahman mahmoud",
    author_email="abdelrahman.mahmoud355@gmail.com",
    description="Description",
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'Data Reading', 'Data Summary',
              'Handling Missing Values', 'Categorical Data Encoding', ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
