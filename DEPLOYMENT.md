# Deployment Guide

This guide explains how to deploy the BlobEvent Azure Function to Azure.

## Prerequisites

1. **Azure CLI** installed and authenticated
2. **Azure Functions Core Tools** installed
3. **Azure Storage Account** with versioning enabled
4. **Azure Subscription** with appropriate permissions

## Step 1: Create Azure Resources

### Create Resource Group

```bash
az group create \
  --name my-blob-function-rg \
  --location eastus
```

### Create Storage Account

```bash
az storage account create \
  --name myblobfunctionstorage \
  --resource-group my-blob-function-rg \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2
```

### Enable Blob Versioning

```bash
az storage account blob-service-properties update \
  --account-name myblobfunctionstorage \
  --resource-group my-blob-function-rg \
  --enable-versioning true
```

### Create Function App

```bash
az functionapp create \
  --resource-group my-blob-function-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4 \
  --name my-blob-function-app \
  --storage-account myblobfunctionstorage \
  --os-type linux
```

## Step 2: Deploy the Function

```bash
# Navigate to your project directory
cd /path/to/your/AzureTask

# Deploy the function
func azure functionapp publish my-blob-function-app
```

## Step 3: Configure Event Grid Subscription

### Get Storage Account Resource ID

```bash
STORAGE_ACCOUNT_ID=$(az storage account show \
  --name myblobfunctionstorage \
  --resource-group my-blob-function-rg \
  --query id \
  --output tsv)
```

### Get Function App Resource ID

```bash
FUNCTION_APP_ID=$(az functionapp show \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg \
  --query id \
  --output tsv)
```

### Create Event Grid Subscription

```bash
az eventgrid event-subscription create \
  --source-resource-id $STORAGE_ACCOUNT_ID \
  --name blob-created-events \
  --endpoint-type azurefunction \
  --endpoint "$FUNCTION_APP_ID/functions/BlobEvent" \
  --included-event-types Microsoft.Storage.BlobCreated
```

## Step 4: Test the Deployment

### Create a Test Container

```bash
az storage container create \
  --name testcontainer \
  --account-name myblobfunctionstorage
```

### Upload a Test File

```bash
echo "Hello, World!" > test.txt
az storage blob upload \
  --container-name testcontainer \
  --name test.txt \
  --file test.txt \
  --account-name myblobfunctionstorage
```

### Check Function Logs

```bash
az functionapp logs tail \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg
```

## Step 5: Monitor and Troubleshoot

### View Function Logs

```bash
# Stream logs in real-time
az functionapp logs tail \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg

# View recent logs
az functionapp logs show \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg
```

### Check Function Status

```bash
az functionapp show \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg \
  --query "state"
```

### Monitor Event Grid

```bash
# List event subscriptions
az eventgrid event-subscription list \
  --source-resource-id $STORAGE_ACCOUNT_ID
```

## Environment Variables

The function uses these environment variables:

- `AzureWebJobsStorage`: Automatically set by Azure Functions
- `FUNCTIONS_WORKER_RUNTIME`: Set to `python`

## Cleanup

To remove all resources:

```bash
az group delete \
  --name my-blob-function-rg \
  --yes
```

## Troubleshooting

### Common Issues

1. **Function not triggered**: Check Event Grid subscription configuration
2. **Permission errors**: Ensure Function App has access to Storage Account
3. **Versioning not working**: Verify blob versioning is enabled on storage account
4. **Deployment failures**: Check Azure CLI authentication and permissions

### Debug Commands

```bash
# Check function app configuration
az functionapp config show \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg

# Check function app settings
az functionapp config appsettings list \
  --name my-blob-function-app \
  --resource-group my-blob-function-rg
``` 