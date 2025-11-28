docker run -d -p 6333:6333 \
    -v $(pwd)/.qdrant/data:/qdrant/storage \
    -v $(pwd)/.qdrant/snapshots:/qdrant/snapshots \
    -v $(pwd)/.qdrant/config.yaml:/qdrant/config/production.yaml \
    qdrant/qdrant