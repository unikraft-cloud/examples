FROM alpine:3.14 as base

WORKDIR /

# Create a symlink for default model
RUN set -xe; \
    mkdir -p /models/stories15M && \
    ln -sfn /models/stories15M /models/DEFAULT

FROM scratch

COPY --from=base ./models /models
COPY ./stories15M.bin /models/stories15M/model.bin
COPY ./tokenizer.bin /models/stories15M/tokenizer.bin
