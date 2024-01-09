"""channel module"""

from dataclasses import dataclass

from matatika import Resource


@dataclass
class Channel(Resource):
    """Class for channel objects"""

    channel_id: str = None
    name: str = None
    workspace_id: str = None
    description: str = None
    picture: str = None
    version: str = None

    attr_translations = {
        "id": "channel_id",
        "workspaceId": "workspace_id",
    }

    @classmethod
    def from_dict(cls, resource_dict: dict):
        channel, channel_dict = super().from_dict(resource_dict)

        channel.channel_id = channel_dict.get("channel_id")
        channel.name = channel_dict.get("name")
        channel.workspace_id = channel_dict.get("workspace_id")
        channel.description = channel_dict.get("description")
        channel.picture = channel_dict.get("picture")

        return channel


@dataclass
class ChannelV0_1(Channel):  # pylint: disable=invalid-name
    """Class for channel resource version 0.1"""

    version: str = "channels/v0.1"
