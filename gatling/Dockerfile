FROM openjdk:17-slim-buster

ENV GATLING_VERSION=3.10.5
ENV GATLING_HOME=/opt/gatling
ENV GATLING_BIN=${GATLING_HOME}/bin/
ENV GATLING_RESOURCES=${GATLING_HOME}/user-files/resources
ENV GATLING_SIMULATIONS=${GATLING_HOME}/user-files/simulations

RUN \
    apt-get update && apt-get install -y \
    curl \
    unzip \
    tini \
    python3 \
    && rm -rf /var/lib/apt/lists/*

RUN \
    curl -fsSL "https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/${GATLING_VERSION}/gatling-charts-highcharts-bundle-${GATLING_VERSION}-bundle.zip" > gatling.zip && \
    unzip gatling.zip && rm gatling.zip && \
    mv gatling-charts-highcharts-bundle-${GATLING_VERSION}/ ${GATLING_HOME}

COPY scripts ${GATLING_BIN}
COPY simulations ${GATLING_SIMULATIONS}
COPY rinha.ascii ${GATLING_HOME}

WORKDIR ${GATLING_HOME}
ENV PATH="$PATH:$GATLING_BIN"
RUN generate-resources.sh

ENTRYPOINT ["/usr/bin/tini", "--", "docker-entrypoint.sh"]
CMD ["run.sh"]
