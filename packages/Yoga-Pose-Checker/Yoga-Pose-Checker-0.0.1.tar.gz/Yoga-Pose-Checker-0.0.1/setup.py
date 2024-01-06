import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Yoga-Pose-Checker",
    version="0.0.1",
    author="moe endo",
    author_email="s2122009@stu.musashino-u.ac.jp",
    description="A package for counting BLOB objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moe1030/Yoga-Pose-Checker",
    project_urls={
        "Bug Tracker": "https://github.com/moe1030/Yoga-Pose-Checker",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['Yoga-Pose-Checker'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'YogaPoseCheckert = YogaPoseChecker:main'
        ]
    },
)