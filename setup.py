from setuptools import setup

VERSION = "0.1"

setup(name="taciturn",
      version=VERSION,
      author="Derek Guenther",
      description="A turn order calculator for a Final Fantasy: Tactics tabletop RPG",
      url="https://github.com/t0asterb0t/taciturn",
      packages=["taciturn"],
      install_requires=([
          "xlrd"
      ])
      )

