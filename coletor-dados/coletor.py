import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import psycopg2
from psycopg2 import sql

# Lista das 5 ações brasileiras que você deseja monitorar
ACOES = ['VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA']

def coletar_dados_enriquecidos():
    # Lista das 5 ações brasileiras que você deseja monitorar
    ACOES = ['VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA']

    #def coletar_dados_enriquecidos():
    """
    Coleta o histórico e calcula features técnicas para um modelo de ML.
    """
    periodo_dias = '90d'
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    print(f"[{data_hoje}] - Iniciando a coleta de dados de {periodo_dias} para as ações: {ACOES}")


    # Baixa os dados de todos os tickers com 'group_by=True' (padrão)
    df_final = []
    for acao in ACOES:
        df_temp = yf.download(tickers=acao, period=periodo_dias)
        tt1 = df_temp.reset_index(drop=False)
        tt1.columns = ['data','close','high','low','open','volume']
        tt1["ticket"] = acao
        df_final.append(tt1)

    df = pd.concat(df_final)
    print('Dataframe baixado')
    ### Processando


    ultima_linhas = []
    for acao in df["ticket"].unique():
        try:
            ticker_limpo = acao
            df_acao = df[df["ticket"] == acao]
            df_acao = df_acao.dropna()

            # Adiciona a coluna 'ticker' ao DataFrame da ação
            df_acao['ticker'] = ticker_limpo

            # --- Cálculo das Features Técnicas com pandas_ta ---
            df_acao['SMA_3d'] = ta.sma(df_acao['close'], length=3)
            df_acao['SMA_7d'] = ta.sma(df_acao['close'], length=7)
            df_acao['SMA_14d'] = ta.sma(df_acao['close'], length=14)

            df_acao['EMA_3d'] = ta.ema(df_acao['close'], length=3)
            df_acao['EMA_7d'] = ta.ema(df_acao['close'], length=7)
            df_acao['EMA_14d'] = ta.ema(df_acao['close'], length=14)

            df_acao['RSI_14d'] = ta.rsi(df_acao['close'], length=14)

            # Adiciona colunas diretamente ao DataFrame df_acao
            df_acao.ta.bbands(append=True)
            df_acao.ta.macd(append=True)

            # ['BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0']
            ['data', 'close', 'high', 'low', 'open', 'volume', 'ticket', 'ticker',
                'SMA_3d', 'SMA_7d', 'SMA_14d', 'EMA_3d', 'EMA_7d', 'EMA_14d', 'RSI_14d',
                'BBL_5_2.0_2.0', 'BBM_5_2.0_2.0', 'BBU_5_2.0_2.0', 'BBB_5_2.0_2.0',
                'BBP_5_2.0_2.0', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']
            df_acao = df_acao.rename(columns={'BBL_5_2.0_2.0':'BBL_20','BBM_5_2.0_2.0':'BBM_20','BBU_5_2.0_2.0':'BBU_20'})
            # Renomeia as colunas de volume e fechamento

            # Seleciona a última linha de dados (mais recente)
            ultima_linha = df_acao.iloc[-1].to_frame().T

            colunas_modelo = [
                'data','ticker', 'close', 'volume', 'SMA_3d', 'SMA_7d', 'SMA_14d',
                'EMA_3d', 'EMA_7d', 'EMA_14d', 'RSI_14d', 'BBL_20',
                'BBM_20', 'BBU_20', 'MACD_12_26_9', 'MACDh_12_26_9',
                'MACDs_12_26_9'
            ]

            ultima_linha = ultima_linha[colunas_modelo]
            
            ultima_linhas.append(ultima_linha.values[0])
            print(f'Sucesso no ticket: {acao}')
        except:
            print(f'Erro no ticket: {acao}')
    print('\n')
    colunas = ultima_linha.columns
    df_final = pd.DataFrame(ultima_linhas, columns=colunas)
    print(df_final)

    return df_final

def salvar_no_banco(df, conn_params):
    """
    Salva o DataFrame no banco de dados usando ON CONFLICT.
    """
    conn = None
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Prepara a query SQL com ON CONFLICT
        # O nome da tabela será 'acoes'
        table_name = "acoes"
        
        # Cria a tabela se ela não existir
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            data DATE,
            ticker VARCHAR(10),
            close FLOAT,
            volume BIGINT,
            "SMA_3d" FLOAT,
            "SMA_7d" FLOAT,
            "SMA_14d" FLOAT,
            "EMA_3d" FLOAT,
            "EMA_7d" FLOAT,
            "EMA_14d" FLOAT,
            "RSI_14d" FLOAT,
            "BBL_20_2.0" FLOAT,
            "BBM_20_2.0" FLOAT,
            "BBU_20_2.0" FLOAT,
            "MACD_12_26_9" FLOAT,
            "MACDh_12_26_9" FLOAT,
            "MACDs_12_26_9" FLOAT,
            PRIMARY KEY (data, ticker)
        );
        """
        cursor.execute(create_table_query)

        # Insere ou atualiza os dados
        for index, row in df.iterrows():
            insert_query = """
            INSERT INTO acoes (data, ticker, close, volume, "SMA_3d", "SMA_7d", "SMA_14d", "EMA_3d", "EMA_7d", "EMA_14d", "RSI_14d", "BBL_20_2.0", "BBM_20_2.0", "BBU_20_2.0", "MACD_12_26_9", "MACDh_12_26_9", "MACDs_12_26_9")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (data, ticker) DO UPDATE SET
                close = EXCLUDED.close,
                volume = EXCLUDED.volume,
                "SMA_3d" = EXCLUDED."SMA_3d",
                "SMA_7d" = EXCLUDED."SMA_7d",
                "SMA_14d" = EXCLUDED."SMA_14d",
                "EMA_3d" = EXCLUDED."EMA_3d",
                "EMA_7d" = EXCLUDED."EMA_7d",
                "EMA_14d" = EXCLUDED."EMA_14d",
                "RSI_14d" = EXCLUDED."RSI_14d",
                "BBL_20_2.0" = EXCLUDED."BBL_20_2.0",
                "BBM_20_2.0" = EXCLUDED."BBM_20_2.0",
                "BBU_20_2.0" = EXCLUDED."BBU_20_2.0",
                "MACD_12_26_9" = EXCLUDED."MACD_12_26_9",
                "MACDh_12_26_9" = EXCLUDED."MACDh_12_26_9",
                "MACDs_12_26_9" = EXCLUDED."MACDs_12_26_9";
            """
            cursor.execute(insert_query, tuple(row))
        
        conn.commit()
        print("Dados salvos no banco de dados com sucesso!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao salvar no banco de dados: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    df_dados = coletar_dados_enriquecidos()
    if df_dados is not None:
        db_params = {
            "dbname": "b3_data",
            "user": "admin",
            "password": "password",
            "host": "database",
            "port": "5432"
        }
        salvar_no_banco(df_dados, db_params)