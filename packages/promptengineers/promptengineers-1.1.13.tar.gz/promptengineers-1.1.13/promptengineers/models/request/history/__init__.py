from promptengineers.models.history import History, HISTORY

class ReqBodyHistory(History): # pylint: disable=too-few-public-methods

	class Config: # pylint: disable=too-few-public-methods
		"""Request body for settings"""
		json_schema_extra = {
			"example": HISTORY
		}