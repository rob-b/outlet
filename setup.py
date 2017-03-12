from setuptools import setup


setup(
    name='outlet',
    version='0.0.0',
    description='Playing with braintree',
    long_description=open('README.rst').read(),
    license='BSD',
    install_requires=['braintree', 'falcon', 'gunicorn', 'sumtypes', 'money',
                      'wsgi-request-logger', 'sqlalchemy', 'voluptuous',
                      'braintree', 'psycopg2'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=['outlet'],
    entry_points="""\
    [console_scripts]
    runoutlet = outlet.server:main
    createoutletdb = outlet.db:make_db
    """,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
    ]
)
