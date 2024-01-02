import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mbonig.state-machine",
    "version": "0.0.32",
    "description": "A Step Function state machine construct focused on working well with the Workflow Studio",
    "license": "MIT",
    "url": "https://github.com/mbonig/state-machine.git",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mbonig/state-machine.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.state-machine",
        "mbonig.state-machine._jsii"
    ],
    "package_data": {
        "mbonig.state-machine._jsii": [
            "state-machine@0.0.32.jsii.tgz"
        ],
        "mbonig.state-machine": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.85.0, <3.0.0",
        "constructs>=10.1.203, <11.0.0",
        "jsii>=1.82.0, <2.0.0",
        "projen>=0.71.34, <0.72.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
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
