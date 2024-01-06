import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='humata',
    author='Humata',
    author_email='support@humata.ai',
    description='Humata.ai Python SDK',
    keywords='humata, humata.ai',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.humata.ai/',
    project_urls={
        'Documentation': 'https://www.humata.ai/',
        'Bug Reports': 'https://ww.humata.ai/'
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[],
    python_requires='>=3.6',
    install_requires=[
        "supabase==2.3.1"
    ],
    extras_require={
        'dev': ['check-manifest'],
    },
)
