from setuptools import setup, find_packages

# Зчитування довгого опису з файлу long.txt
with open('long.txt', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='bumpAPI',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    author="ecomatedev",
    author_email="ecomatedev@gmail.com",
    description="Python library for interacting with the site's external API.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/bumpAPI",
)
