import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "acm-auto-validate",
    "version": "0.0.5",
    "description": "AWS CDK construct for automated cross-account ACM certificate validation using DNS",
    "license": "Apache-2.0",
    "url": "https://github.com/jvardanian/acm-auto-validate.git",
    "long_description_content_type": "text/markdown",
    "author": "John Vardanian<jvardanian@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/jvardanian/acm-auto-validate.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "acm_auto_validate",
        "acm_auto_validate._jsii"
    ],
    "package_data": {
        "acm_auto_validate._jsii": [
            "acm-auto-validate@0.0.5.jsii.tgz"
        ],
        "acm_auto_validate": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
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
