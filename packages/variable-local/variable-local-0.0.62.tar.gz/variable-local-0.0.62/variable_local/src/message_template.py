from database_mysql_local.generic_crud_ml import GenericCRUDML
from logger_local.Logger import Logger
from profiles_local.profiles_local import ProfilesLocal

from .constants import variable_local_logger_init_object

logger = Logger.create_logger(object=variable_local_logger_init_object)


class MessageTemplate(GenericCRUDML):
    def __init__(self):
        super().__init__(default_schema_name="field", default_table_name="field_table")
        self.profile_local = ProfilesLocal()

    def is_critiria_id_match_profile_id(self, criteria_json: dict, profile_id: int) -> dict:
        where = self.get_where_by_criteria(criteria_json)
        if profile_id:  # else raise?
            where += f" AND user.profile_id = {profile_id}"
        self.set_schema(schema_name="profile")
        query_for_potentials_receipients = f"""
SELECT DISTINCT user_id, person_id, user_main_email, user.profile_id AS profile_id, 
   profile_phone_full_number_normalized, profile_preferred_lang_code
 FROM user.user_general_view AS user
    JOIN group_profile.group_profile_view AS group_profile on group_profile.profile_id = user.profile_id
  WHERE {where}"""
        self.cursor.execute(query_for_potentials_receipients)
        result = self.cursor.fetchone()
        columns = ("user_id, person_id, user_main_email, profile_id,"
                   "profile_phone_full_number_normalized, profile_preferred_lang_code")
        return self.convert_to_dict(result, columns)

    def get_where_by_criteria(self, criteria_json: dict):
        min_age = criteria_json.get("min_age")
        max_age = criteria_json.get("max_age")
        gender_list_id = criteria_json.get("gender_list_id")
        group_list_id = criteria_json.get("group_list_id")
        logger.info(object={"min_age": min_age, "max_age": max_age, "gender_list_id": gender_list_id,
                            "group_list_id": group_list_id})
        # profile_id didn't receive messages from this campaign for campaign.minimal_days
        where = "TRUE "
        if min_age is not None:
            where += f" AND TIMESTAMPDIFF(YEAR, person_birthday_date, CURDATE()) >= {min_age}"
        if max_age is not None:
            where += f" AND TIMESTAMPDIFF(YEAR, person_birthday_date, CURDATE()) <= {max_age}"

        if gender_list_id is not None:
            where += " AND profile_gender_id " + self.sql_in_list_by_entity_list_id(
                schema_name="profile", entity_name="gender", entity_list_id=gender_list_id)

        if group_list_id is not None:
            where += " AND group_profile.group_id " + self.sql_in_list_by_entity_list_id(
                schema_name="`group`", entity_name="group", entity_list_id=group_list_id)
        return where

    def get_message_template_textblock_and_attributes(
            self, message_template_id: int, destination_profile_id: int) -> list[dict]:
        """Returns the message template text block and attributes for the given message template id and profile id.
        The attributes are:
            - sms_body_template
            - email_subject_template
            - email_body_html_template
            - whatsapp_body_template
            - question_id
            - question_type_id
            - question_title
            - question_type_name
        for each text block in the message template.
        """
        query = """
SELECT DISTINCT min_age, max_age, gender_list_id, group_list_id
  FROM message_template.message_template_view
    JOIN message_template.message_template_message_template_text_block_view AS message_template_message_template_text_block
        ON message_template_message_template_text_block.message_template_id = message_template_view.message_template_id
    JOIN message_template.message_template_text_block_view AS message_template_text_block
        ON message_template_text_block.message_template_text_block_id = message_template_message_template_text_block.message_template_id
    JOIN criteria.criteria_view AS criteria
        ON criteria.criteria_id = message_template_text_block.criteria_id
  WHERE message_template_view.message_template_id = %s"""  # noqa
        self.cursor.execute(query, (message_template_id,))
        preferred_lang_code = self.profile_local.get_preferred_lang_code_by_profile_id(destination_profile_id)
        columns = "min_age, max_age, gender_list_id, group_list_id"

        results = []
        for row in self.cursor.fetchall():
            criteria_json = self.convert_to_dict(row, columns)
            if self.is_critiria_id_match_profile_id(criteria_json, destination_profile_id):
                query = """
SELECT sms_body_template, email_subject_template, email_body_html_template, whatsapp_body_template,
            question.question_id, question.question_type_id,
            question_ml.title AS question_title, question_type.name AS question_type_name
    FROM message_template.message_template_text_block_view AS message_template_text_block
        JOIN message_template.message_template_text_block_ml_view AS message_template_text_block_ml
            ON message_template_text_block_ml.message_template_text_block_id = message_template_text_block.message_template_text_block_id
                AND message_template_text_block_ml.lang_code = %s
        LEFT JOIN question.question_view AS question
            ON question.question_id = message_template_text_block.question_id
        LEFT JOIN question.question_ml_view AS question_ml
            ON question_ml.question_id = question.question_id AND question_ml.lang_code = %s
        LEFT JOIN question.question_type_view AS question_type
            ON question_type.question_type_id = question.question_type_id

    """  # noqa
                columns = ",".join(["sms_body_template", "email_subject_template", "email_body_html_template",
                                    "whatsapp_body_template", "question_id", "question_type_id",
                                    "question_title", "question_type_name"])
                self.cursor.execute(query, (preferred_lang_code, preferred_lang_code))
                for row in self.cursor.fetchall():
                    text_block_dict = self.convert_to_dict(row, columns)
                    text_block_dict["preferred_lang_code"] = preferred_lang_code
                    results.append(text_block_dict)

        return results
