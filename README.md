# random-tools
Some random tools and stuff, mostly for work but also not always.

## s3curl

ECS version.

Set up your .s3curl file in the home directory like this:

```
%awsSecretAccessKeys = (
    profile1 => {
        id => 'ID1GOESHERE',
        key => 'KEY1GOESHERE',
    },
   profile2 => {
        id => 'ID2GOESHERE',
        key => 'KEY2GOESHERE',
    },
);
push @endpoints , (
    'endpoint.aws.com',
);
```

List the accessible buckets like:

`./s3curl.pl --id=profile1 --debug https://citz-dev-exchange.objectstore.gov.bc.ca`

Then call the bucket like:

`./s3curl.pl --id=profile1 https://citz-dev-exchange.objectstore.gov.bc.ca/bucketname/`
