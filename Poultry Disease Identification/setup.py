import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="cnnClassifier",
    version="0.0.1",
    author="Prithu Sarkar",
    description="Poultry Disease Identification using VGG16 CNN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
