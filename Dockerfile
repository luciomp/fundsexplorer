# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster
#FROM selenium/standalone-chrome

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

# Install Chrome
RUN apt-get -y update && apt-get install -y gnupg2
#ADD https://dl-ssl.google.com/linux/linux_signing_key.pub ./chrome_key
#RUN apt-key add ./chrome_key
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get install -y google-chrome-stable
RUN apt install -y /app/bin/google-chrome-stable_current_amd64.deb

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 8080

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "application.py"]
