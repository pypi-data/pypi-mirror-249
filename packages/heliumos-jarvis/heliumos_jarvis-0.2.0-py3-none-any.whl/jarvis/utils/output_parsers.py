from langchain.agents.conversational_chat.output_parser import ConvoOutputParser


class CustomOutputParser(ConvoOutputParser):
    def get_format_instructions(self) -> str:
        """Returns formatting instructions for the given output parser."""
        # return FORMAT_INSTRUCTIONS
        return super().get_format_instructions()
