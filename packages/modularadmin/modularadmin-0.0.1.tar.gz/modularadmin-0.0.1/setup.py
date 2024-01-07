from setuptools import setup, find_packages

setup(
    name='modularadmin',
    version='0.0.1',
    description='PoC',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/sjnscythe',
    author='scythe abhi',
    author_email='scytheabhi97@gmail.com',
    license='MIT',
    keywords='PoC',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
