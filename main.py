# Carregar o modelo do material específico
import joblib
import pandas as pd
import boto3
import os

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', 
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name='us-east-1')

# Definir parâmetros da previsão
codigo = '10000'
s3_filename = f'previsao_material_{codigo}.json'
bucket_name = 'previsoes-preco-sugerido'
s3_folder = 'previsoes/'
local_path = f'predicts/{s3_filename}'
s3_key = f'{s3_folder}{s3_filename}'

# Busca modelo do S3
file_key = f'modelo_material_{codigo}.joblib'
processed_bucket_name = 'processed-models'
s3.download_file(processed_bucket_name, file_key, f'./models/{file_key}')

# Carregar o modelo
modelo = joblib.load(f'models/modelo_material_{codigo}.joblib')

# Fazer uma previsão
amostra = {
    'Fornecedor': ['Alpha Ltda'],
    'Quantidade': [200],
    'PrazoEntrega(dias)': [10],
    'CondicoesPagamento': ['À vista'],
    'FreteIncluso': ['Não'],
    'ValidadeProposta(dias)': [30],
    'PrecoUnitario(R$)': [350.00]
}

df_amostra = pd.DataFrame(amostra)

previsao = modelo.predict(df_amostra)
print(f"Desconto sugerido: {previsao[0]:.2f}%")

# Adicionar previsão ao DataFrame
df_amostra['DescontoSugerido(%)'] = previsao

# Salvar CSV localmente
df_amostra.to_json(local_path, index=False)

s3.upload_file(local_path, bucket_name, s3_key)
print(f"Previsão salva em s3://{bucket_name}/{s3_key}")
os.remove(local_path)
os.remove(f'models/{file_key}')