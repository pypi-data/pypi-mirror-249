from setuptools import setup, find_packages

setup(
    name="YouTubeUploader",
    version="0.0.2",
    author=[{'name': 'David', 'email': 'david2002belozerov@mail.ru'}],
    description="Uploading videos to YouTube",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=['selenium==4.16.0'],
)