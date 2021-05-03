export $(grep -v '^#' .env | xargs)

streamlit run interface/translator_interface.py --server.port $INTERFACE_PORT &
uvicorn translator.api.server:app --reload --workers $(nproc --all) --host 0.0.0.0 --port $AI_PORT