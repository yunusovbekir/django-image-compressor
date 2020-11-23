from setuptools import setup, find_packages

PACKAGES = (
    'Django>=3.1',
    'Pillow>=8.0',
)


setup(
    name='django-image-compressor',
    version='0.1',
    description="Image compressor for Django apps.",
    url='',
    download_url='',
    author='Bakir Yunusov',
    author_email='yunusovbekir@gmail.com',
    license='',
    packages=find_packages(),
    install_requires=PACKAGES,
    zip_safe=False,
    keywords=['django', 'image', 'compressor']
)
