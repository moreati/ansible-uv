# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Matt Wright <matt@nobien.net>
# Copyright: (c) 2024, Alex Willmer <alex@moreati.org.uk>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


DOCUMENTATION = '''
---
module: pip
short_description: Manages Python library dependencies with Astral uv.
description:
     - "Manage Python library dependencies. To use this module, one of the following keys is required: O(name)
       or O(requirements)."
options:
  name:
    description:
      - The name of a Python library to install or the url(bzr+,hg+,git+,svn+) of the remote package.
      - This can be a list and contain version specifiers.
    type: list
    elements: str
  version:
    description:
      - The version number to install of the Python library specified in the O(name) parameter.
    type: str
  requirements:
    description:
      - The path to a requirements file, which should be local to the remote system.
        File can be specified as a relative path if using the chdir option.
    type: str
  virtualenv:
    description:
      - An optional path to a I(virtualenv) directory to install into.
        It cannot be specified together with the 'executable' parameter
        .
        If the virtualenv does not exist, it will be created before installing
        packages. The optional virtualenv_site_packages, virtualenv_command,
        and virtualenv_python options affect the creation of the virtualenv.
    type: path
  virtualenv_site_packages:
    description:
      - Whether the virtual environment will inherit packages from the
        global site-packages directory.  Note that if this setting is
        changed on an already existing virtual environment it will not
        have any effect, the environment must be deleted and newly
        created.
    type: bool
    default: "no"
  virtualenv_command:
    type: str
    default: uv pip
  virtualenv_python:
    description:
      - The Python executable used for creating the virtual environment.
        For example V(python3.12), V(python2.7). When not specified, the
        Python version used to run the ansible module is used.
    type: str
  state:
    description:
      - The state of module
    type: str
    choices: [ absent, forcereinstall, latest, present ]
    default: present
  extra_args:
    description:
      - Extra arguments passed to uv pip.
    type: str
  editable:
    description:
      - Pass the editable flag.
    type: bool
    default: 'no'
  chdir:
    description:
      - cd into this directory before running the command
    type: path
  executable:
    type: str
    default: uv pip
  umask:
    description:
      - The system umask to apply before installing the pip package. This is
        useful, for example, when installing on systems that have a very
        restrictive umask by default (e.g., "0077") and you want to pip install
        packages which are to be used by all users. Note that this requires you
        to specify desired umask mode as an octal string, (e.g., "0022").
    type: str
  break_system_packages:
    description:
      - Allow uv pip to modify an externally-managed Python installation as defined by PEP 668.
      - This is typically required when installing packages outside a virtual environment on modern systems.
    type: bool
    default: false
extends_documentation_fragment:
  -  action_common_attributes
attributes:
    check_mode:
        support: full
    diff_mode:
        support: none
    platform:
        platforms: posix
notes:
   - Python installations marked externally-managed (as defined by PEP668) cannot be updated by uv pip without the use of
     a virtual environment or setting the O(break_system_packages) option.
   - Astral uv must be installed on the remote host.
   - Astral uv >= 0.5.6 is required for O(state) = V(absent) in check mode.
requirements:
- uv
author:
- Matt Wright (@mattupstate)
- Alex Willmer (@moreati)
'''

