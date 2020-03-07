import hashlib
import time
DEFAULT_URL = 'http://127.0.0.1:8008'

TP_FAMILYNAME = 'consumer-data'
TP_VERSION = '1.0'

CONSUMER_ENTITY_CODE = '01'
ACADEMIC_ENTITY_CODE = '03'
CONSUMER_DATA_ENTITY_CODE = '04'

CONSUMER_DATA__RELATION_CODE = "71"
DATA_CONSUMER__RELATION_CODE = "72"


def _hash(identifier):
    return hashlib.sha512(identifier.encode('utf-8')).hexdigest()


TP_PREFFIX_HEX6 = _hash(TP_FAMILYNAME)[0:6]


def make_academic_address(academic_pkey):
    return TP_PREFFIX_HEX6 + ACADEMIC_ENTITY_CODE + _hash(academic_pkey)[:62]


def make_academic_list_address():
    return TP_PREFFIX_HEX6 + ACADEMIC_ENTITY_CODE


def make_consumer_address(consumer_pkey):
    return TP_PREFFIX_HEX6 + CONSUMER_ENTITY_CODE + _hash(consumer_pkey)[:62]


def make_consumer_list_address():
    return TP_PREFFIX_HEX6 + CONSUMER_ENTITY_CODE


# Data entity
def make_data_address(data_id):
    return TP_PREFFIX_HEX6 + CONSUMER_DATA_ENTITY_CODE + _hash(data_id)[:62]


def make_data_list_address():
    return TP_PREFFIX_HEX6 + CONSUMER_DATA_ENTITY_CODE


# Data <-> Consumer relation
def make_data_consumer__relation_address(data_id, client_pkey):
    return TP_PREFFIX_HEX6 + DATA_CONSUMER__RELATION_CODE + \
        CONSUMER_DATA_ENTITY_CODE + _hash(data_id)[:30] + \
        CONSUMER_ENTITY_CODE + _hash(client_pkey)[:28]


def make_consumer_list_by_data_address(data_id):
    return TP_PREFFIX_HEX6 + DATA_CONSUMER__RELATION_CODE + CONSUMER_DATA_ENTITY_CODE + _hash(data_id)[:30]


# Consumer <-> Data relation
def make_consumer_data__relation_address(client_pkey, data_id):
    return TP_PREFFIX_HEX6 + CONSUMER_DATA__RELATION_CODE + \
        CONSUMER_ENTITY_CODE + _hash(client_pkey)[:30] + \
        CONSUMER_DATA_ENTITY_CODE + _hash(data_id)[:28]


def make_data_list_by_consumer_address(client_pkey):
    return TP_PREFFIX_HEX6 + CONSUMER_DATA__RELATION_CODE + CONSUMER_ENTITY_CODE + _hash(client_pkey)[:30]


def get_current_timestamp():
    return int(round(time.time() * 1000))
