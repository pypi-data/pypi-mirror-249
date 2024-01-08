from uuid import UUID

from celery import Celery


class Notification:
    def __init__(self, service_name: str, broker_url) -> None:
        self.app = Celery(service_name, broker=broker_url)
        self.service_name = service_name

    def send_notification(
            self,
            body: dict,
            recipients: list[dict],
            send_datetime: int,
            group_uuid: UUID = None
    ) -> None:
        if group_uuid:
            group_uuid = str(group_uuid)
        if type(send_datetime) is not int:
            raise ValueError("send_datetime must be string")
        if "subject" not in body or "content" not in body:
            raise ValueError("subject or content missing")

        self.app.send_task('notification.notification.send_notification',
                           (body,
                            recipients,
                            self.service_name,
                            send_datetime,
                            group_uuid),
                           queue='notification')
