'''
# Next.js Static Export S3 Site with Dynamic Routing

[NPM](https://www.npmjs.com/package/cdk-nextjs-export-s3-dynamic-routing)

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-nextjs-export-s3-dynamic-routing)](https://constructs.dev/packages/cdk-nextjs-export-s3-dynamic-routing)

*Have a more complex use case for Next.js 13? Perhaps check out [cdk-nextjs-standalone](https://constructs.dev/packages/cdk-nextjs-standalone).*

Deploy a static export Next.js site to Cloudfront and S3 while maintaining the ability to use dynamic routes.

This effectively takes all of the benefits of Next.js, including routing, code-splitting, static HTML exporting, and also gives you the benefits of a SPA (single page application). This will be mostly useful for client-generated pages, but you can also partially server side generate some data should you choose.

This may also be useful if you use Next.js SSR in other frontends, and just want to keep a consistent experience for your developers.

## Getting Started

You can use this construct effectively with no props, but here is a minimal example with a custom domain:

```python
export class MyStaticSiteStack extends cdk.Stack {
    private readonly hostedZone: route53.IHostedZone;
    private readonly customDomainName: string;
    private readonly site: NextjsExportS3DynamicRoutingSite;

    constructor(scope: sst.App, id: string, props?: sst.StackProps) {
        super(scope, id, props);

        this.hostedZone = this.findHostedZone();
        this.customDomainName = "yourdomain.com";

        this.site = this.createNextJsSite();
        this.createDnsRecord();
    }

    private findHostedZone(): route53.IHostedZone {
        return route53.HostedZone.fromLookup(this, "HostedZone", {
            domainName: this.customDomainName,
        });
    }

    private createNextJsSite(): NextjsExportS3DynamicRoutingSite {
        const certificate = new acm.Certificate(
            this,
            "Certificate",
            {
                domainName: this.customDomainName,
                validation: acm.CertificateValidation.fromDns(this.hostedZone),
            }
        );

        return new NextjsExportS3DynamicRoutingSite(this, "NextJsSite", {
            distributionProps: {
                certificate,
                domainNames: [this.customDomainName],
            }
        });
    }

    private createDnsRecord = (): route53.ARecord => {
        return new route53.ARecord(this, `AliasRecord`, {
            recordName: this.customDomainName,
            target: route53.RecordTarget.fromAlias(
                new r53Targets.CloudFrontTarget(
                    this.site.cloudfrontDistribution
                )
            ),
            zone: this.hostedZone,
        });
    };
}
```

There are no outside requirements for this construct, and it will delete all of its resources when the stack is deleted.
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

import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_cloudfront_origins as _aws_cdk_aws_cloudfront_origins_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-nextjs-export-s3-dynamic-routing.NextjsExportS3DynamicRoutingDistributionProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_behaviors": "additionalBehaviors",
        "certificate": "certificate",
        "comment": "comment",
        "default_behavior": "defaultBehavior",
        "default_root_object": "defaultRootObject",
        "domain_names": "domainNames",
        "enabled": "enabled",
        "enable_ipv6": "enableIpv6",
        "enable_logging": "enableLogging",
        "error_responses": "errorResponses",
        "geo_restriction": "geoRestriction",
        "http_version": "httpVersion",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
        "minimum_protocol_version": "minimumProtocolVersion",
        "price_class": "priceClass",
        "ssl_support_method": "sslSupportMethod",
        "web_acl_id": "webAclId",
    },
)
class NextjsExportS3DynamicRoutingDistributionProps:
    def __init__(
        self,
        *,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        default_behavior: typing.Optional[typing.Union["PartialBehaviorOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        minimum_protocol_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        ssl_support_method: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Differences from cloudfront.DistributionProps: - defaultBehavior is optional.

        :param additional_behaviors: Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: Any comments you want to include about the distribution. Default: - no comment
        :param default_behavior: The default behavior for the distribution. Optional and Partial here, not usually either in the CDK.
        :param default_root_object: The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/). Default: - no default root object
        :param domain_names: Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: Enable or disable the distribution. Default: true
        :param enable_ipv6: Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: The Amazon S3 bucket to store the access logs in. Make sure to set ``objectOwnership`` to ``s3.ObjectOwnership.OBJECT_WRITER`` in your custom bucket. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param minimum_protocol_version: The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SecurityPolicyProtocol.TLS_V1_2_2021 if the '@aws-cdk/aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021' feature flag is set; otherwise, SecurityPolicyProtocol.TLS_V1_2_2019.
        :param price_class: The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param ssl_support_method: The SSL method CloudFront will use for your distribution. Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate. CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support. If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP). See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/ Default: SSLMethod.SNI
        :param web_acl_id: Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).
        '''
        if isinstance(default_behavior, dict):
            default_behavior = PartialBehaviorOptions(**default_behavior)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad08446f9193ea6e64959961342f48326a00eb623759c2c3087941f5d4b58606)
            check_type(argname="argument additional_behaviors", value=additional_behaviors, expected_type=type_hints["additional_behaviors"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument default_behavior", value=default_behavior, expected_type=type_hints["default_behavior"])
            check_type(argname="argument default_root_object", value=default_root_object, expected_type=type_hints["default_root_object"])
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_ipv6", value=enable_ipv6, expected_type=type_hints["enable_ipv6"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument error_responses", value=error_responses, expected_type=type_hints["error_responses"])
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument log_file_prefix", value=log_file_prefix, expected_type=type_hints["log_file_prefix"])
            check_type(argname="argument log_includes_cookies", value=log_includes_cookies, expected_type=type_hints["log_includes_cookies"])
            check_type(argname="argument minimum_protocol_version", value=minimum_protocol_version, expected_type=type_hints["minimum_protocol_version"])
            check_type(argname="argument price_class", value=price_class, expected_type=type_hints["price_class"])
            check_type(argname="argument ssl_support_method", value=ssl_support_method, expected_type=type_hints["ssl_support_method"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_behaviors is not None:
            self._values["additional_behaviors"] = additional_behaviors
        if certificate is not None:
            self._values["certificate"] = certificate
        if comment is not None:
            self._values["comment"] = comment
        if default_behavior is not None:
            self._values["default_behavior"] = default_behavior
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if http_version is not None:
            self._values["http_version"] = http_version
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies
        if minimum_protocol_version is not None:
            self._values["minimum_protocol_version"] = minimum_protocol_version
        if price_class is not None:
            self._values["price_class"] = price_class
        if ssl_support_method is not None:
            self._values["ssl_support_method"] = ssl_support_method
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def additional_behaviors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]]:
        '''Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to.

        :default: - no additional behaviors are added.
        '''
        result = self._values.get("additional_behaviors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''A certificate to associate with the distribution.

        The certificate must be located in N. Virginia (us-east-1).

        :default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Any comments you want to include about the distribution.

        :default: - no comment
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_behavior(self) -> typing.Optional["PartialBehaviorOptions"]:
        '''The default behavior for the distribution.

        Optional and Partial here, not usually either in the CDK.
        '''
        result = self._values.get("default_behavior")
        return typing.cast(typing.Optional["PartialBehaviorOptions"], result)

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        '''The object that you want CloudFront to request from your origin (for example, index.html) when a viewer requests the root URL for your distribution. If no default object is set, the request goes to the origin's root (e.g., example.com/).

        :default: - no default root object
        '''
        result = self._values.get("default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Alternative domain names for this distribution.

        If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name,
        you can add an alternate domain name to your distribution. If you attach a certificate to the distribution,
        you must add (at least one of) the domain names of the certificate to this list.

        :default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable the distribution.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_ipv6(self) -> typing.Optional[builtins.bool]:
        '''Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address.

        If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses.
        This allows viewers to submit a second request, for an IPv4 address for your distribution.

        :default: true
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable access logging for the distribution.

        :default: - false, unless ``logBucket`` is specified.
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_responses(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]]:
        '''How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - No custom error responses.
        '''
        result = self._values.get("error_responses")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]], result)

    @builtins.property
    def geo_restriction(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction]:
        '''Controls the countries in which your content is distributed.

        :default: - No geographic restrictions
        '''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction], result)

    @builtins.property
    def http_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion]:
        '''Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront.

        For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI).

        :default: HttpVersion.HTTP2
        '''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''The Amazon S3 bucket to store the access logs in.

        Make sure to set ``objectOwnership`` to ``s3.ObjectOwnership.OBJECT_WRITER`` in your custom bucket.

        :default: - A bucket is created if ``enableLogging`` is true
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix
        '''
        result = self._values.get("log_file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether you want CloudFront to include cookies in access logs.

        :default: false
        '''
        result = self._values.get("log_includes_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimum_protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol]:
        '''The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

        CloudFront serves your objects only to browsers or devices that support at
        least the SSL version that you specify.

        :default: - SecurityPolicyProtocol.TLS_V1_2_2021 if the '@aws-cdk/aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021' feature flag is set; otherwise, SecurityPolicyProtocol.TLS_V1_2_2019.
        '''
        result = self._values.get("minimum_protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol], result)

    @builtins.property
    def price_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass]:
        '''The price class that corresponds with the maximum price that you want to pay for CloudFront service.

        If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations.
        If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location
        that has the lowest latency among the edge locations in your price class.

        :default: PriceClass.PRICE_CLASS_ALL
        '''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass], result)

    @builtins.property
    def ssl_support_method(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod]:
        '''The SSL method CloudFront will use for your distribution.

        Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates
        which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present
        multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites
        (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate.

        CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support.

        If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for
        using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP).

        See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/

        :default: SSLMethod.SNI
        '''
        result = self._values.get("ssl_support_method")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.
        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateDistribution.html#API_CreateDistribution_RequestParameters.
        '''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsExportS3DynamicRoutingDistributionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NextjsExportS3DynamicRoutingSite(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nextjs-export-s3-dynamic-routing.NextjsExportS3DynamicRoutingSite",
):
    '''Deploy an exported, static site using Next.js. Compatible with a Next 13 project using /pages routing.

    :see:

    For Static Site Limitations: https://nextjs.org/docs/advanced-features/static-html-export

    Additional Limitations:

    - Cloudfront function size is capped at 10KB. This may be exceeded if the amount of pages (page types, not static pages with many static paths) is extremely large, as each represents a JSON object in the code.
    - For estimation, if we assume around 1000 characters of natural overhead and average 100 characters per page type, this calculates to about 90 page types (files in the pages folder).
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_props: typing.Optional[typing.Union[NextjsExportS3DynamicRoutingDistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        next_build_dir: typing.Optional[builtins.str] = None,
        next_export_path: typing.Optional[builtins.str] = None,
        s3_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_props: Passthrough props to customize the S3 bucket. Default: { publicReadAccess: false, blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL, autoDeleteObjects: true, removalPolicy: cdk.RemovalPolicy.DESTROY, }
        :param distribution_props: Passthrough props to customize the Cloudfront distribution. Default: Sets up the S3 Origin and Cache Policy.
        :param next_build_dir: Default: ./.next
        :param next_export_path: The relative path to the Next.js project. Default: ./out
        :param s3_origin_props: Passthrough props to customize the S3 Origin. Default: S3 Origin defaults.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21505129492fd182d431623c4451967980f3702dd1daa0f7794e211855fd377)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NextjsExportS3DynamicRoutingSiteProps(
            bucket_props=bucket_props,
            distribution_props=distribution_props,
            next_build_dir=next_build_dir,
            next_export_path=next_export_path,
            s3_origin_props=s3_origin_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RECOMMENDED_CACHE_POLICY")
    def RECOMMENDED_CACHE_POLICY(
        cls,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps:
        '''Included for convenience, this cache policy is very similar to Amplify's cache policy, but with a higher maxTtl.'''
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.CachePolicyProps, jsii.sget(cls, "RECOMMENDED_CACHE_POLICY"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontDistribution")
    def cloudfront_distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.get(self, "cloudfrontDistribution"))

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.get(self, "s3Bucket"))

    @builtins.property
    @jsii.member(jsii_name="viewerRequestCloudfrontFunction")
    def viewer_request_cloudfront_function(
        self,
    ) -> _aws_cdk_aws_cloudfront_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Function, jsii.get(self, "viewerRequestCloudfrontFunction"))


@jsii.data_type(
    jsii_type="cdk-nextjs-export-s3-dynamic-routing.NextjsExportS3DynamicRoutingSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_props": "bucketProps",
        "distribution_props": "distributionProps",
        "next_build_dir": "nextBuildDir",
        "next_export_path": "nextExportPath",
        "s3_origin_props": "s3OriginProps",
    },
)
class NextjsExportS3DynamicRoutingSiteProps:
    def __init__(
        self,
        *,
        bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_props: typing.Optional[typing.Union[NextjsExportS3DynamicRoutingDistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
        next_build_dir: typing.Optional[builtins.str] = None,
        next_export_path: typing.Optional[builtins.str] = None,
        s3_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Deploy a static export Next.js site to Cloudfront and S3 while maintaining the ability to use dynamic routes.

        Deploys Cloudfront, a Cloudfront Function, an S3 Bucket, and an S3 Deployment.

        With defaults set, if this construct is removed, all resources will be cleaned up.

        :param bucket_props: Passthrough props to customize the S3 bucket. Default: { publicReadAccess: false, blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL, autoDeleteObjects: true, removalPolicy: cdk.RemovalPolicy.DESTROY, }
        :param distribution_props: Passthrough props to customize the Cloudfront distribution. Default: Sets up the S3 Origin and Cache Policy.
        :param next_build_dir: Default: ./.next
        :param next_export_path: The relative path to the Next.js project. Default: ./out
        :param s3_origin_props: Passthrough props to customize the S3 Origin. Default: S3 Origin defaults.
        '''
        if isinstance(bucket_props, dict):
            bucket_props = _aws_cdk_aws_s3_ceddda9d.BucketProps(**bucket_props)
        if isinstance(distribution_props, dict):
            distribution_props = NextjsExportS3DynamicRoutingDistributionProps(**distribution_props)
        if isinstance(s3_origin_props, dict):
            s3_origin_props = _aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps(**s3_origin_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4dc35e455689903e14416754ae4eeee55f27d1bd555c9fc86b3d3afe2067d1)
            check_type(argname="argument bucket_props", value=bucket_props, expected_type=type_hints["bucket_props"])
            check_type(argname="argument distribution_props", value=distribution_props, expected_type=type_hints["distribution_props"])
            check_type(argname="argument next_build_dir", value=next_build_dir, expected_type=type_hints["next_build_dir"])
            check_type(argname="argument next_export_path", value=next_export_path, expected_type=type_hints["next_export_path"])
            check_type(argname="argument s3_origin_props", value=s3_origin_props, expected_type=type_hints["s3_origin_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_props is not None:
            self._values["bucket_props"] = bucket_props
        if distribution_props is not None:
            self._values["distribution_props"] = distribution_props
        if next_build_dir is not None:
            self._values["next_build_dir"] = next_build_dir
        if next_export_path is not None:
            self._values["next_export_path"] = next_export_path
        if s3_origin_props is not None:
            self._values["s3_origin_props"] = s3_origin_props

    @builtins.property
    def bucket_props(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps]:
        '''Passthrough props to customize the S3 bucket.

        :default:

        {
        publicReadAccess: false,
        blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
        autoDeleteObjects: true,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        }
        '''
        result = self._values.get("bucket_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps], result)

    @builtins.property
    def distribution_props(
        self,
    ) -> typing.Optional[NextjsExportS3DynamicRoutingDistributionProps]:
        '''Passthrough props to customize the Cloudfront distribution.

        :default: Sets up the S3 Origin and Cache Policy.
        '''
        result = self._values.get("distribution_props")
        return typing.cast(typing.Optional[NextjsExportS3DynamicRoutingDistributionProps], result)

    @builtins.property
    def next_build_dir(self) -> typing.Optional[builtins.str]:
        '''
        :default: ./.next
        '''
        result = self._values.get("next_build_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def next_export_path(self) -> typing.Optional[builtins.str]:
        '''The relative path to the Next.js project.

        :default: ./out
        '''
        result = self._values.get("next_export_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_origin_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps]:
        '''Passthrough props to customize the S3 Origin.

        :default: S3 Origin defaults.
        '''
        result = self._values.get("s3_origin_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NextjsExportS3DynamicRoutingSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-nextjs-export-s3-dynamic-routing.PartialBehaviorOptions",
    jsii_struct_bases=[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "cache_policy": "cachePolicy",
        "compress": "compress",
        "edge_lambdas": "edgeLambdas",
        "function_associations": "functionAssociations",
        "origin_request_policy": "originRequestPolicy",
        "response_headers_policy": "responseHeadersPolicy",
        "smooth_streaming": "smoothStreaming",
        "trusted_key_groups": "trustedKeyGroups",
        "viewer_protocol_policy": "viewerProtocolPolicy",
        "origin": "origin",
    },
)
class PartialBehaviorOptions(_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions):
    def __init__(
        self,
        *,
        allowed_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods] = None,
        cached_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods] = None,
        cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
        compress: typing.Optional[builtins.bool] = None,
        edge_lambdas: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda, typing.Dict[builtins.str, typing.Any]]]] = None,
        function_associations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation, typing.Dict[builtins.str, typing.Any]]]] = None,
        origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
        response_headers_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy] = None,
        smooth_streaming: typing.Optional[builtins.bool] = None,
        trusted_key_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudfront_ceddda9d.IKeyGroup]] = None,
        viewer_protocol_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy] = None,
        origin: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOrigin] = None,
    ) -> None:
        '''Options for creating a new behavior.

        origin is optional here, not usually in the CDK.

        :param allowed_methods: HTTP methods to allow for this behavior. Default: AllowedMethods.ALLOW_GET_HEAD
        :param cached_methods: HTTP methods to cache for this behavior. Default: CachedMethods.CACHE_GET_HEAD
        :param cache_policy: The cache policy for this behavior. The cache policy determines what values are included in the cache key, and the time-to-live (TTL) values for the cache. Default: CachePolicy.CACHING_OPTIMIZED
        :param compress: Whether you want CloudFront to automatically compress certain files for this cache behavior. See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types for file types CloudFront will compress. Default: true
        :param edge_lambdas: The Lambda@Edge functions to invoke before serving the contents. Default: - no Lambda functions will be invoked
        :param function_associations: The CloudFront functions to invoke before serving the contents. Default: - no functions will be invoked
        :param origin_request_policy: The origin request policy for this behavior. The origin request policy determines which values (e.g., headers, cookies) are included in requests that CloudFront sends to the origin. Default: - none
        :param response_headers_policy: The response headers policy for this behavior. The response headers policy determines which headers are included in responses Default: - none
        :param smooth_streaming: Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior. Default: false
        :param trusted_key_groups: A list of Key Groups that CloudFront can use to validate signed URLs or signed cookies. Default: - no KeyGroups are associated with cache behavior
        :param viewer_protocol_policy: The protocol that viewers can use to access the files controlled by this behavior. Default: ViewerProtocolPolicy.ALLOW_ALL
        :param origin: The origin that you want CloudFront to route requests to when they match this behavior.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde990c4954add27759c23484c18675688ae08e455ff890c719dde2e2b707c0a)
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument cached_methods", value=cached_methods, expected_type=type_hints["cached_methods"])
            check_type(argname="argument cache_policy", value=cache_policy, expected_type=type_hints["cache_policy"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument edge_lambdas", value=edge_lambdas, expected_type=type_hints["edge_lambdas"])
            check_type(argname="argument function_associations", value=function_associations, expected_type=type_hints["function_associations"])
            check_type(argname="argument origin_request_policy", value=origin_request_policy, expected_type=type_hints["origin_request_policy"])
            check_type(argname="argument response_headers_policy", value=response_headers_policy, expected_type=type_hints["response_headers_policy"])
            check_type(argname="argument smooth_streaming", value=smooth_streaming, expected_type=type_hints["smooth_streaming"])
            check_type(argname="argument trusted_key_groups", value=trusted_key_groups, expected_type=type_hints["trusted_key_groups"])
            check_type(argname="argument viewer_protocol_policy", value=viewer_protocol_policy, expected_type=type_hints["viewer_protocol_policy"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cached_methods is not None:
            self._values["cached_methods"] = cached_methods
        if cache_policy is not None:
            self._values["cache_policy"] = cache_policy
        if compress is not None:
            self._values["compress"] = compress
        if edge_lambdas is not None:
            self._values["edge_lambdas"] = edge_lambdas
        if function_associations is not None:
            self._values["function_associations"] = function_associations
        if origin_request_policy is not None:
            self._values["origin_request_policy"] = origin_request_policy
        if response_headers_policy is not None:
            self._values["response_headers_policy"] = response_headers_policy
        if smooth_streaming is not None:
            self._values["smooth_streaming"] = smooth_streaming
        if trusted_key_groups is not None:
            self._values["trusted_key_groups"] = trusted_key_groups
        if viewer_protocol_policy is not None:
            self._values["viewer_protocol_policy"] = viewer_protocol_policy
        if origin is not None:
            self._values["origin"] = origin

    @builtins.property
    def allowed_methods(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods]:
        '''HTTP methods to allow for this behavior.

        :default: AllowedMethods.ALLOW_GET_HEAD
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods], result)

    @builtins.property
    def cached_methods(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods]:
        '''HTTP methods to cache for this behavior.

        :default: CachedMethods.CACHE_GET_HEAD
        '''
        result = self._values.get("cached_methods")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods], result)

    @builtins.property
    def cache_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy]:
        '''The cache policy for this behavior.

        The cache policy determines what values are included in the cache key,
        and the time-to-live (TTL) values for the cache.

        :default: CachePolicy.CACHING_OPTIMIZED

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html.
        '''
        result = self._values.get("cache_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy], result)

    @builtins.property
    def compress(self) -> typing.Optional[builtins.bool]:
        '''Whether you want CloudFront to automatically compress certain files for this cache behavior.

        See https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront-file-types
        for file types CloudFront will compress.

        :default: true
        '''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edge_lambdas(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda]]:
        '''The Lambda@Edge functions to invoke before serving the contents.

        :default: - no Lambda functions will be invoked

        :see: https://aws.amazon.com/lambda/edge
        '''
        result = self._values.get("edge_lambdas")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda]], result)

    @builtins.property
    def function_associations(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation]]:
        '''The CloudFront functions to invoke before serving the contents.

        :default: - no functions will be invoked
        '''
        result = self._values.get("function_associations")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation]], result)

    @builtins.property
    def origin_request_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy]:
        '''The origin request policy for this behavior.

        The origin request policy determines which values (e.g., headers, cookies)
        are included in requests that CloudFront sends to the origin.

        :default: - none
        '''
        result = self._values.get("origin_request_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy], result)

    @builtins.property
    def response_headers_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy]:
        '''The response headers policy for this behavior.

        The response headers policy determines which headers are included in responses

        :default: - none
        '''
        result = self._values.get("response_headers_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy], result)

    @builtins.property
    def smooth_streaming(self) -> typing.Optional[builtins.bool]:
        '''Set this to true to indicate you want to distribute media files in the Microsoft Smooth Streaming format using this behavior.

        :default: false
        '''
        result = self._values.get("smooth_streaming")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trusted_key_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.IKeyGroup]]:
        '''A list of Key Groups that CloudFront can use to validate signed URLs or signed cookies.

        :default: - no KeyGroups are associated with cache behavior

        :see: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html
        '''
        result = self._values.get("trusted_key_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.IKeyGroup]], result)

    @builtins.property
    def viewer_protocol_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy]:
        '''The protocol that viewers can use to access the files controlled by this behavior.

        :default: ViewerProtocolPolicy.ALLOW_ALL
        '''
        result = self._values.get("viewer_protocol_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy], result)

    @builtins.property
    def origin(self) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOrigin]:
        '''The origin that you want CloudFront to route requests to when they match this behavior.'''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOrigin], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PartialBehaviorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NextjsExportS3DynamicRoutingDistributionProps",
    "NextjsExportS3DynamicRoutingSite",
    "NextjsExportS3DynamicRoutingSiteProps",
    "PartialBehaviorOptions",
]

publication.publish()

def _typecheckingstub__ad08446f9193ea6e64959961342f48326a00eb623759c2c3087941f5d4b58606(
    *,
    additional_behaviors: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    comment: typing.Optional[builtins.str] = None,
    default_behavior: typing.Optional[typing.Union[PartialBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_ipv6: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_file_prefix: typing.Optional[builtins.str] = None,
    log_includes_cookies: typing.Optional[builtins.bool] = None,
    minimum_protocol_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    ssl_support_method: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21505129492fd182d431623c4451967980f3702dd1daa0f7794e211855fd377(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_props: typing.Optional[typing.Union[NextjsExportS3DynamicRoutingDistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    next_build_dir: typing.Optional[builtins.str] = None,
    next_export_path: typing.Optional[builtins.str] = None,
    s3_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4dc35e455689903e14416754ae4eeee55f27d1bd555c9fc86b3d3afe2067d1(
    *,
    bucket_props: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_props: typing.Optional[typing.Union[NextjsExportS3DynamicRoutingDistributionProps, typing.Dict[builtins.str, typing.Any]]] = None,
    next_build_dir: typing.Optional[builtins.str] = None,
    next_export_path: typing.Optional[builtins.str] = None,
    s3_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde990c4954add27759c23484c18675688ae08e455ff890c719dde2e2b707c0a(
    *,
    allowed_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods] = None,
    cached_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods] = None,
    cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
    compress: typing.Optional[builtins.bool] = None,
    edge_lambdas: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.EdgeLambda, typing.Dict[builtins.str, typing.Any]]]] = None,
    function_associations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.FunctionAssociation, typing.Dict[builtins.str, typing.Any]]]] = None,
    origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
    response_headers_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy] = None,
    smooth_streaming: typing.Optional[builtins.bool] = None,
    trusted_key_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudfront_ceddda9d.IKeyGroup]] = None,
    viewer_protocol_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy] = None,
    origin: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOrigin] = None,
) -> None:
    """Type checking stubs"""
    pass
