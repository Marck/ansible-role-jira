# jira custom actions

Role for actions involving custom actions for JIRA.

---

## Prerequisites

- Install pip requirements:

```bash
pip3 install -r requirements.txt
```

## Replace attachments

> Note: this deletes any attachments found with **the same name** as the name of the attachment you want to upload

### Python testing

- Create `.vscode` folder at the root (in gitignore)
- Create a `launch`.json with the following values:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": [
                "library/args.json"
            ]
        }
    ]
}
```

- Create a test file at `library/testfile.extension` and use that below
- Create a args.json at *library/args.json* with the following values:

```json
{
    "ANSIBLE_MODULE_ARGS": {
        "url": "https://jira-url.domain",
        "username": "username",
        "password": "plaintext-password",
        "ticket": "JIRA-007",
        "attachment": "library/testfile.extension"
    }
}
```

- Run `library/replace_attachments.py` with VSCode

### Ansible playbook

```yaml
  - name: Replace existing attachments and upload new one
    include_role:
      name: roles/ans_tp_role_jira
      tasks_from: replace_attachments.yaml
    vars:
      jira_settings: "{{ jira }}"
      jira_password: "SuperSecretPassw0rd"
      jira_ticket_number: "{{ item }}"
      local_attachment: "files/testfile.extension"
    loop: "{{ jira_found_tickets.meta.issues }}"
```
