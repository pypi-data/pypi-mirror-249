"""Module to save and load app configuration."""
import json
import logging
import os
import tempfile

log = logging.getLogger(__name__)


class Config:
    """Configuration Class."""

    def __init__(self, config_path=None, default_config=None):
        """Initializes the Config object.

        Args:
            config_path (str, optional): The path to the configuration file. Defaults to None.
            default_config (dict, optional): The default configuration. Defaults to None.

        """
        # Set the default values for the configuration
        self._config = default_config if default_config else {}

        # Set the config path to the current user's temp directory as the default
        self._config["CachePath"] = tempfile.gettempdir()
        self._config_path = config_path

        if self._config_path and self._config_path.exists():
            self.load()
        elif self._config_path:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            self.save()
            os.chmod(self._config_path, 0o600)
        else:
            log.warning("No config path set")

    def save(self):
        """Save configuration to CONFIG_FILE."""
        with open(self._config_path, "w", encoding="utf-8") as outfile:
            json.dump(self._config, outfile, indent=4)

    def load(self):
        """Load configuration from self._config_path."""
        with open(self._config_path, "r", encoding="utf-8") as infile:
            self._config = json.load(infile)

    def update(self, updates):
        """Update Configuration on disk.

        Args:
            updates (dict): Dictionary to update the configuration with.
        """
        for key, val in updates.items():
            if (key not in self._config) or (val != self._config[key]):
                self._config[key] = val
                log.debug("Updating config  {%s: %s}", key, val)
        self.save()

    def get(self, key, default=None):
        """Get specified configuration from key.

        Args:
            key (str): Key of value to get.
            default (str, optional): Default to return if None. Defaults to None.

        Returns:
            Value or None: The configuration value or None.
        """
        return self._config.get(key, default)

    def __getitem__(self, item):
        """Get Item.

        Args:
            item (str): Key for a dictionary.

        Returns:
            Value: Value of dictionary at key.
        """
        return self._config[item]

    def __setitem__(self, key, value):
        """Set Item.

        Args:
            key (str): Key for a dictionary.
            value (value): Value to set at key.
        """
        self._config[key] = value
        self.save()

    def __delitem__(self, key):
        """Delete Item in config.

        Args:
            key (str): Item to delete at key.
        """
        del self._config[key]
        self.save()

    def __contains__(self, item):
        """Check for item in Config.

        Args:
            item (str): Key to check for in config.

        Returns:
            bool: True if item is in config. Else False.
        """
        return item in self._config

    def __iter__(self):
        """Iterate through config.

        Returns:
            iterator: An iterator for the config.
        """
        return iter(self._config)
