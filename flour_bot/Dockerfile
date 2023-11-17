FROM python

WORKDIR /bot
EXPOSE 8443
COPY ./src /bot
RUN pip3 install -r requirements.txt
CMD ["python3", "/bot/main.py"]

