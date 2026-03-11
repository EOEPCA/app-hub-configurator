# Run the CLI with Docker

The configurator CLI can be executed directly from the Docker image.

This is useful when:
- you don’t want to install Python locally
- you want reproducible config generation
- you want to mount external profiles/plugins into the container

## Build the image

From the project root:

```bash
docker build -t application-hub-configurator .
```

## Example

From the project root:

```bash
docker run --rm -it \
  -v $PWD/output:/work \
  -v $PWD/data:/data \
  application-hub-configurator \
  dump-config \
  --profiles-dir /data \
  --profiles coder_app \
  --output /work/config.yaml \
  --groups group-2
```

## Notes

`--profiles-dir` allows loading extra profile modules/packages dynamically (plugin-style).

This is the recommended approach for:

* site-specific profiles
* experimental profiles
* profiles not shipped with the core configurator repository

## Volume mounts

You typically want:

- one mount for the output config location
- one mount for external profiles (plugins)

Example layout:

- `/data/...` contains external profiles
- `/work/...` contains your output folder

## Recommended pattern

```bash
docker run --rm -it \
  -v $PWD/output:/work \
  -v $PWD/extra-profiles:/extra-profiles \
  application-hub-configurator \
  dump-config \
  --profiles-dir /extra-profiles \
  --profiles my_custom_coder \
  --groups group-2 \
  --output /work/config.yaml
```

This produces `./output/config.yaml` on your host
