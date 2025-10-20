import requests, streamlit as st, pandas as pd, logging, time

API_BASE_URL = "http://127.0.0.1:8000/"

def request_api(path_to_api: str, data: str = None):
    trying = 5
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    logger = logging.getLogger(__name__)

    while trying > 0:
        try:
            url = f"{API_BASE_URL}{path_to_api}"

            if data:
                response = requests.get(f'{url}{data}')
            else:
                response = requests.get(url)

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
    def click_btn(path_to_api: str, data_api: str, collabarativ: bool = False):
        with st.spinner("Ожидайте ответ от API"):
            df_response = request_api(path_to_api, data_api)
            if collabarativ:
                df_user_rating_films = request_api('get_find_rating_films_user/', data_api)
                df_user_rating_genres = request_api('get_find_favorite_genres_user/', data_api)

        if collabarativ:
            st.write(pd.DataFrame(df_user_rating_films))
            st.write(pd.DataFrame(df_user_rating_genres))

        st.dataframe(df_response)


    def page_rendering(path_to_api: str, title_text: str, api_for_dropdown_list: str | None = None):
        st.header(title_text)
        if title_text == "Топ 10 фильмов":
            with st.spinner("Ожидайте ответ от API"):
                df_popularite_films = request_api(path_to_api)
                st.dataframe(df_popularite_films)
            return
        
        with st.spinner("Ожидайте ответ от API"):
            data_for_dropdown_list = request_api(api_for_dropdown_list)

        option =  st.selectbox("Выберете значение:", data_for_dropdown_list)
        st.button('Нажмите для получения списка фильмов', on_click=click_btn(path_to_api, option, collabarativ=True if title_text == 'Топ 10 фильмов по схожести интересов' else False))

    def information_page():
        st.header("Проект для рекомендации фильмов")
        st.text("Проект напрвален на рекомендации фильмов.\nДанные о фильмах(датасет) были взяты с онлайн кинотеатра 'MoveiLens'.\n\nИспользование сайта:\n1.Рекомендация топ 10 фильмов - шаги, как использовать: выбрать вкладку 'Топ 10 фильмов';\n2.Рекомендация топ 10 фильмов по жанрам - шаги, как использовать: выбрать вкладку 'Топ 10 фильмов по жанрам', выбрать жанр из выпадающего списка;\n3.Рекомендация топ 10 фильмов по названию - шаги, как использовать: выбрать вкладку 'Топ 10 фильмов по жанрам', выбрать название фильма из выпадающего списка;\n4.Рекомендация топ 10 фильмов по схожести интересов - шаги, как использовать: выбрать вкладку 'Топ 10 фильмов по схожести интересов', выбрать номер пользователя(id) из выпадающего списка;")

    st.set_page_config(
        page_title="Система для рекомендации фильмов",
        layout="wide"
    )

    st.title("Система для рекомендации фильмов")

    page = st.sidebar.radio("Выберите вкладку:",
                            ["Топ 10 фильмов", "Топ 10 фильмов по жанрам", "Топ 10 фильмов по названию", "Топ 10 фильмов по схожести интересов", "Информация о проекте"])
    
    match(page):
        case "Топ 10 фильмов":
            page_rendering("get_popularite_films", "Топ 10 фильмов")
        
        case "Топ 10 фильмов по жанрам":
            page_rendering("get_popularite_films_by_genre/", "Топ 10 фильмов по жанрам", 'get_genre_films/')
        
        case "Топ 10 фильмов по названию":
            page_rendering("get_same_films_by_name/", "Топ 10 фильмов по названию", 'get_name_films/')

        case "Топ 10 фильмов по схожести интересов":
            page_rendering("get_favorite_films/", "Топ 10 фильмов по схожести интересов", 'get_users_id/')

        case "Информация о проекте":
            information_page()

if __name__ == '__main__':
    site()