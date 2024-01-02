import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudfront-associate-alias",
    "version": "1.0.4",
    "description": "A simple construct to handle automated Cloudfront DNS alias migration with zero downtime",
    "license": "Apache-2.0",
    "url": "https://github.com/dkershner6/cdk-cloudfront-associate-alias.git",
    "long_description_content_type": "text/markdown",
    "author": "Derek Kershner",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/dkershner6/cdk-cloudfront-associate-alias.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudfront-associate-alias",
        "cdk_cloudfront-associate-alias._jsii"
    ],
    "package_data": {
        "cdk_cloudfront-associate-alias._jsii": [
            "cdk-cloudfront-associate-alias@1.0.4.jsii.tgz"
        ],
        "cdk_cloudfront-associate-alias": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.101.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.93.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
