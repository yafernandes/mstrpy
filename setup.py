from distutils.core import setup

setup(name='mstrpy',
      version='0.1',
      description='MicroStrategy API for Python',
      author=['Alex Fernandes'],
      author_email=['afernandes@microstrategy.com'],
      packages=['mstrpy'],
      install_requires=[
          'requests',
          'pandas'
      ]
     )