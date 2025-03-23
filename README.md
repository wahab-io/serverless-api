# Serverless API with AWS CDK

This project creates a serverless API using AWS CDK with Python. It deploys an API Gateway REST API that uses a Lambda function as a proxy for all methods. The application uses CodeDeploy to deploy changes to the Lambda function and includes a GitHub Actions pipeline that leverages CodeDeploy actions to deploy changes.

## Architecture

- **API Gateway**: REST API with proxy integration to Lambda
- **Lambda**: Python 3.9 function that handles all API requests
- **CodeDeploy**: Manages Lambda deployments with traffic shifting
- **GitHub Actions**: CI/CD pipeline for automated deployments

## Prerequisites

- AWS CLI configured with appropriate permissions
- Node.js and npm installed
- Python 3.9 or higher
- AWS CDK installed (`npm install -g aws-cdk`)

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure GitHub repository secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `AWS_REGION`: Your AWS region (e.g., us-east-1)

## Deployment

### Local Deployment

To deploy the stack manually:

```
cdk deploy
```

### GitHub Actions Deployment

The project includes a GitHub Actions workflow that automatically deploys changes when you push to the main branch. The workflow:

1. Sets up the environment
2. Installs dependencies
3. Deploys the CDK stack
4. Creates a new Lambda version
5. Updates the Lambda alias
6. Creates a CodeDeploy deployment

## Making Changes

To update the Lambda function:

1. Modify the code in the `lambda/index.py` file
2. Commit and push your changes to the main branch
3. GitHub Actions will automatically deploy the changes using CodeDeploy

## Testing the API

After deployment, you can find the API URL in the CloudFormation stack outputs. Use this URL to test your API:

```
curl https://your-api-id.execute-api.region.amazonaws.com/prod/
```

## Clean Up

To remove all resources:

```
cdk destroy
```