EXAMPLES = '''
- name: Install bottle python package
  moreati.uv.pip:
    name: bottle

- name: Install bottle python package on version 0.11
  moreati.uv.pip:
    name: bottle==0.11

- name: Install bottle python package with version specifiers
  moreati.uv.pip:
    name: bottle>0.10,<0.20,!=0.11

- name: Install multi python packages with version specifiers
  moreati.uv.pip:
    name:
      - django>1.11.0,<1.12.0
      - bottle>0.10,<0.20,!=0.11

- name: Install python package using a proxy
  moreati.uv.pip:
    name: six
  environment:
    http_proxy: 'http://127.0.0.1:8080'
    https_proxy: 'https://127.0.0.1:8080'

# You do not have to supply '-e' option in extra_args
- name: Install MyApp using one of the remote protocols (bzr+,hg+,git+,svn+)
  moreati.uv.pip:
    name: svn+http://myrepo/svn/MyApp#egg=MyApp

- name: Install MyApp using one of the remote protocols (bzr+,hg+,git+)
  moreati.uv.pip:
    name: git+http://myrepo/app/MyApp

- name: Install MyApp from local tarball
  moreati.uv.pip:
    name: file:///path/to/MyApp.tar.gz

- name: Install bottle into the specified (virtualenv), inheriting none of the globally installed modules
  moreati.uv.pip:
    name: bottle
    virtualenv: /my_app/venv

- name: Install bottle into the specified (virtualenv), inheriting globally installed modules
  moreati.uv.pip:
    name: bottle
    virtualenv: /my_app/venv
    virtualenv_site_packages: yes

- name: Install bottle into the specified (virtualenv), using Python 3.12
  moreati.uv.pip:
    name: bottle
    virtualenv: /my_app/venv
    virtualenv_python: python3.12

- name: Install bottle within a user home directory
  moreati.uv.pip:
    name: bottle
    extra_args: --user

- name: Install specified python requirements
  moreati.uv.pip:
    requirements: /my_app/requirements.txt

- name: Install specified python requirements in indicated (virtualenv)
  moreati.uv.pip:
    requirements: /my_app/requirements.txt
    virtualenv: /my_app/venv

- name: Install specified python requirements and custom Index URL
  moreati.uv.pip:
    requirements: /my_app/requirements.txt
    extra_args: -i https://example.com/pypi/simple

- name: Install specified python requirements offline from a local directory with downloaded packages
  moreati.uv.pip:
    requirements: /my_app/requirements.txt
    extra_args: "--no-index --find-links=file:///my_downloaded_packages_dir"

- name: Install bottle for Python 3.3 specifically, using the 'pip3.3' executable
  moreati.uv.pip:
    name: bottle
    executable: pip3.3

- name: Install bottle, forcing reinstallation if it's already installed
  moreati.uv.pip:
    name: bottle
    state: forcereinstall

- name: Install bottle while ensuring the umask is 0022 (to ensure other users can use it)
  moreati.uv.pip:
    name: bottle
    umask: "0022"
  become: True

- name: Run a module inside a virtual environment
  block:
    - name: Ensure the virtual environment exists
      pip:
        name: psutil
        virtualenv: "{{ venv_dir }}"
        # On Debian-based systems the correct python*-venv package must be installed to use the `venv` module.
        virtualenv_command: "{{ ansible_python_interpreter }} -m venv"

    - name: Run a module inside the virtual environment
      wait_for:
        port: 22
      vars:
        # Alternatively, use a block to affect multiple tasks, or use set_fact to affect the remainder of the playbook.
        ansible_python_interpreter: "{{ venv_python }}"

  vars:
    venv_dir: /tmp/pick-a-better-venv-path
    venv_python: "{{ venv_dir }}/bin/python"
'''

RETURN = '''
cmd:
  description: pip command used by the module
  returned: success
  type: str
  sample: pip2 install ansible six
name:
  description: list of python modules targeted by pip
  returned: success
  type: list
  sample: ['ansible', 'six']
requirements:
  description: Path to the requirements file
  returned: success, if a requirements file was provided
  type: str
  sample: "/srv/git/project/requirements.txt"
version:
  description: Version of the package specified in 'name'
  returned: success, if a name and version were provided
  type: str
  sample: "2.5.1"
virtualenv:
  description: Path to the virtualenv
  returned: success, if a virtualenv path was provided
  type: str
  sample: "/tmp/virtualenv"
'''

import argparse
import os
import re
import sys
import tempfile
import operator
import shlex

from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule, is_executable
from ansible.module_utils.common.locale import get_best_parsable_locale


_VCS_RE = re.compile(r'(svn|git|hg|bzr)\+')

op_dict = {">=": operator.ge, "<=": operator.le, ">": operator.gt,
           "<": operator.lt, "==": operator.eq, "!=": operator.ne, "~=": operator.ge}


def _is_vcs_url(name):
    """Test whether a name is a vcs url or not."""
    return re.match(_VCS_RE, name)


def _is_venv_command(command):
    venv_parser = argparse.ArgumentParser()
    venv_parser.add_argument('-m', type=str)
    argv = shlex.split(command)
    if argv[0] == 'pyvenv':
        return True
    args, dummy = venv_parser.parse_known_args(argv[1:])
    if args.m == 'venv':
        return True
    return False


def _is_package_name(name):
    """Test whether the name is a package name or a version specifier."""
    return not name.lstrip().startswith(tuple(op_dict.keys()))


