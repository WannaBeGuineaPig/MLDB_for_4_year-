import requests, streamlit as st, logging, time, pandas as pd
from PIL import Image, ImageOps
from streamlit_drawable_canvas import st_canvas

API_BASE_URL = "http://127.0.0.1:8000/"
SIZE_IMAGE_DRAW = (284, 284)

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
    def predict_digit(data):
        with st.spinner("Обработка..."):
            response = request_api('predict', data)
            if response:
                st.table(response)
                st.markdown("<style>div.stTable {font-size: 30px;}</style>", unsafe_allow_html=True)

    def page_rendering():
        st.header("Для предсказания нарисуйте на холсте и нажмите кнопку 'Предсказать'.")
            

        stroke_width = st.slider("Размер кисти: ", 1, 100, 3, width=600)

        canvas_result = st_canvas(
            stroke_color='white',
            stroke_width=stroke_width,
            width=SIZE_IMAGE_DRAW[0],
            height=SIZE_IMAGE_DRAW[1],
        )

        if st.button("Предсказать"):
            image = Image.frombytes('RGBA', SIZE_IMAGE_DRAW, canvas_result.image_data)
        
            data = {'image' : image.tobytes()}
            predict_digit(data)

    def information_page():
        st.html("<h2>Данный проект представляет собой предсказание цифры, по нарисованному пользователем изображением.<br/><h2/>")
        st.html("<p style='font-size: 18px'>Как использовать систему:<br/>- Наведитесь на холст и нарисуйте цифру;<br/> - После того как нарисуете цифру, необходимо нажать на кнопку 'Предсказать'.<br/><br/>Стек используемых технологий:<br/> - FastApi: API для предсказывания автомобиля машинным обучением;<br/> - Streamlit: сайт для удобной работы с машинным обучением.<p/>")

    st.set_page_config(
        page_title="Система для предсказания автомобиля(ВАЗ 2107, LADA GRANTA, LADA NIVA)",
        layout="wide"
    )

    st.title("Система для предсказания цифр")

    page = st.sidebar.radio("Выберите вкладку:",
                            ["Предсказания цифры", "Информация о проекте"])
    
    match(page):
        case "Предсказания цифры":
            page_rendering()

        case "Информация о проекте":
            information_page()

if __name__ == '__main__':
    site()