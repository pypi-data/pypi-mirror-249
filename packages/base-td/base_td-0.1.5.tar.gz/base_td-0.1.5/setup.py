from setuptools import setup, find_packages

setup(
    name='base_td',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            # Define any console scripts or command-line entry points here
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your package',
    url='https://github.com/your-username/your-package',
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
