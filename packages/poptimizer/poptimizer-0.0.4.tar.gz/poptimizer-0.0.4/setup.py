"""
Setup file
"""
from setuptools import setup, find_packages

setup(
    name='poptimizer',
    version='0.0.4',
    description='Utilize Large Language Models to Automatically Optimize Prompts for LLM Application Development',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='alkhalifas',
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "langchain",
        "openai",
        "pylint"
    ],
)
