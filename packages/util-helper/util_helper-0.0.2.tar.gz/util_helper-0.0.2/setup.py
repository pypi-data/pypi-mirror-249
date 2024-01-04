from setuptools import setup, find_packages

with open("./README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="util_helper",
    version="0.0.2",
    packages=find_packages(),
    #install_requires=[],
    #package_data={'glai': ['back_end/model_db/gguf_models/*.json']},
    #include_package_data=True,
    author="Łael Al-Halawani",
    author_email="laelhalawani@gmail.com",
    description="Few scripts to help with various tasks such as text preprocessing, file handling.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "License :: Free for non-commercial use",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['file handling', 'string comparison', 'text preprocessing'],
    url="https://github.com/laelhalawani/glai",
)