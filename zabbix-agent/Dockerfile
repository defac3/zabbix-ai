ARG BASE_IMAGE=debian:latest
FROM ${BASE_IMAGE}

RUN set -e; \
    if [ -f /etc/debian_version ]; then \
        apt-get update && apt-get install -y --no-install-recommends wget ca-certificates; \
        . /etc/os-release; rel="${ID}${VERSION_ID}"; base="https://repo.zabbix.com/zabbix/8.0/release/${ID}/pool/main/z/zabbix-release"; \
        wget -q "${base}/zabbix-release_8.0-0.1+${rel}_all.deb" -O /tmp/zabbix.deb || true; \
        if [ ! -f /tmp/zabbix.deb ]; then fallback=$([ "$ID" = debian ] && echo debian12 || echo ubuntu22.04); wget -q "${base}/zabbix-release_8.0-0.1+${fallback}_all.deb" -O /tmp/zabbix.deb; fi; \
        dpkg -i /tmp/zabbix.deb; apt-get update; apt-get install -y zabbix-agent2 sudo; \
        rm -rf /var/lib/apt/lists/* /tmp/zabbix.deb; \
    elif [ -f /etc/redhat-release ]; then \
        . /etc/os-release; el="${VERSION_ID%%.*}"; \
        dnf install -y "https://repo.zabbix.com/zabbix/8.0/release/rhel/${el}/noarch/zabbix-release-8.0-0.1.el${el}.noarch.rpm"; \
        dnf install -y zabbix-agent2 sudo; dnf clean all; \
    fi

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"

RUN echo '#!/bin/sh' > /usr/local/bin/sudo && echo 'exec /usr/bin/sudo "$@"' >> /usr/local/bin/sudo && chmod 755 /usr/local/bin/sudo
RUN (test -d /bin && test ! -L /bin && (echo '#!/bin/sh'; echo 'exec /usr/bin/sudo "$@"') > /bin/sudo && chmod 755 /bin/sudo) || true

COPY zabbix-agent/zabbix_agent2.conf /etc/zabbix/zabbix_agent2.conf
COPY zabbix-agent/zabbix-sudoers /etc/sudoers.d/zabbix
RUN chmod 0440 /etc/sudoers.d/zabbix
EXPOSE 10050
CMD ["sh", "-c", "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; exec zabbix_agent2 -f -c /etc/zabbix/zabbix_agent2.conf"]
