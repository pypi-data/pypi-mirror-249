import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-versioned-stack-manager",
    "version": "1.0.5",
    "description": "A CDK construct for dealing with Versioned Stacks - multiple copies of the same stack that would forever grow over time without...this.",
    "license": "Apache-2.0",
    "url": "https://github.com/dkershner6/cdk-versioned-stack-manager.git",
    "long_description_content_type": "text/markdown",
    "author": "Derek Kershner",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/dkershner6/cdk-versioned-stack-manager.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_versioned-stack-manager",
        "cdk_versioned-stack-manager._jsii"
    ],
    "package_data": {
        "cdk_versioned-stack-manager._jsii": [
            "cdk-versioned-stack-manager@1.0.5.jsii.tgz"
        ],
        "cdk_versioned-stack-manager": [
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
