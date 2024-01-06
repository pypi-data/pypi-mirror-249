from setuptools import setup, find_packages

setup(
    name='ipulse_shared_core_ftredge',
    version='1.4.0',
    package_dir={'': 'src'},  # Specify the source directory
    packages=find_packages(where='src'),  # Look for packages in 'src'
    install_requires=[
        # List your dependencies here
        'pydantic[email]',
        'uuid'
    ],
    author='Russlan Ramdowar',
    description='Shared models for the Pulse platform project. Using AI for financial advisory and investment management.',
    url='https://github.com/TheFutureEdge/ipulse_shared_core',
)