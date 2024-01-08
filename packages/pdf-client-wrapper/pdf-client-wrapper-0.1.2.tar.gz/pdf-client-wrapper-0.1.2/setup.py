import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdf-client-wrapper",
    version="v0.1.2",
    author="Daryl Xu",
    author_email="xuziqiang@zyheal.com",
    description="pdf client wrapper, more easy to use pdf-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://e.coding.net/xymedimg/pdf-server/pdf-client-wrapper.git",
    packages=setuptools.find_packages(),
    install_requires=['source', 'grpcio', 'protobuf<=3.20.3'],
    entry_points={
        'console_scripts': [
            'pts_render = pdf_client_wrapper.pts_render:_main',
            ]
    },
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ),
)