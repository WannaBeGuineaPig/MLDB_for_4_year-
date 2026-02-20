__all__ = [
    'get_comments_from_bd',
    'save_data_bd',
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
                result_dict = {'Комментарий': [], 'normal(положительный)': [], 'insult(оскорбительный)': [], 'threat(угрожающий)': [], 'obscenity(непристойность)': [], 'Предсказание модели': []}
                for row in result_fetch:
                    result_dict['Комментарий'].append(row[1])
                    result_dict['normal(положительный)'].append(row[2])
                    result_dict['insult(оскорбительный)'].append(row[3])
                    result_dict['threat(угрожающий)'].append(row[4])
                    result_dict['obscenity(непристойность)'].append(row[5])
                    result_dict['Предсказание модели'].append(row[6])
                
                return result_dict

    except Error as e:
        raise e
    
def save_data_bd(comment: str, true_type_comment: str, predict_model_type: str) -> None:
    """
    Сохранение новой записи в базу данных.
    
    :param comment: введённый комментарий
    :type comment: str
    :param true_type_comment: фактический тип комментария
    :type true_type_comment: str
    :param predict_model_type: предсказанный тип моделью
    :type predict_model_type: str
    """
    add_comment_query = f'''
    INSERT INTO mldb.toxis_comments(id_toxis_comments,comment,normal,insult,threat,obscenity,predict_model) 
    VALUES
    (0,'{comment}',{int(true_type_comment=="normal(положительный)")},{int(true_type_comment=="insult(оскорбительный)")},{int(true_type_comment=="threat(угрожающий)")},{int(true_type_comment=="obscenity(непристойность)")},'{predict_model_type}')
    '''

    try:
        with connect(
            host='localhost',
            user='root',
            password='root',
            database="mldb"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(add_comment_query)
                connection.commit()                
                
    except Error as e:
        raise e