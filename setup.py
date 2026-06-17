from setuptools import setup, find_packages

setup(
    name='certbot-storagegrid',
    version='0.9.0',
    description='Certbot plugin for NetApp StorageGRID',
    packages=find_packages(),
    install_requires=[
        'certbot>=2.0',
        'requests',
    ],
    entry_points={
        'certbot.plugins': [
            'storagegrid = certbot_storagegrid.installer:Installer',
        ],
    },
)
