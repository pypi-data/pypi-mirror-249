"""imports"""
import setuptools

PACKAGE_NAME = "message-send-local"
# Since all PACAKGE_NAMEs are with an underscore, we don't need this. Why do we need it?
package_dir = "message_send_platform_invitation"

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.9',  # https://pypi.org/project/message-send-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles message_send_platform_invitation Python",
    long_description="PyPI Package for Circles message_send_platform_invitation Python",
    long_description_content_type='text/markdown',
    url="https://github.com/circles-zone/message-send-platform-invitation-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pytest',
        'message-local',
        'messages-local',
        'database-mysql-local',
        'logger-local'
    ],
)
