# GETTING STARTED - Complete Step-by-Step Guide

This guide assumes you have **zero software development experience** with Git, Terraform, or CDK. Follow each step exactly as written.

> ⚠️ **OS Note:** All commands in this guide are written for **macOS**. If you're using Windows or Linux, you'll need to adapt accordingly — for example, replace `brew install` with your package manager (`apt`, `choco`, `winget`), adjust file paths, and use your OS-equivalent terminal. The Terraform and CDK commands themselves are cross-platform.

---

## Table of Contents

1. [Install Required Tools](#1-install-required-tools)
2. [Set Up Your AWS Account for Deployments](#2-set-up-your-aws-account-for-deployments)
3. [Set Up Git and GitHub](#3-set-up-git-and-github)
4. [How Terraform Works (Explained Simply)](#4-how-terraform-works)
5. [How CDK Works (Explained Simply)](#5-how-cdk-works)
6. [Deploy Project 1: Cloud Resume Challenge](#6-deploy-project-1)
7. [Pushing to GitHub (Commit Workflow)](#17-pushing-to-github)
8. [Cleaning Up (Avoiding AWS Charges)](#18-cleaning-up)
9. [Troubleshooting Common Errors](#19-troubleshooting)

---

## 1. Install Required Tools

Open Terminal on your Mac and run each command one at a time.

### Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install AWS CLI
```bash
brew install awscli
```
Verify: `aws --version` → should show something like `aws-cli/2.x.x`

### Install Terraform
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```
Verify: `terraform --version` → should show `Terraform v1.x.x`

### Install Python 3.11+
```bash
brew install python@3.11
```
Verify: `python3 --version` → should show `Python 3.11.x` or higher

### Install Node.js (required for CDK)
```bash
brew install node
```
Verify: `node --version` → should show `v18.x.x` or higher

### Install AWS CDK
```bash
npm install -g aws-cdk
```
Verify: `cdk --version` → should show `2.x.x`

### Install Git (usually pre-installed on Mac)
```bash
git --version
```
If not installed, it will prompt you to install Xcode Command Line Tools. Say yes.

---

## 2. Set Up Your AWS Account for Deployments

### Step 2.1: Configure AWS Credentials

**Option A: Using Conduit (Amazon internal accounts):**

```bash
# Create AWS config profile
mkdir -p ~/.aws
cat >> ~/.aws/config << 'EOF'
[profile my-dev-account]
region = us-east-1
output = json
EOF

# Fetch credentials (replace ACCOUNT_ID with your 12-digit account number)
ada credentials update --provider conduit --account <ACCOUNT_ID> --role IibsAdminAccess-DO-NOT-DELETE --profile my-dev-account --once

# Set as default
export AWS_PROFILE=my-dev-account
```

> ⚠️ Conduit credentials expire after ~1 hour. Re-run the `ada credentials update` command to refresh.

**Option B: Personal AWS account:**

```bash
aws configure
```

It will ask for 4 things:
```
AWS Access Key ID [None]: PASTE_YOUR_ACCESS_KEY_HERE
AWS Secret Access Key [None]: PASTE_YOUR_SECRET_KEY_HERE
Default region name [None]: us-east-1
Default output format [None]: json
```

### Step 2.2: Verify It Works

```bash
aws sts get-caller-identity
```

You should see something like:
```json
{
    "UserId": "AIDAXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/portfolio-deployer"
}
```

If you see this, your AWS connection is working! ✅

---

## 3. Set Up Git and GitHub

### Step 3.1: Configure Your Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### Step 3.2: Generate SSH Key

GitHub no longer accepts passwords. You need an SSH key.

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

When prompted:
- **File location:** Press Enter (accept default)
- **Passphrase:** Press Enter for no passphrase (or type one you'll remember)

### Step 3.3: Add SSH Key to Your Mac's Keychain

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Step 3.4: Copy Your Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

This prints a long string starting with `ssh-ed25519`. **Select and copy the entire line.**

### Step 3.5: Add the Key to GitHub

1. Go to https://github.com (create account if needed at https://github.com/signup)
2. Click your profile icon (top right) → **Settings**
3. Left sidebar → **SSH and GPG keys**
4. Click **New SSH key**
5. Title: `MacBook 2025`
6. Key: Paste what you copied
7. Click **Add SSH key**

### Step 3.6: Test the Connection

```bash
ssh -T git@github.com
```

Type `yes` if asked about fingerprint. You should see:
```
Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

### Step 3.7: Create the Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `aws-security-portfolio`
3. Description: `AWS Security Engineering Portfolio - Terraform & CDK Python`
4. Select: **Public**
5. Do NOT check any boxes (no README, no .gitignore)
6. Click **Create repository**

### Step 3.8: Connect Your Local Project to GitHub

```bash
cd ~/Projects/01-AWS-Sec-Portfolio
git init
git add .
git commit -m "feat: initial portfolio with 5 AWS security projects"
git branch -M main
git remote add origin git@github.com:<your-username>/aws-security-portfolio.git
git push -u origin main
```

Your code is now live at: `https://github.com/<your-username>/aws-security-portfolio` 🎉

---

## 4. How Terraform Works

**Think of Terraform like a blueprint for buildings.** You write what you want, and Terraform builds it in AWS for you.

### Key Files:
- `providers.tf` — Tells Terraform you're using AWS and which region
- `variables.tf` — Settings you can change (like region, project name)
- `main.tf` — The actual infrastructure definition
- `outputs.tf` — Shows you important info after deployment (URLs, IDs)

### Key Commands (always run from inside the `terraform/` folder):

| Command | What it does |
|---------|-------------|
| `terraform init` | Downloads required plugins (run once per project) |
| `terraform plan` | Shows what will be created (preview, no changes made) |
| `terraform apply` | Actually creates the resources in AWS |
| `terraform destroy` | Deletes everything it created (saves money!) |

### How a typical deploy works:
```bash
cd 01-cloud-resume-challenge/terraform
terraform init       # First time only
terraform plan       # Review what will be created
terraform apply      # Type "yes" when prompted → resources are created
```

---

## 5. How CDK Works

**CDK is the same idea as Terraform, but written in Python.** You define AWS resources using Python code, and CDK converts it to CloudFormation and deploys it.

### Key Files:
- `app.py` — Entry point that creates the stack
- `cdk.json` — Configuration (tells CDK where app.py is)
- `requirements.txt` — Python packages needed
- `stacks/` — The actual infrastructure code

### Key Commands (always run from inside the `cdk/` folder):

| Command | What it does |
|---------|-------------|
| `python3 -m venv .venv` | Creates a Python virtual environment (run once) |
| `source .venv/bin/activate` | Activates the virtual environment |
| `pip install -r requirements.txt` | Installs CDK libraries (run once) |
| `cdk bootstrap` | Prepares your AWS account for CDK (run once per account/region) |
| `cdk diff` | Shows what will change (like terraform plan) |
| `cdk deploy` | Creates the resources in AWS |
| `cdk destroy` | Deletes everything |

### How a typical deploy works:
```bash
cd 01-cloud-resume-challenge/cdk
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap              # First time only for your account
cdk deploy                 # Type "y" when prompted
```

---

## 6. Deploy Project 1: Cloud Resume Challenge

This is the easiest project. Start here.

### Option A: Deploy with Terraform

```bash
# Navigate to the project
cd ~/Projects/01-AWS-Sec-Portfolio/01-cloud-resume-challenge/terraform

# Initialize (downloads AWS plugin)
terraform init

# Preview what will be created
terraform plan

# Deploy (type "yes" when asked)
terraform apply
```

After it finishes, you'll see outputs like:
```
website_url = "https://d1234abcd.cloudfront.net"
api_url = "https://abc123.execute-api.us-east-1.amazonaws.com/count"
s3_bucket = "cloud-resume-site-123456789012"
```

Now upload your resume site to S3:
```bash
aws s3 sync ../site/ s3://cloud-resume-site-123456789012
```

Visit the `website_url` in your browser — your resume is live! 🎉

### Option B: Deploy with CDK

```bash
cd ~/Projects/01-AWS-Sec-Portfolio/01-cloud-resume-challenge/cdk

# Set up Python environment (one time)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Bootstrap CDK (one time per account)
cdk bootstrap

# Deploy
cdk deploy
```

### Clean Up (avoid charges):
```bash
# Terraform
cd ~/Projects/01-AWS-Sec-Portfolio/01-cloud-resume-challenge/terraform
terraform destroy

# OR CDK
cd ~/Projects/01-AWS-Sec-Portfolio/01-cloud-resume-challenge/cdk
source .venv/bin/activate
cdk destroy
```

---

## 7. Pushing to GitHub (Commit Workflow)

Every time you make changes, follow this workflow:

### Check What Changed
```bash
cd ~/Projects/01-AWS-Sec-Portfolio
git status
```
This shows files you modified (red = not staged, green = staged).

### Stage Your Changes
```bash
# Stage everything:
git add .

# OR stage specific files:
git add 01-cloud-resume-challenge/terraform/main.tf
```

### Commit (Save a Snapshot)
```bash
git commit -m "feat: deploy cloud resume with Terraform"
```

Good commit messages:
- `feat: add security landing zone terraform config`
- `fix: correct IAM policy for lambda execution`
- `docs: update README with deployment instructions`

### Push to GitHub
```bash
git push
```

That's it! Your changes are now visible at `https://github.com/<your-username>/aws-security-portfolio`.

### Full Example After Deploying Project 1:
```bash
cd ~/Projects/01-AWS-Sec-Portfolio
git add .
git commit -m "feat: successfully deployed cloud resume challenge to AWS"
git push
```

---

## 8. Cleaning Up (Avoiding AWS Charges)

**IMPORTANT:** Always destroy resources when you're done testing!

### Destroy project (run from each terraform/ or cdk/ folder):
```bash
# Project 1
cd ~/Projects/01-AWS-Sec-Portfolio/01-cloud-resume-challenge/terraform
terraform destroy -auto-approve
```

### Check for leftover resources:
```bash
# Check S3 buckets
aws s3 ls

# Check running Lambda functions
aws lambda list-functions --query 'Functions[].FunctionName'
```

### Monthly cost if you forget to destroy:
- Projects 1-3: ~$0-1/month (free tier)
- Projects 4-5: ~$3-5/month (Config rules + Athena)
- **All projects running:** ~$5-10/month max

---

## 9. Troubleshooting Common Errors

### "No valid credential sources found"
```bash
aws configure    # Re-enter your access key and secret
```

### "Error: No configuration files"
You're not in the right directory. Make sure you `cd` into the `terraform/` or `cdk/` folder first.

### "ResourceAlreadyExistsException"
The resource already exists from a previous deploy. Either:
- Run `terraform destroy` first, then `terraform apply` again
- Or import it: `terraform import aws_resource.name resource-id`

### "cdk bootstrap" fails
Make sure your AWS credentials are set and you have admin access:
```bash
aws sts get-caller-identity   # Should show your user
cdk bootstrap aws://ACCOUNT_ID/us-east-1
```

### "Permission denied (publickey)" when pushing to GitHub
Your SSH key isn't set up correctly:
```bash
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com         # Test connection
```

### Terraform state lock error
Someone (or a crashed process) has the state locked:
```bash
terraform force-unlock LOCK_ID
```

### CDK "This stack uses assets" error
You need to bootstrap first:
```bash
cdk bootstrap
```

---