def _recover_package_name(names):
    """Recover package names as list from user's raw input.

    :input: a mixed and invalid list of names or version specifiers
    :return: a list of valid package name

    eg.
    input: ['django>1.11.1', '<1.11.3', 'ipaddress', 'simpleproject>1.1.0', '<2.0.0']
    return: ['django>1.11.1,<1.11.3', 'ipaddress', 'simpleproject>1.1.0,<2.0.0']

    input: ['django>1.11.1,<1.11.3,ipaddress', 'simpleproject>1.1.0,<2.0.0']
    return: ['django>1.11.1,<1.11.3', 'ipaddress', 'simpleproject>1.1.0,<2.0.0']
    """
    # rebuild input name to a flat list so we can tolerate any combination of input
    tmp = []
    for one_line in names:
        tmp.extend(one_line.split(","))
    names = tmp

    # reconstruct the names
    name_parts = []
    package_names = []
    in_brackets = False
    for name in names:
        if _is_package_name(name) and not in_brackets:
            if name_parts:
                package_names.append(",".join(name_parts))
            name_parts = []
        if "[" in name:
            in_brackets = True
        if in_brackets and "]" in name:
            in_brackets = False
        name_parts.append(name)
    package_names.append(",".join(name_parts))
    return package_names


def _get_cmd_options(module, cmd):
    thiscmd = cmd + " --help"
    rc, stdout, stderr = module.run_command(thiscmd)
    if rc != 0:
        module.fail_json(msg="Could not get output from %s: %s" % (thiscmd, stdout + stderr))

    words = stdout.strip().split()
    cmd_options = [x for x in words if x.startswith('--')]
    return cmd_options


def _get_packages(module, pip, chdir):
    '''Return results of pip command to get packages.'''
    # Try 'pip list' command first.
    command = pip + ['list', '--format=freeze']
    locale = get_best_parsable_locale(module)
    lang_env = {'LANG': locale, 'LC_ALL': locale, 'LC_MESSAGES': locale}
    rc, out, err = module.run_command(command, cwd=chdir, environ_update=lang_env)

    if rc != 0:
            _fail(module, command, out, err)

    return ' '.join(command), out, err


def _get_pip(module, env=None, executable=None):
    candidate_argvs = (
        ['uv', 'pip'],
    )
    pip = None
    if executable is not None:
        argv = shlex.split(executable)
        if os.path.isabs(argv[0]):
            pip = argv
        else:
            # If you define your own executable that executable should be the only candidate.
            # As noted in the docs, executable doesn't work with virtualenvs.
            candidate_argvs = (argv,)

    if pip is None:
            opt_dirs = []
            for basename, *rest in candidate_argvs:
                uv = module.get_bin_path(basename, False, opt_dirs)
                if uv is not None:
                    pip = [uv, *rest]
                    break
            else:
                # For-else: Means that we did not break out of the loop
                # (therefore, that pip was not found)
                basenames = ', '.join(argv[0] for argv in candidate_argvs)
                module.fail_json(msg=f'Unable to find any of {basenames} to use. uv needs to be installed.')

    return pip


def _fail(module, cmd, out, err):
    msg = ''
    if out:
        msg += "stdout: %s" % (out, )
    if err:
        msg += "\n:stderr: %s" % (err, )
    module.fail_json(cmd=cmd, msg=msg)


def setup_virtualenv(module, env, chdir, out, err):
    if module.check_mode:
        module.exit_json(changed=True)

    cmd = shlex.split(module.params['virtualenv_command'])

    # Find the binary for the command in the PATH
    # and switch the command for the explicit path.
    if os.path.basename(cmd[0]) == cmd[0]:
        cmd[0] = module.get_bin_path(cmd[0], True)

    # Add the system-site-packages option if that
    # is enabled, otherwise explicitly set the option
    # to not use system-site-packages if that is an
    # option provided by the command's help function.
    if module.params['virtualenv_site_packages']:
        cmd.append('--system-site-packages')
    else:
        cmd_opts = _get_cmd_options(module, cmd[0])
        if '--no-site-packages' in cmd_opts:
            cmd.append('--no-site-packages')

    # Only use already installed Python interpreters.
    # Don't download them, for now.
    cmd.extend(['--python-preference', 'only-system'])

    virtualenv_python = module.params['virtualenv_python']
    # -p is a virtualenv option, not compatible with pyenv or venv
    # this conditional validates if the command being used is not any of them
    if not _is_venv_command(module.params['virtualenv_command']):
        if virtualenv_python:
            cmd.append('-p%s' % virtualenv_python)
        else:
            # This code mimics the upstream behaviour of using the python
            # which invoked virtualenv to determine which python is used
            # inside of the virtualenv (when none are specified).
            cmd.append('-p%s' % sys.executable)

    # if venv or pyvenv are used and virtualenv_python is defined, then
    # virtualenv_python is ignored, this has to be acknowledged
    elif module.params['virtualenv_python']:
        module.fail_json(
            msg='virtualenv_python should not be used when'
                ' using the venv module or pyvenv as virtualenv_command'
        )

    cmd.append(env)
    rc, out_venv, err_venv = module.run_command(cmd, cwd=chdir)
    out += out_venv
    err += err_venv
    if rc != 0:
        _fail(module, cmd, out, err)
    return out, err


