#FROM python:2
#
#ADD . /SNR
#
#WORKDIR /SNR
#
#RUN pip install -r requirements.txt
#
#CMD [ "python", "./manage.py runserver doc" ]

# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3-onbuild

# COPY startup script into known file location in container
COPY start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!
