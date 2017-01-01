from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='pakalolo',
      version='0.0.1',
      description='A Public Key Infrastructure based on cross-referenced blockchains',
      long_description=readme,
      author='Marios Isaakidis',
      author_email='prometheas@autistici.org',
      url='https://github.com/misaakidis/pakalolo',
      license=license,
      packages=['pakalolo'],
      include_package_data=True,
      install_requires=[
          'Click',
      ],
      entry_points={
          'console_scripts': [
              'pakalolo = pakalolo.__main__:cli'
          ]
      }
      )