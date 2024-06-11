from setuptools import setup, find_packages

setup(
    name='aicli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'openai',
        'requests',
        # Add other dependencies as needed
    ],
    entry_points={
        'console_scripts': [
            'aicli=aicli.cli:cli',
        ],
    },
    author='Paravjot Singh',
    author_email='4sdserver@gmail.com',
    description='AI-driven Kubernetes CLI assistant',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/singhparavjot/aicli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

