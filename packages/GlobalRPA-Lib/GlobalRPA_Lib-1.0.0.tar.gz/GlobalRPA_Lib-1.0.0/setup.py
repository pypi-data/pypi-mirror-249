from setuptools import setup

with open('README.md', 'r') as file:
    readme = file.read()

setup(
    name='GlobalRPA_Lib',
    version='1.0.0',
    license='MIT License',
    author='Mateus Orlandin Dias',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mateus.orlandin@gmail.com',
    keywords='RPA activities',
    description=u'Library RPA Python',
    packages=['email','file', 'selector'],
    install_requires=['secure-smtplib']
)