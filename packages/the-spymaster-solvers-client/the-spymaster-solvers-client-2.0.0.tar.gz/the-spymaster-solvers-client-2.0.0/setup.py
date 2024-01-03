from setuptools import find_packages, setup

setup(
    name="the-spymaster-solvers-client",
    version="2.0.0",
    description="Python client implementation for The Spymaster Solvers HTTP backend.",
    author="Asaf Kali",
    author_email="asaf.kali@mail.huji.ac.il",
    url="https://github.com/asaf-kali/the-spymaster-solvers",
    packages=find_packages(),
    install_requires=["codenames~=4.0", "the-spymaster-util~=3.0", "pydantic~=1.9", "requests~=2.28"],
    include_package_data=True,
)
