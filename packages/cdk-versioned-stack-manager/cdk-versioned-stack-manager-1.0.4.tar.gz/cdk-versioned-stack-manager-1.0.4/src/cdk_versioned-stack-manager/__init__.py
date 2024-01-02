'''
# cdk-versioned-stack-manager

A CDK construct for dealing with Versioned Stacks - multiple copies of the same stack that would forever grow over time without this. This prevents hitting AWS quotas, but allows for some replication.

## Usage

```python
new cdk.Stack(app, `VersionedStack-${Date.now()}`);

// Inside different stack
new VersionedStackManager(this, 'VersionedStackManager', {
  dryRun: false, // Use this to test the construct, will not actually delete but will log what it would delete
  numberOfStacksToKeep: 5, // Keep this many stacks
  requestId: new Date().toISOString(), // Should change every time you want this to run.
  sortDirection: "DESCENDING", // Optional, defaults to DESCENDING, indicates how your stackNames should be sorted
  stackNamePrefix: 'VersionedStack-' // The pertinent stack names should start with this
});
```

## Use Cases

* Blue/Green Deployments of entire stacks
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


@jsii.interface(jsii_type="cdk-versioned-stack-manager.IVersionedStackManagerProps")
class IVersionedStackManagerProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="numberOfStacksToKeep")
    def number_of_stacks_to_keep(self) -> jsii.Number:
        '''The number of stacks to keep.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="requestId")
    def request_id(self) -> builtins.str:
        '''Change this field whenever you would like the VersionedStackManager to run.

        The value can be anything, it is simply here as a trigger, and will do so on every change.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="stackNamePrefix")
    def stack_name_prefix(self) -> builtins.str:
        '''The beginning of the stack name must be consistent for the versioned stacks.

        In this way, we can only give minimal access to ONLY the stacks needed, so it is impossible to delete the wrong stacks.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dryRun")
    def dry_run(self) -> typing.Optional[builtins.bool]:
        '''Will only log what it was going to do, rather than actually doing it.

        This might make you feel better about using this tool.
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="sortDirection")
    def sort_direction(self) -> typing.Optional[builtins.str]:
        '''In case you want to sort the stacks in a different way than the default.

        The FIRST stacks will be kept, and the rest will be deleted.

        :default: DESCENDING
        '''
        ...


class _IVersionedStackManagerPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-versioned-stack-manager.IVersionedStackManagerProps"

    @builtins.property
    @jsii.member(jsii_name="numberOfStacksToKeep")
    def number_of_stacks_to_keep(self) -> jsii.Number:
        '''The number of stacks to keep.'''
        return typing.cast(jsii.Number, jsii.get(self, "numberOfStacksToKeep"))

    @builtins.property
    @jsii.member(jsii_name="requestId")
    def request_id(self) -> builtins.str:
        '''Change this field whenever you would like the VersionedStackManager to run.

        The value can be anything, it is simply here as a trigger, and will do so on every change.
        '''
        return typing.cast(builtins.str, jsii.get(self, "requestId"))

    @builtins.property
    @jsii.member(jsii_name="stackNamePrefix")
    def stack_name_prefix(self) -> builtins.str:
        '''The beginning of the stack name must be consistent for the versioned stacks.

        In this way, we can only give minimal access to ONLY the stacks needed, so it is impossible to delete the wrong stacks.
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackNamePrefix"))

    @builtins.property
    @jsii.member(jsii_name="dryRun")
    def dry_run(self) -> typing.Optional[builtins.bool]:
        '''Will only log what it was going to do, rather than actually doing it.

        This might make you feel better about using this tool.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "dryRun"))

    @builtins.property
    @jsii.member(jsii_name="sortDirection")
    def sort_direction(self) -> typing.Optional[builtins.str]:
        '''In case you want to sort the stacks in a different way than the default.

        The FIRST stacks will be kept, and the rest will be deleted.

        :default: DESCENDING
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sortDirection"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVersionedStackManagerProps).__jsii_proxy_class__ = lambda : _IVersionedStackManagerPropsProxy


class VersionedStackManager(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-versioned-stack-manager.VersionedStackManager",
):
    '''This construct will create a custom resource that will manage the versioned stacks, and if too many stacks are present, it will delete the oldest.

    This prevents inadvertent AWS Limit errors, and keeps your account clean.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IVersionedStackManagerProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f7ccbc70d0bf77fa26996f4297d1df6e16cf7b3a42f241ac9540a2f8161ad3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "IVersionedStackManagerProps",
    "VersionedStackManager",
]

publication.publish()

def _typecheckingstub__a8f7ccbc70d0bf77fa26996f4297d1df6e16cf7b3a42f241ac9540a2f8161ad3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IVersionedStackManagerProps,
) -> None:
    """Type checking stubs"""
    pass
