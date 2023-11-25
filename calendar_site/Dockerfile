# Set version
FROM python:3.8

# Set up workdir
WORKDIR /usr/src/calendar_site

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/calendar_site/entrypoint.sh
RUN chmod +x /usr/src/calendar_site/entrypoint.sh

COPY ./populate_data.py /usr/src/calendar_site/

# Copy static files
COPY ./static /usr/src/calendar_site/


# Copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/calendar_site/entrypoint.sh"]
