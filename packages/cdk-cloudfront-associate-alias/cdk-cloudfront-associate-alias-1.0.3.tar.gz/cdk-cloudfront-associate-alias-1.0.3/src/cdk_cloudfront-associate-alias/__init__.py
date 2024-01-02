'''
# cdk-cloudfront-associate-alias

A simple construct to handle automated Cloudfront DNS alias migration with zero downtime.

[NPM Package](https://www.npmjs.com/package/cdk-cloudfront-associate-alias)

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-cloudfront-associate-alias)](https://constructs.dev/packages/cdk-cloudfront-associate-alias)

## Usage

Usage of this construct is fairly straightforward. Simply pass in the Cloudfront distribution, the Route53 hosted zone, and the alias you want to associate with the distribution.

```python
const customDomain = "example.com";
const hostedZone = route53.HostedZone.fromLookup(this, "HostedZone", {
    domainName: DOMAIN_NAME,
});
const targetDistribution =
    cloudfront.Distribution.fromDistributionAttributes(
        this,
        "Distribution",
        {
            distributionId,
            domainName: distributionDomainName,
        },
    );

new CloudfrontAliasAssociator(
    this,
    "AliasAssociator",
    {
        alias: customDomain,
        hostedZone,
        targetDistribution,
    },
);
```

## What this does

This construct will create:

1. A TXT record, this is specific to the API call used, and ensures you have ownership of the domain.
2. A Custom Resource that makes an `AssociateAlias` API call to Cloudfront. This API specifically is for zero downtime alias migration in Cloudfront. This will work even if the domain isn't pre-associated.
3. An A and AAAA alias record that points to the (new) Cloudfront distribution.

## Use Cases

Notably, this construct can be used to provide Blue/Green style deployments for Cloudfront distributions. This means you can create a new distribution, associate the alias with it and this will result in zero downtime for your users.

You can also use this construct in reverse to rollback your alias to the previous deployment (or any other deployment).

For this use case, I recommend pairing this construct with the [cdk-versioned-stack-manager](https://constructs.dev/packages/cdk-versioned-stack-manager) to manage your versioned stacks.
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

import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class CloudfrontAliasAssociator(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cloudfront-associate-alias.CloudfrontAliasAssociator",
):
    '''A simple construct to handle automated Cloudfront DNS alias migration with zero downtime.

    This creates:

    - A TXT record with the name ``_${alias}`` that points to the targetDistributionDomainName.
    - A Cloudfront custom resource "Custom::CloudfrontAssociateAlias" that associates the alias with the targetDistributionId.

      - Because we use the SDK here, this construct can be used as part of a versioned deployment, and can be used for both standard and rollback scenarios.

    - A Route53 A and AAAA record that alias to the targetDistribution.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: "ICloudfrontAliasAssociatorProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89356deaf5207ec86fa82564e4be83ba93ba8b55a662afe022e04a0cd61f22dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])


@jsii.interface(
    jsii_type="cdk-cloudfront-associate-alias.ICloudfrontAliasAssociatorProps"
)
class ICloudfrontAliasAssociatorProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        '''
        :alias:

        AKA "customDomain" or "the DNS record we want to affect".

        This is the domain name you want to move from one Cloudfront Distribution to another.
        Will also work if it is NOT moving (on the first run).
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="hostedZone")
    def hosted_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        '''The Route53 hosted zone that houses the customDomain.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="targetDistribution")
    def target_distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.IDistribution:
        '''The Cloudfront Distribution we want to move the alias to.'''
        ...


class _ICloudfrontAliasAssociatorPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-cloudfront-associate-alias.ICloudfrontAliasAssociatorProps"

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        '''
        :alias:

        AKA "customDomain" or "the DNS record we want to affect".

        This is the domain name you want to move from one Cloudfront Distribution to another.
        Will also work if it is NOT moving (on the first run).
        '''
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @builtins.property
    @jsii.member(jsii_name="hostedZone")
    def hosted_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        '''The Route53 hosted zone that houses the customDomain.'''
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, jsii.get(self, "hostedZone"))

    @builtins.property
    @jsii.member(jsii_name="targetDistribution")
    def target_distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.IDistribution:
        '''The Cloudfront Distribution we want to move the alias to.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.IDistribution, jsii.get(self, "targetDistribution"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICloudfrontAliasAssociatorProps).__jsii_proxy_class__ = lambda : _ICloudfrontAliasAssociatorPropsProxy


__all__ = [
    "CloudfrontAliasAssociator",
    "ICloudfrontAliasAssociatorProps",
]

publication.publish()

def _typecheckingstub__89356deaf5207ec86fa82564e4be83ba93ba8b55a662afe022e04a0cd61f22dc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: ICloudfrontAliasAssociatorProps,
) -> None:
    """Type checking stubs"""
    pass
