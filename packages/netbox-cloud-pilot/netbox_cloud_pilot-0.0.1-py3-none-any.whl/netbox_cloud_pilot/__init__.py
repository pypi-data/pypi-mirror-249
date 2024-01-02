from importlib.metadata import metadata

from extras.plugins import PluginConfig

metadata = metadata("netbox_cloud_pilot")


class NetBoxCloudPilot(PluginConfig):
    name = metadata.get("Name").replace("-", "_")
    verbose_name = metadata.get("Summary")
    description = metadata.get("Long-Description")
    version = metadata.get("Version")
    author = metadata.get("Author")
    author_email = metadata.get("Author-email")
    base_url = "cloud-pilot"
    min_version = "3.5.0"
    max_version = "3.5.99"


config = NetBoxCloudPilot
