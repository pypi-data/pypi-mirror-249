from setuptools import setup

# if __name__ == "__main__":
setup(
    name='cu-cat',
    version='v0.07.13',
    # cmdclass=versioneer.get_cmdclass(),
    # packages = find_packages(),
    platforms='any',
    description = 'An end-to-end gpu Python library that encodes categorical variables into machine-learnable numerics',
    long_description=open("./README.md").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/graphistry/cu-cat',
    download_url= 'https://github.com/graphistry/cu-cat',
    python_requires='>=3.7',
    author='The Graphistry Team',
    author_email='pygraphistry@graphistry.com',
    # install_requires=core_requires,
    # extras_require=extras_require,
    license='BSD',
    
    keywords=['cudf', 'cuml', 'GPU', 'Rapids']
)



# #!/usr/bin/env python

# from setuptools import setup, find_packages
# # import versioneer

# def unique_flatten_dict(d):
#   return list(set(sum( d.values(), [] )))

# core_requires = [
#   'numpy',
#   'pandas',
#   'setuptools',
#   'logging',
#   'typing',
#   'pyarrow >= 0.15.0',
#   'scikit-learn',
#   'flake8',
#   'mypy',
#   'pytest',
#   'psutil',
#   'build',
# #   'cuml', ## cannot test on github actions
# #   'cudf',
# #   'cupy'
# ]

# # if __name__ == "__main__":
# setup(
#     name='cu-cat',
#     version='v0.07.12',  # versioneer.get_version(),
#     # cmdclass='0.7.7',  # versioneer.get_cmdclass(),
#     packages = find_packages(),
#     platforms='any',
#     description = 'An end-to-end gpu Python library that encodes categorical variables into machine-learnable numerics',
#     long_description=open("./README.md").read(),
#     long_description_content_type='text/markdown',
#     url='https://github.com/graphistry/cu-cat',
#     download_url= 'https://github.com/graphistry/cu-cat',
#     python_requires='>3.7',
#     author='The Graphistry Team',
#     author_email='pygraphistry@graphistry.com',
#     install_requires=core_requires,
#     license='BSD',
#     # dependency_links=['https://pypi.nvidia.com'],
#     keywords=['cudf', 'cuml', 'GPU', 'Rapids']
# )
