from pandas.core.frame import DataFrame
from datetime import datetime
from flask import Flask, render_template, send_from_directory,jsonify,request,Response
from utils import PreparaDado
from sentiment_analyzer import AnaliseDeSentimento
import sys



app = Flask(__name__)
app.debug=True

@app.route('/sentiment_analyzer_csv/<string:text_column>/<string:sep>', methods=['POST'])
@app.route('/sentiment_analyzer_csv/<string:text_column>/<string:sep>/', methods=['POST'])
def run_pipeline(text_column: str, sep: str) -> DataFrame:
    """
    Executa o pipeline de pré-processamento e análise de sentimentos.

    :param text_column: Nome da coluna que contém o texto a ser preparado para a analise de sentimento.
    :param in_csv: Caminho para o arquivo CSV de entrada.
    :param sep: Caractere delimitador do arquivo CSV de entrada.
    :return: DataFrame com as novas colunas de sentimento.
    """

    print(request.data.decode('utf-8'), file=sys.stderr)
    in_csv = request.data.decode('utf-8')

    # Carregar o dataset
    df = AnaliseDeSentimento.load_data(in_csv, sep)

    # Informacoes do dataset
    df.info()

    prep_dado = PreparaDado()
    df = prep_dado.pre_processing(df=df,text_column=text_column)
    
    #aplica VADER para analise de sentimento
    df["sentiment"] = df['cleared_text'].apply(AnaliseDeSentimento.get_sentiment)

    # Classificando o sentimento em positivo, negativo ou neutro
    df["sentiment_class"] = df["sentiment"].apply(AnaliseDeSentimento.classify_sentiment)

    # Salva o dataframe em um arquivo CSV
    csv_data = df.to_csv(index=False)

    response = Response(csv_data,content_type='text/csv')

    # Retorna o dataframe com as novas colunas de sentimento
    return response

@app.route('/sentiment_analyzer_text', methods=['POST'])
def run_pipeline_text() -> str:
    """
    Realiza a análise de sentimentos de um texto fornecido pelo usuario.

    :param text_column: 
    """
    texto_para_analise = request.data.decode('utf-8')
    
    prep_dado = PreparaDado()
    texto_limpo = prep_dado.data_prep(texto_para_analise)

    valor_sentimento = AnaliseDeSentimento.get_sentiment(texto_limpo)

    sentimento_classificado = AnaliseDeSentimento.classify_sentiment(valor_sentimento)

    retorno = jsonify({'Texto Original':texto_para_analise,
                       'Texto apos o tratamento':texto_limpo,
                       'Classificacao do Sentimento':sentimento_classificado
                       })
    return retorno, 200

#Iniciar o aplicativo se este arquivo for executado diretamente
if __name__ == '__main__':
    app.run()