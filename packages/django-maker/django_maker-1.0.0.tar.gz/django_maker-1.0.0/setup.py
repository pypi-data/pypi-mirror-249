# setup.py

from setuptools import setup, find_packages

setup(
    name='django_maker',
    version='1.0.0',
    description='A Python package for managing framework django',
    long_description='''This package provides tools for create app, models, serializer and CRUD.

    To use this package, you must first install it using pip:

    ```bash
    pip install django_maker
    ```

    ## Usage

     # to create app 
     
        python manage.py createapp and follow the steps
        
     # to create models 
     
        python manage.py create_models and follow the steps
        
     # to create serializer 
     
        python manage.py create_serializer and follow the steps
        
     # to create create simple CRUD 
     
        python manage.py create_simple_CRUD 
                    
    ```

    ...

    ''',
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        'django_maker': ['management/commands/*'],
    },
    install_requires=[
        'Django>=3.0',
    ],
)
