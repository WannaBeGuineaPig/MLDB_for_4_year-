__all__ = [
    'PredictClassComment'
]

import re
import numpy as np

from pickle import load
from pymystem3 import Mystem
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing import sequence

MAX_LEN = 300
PATH_MODEL = './model/lstm_model.pkl'
PATH_TOKENIZER = './model/tokenizer.pkl'

class WordProcessing:
    def __init__(self):
        self.mystem = Mystem()
        self.sw = stopwords.words("russian")
    
    def lemmatization_text(self, text) -> str:
        """
        Лемматизация текста.
        
        :param text: входной текст
        :return: лемматизированный текст
        :rtype: str
        """
        lemmatization_text = ''.join(self.mystem.lemmatize(text))
        return lemmatization_text
    
    def preprocess_text(self, text) -> str:
        """
        Функция для предобработки комментария.
        
        :param text: введённый комментарий
        :return: обработанный комментарий
        :rtype: str
        """
        text = text.replace('ё', 'е')
        text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub(r'[^a-zA-Zа-яА-Я]+', ' ', text)
        text = re.sub(' +', ' ', text)
        text = text.lower()
        text = ' '.join([word for word in text.split() if word not in self.sw])
        text = ' '.join([re.sub('^[a-zA-Zа-яА-Я]{,2}$', '', word) for word in text.split()])
        text = self.lemmatization_text(text)
        return text.strip()
    
class PredictClassComment:
    def __init__(self):
        self.word_proccesing = WordProcessing()
        self.model = self.load_pickle(PATH_MODEL)
        self.tokenizer = self.load_pickle(PATH_TOKENIZER)
        self.type_comment = {
            0 : 'normal(положительный)',
            1 : 'insult(оскорбительный)',
            2 : 'threat(угрожающий)',
            3 : 'obscenity(непристойность)',
        }
        self.response_template_predict_comment = 'Тип тональности комментраия: {}.\n\nПроцент схожести к типу normal(положительный): {}.\nПроцент схожести к типу insult(оскорбительный): {}.\nПроцент схожести к типу threat(угрожающий): {}.\nПроцент схожести к типу obscenity(непристойный): {}.'
        
    def load_pickle(self, path: str):
        """
        Функция для чтения модели и токенайзера.
        
        :param path: путь к файлу
        :type path: str
        """
        with open(path, 'rb') as file:
            return load(file)

    def conversion_token_one_dimension(self, clean_text: str):
        """
        Функция для разбиения на токены и приведения к одной размерности.
        
        :param clean_text: преобработанный текст
        :type clean_text: str
        """
        token_text = self.tokenizer.texts_to_sequences([clean_text])
        text = sequence.pad_sequences(token_text, maxlen=MAX_LEN)
        return text

    def get_predict_tonality_comment(self, comment: str) -> str:
        """
        Функция для определения тональности введённого комментария.
        
        :param comment: текст комментария
        :type comment: str
        :return: Тип тональности комментария, а также проценты точности к каждому классу.
        :rtype: str
        """

        clean_comment = self.word_proccesing.preprocess_text(comment)
        token_text = self.conversion_token_one_dimension(clean_comment)
        predict = self.model.predict([token_text])[0]
        
        return self.response_template_predict_comment.format(self.type_comment[np.argmax(predict)], *[f"{i:.12f}" for i in predict])