'''
# DMS Pattern

# Useful commands

Initialize the project:

```
npx projen
```

Run the linter:

```
npm run eslint
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

import constructs as _constructs_77d1e7e8


class S32Rds(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="dms-patterns.S32Rds",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_arn: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: The name of the S3 bucket to be used as data source.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552a74e160ca7b1d71d1b959d87350a7c3c842a653f44cee629f05855e349ac8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S32RdsProps(bucket_arn=bucket_arn)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="dms-patterns.S32RdsProps",
    jsii_struct_bases=[],
    name_mapping={"bucket_arn": "bucketArn"},
)
class S32RdsProps:
    def __init__(self, *, bucket_arn: builtins.str) -> None:
        '''
        :param bucket_arn: The name of the S3 bucket to be used as data source.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6721c1033521e1be0035ea2e58e14e787b064212f206aebe6cd75dde6892e3c)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
        }

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''The name of the S3 bucket to be used as data source.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S32RdsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "S32Rds",
    "S32RdsProps",
]

publication.publish()

def _typecheckingstub__552a74e160ca7b1d71d1b959d87350a7c3c842a653f44cee629f05855e349ac8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6721c1033521e1be0035ea2e58e14e787b064212f206aebe6cd75dde6892e3c(
    *,
    bucket_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
