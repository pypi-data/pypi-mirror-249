import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sokudoku",
    version="0.0.1",
    author="tomihara hikaru",
    author_email="s2122041@stu.musashino-u.ac.jp",
    description="PyPI test ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hikaru163/cs_ai",
    project_urls={
        "Bug Tracker": "https://github.com/Hikaru163/cs_ai",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['sokudoku'], # srcに入れた.pyファイルの名前を入れる
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'sokudoku = sokudoku:main'
        ]
    },
)
