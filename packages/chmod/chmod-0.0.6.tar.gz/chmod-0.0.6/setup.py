import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="chmod",
    version="0.0.6",
    author="Harry Sharma",
    author_email="harrysharma1066@gmail.com",
    description="Basic chmod conversion tool",
    packages=["chmod"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)