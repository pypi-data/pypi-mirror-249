from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='rainbowio',
    version='0.0.1',
    license='MIT License',
    author='José Henrique',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='josepicoli42@gmail.com',
    keywords='rainbowio',
    description=u'Simple pytohn library to make your cli programs more beautiful by adding colors to input and output functions',
    packages=['rainbowio'],
    install_requires=[],)
