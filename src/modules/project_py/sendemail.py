from flask import Flask, request, current_app as app
from flask_mail import Mail, Message
import ntpath
import re
from src.modules.database.dbProcessor import dbProcess


class SendEmail:

    def email_main(self, req_json):
        try:
            output_validate_json = self.send_email(
                toEmailAddress=req_json['to_email_addr'], fromEmailAddress=app.config['DEFAULT_SENDER'],
                ccEmailAddress=req_json['cc_email_addr'],
                subjectLine=req_json['mail_subject_line'], EmailBody=req_json['mail_body']
            )
            if 'status' in output_validate_json and output_validate_json['status'] == 'failure':
                return output_validate_json
            # output_db_entry = self.db_entry(output_validate_json, req_json)
            return 'output_db_entry'
        except Exception as e:
            app.logger.info(f'inside exception - {format(e)}')
            return {"message": format(e), "status": "failure"}

    def send_email(self, toEmailAddress=[], ccEmailAddress=[], subjectLine=None, EmailBody=None,
                   fromEmailAddress=None, filePath=None, htmlEmailBody=None, mimeType=None, bccEmailAddress=[]):
        try:
            mail = Mail(app)
            msg = Message(subjectLine, sender=fromEmailAddress, recipients=toEmailAddress, cc=ccEmailAddress,
                          bcc=bccEmailAddress)
            msg.body = EmailBody
            msg.html = htmlEmailBody
            if filePath and mimeType:
                fileName = ntpath.basename(filePath)
                with app.open_resource(filePath) as fp:
                    msg.attach(fileName, mimeType, fp.read())
            app.logger.info('before_msg')
            mail.send(msg)
            app.logger.info('after_msg')

            app.logger.info('!!!!! mail sent successfully !!!!!')
            return {"message": "mail sent successfully", "status": "success"}
        except Exception as e:
            app.logger.info(f'inside exception - {format(e)}')
            return {"message": format(e), "status": "failure"}

    """
    def db_entry(self, output_validate_json, req_json):
        obj_db = dbProcess('email', select_column_list=['send_to_email_id', 'send_by_email_id'],
                           val_dict_data={'send_to_email_id': req_json['to_email_addr'],
                                          'send_by_email_id': req_json['cc_email_addr']})
        insert_output = obj_db.insert_query()
        return {"status": "success", "message": " data inserted successfully"}
        
         # def email_validation(self, req_json):
    #     app.logger.info(f'email validation starts here')
    #     if 'to_email_addr' not in req_json and not req_json['to_email_addr']:
    #         return {"status": "failure", "message": " 'to_email_addr' cannot be empty"}
    #
    #     result_mail_pattern = self.check_email_pattern(req_json['to_email_addr'], mail_type='to_email_addr')
    #     if result_mail_pattern['status'] == 'failure':
    #         return result_mail_pattern
    #
    #     if 'cc_email_addr' not in req_json:
    #         return {"status": "failure", "message": " 'cc_email_addr' cannot be empty"}
    #
    #     result_mail_pattern = self.check_email_pattern(req_json['cc_email_addr'], mail_type='cc_email_addr')
    #     if result_mail_pattern['status'] == 'failure':
    #         return result_mail_pattern
    #
    #     if 'bcc_email_addr' not in req_json:
    #         return {"status": "failure", "message": " 'bcc_email_addr' cannot be empty"}
    #
    #     result_mail_pattern = self.check_email_pattern(req_json['bcc_email_addr'], mail_type='bcc_email_addr')
    #     if result_mail_pattern['status'] == 'failure':
    #         return result_mail_pattern
    #
    #     else:
    #         return {"status": "success", "message": " email validated successfully", 'data': req_json}
    
    app.logger.info(f'request_json validation starts here')
    #     if not req_json:
    #         return {"status": "failure", "message": "request parameter cannot be empty"}
    #
    #     app.logger.info(f'email_list validation starts here')
    #     if not type(req_json['to_email_addr']) == list or not type(req_json['cc_email_addr']) == list or not type(
    #             req_json['bcc_email_addr']) == list:
    #         return {"status": "failure", "message": "'to_email_addr' or 'cc_emil_addr' or 'bcc_email_addr' should be "
    #                                                 "in list format"}
    #
    #     output_email_validation = self.email_validation(req_json)
    #     if output_email_validation['status'] == 'failure':
    #         return output_email_validation
    #
    #     elif 'mail_subject_line' not in req_json or not req_json['mail_subject_line']:
    #         return {"status": "failure", "message": "mail_subject_line cannot be empty"}
    #
    #     elif 'mail_body' not in req_json or not req_json['mail_body']:
    #         return {"status": "failure", "message": "mail_body cannot be empty"}
    #     # -----------
    #     return output_email_validation
    """
