from enum import Enum

class EventSource(Enum):
    APIGateway: str = 'APIGateway'
    Lambda: str = 'Lambda'
    S3Bucket: str = "S3Bucket"
    Unknown: str = 'Unknown'
