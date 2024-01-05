from setuptools import setup, find_packages

setup(
    name='annxuncements',
    version='0.0.1',
    author='Eryx Team',
    author_email='info@eryx.co',
    license='MIT',
    description='A small package to handle announcements in your application.',
    url='https://github.com/eryxcoop/announcements',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        'Topic :: Software Development',
    ],
    python_requires='>=3.5',
)
