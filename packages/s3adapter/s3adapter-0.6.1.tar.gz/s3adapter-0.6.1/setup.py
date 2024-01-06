from setuptools import setup, find_packages

setup(
    name='s3adapter',
    version='0.6.1',
    packages=find_packages(),
    author='Flavio Lopes',
    author_email='flavio.lopes@ideiasfactory.tech',
    maintainer='Ideias Factory',
    license='MIT',
    description='A AWS S3 Python Adapter to Readn, Write and Check existence of files in S3 Buckets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'boto3==1.34.12',
        'botocore==1.34.12',
        'jmespath==1.0.1',
        'numpy==1.26.3',
        'pandas==2.1.4',
        'python-dateutil==2.8.2',
        'python-dotenv==1.0.0',
        'pytz==2023.3.post1',
        's3transfer==0.10.0',
        'six==1.16.0',
        'tzdata==2023.4',
        'urllib3==1.26.18'
    ],
)
