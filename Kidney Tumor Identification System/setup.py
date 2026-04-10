import setuptools

setuptools.setup(
    name="cnnClassifier",
    version="0.0.0",
    author="KidneyTumorSystem",
    description="CNN-based Kidney Tumor Classification",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
