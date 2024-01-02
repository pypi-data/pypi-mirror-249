from langchain.prompts import PromptTemplate

PREFIX = """{character}

You should think step by step to find the answer.

TOOLS:
------

You has access to the following tools:"""

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, \
or there is not a available tool for using, you MUST use the format:

```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```"""

SUFFIX = """Begin!
Previous conversation history:
{chat_history}

(You do not need to use these pieces of information if not relevant)

You MUST always respond to me in {language}. 
If the response is not {language}, You should translate it to {language}.
You should think step by step.

Human: {input}
{agent_scratchpad}"""

SUFFIX_WITHOUT_HISTORY = """Begin!

(You do not need to use these pieces of information if not relevant)

You MUST always respond to me in {language}. 
If the response is not {language}, You should translate it to {language}.
You should think step by step.

Human: {input}
{agent_scratchpad}"""

_rephrase_question_template = """Given the following conversation and user input questions.
You should think carefully, If the conversation are related to user input questions, rephrase a new standalone question \
based on these contents. If the conversation has nothing to do with the user input question, use the entered question \
as an independent question directly.

Chat History:
{chat_history}
Follow Up Input: {input}
Standalone question:"""
REPHRASE_QUESTION_PROMPT = PromptTemplate.from_template(_rephrase_question_template)

# You are a friendly Assistant that having a conversation with a human. You NEVER \
# answer that you are an AI language model. If you don't know the answer truthfully \
# say you don't have an answer. Don't make up an answer.
# _summary_map_prompt_template = """Write a concise summary of the following:
# "{text}"
# CONCISE SUMMARY:"""
# SUMMARY_MAP_PROMPT = PromptTemplate(template=_summary_map_prompt_template, input_variables=["text"])
#
# _summary_combine_prompt_template = """Combine these summaries in 500 words:
# "{text}"
# COMBINED SUMMARY:"""
# SUMMARY_COMBINE_PROMPT = PromptTemplate(template=_summary_combine_prompt_template, input_variables=["text"])
#
# _translate_prompt_template = """You are professional Translator to translate following text to {language}.
#
# {input}"""
# TRANSLATE_PROMPT = PromptTemplate(template=_translate_prompt_template, input_variables=["input", "language"], )
#
