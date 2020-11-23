from setuptools import setup, find_packages

PACKAGES = (
    'Django>=3.1',
    'Pillow>=8.0',
)


setup(
    name='django-image-compressor',
    version='0.1',
    description="Image compressor for Django apps.",
    url='https://github.com/yunusovbekir/django-image-compressor',
    download_url='https://github.com/yunusovbekir/django-image-compressor',
    author='Bakir Yunusov',
    author_email='yunusovbekir@gmail.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=PACKAGES,
    zip_safe=False,
    keywords=['django', 'image', 'compressor'],
)
