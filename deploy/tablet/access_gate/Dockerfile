FROM python:3.13.18-slim-trixie@sha256:76baad6037690d6e8c4397fbcaef17bca6f19eecef822b708fe8fa3417d30bb5
WORKDIR /gate
COPY deploy/tablet/access_gate/requirements.lock ./
RUN python -m pip install --no-cache-dir -r requirements.lock \
    && python -m pip uninstall --yes pip
COPY deploy/tablet/access_gate/gate.py ./
USER 10001:10001
ENV PYTHONDONTWRITEBYTECODE=1
CMD ["python", "gate.py"]
