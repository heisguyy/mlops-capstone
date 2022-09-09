FROM public.ecr.aws/lambda/python:3.9

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

RUN pip install -r requirements.txt

ARG WANDB_KEY
RUN wandb login $WANDB_KEY
RUN wandb artifact get --root artifacts/ heisguyy/capstone-mlops/capstone-model:latest
RUN wandb artifact get --root artifacts/ heisguyy/capstone-mlops/capstone-encoder:latest

CMD ["main.handler"]
