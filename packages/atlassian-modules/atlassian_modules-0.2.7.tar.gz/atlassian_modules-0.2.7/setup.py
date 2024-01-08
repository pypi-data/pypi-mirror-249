from setuptools import setup, find_packages

setup(
    name="atlassian_modules",
    version="0.2.7",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    author="Pavan Bhatt",
    author_email="pavanhbhatt1@gmail.com",
    description="Modules for interacting with Atlassian products.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="",  # Replace with your repository URL
)
