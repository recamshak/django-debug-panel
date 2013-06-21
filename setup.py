# coding: utf-8
from distutils.core import setup

setup(
    name='django-debug-panel',
    version='0.5.2',
    author='Joël Billaud',
    author_email='jbillaud@gmail.com',
    packages=['debug_panel'],
    url='https://github.com/recamshak/django-debug-panel',
    license='BSD',
    description='django-debug-toolbar in WebKit DevTools. Works fine with background Ajax requests and non-HTML responses',
    long_description=open('README.rst').read(),
    install_requires=[
        "django-debug-toolbar >= 0.9.0"
    ],
)
