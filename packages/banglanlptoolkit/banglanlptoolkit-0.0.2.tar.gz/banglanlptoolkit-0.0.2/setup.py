from setuptools import setup, find_packages

# setup(
#     name='banglanlptoolkit',
#     version='0.0.2',
#     author='A F M Mahfuzul Kabir',
#     author_email='afmmahfuzulkabir@gmail.com',
#     description='Toolkits for text processing and augmentation for Bangla NLP',
#     long_description=open('README.md').read(),
#     long_description_content_type='text/markdown',
#     url='https://github.com/Kabir5296/banglanlptoolkit',
#     project_urls={'Repository': 'https://github.com/Kabir5296/banglanlptoolkit'},
#     classifiers=[
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent'
#     ],
#     package_dir={'': 'banglanlptoolkit'},
#     packages=find_packages(where='banglanlptoolkit'),
#     python_requires='>=3.8',
#     install_requires=[
#         'bnunicodenormalizer',
#         # 'normalizer',
#         # 'git@github.com/csebuetnlp/normalizer.git@main#egg=normalizer',
#         'numpy',
#         'pandas',
#         'sentencepiece',
#         'torch',
#         'tqdm',
#         'transformers'
#     ],
#     dependency_links=['http://github.com/csebuetnlp/normalizer.git']
# )

# [options.packages.find]
# where = banglanlptoolkit

from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'banglanlptoolkit'
# LONG_DESCRIPTION = 'pip installable version of - Official PyTorch Implementation of CleanUNet (ICASSP 2022) '

# Setting up
setup(
        name="banglanlptoolkit", 
        version=VERSION,
        author="A F M Mahfuzul Kabir",
        author_email="<afmmahfuzulkabir@gmail.com>",
        description=DESCRIPTION,
        # long_description=LONG_DESCRIPTION,
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[
            'bnunicodenormalizer',
            'numpy',
            'pandas',
            'sentencepiece',
            'torch',
            'tqdm',
            'transformers'
        ],
        dependency_links=['http://github.com/csebuetnlp/normalizer.git'],
        url='https://github.com/Kabir5296/banglanlptoolkit',
        project_urls={'Repository': 'https://github.com/Kabir5296/banglanlptoolkit'},
)