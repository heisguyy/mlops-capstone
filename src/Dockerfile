FROM tiangolo/uvicorn-gunicorn:python3.8

# Extension Code
COPY extensions/runner /opt/extensions/model-monitor-extension
RUN chmod +x /opt/extensions/model-monitor-extension

COPY extensions/model-monitor-extension/ /opt/model-monitor-extension/
WORKDIR /opt/model-monitor-extension/
RUN pip install -r requirements.txt -t .
RUN chmod +x extension.py

# Function code
WORKDIR /var/task

COPY *.py .
COPY requirements.txt .


RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ARG WANDB_KEY
RUN wandb login $WANDB_KEY
RUN wandb artifact get --root artifacts/ heisguyy/capstone-mlops/capstone-model:latest
RUN wandb artifact get --root artifacts/ heisguyy/capstone-mlops/capstone-encoder:latest

CMD ["main.app.handler"]