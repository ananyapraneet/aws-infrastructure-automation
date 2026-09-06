FROM python:3.13-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" \
    -o /tmp/session-manager-plugin.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       /tmp/session-manager-plugin.deb \
    && rm -f /tmp/session-manager-plugin.deb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "ansible-core==2.20.6" \
    "boto3" \
    "botocore"

RUN ansible-galaxy collection install \
    "amazon.aws:==10.1.2" \
    "community.general:==13.3.0" \
    "ansible.posix:==2.1.0"

WORKDIR /workspace
