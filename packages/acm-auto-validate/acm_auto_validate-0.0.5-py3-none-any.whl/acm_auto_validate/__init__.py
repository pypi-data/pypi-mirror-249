'''
# ACM Auto-Validate Construct

## Overview

The ACM Auto-Validate Construct is designed to automate the validation of AWS Certificate Manager (ACM) certificates using DNS validation, especially useful in continuous deployment pipelines. It handles the complexity of validating certificates in a hosted zone that resides in a different AWS account. This automation ensures that certificates requested during infrastructure deployment are validated promptly, allowing CloudFormation templates to proceed without waiting for manual intervention.

## Use Case

This construct was initially created to support CDK-based deployment pipelines where certificates requested remained pending validation. By automating this step, it significantly reduces the deployment time and manual overhead, especially in cross-account DNS validation scenarios.

## Features

* **Automated DNS Validation**: Automates the creation and deletion of DNS records for ACM certificate validation.
* **Cross-Account Support**: Capable of handling DNS records in a hosted zone that is in a different AWS account.
* **Event-Driven**: Utilizes AWS Lambda and Amazon EventBridge to respond to certificate request events.
* **SSM Parameter Tracking**: Tracks the certificates processed using AWS Systems Manager Parameter Store. Note that SSM parameters are created in the `us-east-1` region, but this construct can be deployed to any region that supports ACM, Lambda, and EventBridge.

## Prerequisites

* Two AWS accounts: a source account where the ACM certificates are requested and a zone account where the hosted zone resides.
* IAM permissions to create necessary resources in both accounts.
* AWS CDK v2 installed.

## Installation

To use this construct, install it from npm:

```bash
npm install acm-auto-validate
```

Python installation:

```bash
pip install acm-auto-validate
```

## Usage

Here's an example of how to use these constructs in your CDK application:

TypeScript

```python
import { ACMValidationConstruct, DnsValidationRoleConstruct } from 'acm-auto-validate';
import { App, Stack } from 'aws-cdk-lib';

const app = new App();

// Create a stack in the account where certificates will be requested
const sourceStack = new Stack(app, 'SourceStack', {
  env: { account: '111111111111' }  // source account ID
});

// Deploy the ACM validation construct in the source account stack
new ACMValidationConstruct(sourceStack, 'ACMValidationConstruct', {
  rolePrefix: 'prod',  // must match prefix used in DnsValidationRoleConstruct
  zoneAccountId: '222222222222',
  zoneName: 'example.com',
});

// Create a stack in the account where the zone is hosted
const zoneStack = new Stack(app, 'ZoneStack', {
  env: { account: '222222222222' }  // zone account ID
});

// Deploy the DNS validation role construct in the zone account stack
new DnsValidationRoleConstruct(zoneStack, 'DnsValidationRoleConstruct', {
  rolePrefix: 'prod',  // must match prefix used in ACMValidationConstruct
  sourceAcctId: '111111111111',
  zoneAcctId: '222222222222',
});
```

Python

```python
from aws_cdk import App, Stack
from acm_auto_validate import (
    ACMValidationConstruct,
    DnsValidationRoleConstruct
)

app = App()

# Create a stack in the account where certificates will be requested
source_stack = Stack(app, 'SourceStack', env={'account': '111111111111'})

# Deploy the ACM validation construct in the source account stack
ACMValidationConstruct(
    source_stack,
    'ACMValidationConstruct',
    role_prefix='prod',  # must match prefix used in DnsValidationRoleConstruct
    zone_account_id='222222222222',
    zone_name='example.com'
)

# Create a stack in the account where the zone is hosted
zone_stack = Stack(app, 'ZoneStack', env={'account': '222222222222'})

# Deploy the DNS validation role construct in the zone account stack
DnsValidationRoleConstruct(
    zone_stack,
    'DnsValidationRoleConstruct',
    role_prefix='prod',  # must match prefix used in ACMValidationConstruct
    source_acct_id='111111111111',
    zone_acct_id='222222222222'
)

app.synth()
```

## Configuration

* `ACMValidationConstruct`: Deploys the Lambda function (written in Python) and EventBridge rule in the source account. Requires a rolePrefix (such as 'dev' or 'prod'; this is used for naming resources), the zone account ID and the zone name.
* `DnsValidationRoleConstruct`: Deploys the IAM role in the zone account, which the Lambda function assumes. Requires a rolePrefix (such as 'dev' or 'prod'; this is used for naming resources), the source account ID, and the zone account ID.

## Contributing

Contributions to this project are welcome. Please follow the standard procedures for submitting issues or pull requests.

## License

This project is distributed under the [Apache License 2.0](LICENSE).
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


class ACMValidationConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="acm-auto-validate.ACMValidationConstruct",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        role_prefix: builtins.str,
        zone_account_id: builtins.str,
        zone_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role_prefix: 
        :param zone_account_id: 
        :param zone_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1851ad0879b82e1ac3f1c783c775f2d80cf2cda9e74edf26e53aca38aa2f13c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ACMValidationConstructProps(
            role_prefix=role_prefix,
            zone_account_id=zone_account_id,
            zone_name=zone_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="acm-auto-validate.ACMValidationConstructProps",
    jsii_struct_bases=[],
    name_mapping={
        "role_prefix": "rolePrefix",
        "zone_account_id": "zoneAccountId",
        "zone_name": "zoneName",
    },
)
class ACMValidationConstructProps:
    def __init__(
        self,
        *,
        role_prefix: builtins.str,
        zone_account_id: builtins.str,
        zone_name: builtins.str,
    ) -> None:
        '''
        :param role_prefix: 
        :param zone_account_id: 
        :param zone_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040201ae6f6f55896fbe51f566d27f2f34eadc054a2a2488dd5b7c32324f374a)
            check_type(argname="argument role_prefix", value=role_prefix, expected_type=type_hints["role_prefix"])
            check_type(argname="argument zone_account_id", value=zone_account_id, expected_type=type_hints["zone_account_id"])
            check_type(argname="argument zone_name", value=zone_name, expected_type=type_hints["zone_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_prefix": role_prefix,
            "zone_account_id": zone_account_id,
            "zone_name": zone_name,
        }

    @builtins.property
    def role_prefix(self) -> builtins.str:
        result = self._values.get("role_prefix")
        assert result is not None, "Required property 'role_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_account_id(self) -> builtins.str:
        result = self._values.get("zone_account_id")
        assert result is not None, "Required property 'zone_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_name(self) -> builtins.str:
        result = self._values.get("zone_name")
        assert result is not None, "Required property 'zone_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ACMValidationConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsValidationRoleConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="acm-auto-validate.DnsValidationRoleConstruct",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        role_prefix: builtins.str,
        source_acct_id: builtins.str,
        zone_acct_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role_prefix: 
        :param source_acct_id: 
        :param zone_acct_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f3d85188203e5dd476bcb2c374196b11b1099c6d4d1d6a1a07399f06c04063e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DnsValidationRoleConstructProps(
            role_prefix=role_prefix,
            source_acct_id=source_acct_id,
            zone_acct_id=zone_acct_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="acm-auto-validate.DnsValidationRoleConstructProps",
    jsii_struct_bases=[],
    name_mapping={
        "role_prefix": "rolePrefix",
        "source_acct_id": "sourceAcctId",
        "zone_acct_id": "zoneAcctId",
    },
)
class DnsValidationRoleConstructProps:
    def __init__(
        self,
        *,
        role_prefix: builtins.str,
        source_acct_id: builtins.str,
        zone_acct_id: builtins.str,
    ) -> None:
        '''
        :param role_prefix: 
        :param source_acct_id: 
        :param zone_acct_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76107b5234fb8dc62338968a8446e7f5a93197b9b2a7061cdfe5db0f7f99f88f)
            check_type(argname="argument role_prefix", value=role_prefix, expected_type=type_hints["role_prefix"])
            check_type(argname="argument source_acct_id", value=source_acct_id, expected_type=type_hints["source_acct_id"])
            check_type(argname="argument zone_acct_id", value=zone_acct_id, expected_type=type_hints["zone_acct_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_prefix": role_prefix,
            "source_acct_id": source_acct_id,
            "zone_acct_id": zone_acct_id,
        }

    @builtins.property
    def role_prefix(self) -> builtins.str:
        result = self._values.get("role_prefix")
        assert result is not None, "Required property 'role_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_acct_id(self) -> builtins.str:
        result = self._values.get("source_acct_id")
        assert result is not None, "Required property 'source_acct_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_acct_id(self) -> builtins.str:
        result = self._values.get("zone_acct_id")
        assert result is not None, "Required property 'zone_acct_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsValidationRoleConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ACMValidationConstruct",
    "ACMValidationConstructProps",
    "DnsValidationRoleConstruct",
    "DnsValidationRoleConstructProps",
]

publication.publish()

def _typecheckingstub__1851ad0879b82e1ac3f1c783c775f2d80cf2cda9e74edf26e53aca38aa2f13c6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    role_prefix: builtins.str,
    zone_account_id: builtins.str,
    zone_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040201ae6f6f55896fbe51f566d27f2f34eadc054a2a2488dd5b7c32324f374a(
    *,
    role_prefix: builtins.str,
    zone_account_id: builtins.str,
    zone_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3d85188203e5dd476bcb2c374196b11b1099c6d4d1d6a1a07399f06c04063e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    role_prefix: builtins.str,
    source_acct_id: builtins.str,
    zone_acct_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76107b5234fb8dc62338968a8446e7f5a93197b9b2a7061cdfe5db0f7f99f88f(
    *,
    role_prefix: builtins.str,
    source_acct_id: builtins.str,
    zone_acct_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
