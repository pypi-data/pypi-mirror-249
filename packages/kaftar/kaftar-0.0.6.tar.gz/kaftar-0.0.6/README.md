# Kaftar SDK

## Usage

Package installation

``` bash
pip install kaftar
```

Usage:

``` python
import uuid
from kaftar import Notification


app = Notification('app_name')
message_uuid = uuid.uuid4()
recipients = [
    {
        'receiver': "076f08cc-4122-400a-bffa-2a0157ba57eb",  # can be email or phone number
        'message_uuid': str(message_uuid),
        'uuid': "076f08cc-4122-400a-bffa-2a0157ba57eb"
    }
]

app.send_notification(
    {
        'subject': 'Course updated222',
        'content': 'Course is available now'
    },
    [
        {
            'receiver': "076f08cc-4122-400a-bffa-2a0157ba57eb",  # can be email or phone number
            'message_uuid': str(message_uuid),
            'uuid': "076f08cc-4122-400a-bffa-2a0157ba57eb"
        }
    ],
    int(time.time()),
    group_uuid=uuid.uuid4() # Optional
)

```
