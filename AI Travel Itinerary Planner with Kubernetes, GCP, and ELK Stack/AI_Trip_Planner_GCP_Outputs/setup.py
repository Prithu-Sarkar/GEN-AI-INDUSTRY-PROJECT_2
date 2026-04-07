from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [l for l in f.read().splitlines()
                    if l and not l.startswith("#") and not l.startswith("uv")]

setup(
    name="AI Trip Planner",
    version="0.1",
    author="divesh",
    packages=find_packages(),
    install_requires=requirements,
)