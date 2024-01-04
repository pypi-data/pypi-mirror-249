from typing import List
from pydantic import BaseModel

from promptengineers.models.settings import ChatSettingDocument, CHAT_SETTING_DOCUMENT

class ResponseSettingsList(ChatSettingDocument): # pylint: disable=too-few-public-methods
	settings: List[ChatSettingDocument] = []

	class Config: # pylint: disable=too-few-public-methods
		"""Return list of agent settings"""
		json_schema_extra = {
			"example": {
				"settings": [CHAT_SETTING_DOCUMENT]
			}
		}

class ResponseSetting(ChatSettingDocument): # pylint: disable=too-few-public-methods
	setting: ChatSettingDocument

	class Config: # pylint: disable=too-few-public-methods
		"""Return single agent settings"""
		json_schema_extra = {
			"example": {
				"setting": CHAT_SETTING_DOCUMENT
			}
		}

