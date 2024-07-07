# Moku
Moku is an utility set for AWS Lambda that allows you to ease interaction between other AWS services.

## Supported interactions

### API Gateway Routing

You can map functions to execute for resources and methods received via event in the lambda handler by using the `APIGatewayRouter`.

```python
from moku.api import APIGatewayRoute, APIGatewayRouter

# You can define multiple routes and...
myroute = APIGatewayRoute(prefix="/myroute")
# ...set route events
myroute.route(path="/", method="GET").to(myaction)
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
mapper.add_event(myevent)

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
---
### WebSockets API Gateway Routing

You can map functions to execute for route keys received via event in the lambda handler by using the `WebSocketAPIRouter`.

```python
from moku.ws import WebSocketAPIRouter


router = WebSocketAPIRouter()

# You can define your events by route key
router.on("$connect").perform(action)

# And call the resolver to get your action according
# to the received route key in your lambda handler
def lambda_handler(event: dict):

    route_key = event["requestContext"].get("routeKey")
    action = router.resolve(route_key)

    return action(event)
```
---
### Authorizer Mapping

You can map authorizer functions and keep all your different authorizers in one place by using the `AuthorizerMapper`.

```python
from moku.authorizer import AuthorizerTypeBuilder, AuthorizerMapper

# You can define your authorizer functions
req_authorizer = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(
    request_procedure
)
token_authorizer = AuthorizerTypeBuilder.for_auth_type('TOKEN').use(
    token_procedure
)

# When using the mapper you only need to add the authorizers
mapper = AuthorizerMapper()
mapper.add_authorizer(req_authorizer)
mapper.add_authorizer(token_authorizer)

# And call the resolver to get your procedure according
# to the received event in your lambda handler
def lambda_handler(event: dict):

    procedure = mapper.resolve(auth_type=event.get('type'))

    return procedure(event)
```
---
### S3 Object Lambda Processor Mapping
You can map processors per file extension with object lambda `ExtensionMapper`.

```python
from moku.s3.object_lambda import ExtensionMapper, ExtensionProcessorBuilder

# You can define your processors per extension
processor = ExtensionProcessorBuilder.bind(extension).to(lambda x: x)

# When using the mapper you only need to add the extension processors
mapper = ExtensionMapper()
mapper.add_extension(processor)

# And call the resolver to get your procedure according
# to the received file extension in your lambda handler
def lambda_handler(event: dict):
    extension = find_file_extension(event)
    func = mapper.resolve(extension)
    return func(event)

```
---
### Custom Lambda Event Handler

You can defined a mapper to expect a custom type of event in order to execute some actions by using the `CustomEventHandler`.

Custom Event Example:
```json
{
    "type": "custom",
    "body": {"some": "data"},
    ...
}
```
Lambda Handler Example:
```python
from moku.lambda_function import CustomEventActionBuilder, CustomEventHandler

# Define your custom actions
custom_action = CustomEventActionBuilder.execute(action).on(
    'custom'
)
# Add them
handler = CustomEventHandler(action_selection_key="type")
handler.add_action(custom_action)

# And call the resolver to execute the action according
# to the received event in your lambda handler
def lambda_handler(event: dict)
    return handler.resolve(event)
```
If you are using `pydantic V2`, you can also specify a model validator for your event. It will be called when resolving and the object will be passed as the argument of the action instead of the original event.
```python
from pydantic import BaseModel, Field


class ContentType(BaseModel):
    message: str
    data: list


class EventValidator(BaseModel):
    type: str = Field(min_length=3)
    content: ContentType


def my_action(event: EventValidator):
    if event.content.message == "OK":
        # Do something
        pass


handler = CustomEventHandler(
    action_selection_key="type",
    event_validator=EventValidator
)
handler.add_action(my_action)
```