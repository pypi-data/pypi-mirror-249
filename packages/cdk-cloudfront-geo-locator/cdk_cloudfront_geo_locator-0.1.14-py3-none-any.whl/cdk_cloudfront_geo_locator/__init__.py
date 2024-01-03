'''
# CloudfrontGeoLocator

![GitHub](https://img.shields.io/github/license/ilkrklc/cdk-cloudfront-geo-locator) ![npm version](https://img.shields.io/npm/v/cdk-cloudfront-geo-locator) [![Maven Central](https://maven-badges.herokuapp.com/maven-central/io.github.ilkrklc/cdk.cloudfront.geo.locator/badge.svg)](https://maven-badges.herokuapp.com/maven-central/io.github.ilkrklc/cdk.cloudfront.geo.locator) [![NuGet latest version](https://badgen.net/nuget/v/CDK.CloudFront.Geo.Locator/latest)](https://nuget.org/packages/CDK.CloudFront.Geo.Locator) [![Go Reference](https://pkg.go.dev/badge/github.com/ilkrklc/cdk-cloudfront-geo-locator/cdkcloudfrontgeolocator.svg)](https://pkg.go.dev/github.com/ilkrklc/cdk-cloudfront-geo-locator/cdkcloudfrontgeolocator)

The `CloudfrontGeoLocator` is an AWS CDK construct that automates the setup of a CloudFront distribution with an Origin Request Lambda function, enabling applications to determine the geolocation of their users based on incoming HTTP requests. It's an ideal solution for developers looking to enhance their cloud applications with geolocation awareness without delving into the complexities of AWS configurations.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Documentation](#documentation)
* [Geolocation Endpoint Response](#geolocation-endpoint-response)
* [Contributing](#contributing)
* [Pull Request Guidelines](#pull-request-guidelines)
* [License](#license)

## Installation

To install `CloudfrontGeoLocator` construct library using npm, run the following command:

```bash
npm i cdk-cloudfront-geo-locator
```

## Usage

To initialize the `CloudfrontGeoLocator` construct you can use the following code:

```python
import cdk = require('aws-cdk-lib');
import { Construct } from 'constructs';
import { CloudfrontGeoLocator } from 'cdk-cloudfront-geo-locator';

// stack initialization with default props
const geoLocator = new CloudfrontGeoLocator(this, 'GeoLocator');

// stack initialization with custom props
const geoLocatorWithProps = new CloudfrontGeoLocator(
  this,
  'GeoLocatorWithProps',
  {
    s3BucketName: 'cloudfront-origin-bucket-name', // optional
    lambdaFunctionName: 'cloudfront-origin-request-edge-lambda-function-name', // optional
    cloudfrontCachePolicyName: 'cloudfront-cache-policy-name', // optional
    cloudfrontOriginRequestPolicyName: 'cloudfront-origin-request-policy-name', // optional
    cloudfrontPriceClass: cloudfront.PriceClass.PRICE_CLASS_100, // optional
  }
);

// stack initialization with custom domain
const customDomainGeoLocator = new CloudfrontGeoLocator(
  this,
  'CustomDomainGeoLocator',
  {
    customDomain: {
      domainName: 'example.com',
      certificateArn:
        'arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012',
    },
  }
);

// exported properties
console.log(geoLocator.s3BucketArn); // The ARN of the S3 bucket.
console.log(geoLocator.lambdaFunctionArn); // The ARN of the Lambda function.
console.log(geoLocator.lambdaFunctionVersion); // The current version of the Lambda function.
console.log(geoLocator.distributionId); // The ID of the CloudFront distribution.
console.log(geoLocator.distributionDomainName); // The domain name of the CloudFront distribution.
console.log(geoLocator.cloudfrontCachePolicyId); // The ID of the CloudFront cache policy.
console.log(geoLocator.cloudfrontOriginRequestPolicyId); // The ID of the CloudFront origin request policy.
```

## Documentation

To initialize the `CloudfrontGeoLocator` construct you can use the following props:

```python
/**
 * Properties for the CloudfrontGeoLocator construct.
 */
export interface CloudfrontGeoLocatorProps extends ResourceProps {
  /**
   * A unique name to identify the s3 bucket.
   *
   * @default - cloudfront-geo-locator-origin
   */
  readonly s3BucketName?: string;

  /**
   * A unique name to identify the lambda function.
   *
   * @default - cloudfront-geo-locator
   */
  readonly lambdaFunctionName?: string;

  /**
   * A unique name to identify the cloudfront cache policy.
   *
   * @default - CloudfrontGeoLocatorCachePolicy
   */
  readonly cloudfrontCachePolicyName?: string;

  /**
   * A unique name to identify the cloudfront origin request policy.
   *
   * @default - CloudfrontGeoLocatorOriginRequestPolicy
   */
  readonly cloudfrontOriginRequestPolicyName?: string;

  /**
   * The price class for the CloudFront distribution.
   *
   * @default - PRICE_CLASS_100
   */
  readonly cloudfrontPriceClass?: cloudfront.PriceClass;

  /**
   * The domain name and certificate arn configuration for the CloudFront distribution.
   *
   * @default - undefined
   */
  readonly customDomain?: {
    /**
     * The domain name for the CloudFront distribution.
     */
    readonly domainName: string;

    /**
     * The ARN of the certificate.
     */
    readonly certificateArn: string;
  };
}
```

## Geolocation Endpoint Response

The geolocation endpoint returns a JSON object with the following properties:

```json
{
  "country": "TR",
  "countryName": "Türkiye",
  "countryRegion": "35",
  "countryRegionName": "Izmir",
  "city": "Izmir"
}
```

## Contributing

We welcome contributions! Please review [code of conduct](.github/CODE_OF_CONDUCT.md) and [contributing guide](.github/CONTRIBUTING.md) so that you can understand what actions will and will not be tolerated.

### Pull Request Guidelines

* The `main` branch is just a snapshot of the latest stable release. All development should be done in development branches. **Do not submit PRs against the `main` branch.**
* Work in the `src` folder and **DO NOT** checkin `dist` in the commits.
* It's OK to have multiple small commits as you work on the PR
* If adding a new feature add accompanying test case.
* If fixing bug,

  * Add accompanying test case if applicable.
  * Provide a detailed description of the bug in the PR.
  * If you are resolving an opened issue add issue number in your PR title.

## License

`CloudfrontGeoLocator` is [MIT licensed](./LICENSE).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class CloudfrontGeoLocator(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cloudfront-geo-locator.CloudfrontGeoLocator",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloudfront_cache_policy_name: typing.Optional[builtins.str] = None,
        cloudfront_origin_request_policy_name: typing.Optional[builtins.str] = None,
        cloudfront_price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        custom_domain_certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        lambda_function_name: typing.Optional[builtins.str] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloudfront_cache_policy_name: (experimental) A unique name to identify the cloudfront cache policy. Default: - CloudfrontGeoLocatorCachePolicy
        :param cloudfront_origin_request_policy_name: (experimental) A unique name to identify the cloudfront origin request policy. Default: - CloudfrontGeoLocatorOriginRequestPolicy
        :param cloudfront_price_class: (experimental) The price class for the CloudFront distribution. Default: - PRICE_CLASS_100
        :param custom_domain_certificate_arn: (experimental) The ARN of the certificate. Default: - undefined
        :param custom_domain_name: (experimental) The domain name for the CloudFront distribution. Default: - undefined
        :param lambda_function_name: (experimental) A unique name to identify the lambda function. Default: - cloudfront-geo-locator
        :param s3_bucket_name: (experimental) A unique name to identify the s3 bucket. Default: - cloudfront-geo-locator-origin
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb281bb926aebed89ca79a71242c3426e47a7e9b8f8cd4ff25fa4b33947b326)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudfrontGeoLocatorProps(
            cloudfront_cache_policy_name=cloudfront_cache_policy_name,
            cloudfront_origin_request_policy_name=cloudfront_origin_request_policy_name,
            cloudfront_price_class=cloudfront_price_class,
            custom_domain_certificate_arn=custom_domain_certificate_arn,
            custom_domain_name=custom_domain_name,
            lambda_function_name=lambda_function_name,
            s3_bucket_name=s3_bucket_name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cloudfrontCachePolicyId")
    def cloudfront_cache_policy_id(self) -> builtins.str:
        '''(experimental) The ID of the CloudFront cache policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cloudfrontCachePolicyId"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontOriginRequestPolicyId")
    def cloudfront_origin_request_policy_id(self) -> builtins.str:
        '''(experimental) The ID of the CloudFront origin request policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "cloudfrontOriginRequestPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        '''(experimental) The domain name of the CloudFront distribution.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionDomainName"))

    @builtins.property
    @jsii.member(jsii_name="distributionId")
    def distribution_id(self) -> builtins.str:
        '''(experimental) The ID of the CloudFront distribution.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionId"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionArn")
    def lambda_function_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Lambda function.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "lambdaFunctionArn"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunctionVersion")
    def lambda_function_version(self) -> _aws_cdk_aws_lambda_ceddda9d.Version:
        '''(experimental) The current version of the Lambda function.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Version, jsii.get(self, "lambdaFunctionVersion"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketArn")
    def s3_bucket_arn(self) -> builtins.str:
        '''(experimental) The ARN of the S3 bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3BucketArn"))


@jsii.data_type(
    jsii_type="cdk-cloudfront-geo-locator.CloudfrontGeoLocatorProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cloudfront_cache_policy_name": "cloudfrontCachePolicyName",
        "cloudfront_origin_request_policy_name": "cloudfrontOriginRequestPolicyName",
        "cloudfront_price_class": "cloudfrontPriceClass",
        "custom_domain_certificate_arn": "customDomainCertificateArn",
        "custom_domain_name": "customDomainName",
        "lambda_function_name": "lambdaFunctionName",
        "s3_bucket_name": "s3BucketName",
    },
)
class CloudfrontGeoLocatorProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cloudfront_cache_policy_name: typing.Optional[builtins.str] = None,
        cloudfront_origin_request_policy_name: typing.Optional[builtins.str] = None,
        cloudfront_price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        custom_domain_certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        lambda_function_name: typing.Optional[builtins.str] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for the CloudfrontGeoLocator construct.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cloudfront_cache_policy_name: (experimental) A unique name to identify the cloudfront cache policy. Default: - CloudfrontGeoLocatorCachePolicy
        :param cloudfront_origin_request_policy_name: (experimental) A unique name to identify the cloudfront origin request policy. Default: - CloudfrontGeoLocatorOriginRequestPolicy
        :param cloudfront_price_class: (experimental) The price class for the CloudFront distribution. Default: - PRICE_CLASS_100
        :param custom_domain_certificate_arn: (experimental) The ARN of the certificate. Default: - undefined
        :param custom_domain_name: (experimental) The domain name for the CloudFront distribution. Default: - undefined
        :param lambda_function_name: (experimental) A unique name to identify the lambda function. Default: - cloudfront-geo-locator
        :param s3_bucket_name: (experimental) A unique name to identify the s3 bucket. Default: - cloudfront-geo-locator-origin

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea747f64b4676813f071a3e4cca17de7e0563361efd0b0b921b5fdaf906eec96)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cloudfront_cache_policy_name", value=cloudfront_cache_policy_name, expected_type=type_hints["cloudfront_cache_policy_name"])
            check_type(argname="argument cloudfront_origin_request_policy_name", value=cloudfront_origin_request_policy_name, expected_type=type_hints["cloudfront_origin_request_policy_name"])
            check_type(argname="argument cloudfront_price_class", value=cloudfront_price_class, expected_type=type_hints["cloudfront_price_class"])
            check_type(argname="argument custom_domain_certificate_arn", value=custom_domain_certificate_arn, expected_type=type_hints["custom_domain_certificate_arn"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if cloudfront_cache_policy_name is not None:
            self._values["cloudfront_cache_policy_name"] = cloudfront_cache_policy_name
        if cloudfront_origin_request_policy_name is not None:
            self._values["cloudfront_origin_request_policy_name"] = cloudfront_origin_request_policy_name
        if cloudfront_price_class is not None:
            self._values["cloudfront_price_class"] = cloudfront_price_class
        if custom_domain_certificate_arn is not None:
            self._values["custom_domain_certificate_arn"] = custom_domain_certificate_arn
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if lambda_function_name is not None:
            self._values["lambda_function_name"] = lambda_function_name
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront_cache_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique name to identify the cloudfront cache policy.

        :default: - CloudfrontGeoLocatorCachePolicy

        :stability: experimental
        '''
        result = self._values.get("cloudfront_cache_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront_origin_request_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique name to identify the cloudfront origin request policy.

        :default: - CloudfrontGeoLocatorOriginRequestPolicy

        :stability: experimental
        '''
        result = self._values.get("cloudfront_origin_request_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudfront_price_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass]:
        '''(experimental) The price class for the CloudFront distribution.

        :default: - PRICE_CLASS_100

        :stability: experimental
        '''
        result = self._values.get("cloudfront_price_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass], result)

    @builtins.property
    def custom_domain_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the certificate.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("custom_domain_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The domain name for the CloudFront distribution.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique name to identify the lambda function.

        :default: - cloudfront-geo-locator

        :stability: experimental
        '''
        result = self._values.get("lambda_function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique name to identify the s3 bucket.

        :default: - cloudfront-geo-locator-origin

        :stability: experimental
        '''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudfrontGeoLocatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudfrontGeoLocator",
    "CloudfrontGeoLocatorProps",
]

publication.publish()

def _typecheckingstub__6eb281bb926aebed89ca79a71242c3426e47a7e9b8f8cd4ff25fa4b33947b326(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloudfront_cache_policy_name: typing.Optional[builtins.str] = None,
    cloudfront_origin_request_policy_name: typing.Optional[builtins.str] = None,
    cloudfront_price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    custom_domain_certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    lambda_function_name: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea747f64b4676813f071a3e4cca17de7e0563361efd0b0b921b5fdaf906eec96(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    cloudfront_cache_policy_name: typing.Optional[builtins.str] = None,
    cloudfront_origin_request_policy_name: typing.Optional[builtins.str] = None,
    cloudfront_price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    custom_domain_certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    lambda_function_name: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
