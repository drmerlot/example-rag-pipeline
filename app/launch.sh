# launch the nessesary services

# launch the chromaDB server
chroma run

# Launch the service locally
export RAY_ROTATION_MAX_BYTES=102400
export RAY_ROTATION_BACKUP_COUNT=1

# start the ray cluster
ray start --head --disable-usage-stats  #--num-cpus
serve deploy ./launch.py
