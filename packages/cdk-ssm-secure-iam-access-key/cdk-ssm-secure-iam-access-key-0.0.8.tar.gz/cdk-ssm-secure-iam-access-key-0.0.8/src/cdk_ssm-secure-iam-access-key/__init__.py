'''
# cdk-ssm-secure-iam-access-key

Creates an IAM Access Key for a provided IAM User and stores the result in an SSM SecureString Parameter

[NPM Package](https://www.npmjs.com/package/cdk-ssm-secure-iam-access-key)

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-ssm-secure-iam-access-key)](https://constructs.dev/packages/cdk-ssm-secure-iam-access-key)

## Installation

`npm i -D cdk-ssm-secure-iam-access-key`

## Usage

```python
        const user = new iam.User(this, "SMTPUser");

        user.addToPolicy(
            new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                actions: ["ses:SendRawEmail"],
                resources: ["*"],
            })
        );

        new SSMSecureIAMAccessKey(this, "SMTPUserCredentials", {
            parameterName: "/smtpCredentials",
            user,
        });

        // JSON.stringified {accessKeyId: "...", secretAccessKey: "..."}
        return ssm.StringParameter.fromSecureStringParameterAttributes(
            this,
            "SMTPUserCredentialsSSM",
            {
                parameterName: "/smtpCredentials",
            }
        );
```
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-ssm-secure-iam-access-key.IAMAccessKey")
class IAMAccessKey(typing_extensions.Protocol):
    '''The IAMAccessKey created is stored JSON.stringified using this interface.'''

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        ...

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        ...

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        ...


class _IAMAccessKeyProxy:
    '''The IAMAccessKey created is stored JSON.stringified using this interface.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-ssm-secure-iam-access-key.IAMAccessKey"

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @access_key_id.setter
    def access_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff15d03816d1c8500f53ee04eebdfd28327ed3f8dbaa513a88b5b79257dbf9ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretAccessKey"))

    @secret_access_key.setter
    def secret_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e3d7300ccbfb0b51b9052a06e3553928a524faa7a54ba9355f54c4560080ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretAccessKey", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAMAccessKey).__jsii_proxy_class__ = lambda : _IAMAccessKeyProxy


@jsii.interface(jsii_type="cdk-ssm-secure-iam-access-key.ISSMSecureIAMAccessKeyProps")
class ISSMSecureIAMAccessKeyProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> _aws_cdk_aws_iam_ceddda9d.IUser:
        ...

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        ...


class _ISSMSecureIAMAccessKeyPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-ssm-secure-iam-access-key.ISSMSecureIAMAccessKeyProps"

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> _aws_cdk_aws_iam_ceddda9d.IUser:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IUser, jsii.get(self, "user"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISSMSecureIAMAccessKeyProps).__jsii_proxy_class__ = lambda : _ISSMSecureIAMAccessKeyPropsProxy


class SSMSecureIAMAccessKey(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ssm-secure-iam-access-key.SSMSecureIAMAccessKey",
):
    '''Custom resource that creates a new IAM access key for the given user, then stores the AccessKeyId and Secret in a SSM SecureString Parameter.

    :return: (Not actually returned) The Value of the Parameter is the JSON representation of the AccessKeyId and Secret:

    :see:

    IAMAccessKey * Example: { "accessKeyId": "AKIAXXXXXXXXXXXXXXXX", "secretAccessKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" }

    Give permission to use this secret SSM Parameter:
    ssm.StringParameter.fromSecureStringParameterAttributes(this, "ID", {
    parameterName: this.props.parameterName,
    });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: ISSMSecureIAMAccessKeyProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9851ebd5d1676bc0f3ae1628ac4915201271d9f739704072487add8bda0d46)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "IAMAccessKey",
    "ISSMSecureIAMAccessKeyProps",
    "SSMSecureIAMAccessKey",
]

publication.publish()

def _typecheckingstub__ff15d03816d1c8500f53ee04eebdfd28327ed3f8dbaa513a88b5b79257dbf9ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e3d7300ccbfb0b51b9052a06e3553928a524faa7a54ba9355f54c4560080ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9851ebd5d1676bc0f3ae1628ac4915201271d9f739704072487add8bda0d46(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: ISSMSecureIAMAccessKeyProps,
) -> None:
    """Type checking stubs"""
    pass
