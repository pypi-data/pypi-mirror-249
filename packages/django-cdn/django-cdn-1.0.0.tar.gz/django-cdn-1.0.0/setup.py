import os

import setuptools

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setuptools.setup(
    name='django-cdn',
    version=os.getenv('PACKAGE_VERSION').split('/')[-1],
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='Django library that simplifies HTML imports of JS and CSS code with a NPM like command.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Arnau Casas Saez',
    author_email='casassarnau@gmail.com',  # SEE NOTE BELOW (*)
    url='https://github.com/Casassarnau/django-cdn',
    license='MIT',
    python_requires='>=3.6',
    project_urls={
        "Bug Tracker": "https://github.com/Casassarnau/django-cdn/issues",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'django>=2.2',
        'semver',
        'requests'
    ]
)

# (*) Please direct queries to the discussion group, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
