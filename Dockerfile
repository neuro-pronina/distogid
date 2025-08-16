FROM python:3.11-slim

ENV OPENFACE_CMD=/opt/OpenFace/build/bin/FeatureExtraction

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg git build-essential cmake libopencv-dev && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/TadasBaltrusaitis/OpenFace.git /opt/OpenFace && \
    cd /opt/OpenFace && mkdir build && cd build && \
    cmake .. && make -j$(nproc)

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
