from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [
        l.strip() for l in f
        if l.strip() and not l.startswith("#")
    ]

setup(
    name="autogen-data-analyzer-gpt",
    version="1.0.0",
    author="Your Name",
    description="AutoGen AI-Powered Data Analysis System",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.9",
)