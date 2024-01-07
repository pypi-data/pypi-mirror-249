from setuptools import setup, find_packages

setup(
    name='AmbuView',
    version='0.1.0',
    packages=find_packages(),
    description='A package for ambulance hub analysis with respect to population density',
    author='Tom J Owen, Helen Ahmed, Rushanai Lerssupsin',
    author_email='tjo206@exeter.ac.uk, ha567@exeter.ac.uk, rl645@exeter.ac.uk',
    url='https://github.com/Tjowen12345/AmbuView',
    install_requires=[
        'numpy==1.26.3',
        'osmnx==1.8.1',
        'networkx==3.2.1',
        'folium==0.15.1',
        'alphashape==1.3.1',
        'requests==2.31.0',
        'pandas==2.1.4',
        'geopandas==0.14.1',
        'shapely==2.0.2',
        'scipy==1.11.4',
        'setuptools==60.2.0',
        'scikit-learn==1.3.2',
        'geopy==2.4.1'
    ],
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent'],
    python_requires='>=3.10',
    include_package_data=True,
    package_data={
        'AmbuView': ['*.csv']
    }
)
