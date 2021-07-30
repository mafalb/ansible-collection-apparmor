#!/usr/bin/python
# vim: set ft=python:

# This file is part of Ansible collection mafalb.apparmor
# Copyright (c) 2021 Markus Falb <markus.falb@mafalb.at>
#
# Ansible collection mafalb.apparmor is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Ansible collection mafalb.apparmor is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible collection mafalb.apparmor.
# If not, see <https://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: profile

short_description: Set the state of a apparmor profile

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "0.0.1"

description: Set the state of a apparmor profile.

options:
    name:
        description: This is the profile to operate on.
        required: true
        type: str
    state:
        description: The state of the profile
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
#extends_documentation_fragment:
#    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Markus Falb (@mafalb)
'''

EXAMPLES = r'''
- name: permissive mode
  mafalb.apparmor.profile:
    name: 'usr.sbin.mysql'
    state: complain

- name: enforce a profile
  mafalb.apparmor.profile:
    name: 'usr.sbin.mysql'
    state: enforce
'''

RETURN = r'''
original_state:
    description: The original state of the profile
    type: str
    returned: always
    sample: 'enforce'
state:
    description: The resulting state of the profile
    type: str
    returned: always
    sample: 'complain'
'''

from ansible.module_utils.basic import AnsibleModule  # noqa: E402
import json                                           # noqa: E402


# get the status of a profile
#
def get_profile_state(profile, module, result):
    status_cmd = '/usr/sbin/aa-status'
    rc, out, err = module.run_command([status_cmd, '--json'],
                                      check_rc=True)
    aa_status = json.loads(out)
    if profile not in aa_status['profiles']:
        # the profile is not known to apparmor
        module.fail_json(msg="unknown profile '%s'" % profile, **result)
    return aa_status['profiles'][profile]


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_state='',
        state=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    commands = dict(
        complain='/usr/sbin/aa-complain',
        enforce='/usr/sbin/aa-enforce'
    )

    # check if we implemented the requested state
    #
    if (module.params['state'] not in commands):
        module.fail_json(msg="Unknown state '%s' requested or not implemented"
                         % module.params['state'], **result)

    # get the status of the profile
    #
    result['original_state'] = get_profile_state(module.params['name'], module, result)  # noqa E501
    if module.check_mode:
        # return if in check mode
        module.exit_json(**result)
    if result['original_state'] != module.params['state']:
        # state is not what we want
        rc, out, err = module.run_command([commands[module.params['state']],
                                          module.params['name']],
                                          check_rc=True)
        profile_state = get_profile_state(module.params['name'], module, result)  # noqa E501
        if profile_state != module.params['state']:
            # state ist still not what we want
            module.fail_json(msg="setting state '%s' failed: actual state %s"
                             % (module.params['state'], profile_state),
                             **result)
        result['state'] = module.params['state']
        result['changed'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
