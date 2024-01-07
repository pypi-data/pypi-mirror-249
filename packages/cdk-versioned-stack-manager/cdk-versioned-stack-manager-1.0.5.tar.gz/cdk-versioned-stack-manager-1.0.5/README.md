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
