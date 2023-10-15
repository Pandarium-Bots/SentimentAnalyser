import re
import sys
import nltk
import numpy as np
from langdetect import detect
from urllib.parse import urlparse
from nltk.corpus import stopwords
from pandas.core.frame import DataFrame
from nltk.stem import WordNetLemmatizer
from argostranslate import package, translate


class PreparaDado():

    def __init__(self):
        pass

    def data_prep(self,text: str) -> str:
        """
        Função que realiza a preparacao do dado da coluna de texto para a analise de sentimento.    
        :param text: Texto a ser pré-processado.
        :return: Texto pré-processado.
        """
        # detecta o idioma do texto e faz o translate para Ingles 
        lang = detect(text)

        print("****LANGUAGEEEEEEEEEEEE: "+lang,file=sys.stderr)

        translated_text = self.translate_to_english(text, lang)

        print("****TRADUZIDOOOOOOOOOO: "+translated_text,file=sys.stderr)

        # Removendo brackets 
        text = re.sub(r'[][)(]',' ', text)

        # Removendo links
        text = ' '.join([word for word in text.split() if not urlparse(word).scheme])

        # Remove tags
        text = re.sub(r"\@\w+", "", text)

        # Remove marcacoes/marcadores html
        text = re.sub(re.compile('<.*?>'), '', text)
        
        # Remove tudo que não for letra e número
        text = re.sub('[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]+', ' ', text)
        
        # Remove letras soltas nas frases
        text = re.sub(r'\b\w\b', '', text)
        
        # Transforma tudo em letra minúscula
        text = text.lower()

        # Tokenização - divide o texto em palavras separadas.
        tokens = nltk.word_tokenize(text)

        # Remove stopwords
        stop_words = stopwords.words('english')
        tokens = [word for word in tokens if word not in stop_words]

        # Lematização
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        
        return ' '.join(tokens)


    def pre_processing(self, df: DataFrame, text_column: str) -> DataFrame:
        """
        Função para realizar pré-processamento do dataset removendo registros vazios e duplicados.


        :param df: DataFrame com os dados a serem preparados.
        :param text_column: Nome da coluna contendo o texto.
        :return: DataFrame com os dados preparados.
        """
        
        # Substitui strings vazias por NaN
        df[text_column] = df[text_column].replace('', np.nan)
        # Textos Vazios/nulos
        print('Textos nulos: ', df[text_column].isnull().sum())
        
        # Remove registros com coluna de texto vazias
        df = df.dropna(subset=[text_column])
        
        # Registros duplicados
        print('Registros duplicados: ', df.duplicated(keep=False).sum())
        
        # Remove registros duplicados
        df = df.drop_duplicates().reset_index(drop=True)
        print('Formato do dataset após remoção:', df.shape)
        
        # Aplica a função de pré-processamento a todo o DataFrame
        df['cleared_text'] = df[text_column].apply(self.data_prep)
        
        # Retorna df limpo e tratado para melhor analise
        return df


    def translate_to_english(self, text, source_lang_code):
        installed_languages = translate.load_installed_languages()
        source_language = None
        
        print(installed_languages, file=sys.stderr)

        for lang in installed_languages:
            if lang.code == source_lang_code:
                source_language = lang
                print("source_language : "+lang, file=sys.stderr)
                break

        if source_language is None:
            return text  # Se o idioma fonte não é suportado, retorne o texto original

        # Obtenha o modelo de tradução para inglês
        translation = source_language.get_translation(translate.Language('en'))

        if translation is not None:
            return translation.translate(text)
        else:
            return text