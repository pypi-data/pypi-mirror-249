# workflows-aggregator app

This service computes the `workflows.state` Kafka stream from the
`workflows.events` log.

## Usage

Build the image:

```bash
docker build -t workflows-aggregator .
```

Run the container:

```bash
docker run --rm -it workflows-aggregator
```

## Configuration

The following environment variables are available for configuration:

`DYFF_KAFKA__CONFIG__BOOTSTRAP_SERVERS`

`DYFF_KAFKA__STREAMS__APPLICATION_ID`

`DYFF_KAFKA__STREAMS__STATE_DIR`

`DYFF_KAFKA__STREAMS__PROCESSING_GUARANTEE`

`DYFF_KAFKA__TOPICS__WORKFLOWS_EVENTS`

`DYFF_KAFKA__TOPICS__WORKFLOWS_STATE`
