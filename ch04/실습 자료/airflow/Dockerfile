FROM apache/airflow:2.11.0
USER root
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh
RUN usermod -aG root airflow
RUN apt-get install -y acl
RUN setfacl -Rm d:g:root:rwx,g:root:rwx /var/run/
RUN apt install -y openssh-server
RUN mkdir /run/sshd && chmod 700 /run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/g' \
            /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' \
            /etc/ssh/sshd_config \
    && sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' \
            /etc/ssh/sshd_config \
    && sed -i 's/#AuthorizedKeysFile/AuthorizedKeysFile/g' \
            /etc/ssh/sshd_config
USER airflow