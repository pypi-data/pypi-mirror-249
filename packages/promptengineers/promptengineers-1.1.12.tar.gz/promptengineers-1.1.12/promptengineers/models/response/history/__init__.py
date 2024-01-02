from promptengineers.models.history import HistoryDocument, HISTORY_DOCUMENT

class ResponseHistoryIndex(HistoryDocument): # pylint: disable=too-few-public-methods
	histories: list[HistoryDocument]

	class Config: # pylint: disable=too-few-public-methods
		"""Response body for history index"""
		json_schema_extra = {
			"example": {
				"histories": [HISTORY_DOCUMENT]
            }
		}

class ResponseHistoryShow(HistoryDocument): # pylint: disable=too-few-public-methods
	history: HistoryDocument

	class Config: # pylint: disable=too-few-public-methods
		"""Request body for history show"""
		json_schema_extra = {
			"example": {
				"history": HISTORY_DOCUMENT
            }
		}