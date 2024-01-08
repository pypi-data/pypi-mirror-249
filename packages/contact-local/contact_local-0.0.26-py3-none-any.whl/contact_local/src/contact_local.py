from dotenv import load_dotenv
load_dotenv()
from .contact_constants import SCHEMA_NAME, TABLE_NAME, VIEW_TABLE_NAME, ID_COLUMN_NAME, logger  # noqa: E402, E501
from .contact import Contact  # noqa: E402
from database_mysql_local.generic_crud import GenericCRUD  # noqa: E402, E501
from typing import List, Dict   # noqa: E402
from .contact_local_extentions import (     # noqa: E402
    ContactBatchInsertionError,
    ContactDeletionError,
    ContactInsertionError,
    ContactObjectInsertionError,
    ContactUpdateError)


class ContactsLocal(GenericCRUD):

    def __init__(self) -> None:
        super().__init__(
            default_schema_name=SCHEMA_NAME,
            default_table_name=TABLE_NAME,
            default_view_table_name=VIEW_TABLE_NAME,
            default_id_column_name=ID_COLUMN_NAME
        )

    @staticmethod
    def insert_contact_dict(contact_dict: dict) -> int:
        logger.start(object={'contact_to_insert': contact_dict})
        if not contact_dict:
            logger.error("contact_to_insert cannot be empty")
            logger.end()
            raise ContactInsertionError("contact_to_insert cannot be empty")

        first_name = contact_dict.get('first_name')
        last_name = contact_dict.get('last_name')
        organization = contact_dict.get('organization')
        if not first_name and not last_name and not organization:  # noqa: E501
            logger.error(
                "contact_to_insert must have at least one of the following " +
                "fields: first_name, last_name, organization")
            logger.end()
            raise ContactInsertionError(
                "contact_to_insert must have at least one of the following" +
                "fields: first_name, last_name, organization")

        try:
            contact_json = {
                'owner_profile_id': contact_dict.get('owner_profile_id', None),  # noqa: E501
                'account_name': contact_dict.get('account_name', None),
                'person_id': contact_dict.get('person_id', None),
                'name_prefix': contact_dict.get('name_prefix', None),
                'first_name': contact_dict.get('first_name', None),
                'additional_name': contact_dict.get('additional_name', None),  # noqa: E501
                'last_name': contact_dict.get('last_name', None),
                'full_name': contact_dict.get('full_name', None),
                'name_suffix': contact_dict.get('name_suffix', None),
                'nickname': contact_dict.get('nickname', None),
                'display_as': contact_dict.get('display_as', None),
                'title': contact_dict.get('title', None),
                'organization': contact_dict.get('organization', None),
                'organization_profile_id': contact_dict.get('organization_profile_id', None),  # noqa: E501
                'job_title': contact_dict.get('job_title', None),
                'department': contact_dict.get('department', None),
                'notes': contact_dict.get('notes', None),
                'email1': contact_dict.get('email1', None),
                'email2': contact_dict.get('email2', None),
                'email3': contact_dict.get('email3', None),
                'phone1': contact_dict.get('phone1', None),
                'phone2': contact_dict.get('phone2', None),
                'phone3': contact_dict.get('phone3', None),
                'address1_street': contact_dict.get('address1_street', None),  # noqa: E501
                'address1_city': contact_dict.get('address1_city', None),
                'address1_state': contact_dict.get('address1_state', None),  # noqa: E501
                'address1_postal_code': contact_dict.get('address1_postal_code', None),  # noqa: E501
                'address1_country': contact_dict.get('address1_country', None),  # noqa: E501
                'address2_street': contact_dict.get('address2_street', None),  # noqa: E501
                'address2_city': contact_dict.get('address2_city', None),  # noqa: E501
                'address2_state': contact_dict.get('address2_state', None),  # noqa: E501
                'address2_postal_code': contact_dict.get('address2_postal_code', None),    # noqa: E501
                'address2_country': contact_dict.get('address2_country', None),    # noqa: E501
                'birthday': contact_dict.get('birthday', None),
                'day': contact_dict.get('day', None),
                'month': contact_dict.get('month', None),
                'year': contact_dict.get('year', None),
                'cira': contact_dict.get('cira', None),
                'anniversary': contact_dict.get('anniversary', None),
                'website1': contact_dict.get('website1', None),
                'website2': contact_dict.get('website2', None),
                'website3': contact_dict.get('website3', None),
                'photo_url': contact_dict.get('photo_url', None),
                'photo_file_name': contact_dict.get('photo_file_name', None),  # noqa: E501
                'source': contact_dict.get('source', None),
                'import_contact_id': contact_dict.get('import_contact_id', None),  # noqa: E501
                'created_user_id': contact_dict.get('created_user_id', 0),
            }
            if contact_dict.get('display_as', None) is None:
                contact_json['display_as'] = contact_dict.get(
                    'first_name', None)
                if contact_dict.get('last_name', None) is not None:
                    contact_json['display_as'] += " " + \
                        contact_dict.get('last_name', None)
            contact_id = GenericCRUD.insert(
                self=ContactsLocal(), data_json=contact_json)
            logger.end("contact added", object={'contact_id': contact_id})
        except Exception as err:
            logger.exception(f"Contact.insert Error: {err}, contact_id:{contact_id}", object=err)
            logger.end()
            raise ContactInsertionError("Error occurred while inserting contact." + str(err))  # noqa: E501

        return contact_id

    @staticmethod
    def update(contact_id: int, person_id: int, name_prefix: str, first_name: str,
               additional_name: str, job_title: str) -> None:
        try:
            object1 = {
                'person_id': person_id,
                'name_prefix': name_prefix,
                'first_name': first_name,
                'additional_name': additional_name,
                'job_title': job_title,
                'contact_id': contact_id
            }
            logger.start(object=object1)
            contact_data = {
                'person_id': person_id,
                'name_prefix': name_prefix,
                'first_name': first_name,
                'additional_name': additional_name,
                'job_title': job_title,
                'contact_id': contact_id
            }
            GenericCRUD.update_by_id(ContactsLocal(), id_column_value=contact_id, data_json=contact_data)  # noqa: E501
            logger.end("contact updated", object={'contact_id': contact_id})
        except Exception as err:
            logger.exception(f"Contact.update Error: {err}, contact_id: {contact_id}", object=err)
            logger.end()
            raise ContactUpdateError("Error occurred while updating contact." + str(err))  # noqa: E501

    @staticmethod
    def delete_by_contact_id(contact_id: any) -> None:
        try:
            logger.start(object={'contact_id': contact_id})
            GenericCRUD.delete_by_id(ContactsLocal(), id_column_value=contact_id)  # noqa: E501
            logger.end("contact deleted", object={'contact_id': contact_id})
        except Exception as err:
            logger.exception(f"Contact.delete Error: {err}", object=err)
            # cursor.close()
            logger.end()
            raise ContactDeletionError("Error occurred while deleting contact." + str(err))  # noqa: E501

    @staticmethod
    def insert_batch(contact_list: List[Dict]) -> List[int]:
        try:
            logger.start()
            inserted_ids = []
            for contact in contact_list:
                contact_id = ContactsLocal.insert_contact_dict(contact_dict=contact)
                inserted_ids.append(contact_id)
            logger.end("contacts added", object={'inserted_ids': inserted_ids})
        except Exception as err:
            inserted_ids_str = ",".join(str(x) for x in inserted_ids)
            logger.exception(f"Contact.insert_batch Error: {err} " + inserted_ids_str, object=err)
            raise ContactBatchInsertionError("Error occurred while batch inserting contacts." + str(err))  # noqa: E501

        return inserted_ids

    def get_contact_by_contact_id(contact_id: int) -> dict:
        logger.start(object={'contact_id': contact_id})
        try:
            contact = GenericCRUD.select_one_dict_by_id(self=ContactsLocal(), view_table_name=VIEW_TABLE_NAME,  # noqa: E501
                                                        id_column_name=ID_COLUMN_NAME, id_column_value=contact_id)  # noqa: E501
        except Exception as err:
            logger.exception(
                f"Contact.get_contact_by_id Error: {err}", object=err)
            logger.end()
            raise
        return contact

    @staticmethod
    def insert_contact_object(self, contact: Contact) -> int:
        logger.start(object={'contact': contact})
        if not contact:
            logger.exception("contact cannot be empty")
            logger.end()
            raise ContactBatchInsertionError("contact cannot be empty")

        required_fields = [
            'first_name', 'last_name', 'organization', 'job_title'
        ]
        if not any(getattr(contact, field, None) for field in required_fields):
            logger.error(
                "contact must have at least one of the following " +
                "fields: first_name, last_name, organization, job_title")
            logger.end()
            raise ContactObjectInsertionError(
                "contact must have at least one of the following" +
                "fields: first_name, last_name, organization, job_title")
        try:
            contact_json = vars(contact)

            if contact.display_as is None:
                display_name = contact.first_name
                if contact.last_name is not None:
                    display_name += " " + contact.last_name
                contact_json['display_as'] = display_name

            contact_id = GenericCRUD.insert(
                self=ContactsLocal(), data_json=contact_json)
            logger.end("contact added", object={'contact_id': contact_id})
        except Exception as err:
            logger.exception(f"Contact.insert Error: {err}, contact_id:{contact_id}", object=err)
            logger.end()
            raise ContactObjectInsertionError("Error occurred while inserting contact." + str(err))

        return contact_id
