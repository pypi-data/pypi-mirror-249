from setuptools import setup, find_packages

setup(
    name='mines_market',
    version='0.0.1',
    author='Yamato Matsumura, Keenan Buckley',
    author_email='matsumura.yamato@gmail.com, keenandbuckley@protonmail.com',
    description='Access sodexo api to retrieve menu for desired location',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)