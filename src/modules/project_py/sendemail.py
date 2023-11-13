from flask import Flask, request, current_app as app
from flask_mail import Mail, Message
import re
from src.modules.database.dbProcessor import dbProcess

class SendEmail:

    def email_main(self, req_json):
        output_validate_json = self.validate_json(req_json)
        if 'status' in output_validate_json and output_validate_json['status'] == 'failure':
            return output_validate_json
        # output_db_entry = self.db_entry(output_validate_json, req_json)
        return 'output_db_entry'

    def validate_json(self, req_json):
        app.logger.info(f'request_json validation starts here')
        if not req_json:
            return {"status": "failure", "message": "request parameter cannot be empty"}

        app.logger.info(f'email_list validation starts here')
        if not type(req_json['to_email_addr']) == list or not type(req_json['cc_email_addr']) == list or not type(
                req_json['bcc_email_addr']) == list:
            return {"status": "failure", "message": "'to_email_addr' or 'cc_emil_addr' or 'bcc_email_addr' should be "
                                                    "in list format"}

        output_email_validation = self.email_validation(req_json)
        if output_email_validation['status'] == 'failure':
            return output_email_validation

        elif 'mail_subject_line' not in req_json or not req_json['mail_subject_line']:
            return {"status": "failure", "message": "mail_subject_line cannot be empty"}

        elif 'mail_body' not in req_json or not req_json['mail_body']:
            return {"status": "failure", "message": "mail_body cannot be empty"}
        # -----------
        return output_email_validation

    def email_validation(self, req_json):
        app.logger.info(f'email validation starts here')
        if 'to_email_addr' not in req_json and not req_json['to_email_addr']:
            return {"status": "failure", "message": " 'to_email_addr' cannot be empty"}

        result_mail_pattern = self.check_email_pattern(req_json['to_email_addr'], mail_type='to_email_addr')
        if result_mail_pattern['status'] == 'failure':
            return result_mail_pattern

        if 'cc_email_addr' not in req_json:
            return {"status": "failure", "message": " 'cc_email_addr' cannot be empty"}

        result_mail_pattern = self.check_email_pattern(req_json['cc_email_addr'], mail_type='cc_email_addr')
        if result_mail_pattern['status'] == 'failure':
            return result_mail_pattern

        if 'bcc_email_addr' not in req_json:
            return {"status": "failure", "message": " 'bcc_email_addr' cannot be empty"}

        result_mail_pattern = self.check_email_pattern(req_json['bcc_email_addr'], mail_type='bcc_email_addr')
        if result_mail_pattern['status'] == 'failure':
            return result_mail_pattern

        else:
            return {"status": "success", "message": " email validated successfully", 'data': req_json}

    def check_email_pattern(self, email, mail_type):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        for ids in email:
            if not re.match(pattern, ids):
                return {"status": "failure", "message": f' invalid {mail_type} format', "data": ids}
        else:
            return {"status": "success", "message": " pattern validated successfully"}

    def send_email(self, toEmailAddress=[], ccEmailAddress=[], subjectLine=None, EmailBody=None,
                   fromEmailAddress=None, filePath=None, htmlEmailBody=None, mimeType=None, bccEmailAddress=[]):
        try:
            mail = Mail(app)
            msg = Message(subjectLine, sender=fromEmailAddress, recipients=toEmailAddress, cc=ccEmailAddress,
                          bcc=bccEmailAddress)
            msg.body = EmailBody
            msg.html = htmlEmailBody
        except Exception as e:
            return

    """
    def db_entry(self, output_validate_json, req_json):
        obj_db = dbProcess('email', select_column_list=['send_to_email_id', 'send_by_email_id'],
                           val_dict_data={'send_to_email_id': req_json['to_email_addr'],
                                          'send_by_email_id': req_json['cc_email_addr']})
        insert_output = obj_db.insert_query()
        return {"status": "success", "message": " data inserted successfully"}
    """