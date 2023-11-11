import numpy
from flask import current_app as app
from src.modules.project_py.sendemail import SendEmail


def jsonIntCOnverter(obj):
    if isinstance(obj, numpy.integer):
        app.logger.debug(f'obj integer- {obj} -- {int(obj)}')
        return int(obj)
    if isinstance(obj, numpy.floating):
        app.logger.debug(f'obj floating- {obj} -- {float(obj)}')
        return float(obj)
    if isinstance(obj, numpy.ndarray):
        app.logger.debug(f'obj ndarray- {obj} -- {int(obj)}')
        return obj.tolist()


def fn_send_email(req_json):
    obj_send_email = SendEmail()
    result = obj_send_email.email_main(req_json)
    return result
