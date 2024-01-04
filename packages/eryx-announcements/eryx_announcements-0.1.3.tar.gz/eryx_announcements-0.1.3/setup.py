from setuptools import setup, find_packages

setup(
    name='eryx_announcements',
    version='0.1.3',
    author='Eryx Team',
    author_email='info@eryx.co',
    license='MIT',
    description='A small package to handle announcements in your application.',
    url='https://github.com/eryxcoop/announcements',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development',
    ],
    python_requires='>=3.5',
)
