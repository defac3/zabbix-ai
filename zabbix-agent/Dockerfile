ARG BASE_IMAGE=debian:latest
FROM ${BASE_IMAGE}

RUN set -e; \
    if [ -f /etc/debian_version ]; then \
        apt-get update && apt-get install -y --no-install-recommends wget ca-certificates; \
        . /etc/os-release; rel="${ID}${VERSION_ID}"; base="https://repo.zabbix.com/zabbix/8.0/release/${ID}/pool/main/z/zabbix-release"; \
        wget -q "${base}/zabbix-release_8.0-0.1+${rel}_all.deb" -O /tmp/zabbix.deb || true; \
        if [ ! -f /tmp/zabbix.deb ]; then fallback=$([ "$ID" = debian ] && echo debian12 || echo ubuntu22.04); wget -q "${base}/zabbix-release_8.0-0.1+${fallback}_all.deb" -O /tmp/zabbix.deb; fi; \
        dpkg -i /tmp/zabbix.deb; apt-get update; apt-get install -y zabbix-agent2; \
        rm -rf /var/lib/apt/lists/* /tmp/zabbix.deb; \
    elif [ -f /etc/redhat-release ]; then \
        . /etc/os-release; el="${VERSION_ID%%.*}"; \
        dnf install -y "https://repo.zabbix.com/zabbix/8.0/release/rhel/${el}/noarch/zabbix-release-8.0-0.1.el${el}.noarch.rpm"; \
        dnf install -y zabbix-agent2; dnf clean all; \
    fi

COPY zabbix-agent/zabbix_agent2.conf /etc/zabbix/zabbix_agent2.conf
EXPOSE 10050
CMD ["zabbix_agent2", "-f", "-c", "/etc/zabbix/zabbix_agent2.conf"]
