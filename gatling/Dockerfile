FROM python:3.9-slim-buster

ENV \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    GATLING_VERSION=3.9.5

RUN \
    apt-get update && apt-get install -y \
    curl \
    unzip \
    tini \
    && rm -rf /var/lib/apt/lists/*

# INSTALL JAVA 8
ENV JAVA_HOME="/usr/lib/jvm/java-1.8.0-openjdk-amd64" \
    PATH=${JAVA_HOME}/bin:${PATH}
COPY --from=java:8u111-jdk /usr/lib/jvm /usr/lib/jvm

RUN  \
    mkdir -p /test-runner/user-files/ \
    mkdir -p /test-runner/data/

WORKDIR /test-runner/

RUN \
    curl -fsSL "https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/${GATLING_VERSION}/gatling-charts-highcharts-bundle-${GATLING_VERSION}-bundle.zip" > /test-runner/gatling.zip && \
    unzip gatling.zip && \
    mv gatling-charts-highcharts-bundle-3.9.5 gatling && \
    rm gatling.zip

COPY docker-entrypoint.sh run.sh rinha.ascii /test-runner/
COPY data /test-runner/data/
COPY user-files /test-runner/user-files/

ENTRYPOINT ["/usr/bin/tini", "--", "./docker-entrypoint.sh"]
CMD ["./run.sh"]
