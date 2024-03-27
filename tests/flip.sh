pip install -e  '..[dev]'
cd ../app
ray stop
bash launch.sh
watch -n 1 serve status
