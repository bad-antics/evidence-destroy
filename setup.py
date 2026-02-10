from setuptools import setup,find_packages
setup(name="evidence-destroy",version="2.0.0",author="bad-antics",description="Anti-forensics and evidence destruction research",packages=find_packages(where="src"),package_dir={"":"src"},python_requires=">=3.8")
