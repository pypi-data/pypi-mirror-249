from distutils.core import setup
from setuptools import find_packages

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="lark-oapi-shortcut",
    version="2024.1.4",
    description="Lark OpenAPI SDK for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Wenbo Mao",
    author_email="maowenbo@bytedance.com",
    maintainer="straydragon",
    maintainer_email="straydragonl@foxmail.com",
    url="https://github.com/straydragon/oapi-sdk-python",
    packages=find_packages(),
    install_requires=[
        "pycryptodome",
        "requests",
        "requests_toolbelt",
        "attrs",
        "pydantic>=1,<2",
        "typing_extensions",
    ],
    extras_require={"flask": ["Flask"]},
    python_requires=">=3.7",
    keywords=["Lark", "OpenAPI"],
    include_package_data=True,
    project_urls={
        "Source": "https://github.com/straydragon/oapi-sdk-python",
    },
)