class Package:
    """Python distribution package metadata wrapper.

    A wrapper class for Requirement, which provides
    API to parse package name, version specifier,
    test whether a package is already satisfied.
    """

    # https://packaging.python.org/en/latest/specifications/name-normalization/#name-normalization
    _CANONICALIZE_RE = re.compile(r'[-_.]+')

    # https://packaging.python.org/en/latest/specifications/name-normalization/#name-format
    _NAME_RE = re.compile(r'[A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9]', re.IGNORECASE)

    _VERSION_OPS_RE = re.compile('|'.join(re.escape(s) for s in op_dict))

    def __init__(self, requirement):
            self._unparsed = requirement
            self.name = self._NAME_RE.match(requirement)

    @property
    def has_version_specifier(self):
        if self._VERSION_OPS_RE.search(self._unparsed):
            return True
        return False

    @staticmethod
    def canonicalize_name(name):
        # This is taken from PEP 503.
        return Package._CANONICALIZE_RE.sub("-", name).lower()

    def __str__(self):
        return self._unparsed

    def __repr__(self):
        return f'{self.__class__.__name__}({self._unparsed})'


def main():
    state_map = dict(
        present=['install'],
        absent=['uninstall'],
        latest=['install', '-U'],
        forcereinstall=['install', '-U', '--force-reinstall'],
    )

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=list(state_map.keys())),
            name=dict(type='list', elements='str'),
            version=dict(type='str'),
            requirements=dict(type='str'),
            virtualenv=dict(type='path'),
            virtualenv_site_packages=dict(type='bool', default=False),
            virtualenv_command=dict(type='str', default='uv venv'),
            virtualenv_python=dict(type='str'),
            extra_args=dict(type='str'),
            editable=dict(type='bool', default=False),
            chdir=dict(type='path'),
            executable=dict(type='str', default='uv pip'),
            umask=dict(type='str'),
            break_system_packages=dict(type='bool', default=False),
        ),
        required_one_of=[['name', 'requirements']],
        mutually_exclusive=[['name', 'requirements'], ['executable', 'virtualenv']],
        supports_check_mode=True,
    )

    state = module.params['state']
    name = module.params['name']
    version = module.params['version']
    requirements = module.params['requirements']
    extra_args = module.params['extra_args']
    chdir = module.params['chdir']
    umask = module.params['umask']
    env = module.params['virtualenv']

    venv_created = False
    if env and chdir:
        env = os.path.join(chdir, env)

    if umask and not isinstance(umask, int):
        try:
            umask = int(umask, 8)
        except Exception:
            module.fail_json(msg="umask must be an octal integer",
                             details=to_native(sys.exc_info()[1]))

    old_umask = None
    if umask is not None:
        old_umask = os.umask(umask)
    try:
        if state == 'latest' and version is not None:
            module.fail_json(msg='version is incompatible with state=latest')

        if chdir is None:
            # this is done to avoid permissions issues with privilege escalation and virtualenvs
            chdir = tempfile.gettempdir()

        err = ''
        out = ''

        if env:
            if not os.path.exists(os.path.join(env, 'bin', 'activate')):
                venv_created = True
                out, err = setup_virtualenv(module, env, chdir, out, err)
            py_bin = os.path.join(env, 'bin', 'python')
        else:
            py_bin = module.params['executable'] or sys.executable

        pip = _get_pip(module, env, module.params['executable'])

        cmd = pip + state_map[state]
        cmd.extend(['--python', py_bin])

        # If there's a virtualenv we want things we install to be able to use other
        # installations that exist as binaries within this virtualenv. Example: we
        # install cython and then gevent -- gevent needs to use the cython binary,
        # not just a python package that will be found by calling the right python.
        # So if there's a virtualenv, we add that bin/ to the beginning of the PATH
        # in run_command by setting path_prefix here.
        path_prefix = None
        if env:
            path_prefix = os.path.join(env, 'bin')

        # Automatically apply -e option to extra_args when source is a VCS url. VCS
        # includes those beginning with svn+, git+, hg+ or bzr+
        has_vcs = False
        if name:
            for pkg in name:
                if pkg and _is_vcs_url(pkg):
                    has_vcs = True
                    break

            # convert raw input package names to Package instances
            packages = [Package(pkg) for pkg in _recover_package_name(name)]
            # check invalid combination of arguments
            if version is not None:
                if len(packages) > 1:
                    module.fail_json(
                        msg="'version' argument is ambiguous when installing multiple package distributions. "
                            "Please specify version restrictions next to each package in 'name' argument."
                    )
                if packages[0].has_version_specifier:
                    module.fail_json(
                        msg="The 'version' argument conflicts with any version specifier provided along with a package name. "
                            "Please keep the version specifier, but remove the 'version' argument."
                    )
                # if the version specifier is provided by version, append that into the package
                packages[0] = Package(f'{packages[0]}=={version}')

        if module.params['editable']:
            args_list = []  # used if extra_args is not used at all
            if extra_args:
                args_list = extra_args.split(' ')
            if '-e' not in args_list:
                args_list.append('-e')
                # Ok, we will reconstruct the option string
                extra_args = ' '.join(args_list)

        if extra_args:
            cmd.extend(shlex.split(extra_args))

        if module.params['break_system_packages']:
            # Using an env var instead of the `--break-system-packages` option, to avoid failing under pip 23.0.0 and earlier.
            # See: https://github.com/pypa/pip/pull/11780
            os.environ['PIP_BREAK_SYSTEM_PACKAGES'] = '1'

        if name:
            cmd.extend(to_native(p) for p in packages)
        elif requirements:
            cmd.extend(['-r', requirements])
        else:
            module.exit_json(
                changed=False,
                warnings=["No valid name or requirements file found."],
            )

        if module.check_mode:
            if extra_args or requirements or state == 'latest' or not name:
                module.exit_json(changed=True)

            # `uv pip install --dry-run` requires uv >= 0.1.18 (2024-03-13)
            # `uv pip uninstall --dry-run` requires uv >= 0.5.6 (2024-12-03)
            cmd += ['--dry-run']
            rc, dryrun_out, dryrun_err = module.run_command(cmd, path_prefix=path_prefix, cwd=chdir)
            out += dryrun_out
            err += dryrun_err
            if rc != 0:
                _fail(module, cmd, out, err)
            dryrun_match = re.search(r'^(?:Would uninstall|Would install)', dryrun_err, re.MULTILINE)
            changed = bool(dryrun_match)
            module.exit_json(changed=changed, cmd=cmd, stdout=out, stderr=err)

        out_freeze_before = None
        if requirements or has_vcs:
            dummy, out_freeze_before, dummy = _get_packages(module, pip, chdir)

        rc, out_pip, err_pip = module.run_command(cmd, path_prefix=path_prefix, cwd=chdir)
        out += out_pip
        err += err_pip
        if rc == 1 and state == 'absent' and \
           ('not installed' in out_pip or 'not installed' in err_pip):
            pass  # rc is 1 when attempting to uninstall non-installed package
        elif rc != 0:
            _fail(module, cmd, out, err)

        if state == 'absent':
            changed = 'Successfully uninstalled' in out_pip
        else:
            if out_freeze_before is None:
                changed = 'Successfully installed' in out_pip
            else:
                dummy, out_freeze_after, dummy = _get_packages(module, pip, chdir)
                changed = out_freeze_before != out_freeze_after

        changed = changed or venv_created

        module.exit_json(changed=changed, cmd=cmd, name=name, version=version,
                         state=state, requirements=requirements, virtualenv=env,
                         stdout=out, stderr=err)
    finally:
        if old_umask is not None:
            os.umask(old_umask)


if __name__ == '__main__':
    main()
