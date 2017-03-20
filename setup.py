from setuptools import setup, find_packages

setup(name='maraproto',
      version='0.1.0',
      description='Simple package for analyzing and altering Marathon protobufs'
                  'stored on ZooKeeper, use with caution',
      author='Mateusz Moneta',
      author_email='mateuszmoneta@gmail.com',
      packages=find_packages(),
      install_requires=[
          'click>6,<7',
          'kazoo>2.2,<2.3',
          'protobuf==2.6',
      ],
      entry_points={
          'console_scripts': ['maraproto = maraproto.main:main']
      },
      zip_safe=False,
      )
