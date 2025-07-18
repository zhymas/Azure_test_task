import logging
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(event: func.EventGridEvent):
    try:
        event_data = event.get_json()
        blob_url = event_data.get('url', '')
        event_time = event.event_time.isoformat()
        version_id = event_data.get('versionId', None)
        blob_name = blob_url.split('/')[-1]
        container_name = blob_url.split('/')[3] if len(blob_url.split('/')) > 3 else ''

        if version_id is None:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str=os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
            container_client = blob_service_client.get_container_client(container=container_name)
            blob_client = container_client.get_blob_client(blob=blob_name)
            version_id = blob_client.get_blob_properties().version_id

        logging.info(f"Event data: {json.dumps(event_data, indent=2)}")
        logging.info(f"Blob URL: {blob_url}")
        logging.info(f"Version ID: {version_id}")
        logging.info(f"Container: {container_name}, Blob: {blob_name}")

        blob_size = event_data.get('contentLength', 0)
        logging.info(f"Using contentLength from event data: {blob_size}")

        result = {
            "blob_name": blob_name,
            "blob_size": blob_size,
            "version_id": version_id,
            "event_time": event_time
        }
        logging.info(json.dumps(result, indent=2))
    except Exception as e:
        logging.error(f"Exception occurred: {e}", exc_info=True)
        raise