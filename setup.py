from setuptools import find_packages, setup

setup(
    name="ficha-key",
    version="2.0.0",
    # py_modules=["api", "app_config", "ficha", "logging_service", "secret_key_generator"],
    packages=find_packages(),
    # install_requires=["requests"],
    author="Raphael Mwasaru Mwangangi",
    author_email="raphaelmwasaru@gmail.com",
    description="A store for sensitive tokens like passwords and api tokens.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raphikizolo/ficha_key",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
