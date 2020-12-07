import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quasar-firewall",  # Replace with your own username
    version="1.0.0",
    author="Kyro Dev",
    author_email="kyro.captcha@gmail.com",
    description="An Artificial Intelligent firewall that detects hacks in HTTP requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyro-dev/Quasar-Project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=["proxy.sh"]
)
