from setuptools import setup

setup(
    name='pay_trio',
    packages=['pay_trio_app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'wtforms',
    ],
)



