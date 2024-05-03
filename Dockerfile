FROM python:3.10.13

WORKDIR /crud_hw

COPY appuser.py .
COPY appbutton.py .
COPY basa.py . 
COPY requirements.txt .

RUN pip install -r requirements.txt