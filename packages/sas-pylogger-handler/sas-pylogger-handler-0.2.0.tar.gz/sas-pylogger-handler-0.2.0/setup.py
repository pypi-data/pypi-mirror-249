from setuptools import setup

setup(
    name='sas-pylogger-handler',
    version='0.2.0',
    authors='Alfredo Lorie',
    author_email='a24lorie@gmail.com',
    description="""The SAS Python Logger Handler allows use the python logger system to send logging streams to SAS System logger""",
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    license='GNU',
    url='https://github.com/a24lorie/sas-pylogger-handler',
    install_requires=['saspy'],
    packages=[
        'sas_handler'
    ],
    package_dir={
        'sas_handler': 'src'
    }
)