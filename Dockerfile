# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# RUN flask db init
# RUN flask db migrate
# RUN flask db upgrade

# copy every content from the local file to the image
COPY . /app

EXPOSE 5000

# configure the container to run in an executed manner
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

