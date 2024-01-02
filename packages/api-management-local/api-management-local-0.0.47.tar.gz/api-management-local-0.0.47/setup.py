import setuptools

PACKAGE_NAME = "api-management-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.47',  # https://pypi.org/project/api-management-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles api-management-local-python-package",
    long_description="PyPI Package for Circles api-management-local-python-package",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/api-management-local-python-package",
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'python-sdk-local>=0.0.27',
        'database-mysql-local>=0.0.133',
        'star-local>=0.0.10'
    ],
)
