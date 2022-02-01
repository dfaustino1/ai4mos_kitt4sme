from fipy.cfg.reader import EnvReader, StrVar
from uri import URI


ORION_BASE_URL_VAR = StrVar(var_name='ORION_BASE_URL', default_value='')
reader = EnvReader()


def orion_base_url() -> URI:
    value = reader.read(ORION_BASE_URL_VAR)
    return URI(value)
