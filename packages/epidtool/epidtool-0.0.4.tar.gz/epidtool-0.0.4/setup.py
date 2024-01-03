import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='epidtool',
    version='0.0.4',
    author='Souvik Manik',
    author_email='smanik.astro@gmail.com',
    description='A Python toolkit for analysis, modelling and forecasting Epidemic',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/souvikmanik/Pandemicpy',
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy","scipy", "scikit-learn==1.0.2", "statsmodels==0.13.2", "pandas", "setuptools==69.0.2"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
