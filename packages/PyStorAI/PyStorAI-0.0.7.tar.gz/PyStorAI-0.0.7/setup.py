from setuptools import setup, find_packages

setup(
    name='PyStorAI',
    version='0.0.7',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    package_data={
	'PyStorAI':['images/*.png']
    },
    include_package_data = True,
    author='Your Name',
    author_email='your@email.com',
    description='A short description of your package',
    long_description='A longer description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/VisualXAI/PyStorAI',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
