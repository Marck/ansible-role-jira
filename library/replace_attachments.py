#!/usr/bin/python
import re

from atlassian import Jira
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: replace_attachments

short_description: Replace attachments (get, delete and upload attachments) from a JIRA ticket

version_added: "1.0"

description:
    - "Use this module to replace (get, delete and upload) existing attachments on a JIRA ticket"

options:
    url:
        description:
            - The Atlassian jira URL
        type: str
        required: true
    username:
        description:
            - The username to authenticate with the jira instance
        type: str
        required: true
    password:
        description:
            - The password to authenticate with the jira instance
        type: str
        required: true
    ticket:
        description:
            - The ticket number where the attachments will be uploaded to.
        type: str
        required: true
    attachment:
        description:
            - The full patch to the attachment file
        type: str
        required: true

author:
    - Marc (@Marck)
'''

EXAMPLES = '''
replace_attachments:
    url: "https://jira-url.domain"
    username: "{{ ansible_user }}"
    password: "{{ ansible_password }}"
    ticket: "JIRA-007"
    attachment: "/path-to-file/filename.txt"
'''

RETURN = '''
changed:
    description: if there is made a change
    type: bool
actions:
    description: describes what actions are taken (removed = old attachment removed, upload = attachment uploaded)
    type: str
rc:
    description: return-code 0 is no errors, 1 is an error.
    type: int
'''

def jira():
    try:
        # Define available arguments/parameters that a user can pass to the module
        module_args = dict(
            url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            ticket=dict(type='str', required=True),
            attachment=dict(type='str', required=True)
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )
        
        # JIRA rest api docs: https://docs.atlassian.com/software/jira/docs/api/REST/8.5.0/#api/2
        jira = Jira(url=module.params['url'],
                                username=module.params['username'],
                                password=module.params['password'])
        
        ticket = jira.get_issue(module.params['ticket'], fields='attachment')
        ticket_fields = ticket['fields']
        ticket_attachments = ticket_fields['attachment']
        local_attachment_name = module.params['attachment'].split('/')[-1]
        
        for attachment in ticket_attachments:
            if re.match(local_attachment_name, attachment['filename']):
                # Found attachment that has the same name as the one we want to upload
                ## Delete the existing attachment, upload the new attachment and exit.
                jira.remove_attachment(attachment['id'])
                jira.add_attachment(module.params['ticket'], module.params['attachment'])
                
                result = { 'changed': 'True', 'actions': 'removed, uploaded', 'rc': 0 }
                module.exit_json(**result)
            
        # Attachment(s) don't have the same name as we want to upload. 
        ## Upload the attachment and exit.
        jira.add_attachment(module.params['ticket'], module.params['attachment'])
        result = { 'changed': 'True', 'actions': 'uploaded', 'rc': 0 }
        module.exit_json(**result)
        
    except Exception as error:
        module.fail_json(msg=f'Error on trying to get, delete and/or upload attachment. Error: {error}')


def main():
    jira()


if __name__ == '__main__':
    main()
