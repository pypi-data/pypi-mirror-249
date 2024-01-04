import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="SmileValidation",
    version="1.2.10",
    author="Sitthykun LY",
    author_email="ly.sitthykun@gmail.com",
    description="Python3 Validation in another way",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/sitthykun/smilevalidation",
    packages=[
    "smilevalidation"
    #,"smilevalidation.Validation"
    #,"smilevalidation.RuleSchema"
    #,"smilevalidation.Console"
    #,"smilevalidation.InvalidTypeList"
    ,"smilevalidation.rule"
    #,"smilevalidation.rule.BaseRule"
    #,"smilevalidation.rule.BoolRule"
    #,"smilevalidation.rule.ComparisonRule"
    #,"smilevalidation.rule.DateRule"
    #,"smilevalidation.rule.DateTimeRule"
    #,"smilevalidation.rule.FloatRule"
    #,"smilevalidation.rule.IntegerRule"
    #,"smilevalidation.rule.ListRule"
    #,"smilevalidation.rule.MatchRule"
    #,"smilevalidation.rule.NotMatchRule"
    #,"smilevalidation.rule.NumericRule"
    #,"smilevalidation.rule.StringRule"
    #,"smilevalidation.rule.TimeRule"
    ,"smilevalidation.schema"
    #,"smilevalidation.schema.BaseSchema"
    #,"smilevalidation.schema.ComparisonSchema"
    #,"smilevalidation.schema.DateTimeSchema"
    #,"smilevalidation.schema.FloatSchema"
    #,"smilevalidation.schema.IntegerSchema"
    #,"smilevalidation.schema.NumericSchema"
    #,"smilevalidation.schema.StringSchema"
    #,"smilevalidation.schema.TypeSchema"
    ],
    #packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
