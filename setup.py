from setuptools import setup

setup(
    name='flaskBird',
    version='1.0',
    long_description=__doc__,
    packages=['flaskBird'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    setup_requires=['libsass >= 0.6.0'],
    sass_manifests={
        'flaskBird': ('static/sass', 'static/css', '/static/css')
    }
)
