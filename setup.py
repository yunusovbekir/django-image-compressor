from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

PACKAGES = (
    'Django>=3.0',
    'Pillow>=8.0',
)


setup(
    name='django-image-compressor',
    version='0.1',
    description="Image compressor for Django apps.",
    long_description=long_description,
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
