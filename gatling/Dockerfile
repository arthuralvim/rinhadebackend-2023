FROM openjdk:17-slim-buster

ENV GATLING_VERSION 3.10.5
ENV GATLING_HOME /opt/gatling

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

COPY rinha.ascii ${GATLING_HOME}
COPY scripts/docker-entrypoint.sh scripts/run.sh ${GATLING_HOME}/bin/
ENV PATH="$PATH:$GATLING_HOME/bin"
WORKDIR ${GATLING_HOME}

COPY rinhadebackend/resources ${GATLING_HOME}/user-files/resources
COPY rinhadebackend/simulations ${GATLING_HOME}/user-files/simulations

ENTRYPOINT ["/usr/bin/tini", "--", "docker-entrypoint.sh"]
CMD ["run.sh"]
