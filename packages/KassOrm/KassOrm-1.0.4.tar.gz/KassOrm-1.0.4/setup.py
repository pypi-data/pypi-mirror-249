from setuptools import setup, find_packages

setup(
    name='KassOrm',
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python",'python-dotenv'
        ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={    },
    author='Kássio Douglas',
    author_email='kass.doug@gmail.com',
    description='Gerenciar banco de dados',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kassiodouglas/KassOrm',
    license='MIT',
)
