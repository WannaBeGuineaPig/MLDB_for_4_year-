import time
import json
import logging
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = 'http://127.0.0.1:8000' 

class Site:
    def request_api(self, path_to_api: str, method='GET', data: dict = None):
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        logger = logging.getLogger(__name__)
        trying_request_api = 3

        while trying_request_api > 0:
            try:
                url = f"{API_BASE_URL}{path_to_api}"

                if method == 'GET':
                    response = requests.get(url)
                
                else:
                    response = requests.post(url, data=data)

                return response.json()

            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка при обращении к API\n{str(e)}")

            except requests.exceptions.ConnectionError as e:
                logger.error(f"Ошибка подключения к API\n{str(e)}")
            
            except Exception as e:
                logger.error(f"Неожиданная ошибка\n{str(e)}")

            time.sleep(5)
            trying_request_api -= 1

    def start_page(self):
        st.set_page_config(
            page_title="Система для оценки тотальности комментария",
            layout="wide"
        )

        st.title("Система для оценки тотальности комментария")

        page = st.sidebar.radio("Выберите вкладку:",
                                ["Просмотр комментариев из базы данных", "Определение тональности комментария", "Информация о проекте"])
        
        match(page):
            case "Просмотр комментариев из базы данных":
                self.comments_from_bd_page()

            case "Определение тональности комментария":
                self.predict_comment_page()

            case "Информация о проекте":
                self.information_page()

    def comments_from_bd_page(self):
        st.header('Получение комментариев из базы данных')
        with st.spinner("Ожидайте ответ от API"):
            df_response = self.request_api('/comment')
            st.write(pd.DataFrame(df_response))

    def predict_comment_page(self):
        st.header('Определение тональности комментария')
        comment = st.text_input(label='Введите комментарий:', max_chars=1000, placeholder='Ваш комментарий')

        if st.button(label='Определить тональность'):
            data_request = {
                'comment' : comment
            }
            with st.spinner("Ожидайте ответ от API"):
                response = self.request_api('/predict-tonality-comment', 'POST', json.dumps(data_request))
                st.text(response)

    def information_page(self):
        st.html("<h2>Проект напрвален на предсказывания тональности комментария.<br>Данные о комментариях(датасет) были взяты с подготовленного файла.</h2><br><p style='font-size: 24px;'>Использование сайта:</p><ol><li style='font-size: 18px;'>Перейдите во вкладку 'Определение тональности комментария';</li><li style='font-size: 18px;'>Введите комментарий в поле 'Введите комментарий';</li><li style='font-size: 18px;'>Нажмите на кнопку 'Определить тональность';</li><li style='font-size: 18px;'>Подождите немного и система выведет предсказание.</li></ol><br><p style='font-size: 24px;'>Стэк технологий сайта:</p><ol><li style='font-size: 18px;'>Frontend(сайт): streamlit;</li><li style='font-size: 18px;'>Backend(API): FastApi;</li><li style='font-size: 18px;'>База данных: MySql.</li></ol>")
    
if __name__ == '__main__':
    Site().start_page()