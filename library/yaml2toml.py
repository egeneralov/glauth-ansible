#!/usr/bin/env python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': [
    'preview'
  ],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: yaml2toml
short_description: Convert yaml to toml format
version_added: "2.4"

description:
  - "Convert yaml to toml format"

options:
  payload:
    description:
      - YAML payload
    required: true

author:
  - Eduard Generalov <eduard@generalov.net>
'''

EXAMPLES = '''
- name: Test with a message
  register: mytoml
  my_test:
    payload: |
      debug: true
      ldap:
        enabled: true
        listen: '0.0.0.0:389'
      ldaps:
        enabled: false
        listen: '0.0.0.0:636'
      backend:
        datastore: config
        baseDN: 'dc=glauth,dc=com'
      users:
        - name: admin
          loginShell: /bin/bash
          homeDir: /home/admin
          unixid: 5001
          primarygroup: 6001
      groups:
        - name: admins
          unixid: 6001
      api:
        enabled: false

- name: view variable
  debug:
    var: mytoml

- name: get yaml payload
  debug:
    msg: "{{ mytoml.payload }}"

- name: get toml output
  debug:
    msg: "{{ mytoml.output }}"
'''

RETURN = '''
payload:
  description: The original payload
  type: str
  returned: always
output:
  description: toml output
  type: str
  returned: always
'''


from ansible.module_utils.basic import AnsibleModule

def run_module():
  module = AnsibleModule(
    argument_spec = {
      "payload": {
        "type": "str",
        "required": True
      }
    },
    supports_check_mode = True
  )
  
  try:
    import pytoml as toml
  except ImportError:
    module.fail_json(**{
      "changed": False,
      "msg": "pip install pytoml",
      "output": ""
    })
  except Exception as err:
    module.fail_json(**{
      "changed": False,
      "msg": err,
      "output": ""
    })

  try:
    import yaml
  except ImportError:
    module.fail_json(**{
      "changed": False,
      "msg": "pip install pyyaml",
      "output": ""
    })
  except Exception as err:
    module.fail_json(**{
      "changed": False,
      "msg": err,
      "output": ""
    })
  
  try:
    payload = yaml.load(module.params["payload"])
  except Exception as err:
    module.fail_json(**{
      "changed": False,
      "msg": err,
      "output": ""
    })
  
  try:
    module.exit_json(**{
      "changed": False,
      "payload": module.params["payload"],
      "output": toml.dumps(payload)
    })
  except Exception as err:
    module.fail_json(**{
      "changed": False,
      "msg": err,
      "output": ""
    })

def main():
  run_module()

if __name__ == '__main__':
  main()
