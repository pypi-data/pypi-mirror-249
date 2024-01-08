import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_dog",
    version="0.3.01",
    author="Reversedeer",
    description="Lick the dog diary! Lick the dog and lick to the last nothing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reversedeer/nonebot_plugin_dog",
    project_urls={
        "Bug Tracker": "https://github.com/Reversedeer/nonebot_plugin_dog/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires = [
        'httpx>=0.23.1',
        'nonebot2>=2.0.0rc2',
        'poetry>=1.5.0',
        "nonebot-adapter-onebot>=2.1.3"
    ]
)