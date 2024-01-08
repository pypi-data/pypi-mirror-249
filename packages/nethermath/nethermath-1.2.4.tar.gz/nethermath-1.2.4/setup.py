from setuptools import setup

setup(
    name='nethermath',
    version='1.2.4',
    py_modules=['nethermath'],
    install_requires=[
        'numpy',
        'colorama',
        'scipy',
        'statistics',
        'cryptography',
        'forex_python',
        'requests',
        'datetime',
        'ipaddress',
    ],
    entry_points={
        'console_scripts': [
            'nethermath = nethermath:main',  
        ],
    },
    description= 'Calculator with a sophisticated concepts.',
    long_description=open('README.md').read(),  # Provide README for PyPI
    long_description_content_type='text/markdown',
    author='Saphiraaa',
    author_email='fredmarkivand@gmail.com',
    url='https://github.com/saphiraaa/NetherMath',
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add more classifiers as needed
    ],
)

