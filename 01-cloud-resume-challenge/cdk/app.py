#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.resume_stack import CloudResumeStack

app = cdk.App()
CloudResumeStack(app, "CloudResumeStack", env=cdk.Environment(region="us-east-1"))
app.synth()
