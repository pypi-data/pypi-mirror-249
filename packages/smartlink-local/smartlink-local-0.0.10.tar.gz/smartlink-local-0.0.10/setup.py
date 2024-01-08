import setuptools

PACKAGE_NAME = "smartlink-local"
package_name_to_import = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.10',
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles smart link Python",
    long_description="PyPI Package for Circles smart link Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/smartlink-restapi-python-serverless-com",
    packages=[package_name_to_import],
    package_dir={package_name_to_import: "src"},
    package_data={package_name_to_import: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'logger-local>=0.0.76',
        'message-local>=0.0.47',
        'queue-worker-local',
        'python-sdk-local',
        'language-local',
        'database-mysql-local>=0.0.182',
        'email-address-local'  # action 17
    ],
)
