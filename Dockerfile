FROM python

# create working directory so that we can transfer files from here to that particular folder. From this point on, realize we are working inside the /hms folder
WORKDIR /hms

# copy everything from here to the base image. Since the syntax is COPY source destination, the destination shall be '.' because we are now in the /hms folder
COPY . .

# install all the requirements using Pip
RUN pip install -r requirements.txt

# specify environment variables
ENV FLASK_APP=main.py

# specify the commands for running the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]