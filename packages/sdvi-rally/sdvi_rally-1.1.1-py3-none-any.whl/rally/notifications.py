""" Rally Notification Support

Most notifications destinations are configured with Notification Presets, typically from the UI.
You can send notifications to those recipients using this module.

Import example:

>>> from rally import notifications
"""
__all__ = [
    'send_notification'
]

from .context import context, JOB_UUID
from ._session import _getSession


# TODO this method should bypass the queue
def send_notification(destination, message, subject='No Subject: Notification from Decision Engine', attributes=None, attachments=None, group_id=None):
    """ Send a notification or email.  The notification will be queued with Rally's Notification system and sent in the future.

    :param destination: name of the notification preset, or email address
    :type destination: str
    :param message: notification contents
    :type message: str
    :param subject: notification subject, defaults to empty string
    :type subject: str, optional
    :param attributes: key value pairs to include with the notification, not supported with all notification types,
        defaults to no attributes
    :type attributes: dict, optional
    :param attachments: includes the labeled files as notification attachments, not supported with all notification
        types, defaults to no attachments
    :type attachments: list(str), optional
    :param group_id: the string value of the AWS Message Group Id to use in the notification request if applicable,
        defaults to no group
    :type group_id: str, optional

    Usage:

    >>> notifications.send_notification('Notify Preset', 'Supply Chain is complete!', subject='Asset: Yak Incorporated')

    Sending Emails:

    >>> notifications.send_notification('rally@sdvi.com', 'Did you know Rally can send emails?', subject='Basic Email')
    """
    _attachments = []
    if attachments:
        for file in attachments:
            if not isinstance(file, str):
                raise TypeError(f'invalid attachment \'{file}\' must be of type string')
            _attachments.append(file)

    if not isinstance(subject, str):
        raise TypeError(f'invalid subject \'{subject}\' must be of type string')

    s = _getSession()
    payload = {
        'destination': destination,
        'text': message,
        'jobUuid': context(JOB_UUID),
        'subject': subject,
        'format': 'raw',
        'attributes': attributes,
        'attachments': _attachments if _attachments else None,
        'messageGroupId': group_id
    }

    s.post('v1.0/notify/events/new', json=payload)
