FROM python:3.5

ADD lint.py /lint.py

ADD check_links_md.sh /check_links_md.sh

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
