from setuptools import setup, find_packages

setup(
    name="todoist-sync-gcp",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "python-dateutil",
        "google-cloud-bigquery"
    ],
)
