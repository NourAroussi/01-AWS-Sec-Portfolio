# AWS Security Engineering Portfolio

Hands-on AWS security projects demonstrating infrastructure-as-code, security automation, compliance enforcement, and threat detection. Each project includes both **Terraform** and **AWS CDK (Python)** implementations.

## Projects

| # | Project | Description | Getting Started |
|---|---------|-------------|-----------------|
| 01 | [Cloud Resume Challenge](./01-cloud-resume-challenge/) | Static resume site on S3/CloudFront with serverless visitor counter (CDK + Terraform) | See below |
| 02 | [Security Landing Zone](./02-security-landing-zone/) | Multi-account security baseline: GuardDuty, Security Hub, CloudTrail, SCPs | See below |
| 03 | [Incident Response Pipeline](./03-incident-response-pipeline/) | Automated response to GuardDuty findings via EventBridge + Lambda + SNS | See below |
| 04 | [CIS Compliance Engine](./04-cis-compliance-engine/) | AWS Config rules enforcing CIS benchmarks with auto-remediation | See below |
| 05 | [Threat Detection & Log Analysis](./05-threat-detection-log-analysis/) | CloudTrail → Athena pipeline with alerting on suspicious activity | See below |
| 06-11 | [DevSecOps Projects](./DevSecOps/) | Container security, secrets rotation, CI/CD security gates, WAF, drift detection, zero trust | See below |

---

## Getting Started Per Project

### 01 — Cloud Resume Challenge

```bash
cd 01-cloud-resume-challenge

# Terraform
cd terraform
terraform init
terraform plan
terraform apply

# OR CDK
cd cdk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```

**What it builds:** S3 static site, CloudFront CDN, Lambda visitor counter, API Gateway, DynamoDB.
**Prerequisites:** AWS account with credentials configured. Site files auto-deploy from `site/` folder.

---

### 02 — Security Landing Zone

```bash
cd 02-security-landing-zone

# Terraform
cd terraform
terraform init
terraform plan
terraform apply

# OR CDK
cd cdk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```

**What it builds:** GuardDuty, Security Hub, CloudTrail org trail, SCPs for account guardrails.
**Prerequisites:** AWS Organizations with at least 2 accounts (management + member).

---

### 03 — Incident Response Pipeline

```bash
cd 03-incident-response-pipeline

# Terraform
cd terraform
terraform init
terraform plan
terraform apply

# OR CDK
cd cdk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk deploy
```

**What it builds:** EventBridge rule catching GuardDuty findings → Lambda auto-response → SNS email alerts.
**Prerequisites:** GuardDuty enabled (project 02 does this).

---

### 04 — CIS Compliance Engine

```bash
cd 04-cis-compliance-engine

# Terraform
cd terraform
terraform init
terraform plan
terraform apply

# OR CDK
cd cdk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk deploy
```

**What it builds:** AWS Config rules for CIS benchmarks + Lambda auto-remediation (e.g., close open security groups).
**Prerequisites:** AWS Config enabled in the target region.

---

### 05 — Threat Detection & Log Analysis

```bash
cd 05-threat-detection-log-analysis

# Terraform
cd terraform
terraform init
terraform plan
terraform apply

# OR CDK
cd cdk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk deploy
```

**What it builds:** CloudTrail logs → S3 → Athena queries for suspicious activity + SNS alerting.
**Prerequisites:** CloudTrail enabled (project 02 sets this up).

---

### 06-11 — DevSecOps Projects

Each project in the `DevSecOps/` folder follows the same pattern:

```bash
cd DevSecOps/<project-folder>

# Terraform
cd terraform
terraform init && terraform apply

# OR CDK
cd cdk
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cdk deploy
```

| # | Project | What it builds |
|---|---------|----------------|
| 06 | Secure Container Pipeline | ECR scanning, CodeBuild with Trivy, signed images |
| 07 | Secrets Rotation Pipeline | Secrets Manager auto-rotation via Lambda |
| 08 | GitOps Security Pipeline | CodePipeline with security gates (cfn-nag, tfsec) |
| 09 | WAF & API Security | WAF WebACL rules protecting API Gateway |
| 10 | Infrastructure Drift Detection | Lambda scheduled checks for Terraform/CloudFormation drift |
| 11 | Zero Trust Network | VPC with PrivateLink, no internet access, verified endpoints |

---

