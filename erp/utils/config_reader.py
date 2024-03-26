import yaml


class ConfigReader:
    """Config reader helper

    Uses yaml library to read config files into
    dicts

    """
    @staticmethod
    def read_config(config_file: str) -> dict:
        """Reads yaml file and parses to dict

        Args:
            config_file (str): config file path

        Returns:
            dict object of config file data
        """
        with open(config_file, 'r') as file:
            labels = yaml.safe_load(file)
        return labels
