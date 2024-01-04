import random
import re

from language_local.lang_code import LangCode
from logger_local.Logger import Logger
from profiles_local.profiles_local import ProfilesLocal

from .constants import variable_local_logger_init_object
from .variable import VariablesLocal

logger = Logger.create_logger(object=variable_local_logger_init_object)

LEFT_BRACKETS = '{'
RIGHT_BRACKETS = '}'


class ReplaceFieldsWithValues:
    def __init__(self, message, language: LangCode, variable: VariablesLocal):
        self.message = message
        self.language = language
        self.variable = variable
        self.profile_local = ProfilesLocal()

    # TODO: Not used anymore. Remove?
    # Private method used by get_variable_names_and_chosen_option(self)
    # def choose_option(self, message_index: int, first_param: str) -> (str, int):
    #     """ Gets a message, an index of the first appearance of '|' , and the first parameter of the options
    #         Returns:
    #         1. One of the options randomly selected
    #         2. The index of one char after the next '}'"""
    #     logger.start(
    #         object={'message_index': message_index, 'first_param': first_param})
    #     list_of_params = [first_param]
    #     while self.message[message_index] != '}':
    #         next_param = ""
    #         while self.message[message_index] != '|' and self.message[message_index] != '}':
    #             next_param += self.message[message_index]
    #             message_index += 1
    #         list_of_params.append(next_param)
    #         if self.message[message_index] != '}':
    #             message_index += 1
    #     random_index = random.randint(0, len(list_of_params) - 1)
    #     random_option_selected, index = list_of_params[random_index], message_index + 1
    #     logger.end(object={'random_option_selected': random_option_selected, 'index': index})
    #     return random_option_selected, index

    def get_variable_names_and_chosen_option(self) -> (list, str):
        """Returns:
            1. A list of all variable names that were inside curly braces of message
            2. A string that's a copy of the message but without the variable names inside curly braces,
            and a randomly chosen parameter out of each curly braces options:
            "Hello {First Name}, how are you {feeling|doing}?" --> "Hello {}, how are you doing?" 
        """
        logger.start()
        variable_names_list = []
        message_without_variable_names = self.message

        # choose random option from {A|B}
        pattern = re.compile(r'{.*?}')
        matches = pattern.findall(message_without_variable_names)
        for match in matches:
            match_without_brackets = match[1:-1]
            if '|' in match:
                # pick random choice
                options = match_without_brackets.split('|')
                random_option = random.choice(options)
                message_without_variable_names = message_without_variable_names.replace(match, random_option)
            elif match_without_brackets in self.variable.name2id_dict.keys():
                # replace variable name with '{}' and add variable names to list
                message_without_variable_names = message_without_variable_names.replace(match, '{}')
                variable_names_list.append(match_without_brackets)
            else:
                pass  # TODO: should we do something here?

        return variable_names_list, message_without_variable_names

        # Old code:
        # For the following function to work the message must not have single '{' or '}'.
        # They should always come in pairs.
        #
        # message_without_variable_names = ""
        # message_index = 0
        # while message_index < len(self.message):
        #     index_after_choosing_option = None
        #     if self.message[message_index] == '{':
        #         message_index += 1
        #         next_variable_name = ""
        #         chosen_parameter = None
        #         while self.message[message_index] != '}':
        #             if self.message[message_index] == '|':
        #                 chosen_parameter, index_after_choosing_option = self.choose_option(
        #                     message_index + 1, next_variable_name)
        #                 break
        #             next_variable_name += self.message[message_index]
        #             message_index += 1
        #         if chosen_parameter is not None:
        #             message_without_variable_names += chosen_parameter
        #         elif next_variable_name:
        #             message_without_variable_names += "{}"
        #             variable_names_list.append(next_variable_name)
        #         else:  # error
        #             error = "Error: message has single '{' or '}' or empty variable name"
        #             logger.error(error)
        #             raise Exception(error)
        #
        #     else:
        #         message_without_variable_names += self.message[message_index]
        #     message_index = message_index + 1 if index_after_choosing_option is None \
        #         else index_after_choosing_option
        # logger.end(object={'variable_names_list': variable_names_list,
        #                    'message_without_variable_names': message_without_variable_names})
        # return variable_names_list, message_without_variable_names

    # Should be used both by Dialog workflow and message-local-python-package Message.py
    def get_variable_values_and_chosen_option(self, profile_id: int = None) -> str:
        """Returns:
            1. A list of all variable values by variable names that were inside curly braces of message 
            2. A string that's a copy of the message but without the variable names inside curly braces
            and a randomly chosen parameter out of each curly braces options:
            "Hello {First Name}, how are you {feeling|doing}?" --> "Hello {}, how are you doing?"
        """
        logger.start()
        variable_names_list, message_without_variable_names = self.get_variable_names_and_chosen_option()
        variable_value_list = []
        for variable_name in variable_names_list:
            variable_id = self.variable.get_variable_id_by_variable_name(variable_name)
            variable_value = VariablesLocal.get_variable_value_by_variable_id(
                variable_id=variable_id, lang_code=self.language, profile_id=profile_id)
            variable_value_list.append(variable_value)

        formatted_message = message_without_variable_names.format(*variable_value_list)
        logger.end(object={'formatted_message': formatted_message})
        return formatted_message
