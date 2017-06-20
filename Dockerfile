# Choose your favorite base image
FROM frolvlad/alpine-python2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY saltexporter/salt_exporter.py .

EXPOSE 9118

ENTRYPOINT ["python", "-u", "./salt_exporter.py"]
