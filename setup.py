from setuptools import setup

setup(
    name='AitiA',
    version='0.3.2',
    description='Testing python code for Starling detection project',
    author='Ferenc Nandor Janky & Attila Gombos',
    author_email='info@effective-range.com',
    packages=['example'],
    scripts=['client.py'],
    install_requires=['pytest',
                      'PyYAML>=6.0',
                      'pillow',
                      'pytz',
                      'paho-mqtt',
                      'numpy',
                      'pybase64',
                      'python-context-logger@git+https://github.com/EffectiveRange/python-context-logger.git@latest']
)
