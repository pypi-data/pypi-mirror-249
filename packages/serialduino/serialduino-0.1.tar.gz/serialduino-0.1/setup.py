from setuptools import setup

setup(
    name='serialduino',
    version='0.1',
    packages=['serialduino'],
    url='https://www.youtube.com/@DrasticLp',
    license='',
    author='drasticlp',
    author_email='tarikdu137@gmail.com',
    description='A simple serial based python library to control arduino with (or without) 74hc595 microprocessor',
    include_package_data=True,
    package_data={"": ["Serialduino.ino"]},
    install_requires=["pyserial>=3.5"]
)
