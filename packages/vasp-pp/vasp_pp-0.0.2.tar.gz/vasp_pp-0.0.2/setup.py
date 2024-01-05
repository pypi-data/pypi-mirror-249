from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vasp_pp",
    version="0.0.2",
    description="Post-processes VASP outputs ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brobinson10296/vasp_pp_package",
    author="Brian Robinson",
    author_email="b.p.robinson102@gmail.com",
    python_requires=">=3.9",
    include_package_data=True,
    install_requires=[
        "numpy",
    ],
    extra_requires={"dev": ["twine>=4.0.02"]},
)
