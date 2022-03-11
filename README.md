# ELK

Ansible role for deploying customised version of ELK, packed in docker. There are some pre-defined logstash patterns & pipelines, feel free to define yours.

## Dependencies
Following roles are expected to be present
- `veselahouba/docker`
- `veselahouba/docker_container`


## Usage

### Install role

```
ansible-galaxy install veselahouba.elk
```

Using requirements.yml is recommended.

### Configuration

Role is configured as single-node out-of-the box. Just setup your inventory and create playbook.

Following parts are installed by default, listening on `0.0.0.0`
- elasticsearch : ports 9200,9300
- logstash : port 5044 for beats
- kibana : port 5601
- cerebro : port 9000
- elastalert

It's recommended to change `elk_listen_ip: 127.0.0.1` and wrap services with proxy.

### Example playbook

```YAML
- name: Deploy ELK backend
  become: true
  hosts: elk_backend
  roles:
    - veselahouba.docker
    - veselahouba.elk
```

### Multi-node cluster

1. Put all your cluster hosts in inventory group
1. Pick one host to be initial master
1. Configure following variables
```YAML
elk_cluster: true
elk_group_name: elk
elk_master_hosts: elk-master.domain.com
```
1. Install with the same playbook as single-node

### Custom patterns/pipelines/alerts

### More info
For more detailed info and options consult `defaults/main.yml` file