## Cleanup (Tear Down)

For any project:

```bash
# Terraform
cd <project>/terraform
terraform destroy

# CDK
cd <project>/cdk
source .venv/bin/activate
cdk destroy
```

## Tech Stack

- **IaC:** Terraform, AWS CDK (Python)
- **Languages:** Python 3.11+, HCL
- **AWS Services:** S3, CloudFront, Lambda, API Gateway, DynamoDB, GuardDuty, Security Hub, CloudTrail, Config, EventBridge, SNS, Athena, IAM, Organizations, Control Tower
- **CI/CD:** GitHub Actions

---

## Getting Started (First-Time Setup)

### Prerequisites

1. **AWS Account** — [Create one here](https://aws.amazon.com/free/) if you don't have one
2. **AWS CLI v2** — Install and configure
3. **Terraform** — v1.5+
4. **Python** — 3.11+
5. **Node.js** — 18+ (required for CDK)
6. **AWS CDK** — v2
7. **Git** — latest

### Step 1: Install Tools (macOS)

```bash
# AWS CLI
brew install awscli

# Terraform
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Python (if not already installed)
brew install python@3.11

# Node.js (required for CDK)
brew install node

# AWS CDK
npm install -g aws-cdk

# Verify installations
aws --version
terraform --version
python3 --version
node --version
cdk --version
```

### Step 2: Configure AWS Credentials

```bash
# Using Conduit (Amazon internal):
ada credentials update --provider conduit --account <ACCOUNT_ID> --role IibsAdminAccess-DO-NOT-DELETE --profile my-dev-account --once

# Set as default for this session:
export AWS_PROFILE=my-dev-account

# Verify it works
aws sts get-caller-identity
```

> ⚠️ **Note:** Credentials expire after ~1 hour. Re-run the `ada credentials update` command to refresh.

For personal AWS accounts:
```bash
aws configure
# Enter Access Key ID, Secret Key, region (us-east-1), output (json)
```

### Step 3: Set Up GitHub (Returning After 5 Years)

```bash
# 1. Configure git identity
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# 2. Generate a new SSH key (GitHub no longer supports password auth)
ssh-keygen -t ed25519 -C "your-email@example.com"
# Press Enter for default location, set a passphrase if you want

# 3. Start the SSH agent and add your key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 4. Copy your public key
cat ~/.ssh/id_ed25519.pub
# Copy the output

# 5. Add the key to GitHub:
#    → Go to github.com → Settings → SSH and GPG keys → New SSH key
#    → Paste the key, give it a name like "MacBook 2025"

# 6. Test the connection
ssh -T git@github.com
# Should say: "Hi <your-username>! You've successfully authenticated..."
```

### Step 4: Create the Repository on GitHub

```bash
# Option A: Using GitHub CLI (recommended)
brew install gh
gh auth login  # Follow prompts, choose SSH
gh repo create aws-security-portfolio --public --description "AWS Security Engineering Portfolio - Terraform & CDK"

# Option B: Manual
# → Go to github.com/new
# → Name: aws-security-portfolio
# → Public
# → Don't initialize with README (we already have one)
# → Create repository
```

### Step 5: Push This Portfolio to GitHub

```bash
cd ~/Projects/aws-security-portfolio

# Initialize git
git init
git add .
git commit -m "Initial portfolio structure"

# Connect to GitHub and push
git remote add origin git@github.com:<your-username>/aws-security-portfolio.git
git branch -M main
git push -u origin main
```

### Step 6: Daily Workflow (Git Refresher)

```bash
# After making changes:
git add .                          # Stage all changes
git commit -m "descriptive message" # Commit locally
git push                           # Push to GitHub

# Good commit message examples:
# "feat: add Terraform S3 bucket for resume site"
# "feat: implement visitor counter Lambda"
# "docs: add architecture diagram"
# "fix: correct IAM policy for Lambda execution"
```

---

## Project Structure

Each project follows this layout:

```
project-name/
├── README.md          # Project overview, architecture, deploy instructions
├── terraform/         # Terraform implementation
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   └── modules/      # (if applicable)
├── cdk/              # CDK Python implementation
│   ├── app.py
│   ├── cdk.json
│   ├── requirements.txt
│   └── stacks/
└── diagrams/         # Architecture diagrams
```

## Author

**Your Name** — Cloud Security Engineer  
[LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/your-username)
