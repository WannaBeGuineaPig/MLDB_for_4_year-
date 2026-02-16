__all__ = [
    'get_comments_from_bd'
]

from mysql.connector import connect, Error

def get_comments_from_bd() -> dict:
    """
    Функция для получения комментариев из базы данных.
    
    :return: словарь с комментариями
    :rtype: dict
    """
    show_comment_query = 'SELECT * FROM toxis_comments;'

    try:
        with connect(
            host='localhost',
            user='root',
            password='root',
            database="mldb"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(show_comment_query)
                result_fetch = cursor.fetchall()
                result_dict = {'comment': [], 'normal': [], 'insult': [], 'threat': [], 'obscenity': []}
                for row in result_fetch:
                    result_dict['comment'].append(row[1])
                    result_dict['normal'].append(row[2])
                    result_dict['insult'].append(row[3])
                    result_dict['threat'].append(row[4])
                    result_dict['obscenity'].append(row[5])
                
                return result_dict

    except Error as e:
        raise e