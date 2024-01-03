import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudfront-geo-locator",
    "version": "0.1.14",
    "description": "An AWS CDK construct to create a CloudFront-powered HTTP endpoint delivering requestor's geolocation details.",
    "license": "MIT",
    "url": "https://github.com/ilkrklc/cdk-cloudfront-geo-locator",
    "long_description_content_type": "text/markdown",
    "author": "Ilker Kilic<ilkrklc@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/ilkrklc/cdk-cloudfront-geo-locator"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudfront_geo_locator",
        "cdk_cloudfront_geo_locator._jsii"
    ],
    "package_data": {
        "cdk_cloudfront_geo_locator._jsii": [
            "cdk-cloudfront-geo-locator@0.1.14.jsii.tgz"
        ],
        "cdk_cloudfront_geo_locator": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib==2.117.0",
        "constructs>=10.0.0, <11.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
