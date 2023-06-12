FROM redhat/ubi8
RUN dnf update -y && dnf install -y podman python3.9 git redis wget postfix

CMD ["bash", "-c", "postfix start && tail -f /dev/null"]