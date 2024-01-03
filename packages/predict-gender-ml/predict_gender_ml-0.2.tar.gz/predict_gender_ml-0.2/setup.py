import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="predict_gender_ml",
    version="0.2",
    author="Jumble",
    author_email="help@help.org",
    description="Predicts gender based on name with ML Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JumbleBumble/predict-gender-ml",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data={
        "predict_gender_ml": ["*.*"],
    },
    include_package_data=True,
    install_requires=["joblib==1.3.2", "pandas==2.1.2", "torch==2.1.0"],
)
