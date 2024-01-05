from setuptools import setup, find_packages

setup(
    name='EFCrud',
    version='1.0.1',
    description='API client for EFCrud',
    author='Devi Prakash',
    author_email='dprakash@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dprakash2101/AutomatePython',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    
)
