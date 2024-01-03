from setuptools import setup

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(name='batch_options_price',
      version='0.1',
      description='Batch Black-Scholes pricing European options on stocks without dividends',
      packages=['batch_options_price'],
      # Открытие README.md и присвоение его long_description.
      long_description=long_description,
      long_description_content_type="text/markdown",
      readme="README.md",
      author_email='filimoncevvv.anton@gmail.com',
      zip_safe=False)
