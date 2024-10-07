# main.py

import os

if __name__ == "__main__":
    # Путь к файлу streamlit приложения
    streamlit_app_path = os.path.join("apps", "streamlit_app.py")

    # Запуск streamlit
    os.system(f"streamlit run {streamlit_app_path}")
