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
