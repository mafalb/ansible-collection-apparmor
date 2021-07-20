# Ansible Role mafalb.apparmor.apparmor

## Basic Usage

```yaml
- name: install mafalb.apparmor.apparmor
  hosts: localhost
  roles:
  - role: mafalb.apparmor.apparmor
```

```yaml
- name: install mafalb.apparmor.apparmor
  hosts: localhost
  roles:
  - role: mafalb.apparmor.apparmor
    state: disabled
```

## Variables

```state: enforcing``` # apparmor is enforcing

```state: permissive``` # apparmor is permissive

```state: disabled``` # apparmor is disabled

## License

Copyright (c) 2021 Markus Falb <markus.falb@mafalb.at>

GPL-3.0-or-later
