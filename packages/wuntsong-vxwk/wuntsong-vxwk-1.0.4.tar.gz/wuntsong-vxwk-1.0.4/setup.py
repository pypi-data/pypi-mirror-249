from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='wuntsong-vxwk',
    version='1.0.4',
    author='广州桓创信息科技有限公司',
    author_email='report@wuntsong.com',
    url='https://www.vxwk.com',
    description=u'VXWK项目的Python版本SDK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['vxwk'],
    install_requires=[
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "idna==3.6",
        "requests==2.31.0",
        "urllib3==2.1.0",
    ],
)
