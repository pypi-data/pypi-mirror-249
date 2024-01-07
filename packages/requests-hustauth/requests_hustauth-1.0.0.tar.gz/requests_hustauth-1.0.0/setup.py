from setuptools import setup

with open('README.md','r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='requests_hustauth',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    description='HustPass support for Python-Requests',
    author='MarvinTerry',
    author_email='marvinterry2004@gmail.com',
    url='https://github.com/MarvinTerry/HustAuth',
    packages=['requests_hustauth'],
    license='MIT',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    install_requires=[
        'fake_useragent>=1.2.0',
        'Pillow>=10.0.0',
        'pycryptodome>=3.18.0',
        'Requests>=2.31.0',
        'numpy>=1.21.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)