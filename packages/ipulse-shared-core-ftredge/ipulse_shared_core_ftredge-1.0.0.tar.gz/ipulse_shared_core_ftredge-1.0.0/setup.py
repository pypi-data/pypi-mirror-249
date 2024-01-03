from setuptools import setup, find_packages

setup(
    name='ipulse_shared_core_ftredge',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        'pydantic[email]',
        'uuid'
    ],
    author='Russlan Ramdowar',
    author_email='russlan@ftredge.com',
    description='Shared models for the Pulse platform project. Using AI for financial advisory and investment management.',
    url='https://github.com/TheFutureEdge/ipulse_shared_core',
)