"""
This script contains a class object filled with methods that build the specific message
and handle the exceptions that need to be handled.

It takes a data object as input and formats the message with the given data.
"""
import context
from framework.framework_utils.string_utils import CustomFormatter

NEWLINE = "\n"
TAB = "\t"

DAY_MESSAGE = """
What is up. I've got one daily report for U, my friend

--------------------
{NAME}
{DESCRIPTION}
The date is {DATE}

{BODY}
--------------------
Thank you come again
"""

WEEK_MESSAGE = """
What is up. I've got one summary of last week for ypu, my friend

--------------------
{NAME}
{DESCRIPTION}
The dates are {DATES}

{BODY}
--------------------
Thank you come again
"""

NO_DATA_MESSAGE = """
We live you know, but we're still a bit slow, so the data you've requested is not availabel just yet.

Please try again later, my friend
"""


class MessageBuilder:
    """A class object filled with methods that build the specific message
        and handle the exceptions that need to be handled.
    """
    def start_message() -> str:
        pass 
    
    @staticmethod
    def day_message(input_data: dict) -> str:
        sub_dict = {
            "NAME": input_data['name'],
            "DESCRIPTOIN": input_data["description"],
            "DATE": input_data["date"],
            "BODY": {NEWLINE.join([f"{key}{TAB * 2}{val}" for key, val in input_data['data'].items()])}
        }
        text = CustomFormatter().format(DAY_MESSAGE, **sub_dict)
        return text

    @staticmethod
    def week_message(input_data: dict) -> str:
        sub_dict = {
            "NAME": input_data['name'],
            "DESCRIPTOIN": input_data["description"],
            "DATE": ", ".join(input_data["days"]),
            "BODY": {NEWLINE.join([f"{key}{TAB * 2}{val}" for key, val in input_data['data'].items()])}
        }
        text = CustomFormatter().format(WEEK_MESSAGE, **sub_dict)
        return text