import setuptools

setuptools.setup(
    name="hamon-ai-database",
    version="0.0.1",
    description="Hamonsoft Company Database Python Version Package",
    author="Hamonsoft AI",
    python_requires=">=3.11, <4",
    packages=['src'],
    install_requires=[
        'mysql-connector-python==8.2.0',
        'protobuf==4.21.12'
    ],
    license="MIT",
)
