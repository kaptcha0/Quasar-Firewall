import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent
INSTALL_REQUIRES = (HERE / "requirements.txt").read_text()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quasar-project-firewall",  # Replace with your own username
    version="1.0.1.1",
    author="Kyro Dev",
    author_email="kyro.captcha@gmail.com",
    description="An Artificial Intelligent firewall that detects malicious HTTP requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyro-dev/Quasar-Project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "quasar=quasar.__main__:main",
        ]
    },
    scripts=["scripts/proxy.sh", "scripts/train.sh"]
)
