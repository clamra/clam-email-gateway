from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name = 'clam-email-gateway',
    version = version,
    packages = find_packages(),

    author = 'Clamra Team',
    author_email = 'team@clamra.com',
    license = 'GPLv3',
    description = 'Clam Email Gateway',
    url='https://github.com/clamra/clam-email-gateway',
    install_requires=[
        'docopt',
        'lamson',
        'hiredis',
        'redis',
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'ceg = ceg.cli:main',
        ],
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Linux Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe = False,
)
