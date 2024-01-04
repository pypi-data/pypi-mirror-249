import setuptools


try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Description not found due to load from automated process"


# Using compatible release notation (https://peps.python.org/pep-0440/#compatible-release) make pip solver very slow
# Sort requires by alphabetic order
install_requires = [
    "aiohttp[speedups]==3.8.5",
    "aiomcache==0.8.1",
    "asyncpg==0.28.0",
    "boto3==1.24.56",
    "datadog==0.47.0",
    "ddtrace==1.20.14",
    "dill==0.3.7",  # Required by Ultralytics
    "fastapi==0.103.1",
    "gunicorn==20.1.0",
    "matplotlib==3.7.1",
    "numpy==1.23.5",
    "pandas==1.5.3",
    "platformdirs==3.11.0",
    "plotly-express==0.4.1",
    "psutil==5.9.5",
    "psycopg2-binary==2.9.7",
    "pyarrow==10.0.1",
    "pymemcache==4.0.0",
    "requests==2.31.0",
    "s3fs==2022.11.0",
    "scikit-learn==1.2.2",
    "seaborn==0.12.1",
    "SQLAlchemy[asyncio]==1.4.46",
    "sqlparse==0.4.3",
    "ultralytics==8.0.187",
    "uvicorn[standard]==0.23.2",
]


# Sort requires by alphabetic order
extras_require = {
    "experiments": [
        "ipywidgets==8.1.1",
        "jupyterlab==4.0.7",
        "notebook==7.0.6",
    ],
    "tensor": [
        "grpcio==1.50.0",
        "keras==2.9.0",
        "tensorflow==2.9.3",
    ],
    "test": [
        "awscliv2==2.2.0",
        "pre-commit==3.4.0",
        "pylint==2.17.2",
        "pytest==7.4.2",
        "httpx>=0.23.3",
    ],
    "torch": [
        "torch==1.13.1",
        "torchvision==0.14.1",
    ],
    "xgb": [
        "dask==2023.2.1",
        "dask-cuda==23.4.0a230228",
        "xgboost==1.7.3",
    ],
    "computer-vision": [
        "opencv-python==4.7.0.68",
        "python-dateutil==2.8.2",
    ],
}
# Create the generic "all" extra who regroup all other extras except those contained in the "not in" below
extras_require["all"] = [ev for ek, ev in extras_require.items() if ek not in ["test"]]  # type: ignore


setuptools.setup(
    name="kpler-ai-kai-dependencies",
    version='0.0.2',
    description="A list of KAI package dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kpler/datascience-kai-dependencies",
    author="Kpler",
    author_email="engineering@kpler.com",
    packages=setuptools.find_namespace_packages(
        where="src",
        include=["kpler*"],
    ),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
    extras_require=extras_require,
)
