# Moku
Moku is an utility set for AWS Lambda that allows you to ease interaction between other AWS services.

## Supported interactions
---
### API Gateway Routing

You can map functions to execute for resources and methods received via event in the lambda handler by using the `APIGatewayRouter`.

```python
from moku.api import APIGatewayRoute, APIGatewayRouter

# You can define multiple routes and...
myroute = APIGatewayRoute(prefix="/myroute")
# ...set route events
myroute.when(path="/", method="GET").then(myaction)
...

# When using the router you only need to add them...
router = APIGatewayRouter()
router.add_route(myroute)

# And call the resolver to get your action according
# to the received event in your lambda handler
def lambda_handler(event: dict):

    action = router.resolve(
        resource=event.get("resource"),
        method=event.get("httpMethod")
    )

    return action(event)
```
---
### S3 Event Mapping

You can map functions to execute for s3 events like a put object event in the lambda handler by using the `S3EventMapper`.

```python
from moku.s3 import S3EventBuilder, S3EventMapper

# You can define your events
myevent = S3EventBuilder.on('myevent').do(myaction)

# When using the mapper you only need to add the events
mapper = S3EventMapper()
mapper.add_event(my_event)

# And call the resolver to get your action according
# to the received event in your lambda handler
def lambda_handler(events: dict):

    response_stack: list = []
    for event in events['Records']:
        event_name: str = process_event(event)
        action = mapper.resolve(event_name)
        response_stack.append(action(event))

    return response_stack
```
