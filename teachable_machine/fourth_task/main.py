import requests, streamlit as st, logging, time

API_BASE_URL = "http://127.0.0.1:8000/"

def request_api(path_to_api: str, files: tuple):
    trying = 3
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    logger = logging.getLogger(__name__)

    url = f"{API_BASE_URL}{path_to_api}"
    
    while trying > 0:
        try:
            response = requests.post(url, files=files)

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при обращении к API\n{str(e)}")

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения к API\n{str(e)}")
        
        except Exception as e:
            logger.error(f"Неожиданная ошибка\n{str(e)}")

        time.sleep(5)
        trying -= 1

def site():
    def predict_car(data):
        with st.spinner("Обработка..."):
            response = request_api('get_predict', data)
            if response:
                st.dataframe(response)

    def page_rendering():
        st.header("Для предсказания добавьте фотографию и нажмите кнопку 'Предсказать'.")
        uploaded_file = st.file_uploader(
            "Выберите фото...",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            st.image(uploaded_file)
        
            if st.button("Предсказать"):
                predict_car({'file' : (uploaded_file.name, uploaded_file.read(), uploaded_file.file_id)})

    def information_page():
        st.html("<h2>Данный проект представляет собой предсказание автомоблией(ВАЗ 2107, LADA GRANTA, LADA NIVA), по выбранному пользователем фотографии.<br/><h2/>")
        st.html("<p style='font-size: 18px'>Как использовать систему:<br/>- нажмите на кнопку 'выбрать фото' и выберете фотографию с вашего устройства;<br/> - появится кнопка 'Предсказать', необходимо нажать на неё.<br/><br/>Стек используемых технологий:<br/> - FastApi: API для предсказывания автомобиля машинным обучением;<br/> - Streamlit: сайт для удобной работы с машинным обучением.<p/>")

    st.set_page_config(
        page_title="Система для предсказания автомобиля(ВАЗ 2107, LADA GRANTA, LADA NIVA)",
        layout="wide"
    )

    st.title("Система для предсказания автомобиля(ВАЗ 2107, LADA GRANTA, LADA NIVA)")

    page = st.sidebar.radio("Выберите вкладку:",
                            ["Предсказания автомобиля", "Информация о проекте"])
    
    match(page):
        case "Предсказания автомобиля":
            page_rendering()

        case "Информация о проекте":
            information_page()

if __name__ == '__main__':
    site()