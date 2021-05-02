streamlit run interface/translator_interface.py --server.port 5002 &
uvicorn translator.api.server:app --reload --workers $(nproc --all) --host 0.0.0.0 --port 5001