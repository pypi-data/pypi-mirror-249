ARG CONTAINER_PROXY
FROM ${CONTAINER_PROXY}maven:3.9.3-eclipse-temurin-17 as build
ARG WORKFLOWS_AGGREGATOR_VERSION="0.0.0"

WORKDIR /build/

COPY . ./

RUN mvn versions:set "-DnewVersion=${WORKFLOWS_AGGREGATOR_VERSION}" \
    && mvn clean package

ARG CONTAINER_PROXY
FROM ${CONTAINER_PROXY}eclipse-temurin:17
ARG WORKFLOWS_AGGREGATOR_VERSION="0.0.0"

WORKDIR /workflows-aggregator/

COPY --from=build "/build/target/workflows-aggregator-${WORKFLOWS_AGGREGATOR_VERSION}-jar-with-dependencies.jar" workflows-aggregator.jar

ENTRYPOINT ["java", "-cp", "workflows-aggregator.jar", "io.dyff.kafka.streams.WorkflowsAggregatorApp"]
