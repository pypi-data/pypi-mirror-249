from setuptools import setup, find_packages

setup(
  name="samosila-core",
  author="Mohammad Javad Hosseini",
  version="0.0.1",
  author_email="johndoe2561357@protonmail.com",
  packages=find_packages(),
  install_requires=[
    "appdirs>=1.4.4",
    "aiohttp>=3.9.0",
    "backoff>=2.2.0",
    "certifi>=2023.7.22",
    "cryptography>=41.0.4",
    "importlib-metadata>=6.8.0",
    "jinja2>=3.1.2",
    "jsonmerge>=1.9.2",
    "regex>=2023.5.5",
    "requests>=2.29.0",
    "requests-file>=1.5.1",
    "requests-html>=0.10.0",
    "tokenizers>=0.15.0",
    "Pillow>=10.0.0",
    "python-dotenv>=1.0.0",
    "pydantic_settings>=2.0.0",
    "openai>=1.0.0",
    "six>=1.16.0",
    "tiktoken>=0.5.0",
    "unstructured>=0.11.2",
    "validators>=0.22.0",
  ]
)