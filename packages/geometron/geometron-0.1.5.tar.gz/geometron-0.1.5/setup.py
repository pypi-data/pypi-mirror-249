# setup.py
from setuptools import setup

project_name = 'geometron'

readme_file = open('./README.md', "r")
readme = readme_file.read()
readme_file.close()

setup(setup_requires=["pbr"], pbr=True, long_description=readme, long_description_content_type='text/markdown',
      install_requires=[
          "matplotlib >2.2.0",
          "numpy>=1.15.1, <2.0.0",
          "pandas",
          "geopandas",
          "scipy",
          "shapely",
          "pyvista",
          "descartes",
          "pillow",
          "requests",
          "pyparsing<3",
          "rasterio",
          "svgpath2mpl",
          "svgpathtools",
          "rasterio",
          "svgpath2mpl",
      ])
