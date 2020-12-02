# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3.8-slim-buster
FROM selenium/standalone-chrome

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
#ADD requirements.txt .
#RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app
RUN ls /app
RUN ls /app/bin/
RUN python -m pip install -r /app/requirements.txt
RUN dpkg -i /app/bin/google-chrome-stable_current_amd64.deb

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 8080

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "application.py"]
