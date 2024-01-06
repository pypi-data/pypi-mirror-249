from setuptools import setup, find_packages

setup(
    name="ibott-cv",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["hatchling","pyautogui"],
    author="OnameDohe",
    author_email="enrique.crespo.debenito@gmail.com",
    description="This package moves mouse",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ecrespo66/files_and_folders",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
