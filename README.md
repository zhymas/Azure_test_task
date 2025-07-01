# Azure Function: BlobCreated Event Handler

This Azure Function handles BlobCreated events from Azure Storage with versioning enabled. It processes Event Grid events and logs blob information including name, size, version ID, and event timestamp.

## Features

- ✅ Handles BlobCreated Event Grid events
- ✅ Extracts blob information (name, size, version ID, timestamp)
- ✅ Supports blob versioning scenarios
- ✅ JSON-formatted logging output
- ✅ Error handling and debugging logs
- ✅ Resource-efficient (uses event data instead of additional API calls)

## Project Structure

```
AzureTask/
├── BlobEvent/
│   ├── __init__.py          # Main function implementation
│   └── function.json        # Function configuration
├── function_app.py          # Function app entry point
├── host.json               # Host configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Function Implementation

The function (`BlobEvent/__init__.py`) processes Event Grid events and extracts:

- **Blob name**: Extracted from the blob URL
- **Blob size**: Retrieved from event data (`contentLength`)
- **Version ID**: Retrieved from event data (`versionId`)
- **Event timestamp**: Retrieved from event metadata

### Key Features

1. **Versioning Support**: Properly handles blob versioning by extracting the `versionId` from the event data
2. **Resource Efficient**: Uses event data instead of making additional API calls to the storage account
3. **Error Handling**: Comprehensive error handling with detailed logging
4. **JSON Output**: Structured JSON logging for easy parsing and monitoring

## Testing

### Local Testing

1. Start the function:
   ```bash
   func start
   ```

2. Test with Event Grid event:
   ```bash
   curl -X POST http://localhost:7071/runtime/webhooks/eventgrid \
     -H "Content-Type: application/json" \
     -H "aeg-event-type: Notification" \
     -d '{
       "eventType": "Microsoft.Storage.BlobCreated",
       "eventTime": "2025-06-22T11:21:45.813Z",
       "data": {
         "url": "https://storage.blob.core.windows.net/container/sample.csv",
         "versionId": "2024-06-18T10:13:50.4052361Z",
         "contentLength": 2048
       }
     }'
   ```

### Expected Output

```json
{
  "blob_name": "sample.csv",
  "blob_size": 2048,
  "version_id": "2024-06-18T10:13:50.4052361Z",
  "event_time": "2025-06-22T11:21:45.813Z"
}
```
## How to Unit-Test the Function (Process)

Unit-testing an Azure Function means verifying its logic in isolation, without deploying to Azure or using real cloud resources. Here's how you can approach unit-testing for this function:

1. **Use a Python test framework**: Choose `unittest` or `pytest` to organize and run your tests locally.

2. **Mock Azure dependencies**: Use mocking tools (like `unittest.mock`) to simulate Azure-specific objects, such as the Event Grid event and the logging module. This allows you to test the function's behavior without needing a real Azure environment.

3. **Simulate different event inputs**: Create mock event objects with various combinations of data (e.g., with and without `versionId`, different blob URLs, missing fields) to test how the function handles each scenario.

4. **Invoke the function directly**: Call the function with your mock event and check its behavior. Since the function logs output, you can assert that the correct log messages are produced for each input.

5. **Test error handling**: Provide malformed or incomplete event data to ensure the function logs errors and handles exceptions gracefully.

6. **No real Azure resources required**: All tests are run locally and do not require access to Azure Storage, Event Grid, or deployment to the cloud.

**Summary:**
- Unit tests for this function are fast, repeatable, and run entirely locally.
- They focus on the function's logic and its response to different event payloads, not on integration with Azure services.
- This approach ensures your function is robust and behaves as expected before deploying to Azure.