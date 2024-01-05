import setuptools

REPO_NAME = "sql-to-code-local"
package_dir = "sql_to_code"

setuptools.setup(
    name=REPO_NAME,  # https://pypi.org/project/sql-to-code-local
    version='0.0.4',  # update each time
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles sql-to-code-local Local Python",
    long_description="PyPI Package for Circles sql-to-code-local Local Python",
    long_description_content_type='text/markdown',
    # TODO: fix the link in the following comment
    url="https://github.com/circ-zone/sql2code-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
