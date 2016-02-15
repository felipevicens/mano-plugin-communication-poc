FROM python:2-onbuild
COPY . /home/dev
WORKDIR /home/dev
CMD ["/bin/bash","/home/dev/entrypoint.sh"]
