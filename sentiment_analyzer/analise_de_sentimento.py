import pandas as pd
from pandas.core.frame import DataFrame
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
from io import StringIO

class AnaliseDeSentimento():

    def load_data(file, sep: str) -> DataFrame:
        """
        Função para carregar um arquivo CSV em um DataFrame.

        :param file: Arquivo CSV ou path do arquivo.
        :return: DataFrame com os dados do arquivo CSV.
        """
        print("*****************************************************************")
        print("Carregando dataset...")
        print("*****************************************************************\n")
        print(" ")

        df = pd.read_csv(StringIO(file))

        print(df.info(), file=sys.stderr)
        print(df.head(2), file=sys.stderr)

        print("*****************************************************************")
        print(f"Dataset {file} carregado com sucesso !\n")
        
        return df

    def get_sentiment(text):
        """
        Calcula a polaridade do sentimento do texto fornecido.

        :param text: Texto para analisar o sentimento.
        :return: Um valor float que representa a polaridade do sentimento.
                O valor estará no intervalo [-1.0, 1.0], onde -1.0 é extremamente negativo,
                1.0 é extremamente positivo e 0 é neutro.
        """
        
        # Inicializando o analisador de sentimento
        sia = SentimentIntensityAnalyzer()
        
        # Calculando a pontuação de sentimento
        sentiment = sia.polarity_scores(text)
        return sentiment['compound']


    def classify_sentiment(score : float) -> str:
        """
        Função para classificar o sentimento baseado em um score.
        
        :param score: Score de sentimento, com -1 representando um sentimento extremamente negativo,
                    0 um sentimento neutro e 1 um sentimento extremamente positivo.
        :return: Classificação do sentimento, que pode ser "Positivos", "Negativos" ou "Neutros".
        """
        if score > 0.05:
            return "Positivo"
        elif score < -0.05:
            return "Negativo"
        else:
            return "Neutro"