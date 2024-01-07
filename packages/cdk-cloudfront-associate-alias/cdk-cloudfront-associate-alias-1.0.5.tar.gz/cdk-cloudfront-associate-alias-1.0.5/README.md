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
