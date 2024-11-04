# Ansible Collection - moreati.uv

A module for managing Python packages and virtualenvs using Astral's [uv].
The module is adapted from on Ansible's builtin [ansible.builtin.pip], so it
can be used as a drop in replacement.

[ansible.builtin.pip]: https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pip_module.html
[uv]: https://docs.astral.sh/uv/

## Example

```yaml
- name: Demonstrate moreati.uv
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Install requests to a virtualenv
      moreati.uv.pip:
        name: requests
        virtualenv: ~/venv
```

```console
$ ansible-playbook playbook.yml -v
PLAY [Demonstrate moreati.uv] **************************************************

TASK [Install requests to a virtualenv] ****************************************
changed: [localhost] => changed=true
  cmd:
  - /Users/alex/.cargo/bin/uv
  - pip
  - install
  - --python
  - /Users/alex/venv/bin/python
  - requests
  name:
  - requests
  requirements: null
  state: present
  stderr: |-
    Using CPython 3.13.0 interpreter at: /Users/alex/.local/share/uv/tools/ansible-core/bin/python
    Creating virtual environment at: /Users/alex/venv
    Activate with: source /Users/alex/venv/bin/activate
    Using Python 3.13.0 environment at /Users/alex/venv
    Resolved 5 packages in 44ms
    Installed 5 packages in 5ms
     + certifi==2024.8.30
     + charset-normalizer==3.4.0
     + idna==3.10
     + requests==2.32.3
     + urllib3==2.2.3
  stderr_lines: <omitted>
  stdout: ''
  stdout_lines: <omitted>
  version: null
  virtualenv: /Users/alex/venv

PLAY RECAP *********************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

$ ~/venv/bin/python -c "import requests; print(requests.get('https://httpbin.org/get'))"
<Response [200]>
```
