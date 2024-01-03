from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='llm_task_handler',
    version='2.0.1',
    description='LLM Task Handler',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Jimming Cheng',
    author_email='jimming@gmail.com',
    packages=['llm_task_handler'],
    install_requires=[
        'langchain',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
