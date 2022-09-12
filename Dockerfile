FROM public.ecr.aws/lambda/python:3.9

# Extension Code
COPY src/extensions/runner /opt/extensions/model-monitor-extension
RUN chmod +x /opt/extensions/model-monitor-extension

COPY src/extensions/model-monitor-extension/ /opt/model-monitor-extension/
WORKDIR /opt/model-monitor-extension/
RUN pip install -r requirements.txt -t .
RUN chmod +x extension.py

# Function code
WORKDIR /var/task

COPY src/*.py src/
#when you clean pipfile change this
COPY src/requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["/lambda-entrypoint.sh", "src.main.handler"]
