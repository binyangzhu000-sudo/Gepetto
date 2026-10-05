import openai
import json
import httpx as _httpx

import gepetto.config
import gepetto.models.model_manager
from gepetto.models.openai import GPT

_ = gepetto.config._

# Define all available Atlas Cloud models
DEFAULT_MODELS = [
    "deepseek-ai/DeepSeek-V3.1-Terminus",
    "deepseek-ai/DeepSeek-V3.2-Exp",
    "Qwen/Qwen3-235B-A22B-Instruct-2507",
    "moonshotai/kimi-k2.7-code",
    "moonshotai/kimi-k3",
    "zai-org/glm-4.7",
    "zai-org/glm-5"
]

class AtlasCloud(GPT):
    @staticmethod
    def get_menu_name() -> str:
        return "Atlas Cloud"

    @staticmethod
    def supported_models():
        # Check if custom models are defined in config
        # If not, use the default models
        config_models = gepetto.config.get_config("AtlasCloud", "MODELS")
        if config_models:
            try:
                return json.loads(config_models)
            except json.JSONDecodeError:
                # If it's not valid JSON, treat it as comma-separated list
                return [model.strip() for model in config_models.split(",")]
        return DEFAULT_MODELS

    @staticmethod
    def is_configured_properly() -> bool:
        # The plugin is configured properly if the API key is provided
        return bool(gepetto.config.get_config("AtlasCloud", "API_KEY"))

    def __init__(self, model):
        try:
            super().__init__(model)
        except ValueError:
            pass

        self.model = model
        api_key = gepetto.config.get_config("AtlasCloud", "API_KEY")
        if not api_key:
            raise ValueError(
                _("Please edit the configuration file to insert your {api_provider} API key!")
                .format(api_provider=AtlasCloud.get_menu_name()))

        proxy = gepetto.config.get_config("Gepetto", "PROXY")
        base_url = gepetto.config.get_config("AtlasCloud", "BASE_URL",
                                           default="https://api.atlascloud.ai/v1")

        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=_httpx.Client(proxy=proxy) if proxy else None)

gepetto.models.model_manager.register_model(AtlasCloud)
