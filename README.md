# egeneralov.glauth

Ansible role for [GLAuth](https://github.com/glauth/glauth): LDAP authentication server for developers

## Requirements

Target: debian 9, 10.

## Role Variables

- **version**: `v1.1.1` release version from [GLAuth](https://github.com/glauth/glauth/releases)
- **glauth**: named array, glauth configuration in yaml format
  - **debug**: `true`, boolean
  - **ldap**:
    - **enabled**: `true`, boolean
    - **listen**: `0.0.0.0:389`, string, bind to
  - **ldaps**:
    - **enabled**: `true`, boolean
    - **listen**: `0.0.0.0:636`, string, bind to
    - **cert**: `/etc/glauth.crt`, string, tls crt
    - **key**: `/etc/glauth.key`, string, tls key
  - **backend**:
    - **datastore**: `config`, string, glauth datastore
    - **baseDN**: `dc=glauth,dc=com`, string
  - **users**:
    - **name**: `admin`, string
      - **loginShell**: `/bin/bash`, string
      - **homeDir**: `/home/admin`, string
      - **unixid**: `5001`, int
      - **primarygroup**: `6001`, int
  - **groups**:
    - **name**: `admins`, string
      - **unixid**: `6001`, int
  - **api**:
    - **enabled**: `false`, boolean
- **__urls__**: playbook required variables

Dependencies
------------

- [egeneralov.python](https://github.com/egeneralov/python) with `python_version: "2.7"` variable

## Example Playbook

### My example

    - hosts: all
      gather_facts: yes
      vars:
        python_version: "2.7"
        version: v1.1.1
        glauth:
          debug: true
          ldap:
            enabled: true
            listen: '0.0.0.0:389'
          ldaps:
            enabled: true
            listen: '0.0.0.0:636'
            cert: /etc/glauth.crt
            key: /etc/glauth.key
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
      roles:
        - egeneralov.python
        - egeneralov.glauth


### [sample-simple.cfg](https://github.com/glauth/glauth/blob/master/sample-simple.cfg)

    - hosts: all
      gather_facts: yes
      vars:
        python_version: "2.7"
        version: v1.1.1
        glauth:
          debug: true
          syslog: true
          ldap:
            enabled: true
            listen: 'localhost:3893'
          ldaps:
            enabled: true
            listen: 'localhost:3894'
            cert: certs/server.crt
            key: certs/server.key
          backend:
            datastore: config
            baseDN: 'dc=glauth,dc=com'
          users:
            - name: hackers
              unixid: 5001
              primarygroup: 5501
              passsha256: 6478579e37aff45f013e14eeb30b3cc56c72ccdc310123bcdf53e0333e3f416a
            - name: johndoe
              givenname: John
              sn: Doe
              mail: jdoe@example.com
              unixid: 5002
              primarygroup: 5501
              loginShell: /bin/sh
              homeDir: /root
              passsha256: 6478579e37aff45f013e14eeb30b3cc56c72ccdc310123bcdf53e0333e3f416a
              sshkeys:
                - >-
                  ssh-rsa
                  AAAAB3NzaC1yc2EAAAABJQAAAQEA3UKCEllO2IZXgqNygiVb+dDLJJwVw3AJwV34t2jzR+/tUNVeJ9XddKpYQektNHsFmY93lJw5QDSbeH/mAC4KPoUM47EriINKEelRbyG4hC/ko/e2JWqEclPS9LP7GtqGmscXXo4JFkqnKw4TIRD52XI9n1syYM9Y8rJ88fjC/Lpn+01AB0paLVIfppJU35t0Ho9doHAEfEvcQA6tcm7FLJUvklAxc8WUbdziczbRV40KzDroIkXAZRjX7vXXhh/p7XBYnA0GO8oTa2VY4dTQSeDAUJSUxbzevbL0ll9Gi1uYaTDQyE5gbn2NfJSqq0OYA+3eyGtIVjFYZgi+txSuhw==
                  rsa-key-20160209
              passappsha256:
                - c32255dbf6fd6b64883ec8801f793bccfa2a860f2b1ae1315cd95cdac1338efa
                - c9853d5f2599e90497e9f8cc671bd2022b0fb5d1bd7cfff92f079e8f8f02b8d3
                - 4939efa7c87095dacb5e7e8b8cfb3a660fa1f5edcc9108f6d7ec20ea4d6b3a88
            - name: serviceuser
              unixid: 5003
              primarygroup: 5502
              passsha256: 652c7dc687d98c9889304ed2e408c74b611e86a40caa51c4b43f1dd5913c5cd0
            - name: otpuser
              unixid: 5004
              primarygroup: 5501
              passsha256: 652c7dc687d98c9889304ed2e408c74b611e86a40caa51c4b43f1dd5913c5cd0
              otpsecret: 3hnvnk4ycv44glzigd6s25j4dougs3rk
              yubikey: vvjrcfalhlaa
          groups:
            - name: superheros
              unixid: 5501
            - name: svcaccts
              unixid: 5502
            - name: vpn
              unixid: 5503
              includegroups:
                - 5501
          api:
            enabled: true
            tls: false
            listen: 'localhost:5555'
            cert: cert.pem
            key: key.pem
      roles:
        - egeneralov.python
        - egeneralov.glauth

### [sample-ldap.cfg](https://github.com/glauth/glauth/blob/master/sample-ldap.cfg)

    - hosts: all
      gather_facts: yes
      vars:
        python_version: "2.7"
        version: v1.1.1
        glauth:
          syslog: true
          frontend:
            tls: true
            listen: '0.0.0.0:636'
            cert: cert.pem
            key: key.pem
          backend:
            datastore: ldap
            servers:
              - 'ldaps://server1:636'
              - 'ldaps://server2:636'
          api:
            enabled: true
            tls: true
            listen: 'localhost:5555'
            cert: cert.pem
            key: key.pem
      roles:
        - egeneralov.python
        - egeneralov.glauth

## License

MIT

## Author Information

Eduard Generalov <eduard@generalov.net>
