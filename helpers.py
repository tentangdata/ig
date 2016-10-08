import os
import yaml


class AppConfig(object):
    DB_URL_TEMPLATE = "{}://{}:{}@{}:{}/{}"

    def __init__(self, db_type,
                 db_host, db_port, db_name,
                 db_username, db_password,
                 file_in_dir, file_out_dir,
                 posts_dir):
        self.db_type = db_type
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.file_in_dir = file_in_dir
        self.file_out_dir = file_out_dir
        self.posts_dir = posts_dir

    def get_db_url(self):
        return AppConfig.DB_URL_TEMPLATE.format(
            self.db_type,
            self.db_username,
            self.db_password,
            self.db_host,
            self.db_port,
            self.db_name
        )


class AppConfigParser(object):
    """ IG App Config Parser
     only accept yml format
    """
    def __init__(self):
        self._config_file_path = os.getenv(
            'IG_CONF_PATH',
            'config.yml'
        )

    def parse(self):
        _config = yaml.load(
            open(self._config_file_path, 'r')
        )
        return AppConfig(**_config)


if __name__ == '__main__':
    """ for running simple tests """
    app_conf_parser = AppConfigParser()
    app_conf = app_conf_parser.parse()

    assert app_conf.db_host == 'localhost'
    assert app_conf.db_type == 'postgresql'

    assert app_conf.get_db_url() \
           == 'postgresql://postgres:postgres@localhost:5432/ig'