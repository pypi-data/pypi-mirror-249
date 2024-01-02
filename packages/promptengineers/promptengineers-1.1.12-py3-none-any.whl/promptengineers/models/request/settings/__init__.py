from promptengineers.models.settings import ChatSettings, CHAT_SETTINGS

class ReqBodySettings(ChatSettings): # pylint: disable=too-few-public-methods

	class Config: # pylint: disable=too-few-public-methods
		"""Request body for settings"""
		json_schema_extra = {
			"example": CHAT_SETTINGS
		}