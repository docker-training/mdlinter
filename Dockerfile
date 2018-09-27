FROM python:3.5

ADD lint.py /lint.py

CMD python lint.py
