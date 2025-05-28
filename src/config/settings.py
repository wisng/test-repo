import yaml
from pydantic import BaseModel


class FlaskConfig(BaseModel):
    host: str
    port: int


class Settings(BaseModel):
    flask: FlaskConfig

    @classmethod
    def from_yaml(cls, yaml_file: str = "config.yaml") -> "Settings":
        try:
            with open(yaml_file, 'r') as f:
                config_data = yaml.safe_load(f)

            # Explicitly create nested models first
            flask_config = FlaskConfig(**config_data['flask'])

            # Create final settings object
            return cls(
                flask=flask_config,
            )
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            raise


try:
    settings = Settings.from_yaml()
    print("Configuration loaded successfully!")
except Exception as e:
    print(f"Failed to load configuration: {str(e)}")
