from setuptools import setup


def readme():
    with open('README.rst', "r", encoding="utf8") as f:
        return f.read()


setup(
    name='tfrq',
    version='2.0.95',
    description='A library to parallelize the execution of a function in Python',
    long_description=readme(),
    long_description_content_type='text/x-rst',
    author='Foad Abo Dahood',
    author_email='Foad.ad5491@gmail.com',
    license='MIT',
    py_modules=['tfrq'],
    install_requires=[
        'tqdm'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
