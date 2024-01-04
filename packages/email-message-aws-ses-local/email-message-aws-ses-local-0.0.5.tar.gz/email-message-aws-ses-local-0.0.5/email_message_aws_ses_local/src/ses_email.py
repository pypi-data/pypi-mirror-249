import os
from typing import List

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from logger_local.Logger import Logger
# from message_local.MessageImportance import MessageImportance
from message_local.MessageLocal import MessageLocal
from message_local.Recipient import Recipient

load_dotenv()

EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 208
EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "email_message_aws_ses_local_python_package"
DEVELOPER_EMAIL = "emad.a@circ.zone"

logger = Logger.create_logger(object={
    "component_id": EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    "component_name": EMAIL_MESSAGE_AWS_SES_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    "component_category": "Code",
    "developer_email": DEVELOPER_EMAIL
})

MAIL_TYPE_ID = 1
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'info@circ.zone')
DEFAULT_CONFIGURATION_SET = os.getenv('CONFIGURATION_SET')


class EmailMessageAwsSesLocal(MessageLocal):
    """Assuming the usage is as follows:
    message_local = MessageLocal(...)
    message_local.__class__ = EmailMessageAwsSesLocal
    message_local.__init__()  # calling the "init" of EmailMessageAwsSesLocal
    message_local.send(...)  # calling the "send" of EmailMessageAwsSesLocal
    """
    def __init__(self, subject: str, ses_resource=None, api_type_id=MAIL_TYPE_ID, from_email=FROM_EMAIL,  # noqa
                 configuration_set=DEFAULT_CONFIGURATION_SET):
        # Don't call super().__init__(), we already have the message_local object
        self.ses_resource = ses_resource or boto3.client('ses', region_name=AWS_REGION)
        self.subject = subject
        self._api_type_id = api_type_id  # used by MessageLocal
        self.from_email = from_email
        self.configuration_set = configuration_set

    def __send_email(self, recipient_email: str, body: str) -> str:
        """Returns the message ID of the email sent and the message ID of the email saved in the database"""
        try:
            api_data = {
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': self.subject,
                },
            }

            if self.can_send(api_data=api_data, outgoing_body=api_data["Body"]):
                response = self.ses_resource.send_email(
                    Destination={'ToAddresses': [recipient_email]},
                    Message=api_data,
                    Source=os.getenv('FROM_EMAIL', 'info@circ.zone'),  # Use provided or default sender email
                    ConfigurationSetName=os.getenv('CONFIGURATION_SET', None)  # Set Configuration Set if provided
                )
                # Example MessageId: '0100018c9e7552b1-b8932399-7049-492d-ae47-8f60967f49f1-000000'
                message_id = response['MessageId']
                logger.info(f"Email sent to {recipient_email} with message ID: {message_id}",
                            object={"message_id": message_id, "destination_emails": recipient_email})
                self.after_send_attempt(outgoing_body=api_data, incoming_message=response['ResponseMetadata'],
                                        http_status_code=response['ResponseMetadata']['HTTPStatusCode'],
                                        response_body=response)
            else:
                logger.warn(f"EmailMessageAwsSesLocal.__send_email can_send is False: "
                            f"supposed to send email to {recipient_email} with body {body}")
                message_id = '0'
        except ClientError as e:
            logger.exception(f"Couldn't send email to {recipient_email}. Error: {e}")
            raise
        return message_id

    def send(self, body: str = None, to_recipients: List[Recipient] = None) -> List[int]:
        to_recipients = to_recipients or self.get_recipients()
        logger.start(object={"body": body, "recipients": to_recipients})
        messages_ids = []
        for recipient in to_recipients:
            message_body = body or self.get_body_after_text_template(recipient)
            recipient_email = recipient.get_email_address()
            if recipient_email is not None:
                if os.getenv("REALLY_SEND_EMAIL") == '1':
                    email_messageid = self.__send_email(recipient_email, message_body)
                    # TODO: subject and body should be inside ml table
                    self.set_schema("message")
                    message_id = self.insert(data_json={"email_messageid": email_messageid,
                                                        "body": body,
                                                        "subject": self.subject,
                                                        "to_profile_id": recipient.get_profile_id(),
                                                        "to_email": recipient_email,
                                                        })
                else:
                    logger.info(f"EmailMessageAwsSesLocal.send REALLY_SEND_EMAIL is off: "
                                f"supposed to send email to {recipient_email} with body {message_body}")
                    message_id = 0
            else:
                logger.warn(f"recipient.get_email() is None: {recipient}")
                message_id = 0
            messages_ids.append(message_id)
        return messages_ids
