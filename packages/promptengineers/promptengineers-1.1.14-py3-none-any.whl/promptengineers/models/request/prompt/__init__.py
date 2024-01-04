from promptengineers.models.prompt import PromptSystem

class ReqBodyPromptSystem(PromptSystem): # pylint: disable=too-few-public-methods

	class Config: # pylint: disable=too-few-public-methods
		"""Prompt System Template"""
		json_schema_extra = {
			"example": {
				"title": "Helpful Assistant Prompt",
				"system": "You are a helpful {ASSISTANT_TYPE} assistant. You have have been given context to {INDEX_NAME} to answer user questions.",
				"variables": {
					"ASSISTANT_TYPE": 'document retreival',
					"INDEX_NAME": 'Stripe API docs'
                }
			}
		}