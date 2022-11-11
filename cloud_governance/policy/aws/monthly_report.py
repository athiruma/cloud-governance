import os
from ast import literal_eval

import pandas as pd

from cloud_governance.common.elasticsearch.elasticsearch_operations import ElasticSearchOperations
from cloud_governance.common.logger.init_logger import logger
from cloud_governance.common.mails.mail_message import MailMessage
from cloud_governance.common.mails.postfix import Postfix


class MonthlyReport:
    REPORT_DAYS = 30

    def __init__(self):
        self._es_index = 'cloud-governance-mail-messages'
        self._es_host = os.environ.get('es_host', '')
        self._es_port = os.environ.get('es_port', '')
        self._to_mail = os.environ.get('to_mail', '')
        self._to_cc = literal_eval(os.environ.get('cc_mail', '[]'))
        if self._es_host:
            self._elastic_operations = ElasticSearchOperations(es_host=self._es_host, es_port=self._es_port)
        self._postfix_mail = Postfix()
        self._mail_message = MailMessage()

    def get_monthly_report_data(self):
        """
        This method fetch the last 30 days data from ElasticSearch
        @return:
        """
        if self._es_host:
            mail_messages = self._elastic_operations.get_index_hits(days=self.REPORT_DAYS, index=self._es_index)
            mail_messages_df = pd.DataFrame(mail_messages).drop(['To', 'Cc', 'Message'], axis=1).fillna('NAN')
            mail_messages_df = mail_messages_df[~mail_messages_df.MessageType.str.contains('notify_admin')].reset_index(drop=True)
            mail_messages_df = mail_messages_df[~mail_messages_df.MessageType.str.contains('monthly_report')].reset_index(drop=True)
            mail_messages_df_group = mail_messages_df.groupby(['Policy', 'Account']).agg({'MessageType': list}).reset_index()
            return mail_messages_df_group.to_dict("records")
        else:
            logger.info('es_host is missing')
        return []

    def send_monthly_report(self):
        """
        This method send monthly report to the user
        @return:
        """
        monthly_data = self.get_monthly_report_data()
        prepare_data = {"Perf-Dept".upper(): [], "Perf-Scale".upper(): []}
        for data in monthly_data:
            account_name = data['Account']
            if account_name:
                prepare_data[account_name].append({
                    "Policy": data['Policy'],
                    "Alert": len(data['MessageType'])
                })
        content = self.prepare_html_table_message(prepare_data)
        if content:
            subject, body = self._mail_message.monthly_html_mail_message(data=content)
            self._postfix_mail.send_email_postfix(subject=subject, content=body, to=self._to_mail, cc=self._to_cc, mime_type='html', message_type='monthly_report')
            return 'Successfully Send the Monthly report'
        return 'No Data to send to the Monthly report'

    def row_span(self, cols: int):
        """
        This method return the table data with colspan
        @param cols:
        @return:
        """
        return f'<td rowspan="{cols}" align="center" style="border: 1px solid black;font-weight: bold;color:blue">'

    def prepare_html_table_message(self, data: dict):
        """
        This method gives the html table from dictionary
        @param data:
        @return:
        """
        start_row, end_row = '<tr>', '</tr>'
        start_col, end_col = f'<td align="center" style="border:1px solid black;font-weight:bold;">', '</b></td>'
        start_head, end_head = f'<th align="center" style="border:1px solid black;color:white;background:gray;padding:2px;font-size:12px;">', '</th>'
        html_table = [f"""
                    <table style="border-collapse:collapse;width: 50%">
                        {start_row}
                            {start_head}Account{end_head}
                            {start_head}Policy{end_head}
                            {start_head}Alert{end_head}
                        {end_row}
                      """.strip()]
        for data_key, data_values in data.items():
            row_span = len(data_values)
            html_row = start_row
            if data_key == 'PERF-SCALE':
                data_key = 'Openshift-PerfScale'
            html_row += f'{self.row_span(row_span)}{data_key}{end_col}'
            for data_items in data_values:
                for key, value in data_items.items():
                    if key == "Alert":
                        html_row += f'{start_col[:-2]}color:green;"> {str(value)} {end_col}'
                    else:
                        html_row += f'{start_col} {str(value)} {end_col}'
                html_row += end_row
                html_table.append(html_row)
                html_row = start_row
        html_table.append('</tbody></table>')
        return "\n".join(html_table)

    def run(self):
        """
        This method sends the monthly report
        @return:
        """
        return self.send_monthly_report()
