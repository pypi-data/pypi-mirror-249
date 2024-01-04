import setuptools

setuptools.setup(
    name="hamonsoft-ai-database",
    version="0.0.4",
    description="Hamonsoft Company Database Python Version Package",
    author="Hamonsoft AI",
    python_requires=">=3.11, <4",
    packages=setuptools.find_packages(where='hamonsoft'),
    package_dir={"": "hamonsoft"},
    install_requires=[
        'mysql-connector-python==8.2.0',
        'impyla==0.9.0'
    ],
    license="MIT",
)
