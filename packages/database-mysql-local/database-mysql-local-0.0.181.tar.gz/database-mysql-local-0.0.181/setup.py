import setuptools

PACKAGE_NAME = "database-mysql-local"
# package_dir = "circles_local_database_python"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/database-mysql-local
    version='0.0.181',
    author="Circles",
    author_email="info@circles.life",
    url="https://github.com/circles-zone/database-mysql-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="Database MySQL Local",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TOto avoid "pip install mysqlclient"
    install_requires=[
        "mysql-connector>=2.2.9",  # https://pypi.org/project/mysql-connector/
        "python-dotenv>=1.0.0",  # https://pypi.org/project/python-dotenv/
        "logger-local>=0.0.71",  # https://pypi.org/project/logger-local/
        "pytest>=7.4.3",  # https://pypi.org/project/pytest/
        "PyMySQL>=1.1.0",  # https://pypi.org/project/pymysql/
        "database-infrastructure-local>=0.0.19",  # https://pypi.org/project/database-infrastructure-local/
        "language-remote>=0.0.8",  # https://pypi.org/project/language-local/
        "sql-to-code-local>=0.0.2"  # https://pypi.org/project/sql-to-code-local/
    ]
)
