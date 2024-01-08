import os
import sys

from language_local.lang_code import LangCode
from message_local.Recipient import Recipient

script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_directory, '..'))
from src.smartlink import (VERIFY_EMAIL_ADDRESS_ACTION_ID,  # noqa: E402
                           SmartLinkLocal)
from src.utils import generate_random_string  # noqa: E402

TEST_CAMPAIGN_ID = 1
TEST_SMARTLINK_TYPE_ID = 2

smartlink = SmartLinkLocal()
from_recipient = Recipient(user_id=1,
                           contact_id=2,
                           email_address="test@gmail.com")

to_recipient = Recipient(person_id=1,
                         telephone_number="0501234567",
                         preferred_language=LangCode.ENGLISH.value,
                         email_address="test@gmail.com")


def test_generate_random_string():
    result = generate_random_string(length=10)
    assert len(result) == 10

    result = generate_random_string(length=20)
    assert len(result) == 20


def test_insert_and_get():
    inserted_id = smartlink.insert(smartlink_type_id=TEST_SMARTLINK_TYPE_ID,
                                   from_recipient=from_recipient.to_json(),
                                   to_recipient=to_recipient.to_json(),
                                   campaign_id=TEST_CAMPAIGN_ID)
    assert inserted_id > 0  # no error

    expected_result = smartlink.select_one_dict_by_id(id_column_name="smartlink_id",
                                                      id_column_value=inserted_id)
    smartlink_details = smartlink.get_smartlink_details(smartlink_identifier=expected_result["smartlink_identifier"])

    assert smartlink_details["smartlink_identifier"] == expected_result["smartlink_identifier"]
    assert smartlink_details["from_user_id"] == 1
    assert smartlink_details["from_contact_id"] == 2
    assert smartlink_details["from_email"] == from_recipient.get_email_address()

    assert smartlink_details["to_person_id"] == 1
    assert smartlink_details["to_normalized_phone"] == to_recipient.get_canonical_telephone()
    assert smartlink_details["lang_code"] == to_recipient.get_preferred_language()

    assert smartlink_details["campaign_id"] == TEST_CAMPAIGN_ID
    assert smartlink_details["action_id"] == VERIFY_EMAIL_ADDRESS_ACTION_ID


def test_execute():
    inserted_id = smartlink.insert(smartlink_type_id=TEST_SMARTLINK_TYPE_ID,
                                   from_recipient=from_recipient.to_json(),
                                   to_recipient=to_recipient.to_json(),
                                   campaign_id=TEST_CAMPAIGN_ID)
    assert inserted_id > 0  # no error

    smartlink_identifier = smartlink.select_one_dict_by_id(id_column_name="smartlink_id",
                                                           id_column_value=inserted_id)["smartlink_identifier"]

    session_id = smartlink.execute(smartlink_identifier=smartlink_identifier)

    smartlink.set_schema(schema_name="logger")
    select_clause_value = "return_code"
    execution_details = smartlink.select_one_dict_by_id(view_table_name="logger_view",
                                                        select_clause_value=select_clause_value,
                                                        id_column_name="session",
                                                        id_column_value=session_id)
    assert execution_details[select_clause_value] == 0
