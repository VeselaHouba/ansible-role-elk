#!/usr/bin/env bash
docker \
  run \
  --rm \
  -ti \
  -v "$(pwd):/tmp/$(basename "${PWD}")" \
  -w "/tmp/$(basename "${PWD}")" \
  -e HCLOUD_TOKEN \
  -e MOLECULE_IMAGE="${MOLECULE_IMAGE:-debian-11}" \
  -e OS_VERSION="${MOLECULE_IMAGE//./_}" \
  -e MOLECULE_NO_LOG=false \
  -e REF=manual \
  -e REPO_NAME="$(basename "${PWD}")" \
  veselahouba/molecule bash -c "
  shellcheck_wrapper && \
  flake8 && \
  yamllint . && \
  ansible-lint && \
  cp -a ./ /tmp/role/ && \
  cd /tmp/role && \
  curl https://raw.githubusercontent.com/VeselaHouba/molecule/master/molecule-hetznercloud/pull_files.sh > ci/pull_files.sh && \
  bash ci/pull_files.sh && \
  molecule ${*}"
