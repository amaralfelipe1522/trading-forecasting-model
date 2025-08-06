import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib  # Para salvar modelos
import boto3
import os

# df = pd.read_excel('./data/historico_propostas.xlsx')
bucket_name = 'my-dataset-study'
file_key = 'historico_propostas.xlsx'

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3', 
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name='us-east-1')


s3.download_file(bucket_name, file_key, 'historico_propostas.xlsx')
df = pd.read_excel('historico_propostas.xlsx')

codigos_materiais = df['CodigoMaterial'].unique()

# Loop para criar um modelo por material
for codigo in codigos_materiais:
    print(f"\nTreinando modelo para material {codigo}...")

    # Filtrar dados desse material
    df_material = df[df['CodigoMaterial'] == codigo]

    # Definir X e y
    X = df_material[['Fornecedor', 'Quantidade', 'PrazoEntrega(dias)',
                     'CondicoesPagamento', 'FreteIncluso', 'ValidadeProposta(dias)', 'PrecoUnitario(R$)']]
    y = df_material['DescontoAplicavel(%)']

    # Definir features categóricas
    cat_features = ['Fornecedor', 'CondicoesPagamento', 'FreteIncluso']

    # Pipeline de pré-processamento e modelo
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
        ],
        remainder='passthrough'  # mantém variáveis numéricas
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Split treino/teste
    if len(df_material) < 10:
        print(f"Poucos dados para {codigo}, pulando...")
        continue

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Treinar
    model.fit(X_train, y_train)

    # Avaliação
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE para material {codigo}: {mae:.2f}%")

    # Salvar o modelo
    filename = f'models/modelo_material_{codigo}.joblib'
    joblib.dump(model, filename)
    print(f"Modelo salvo como {filename}")

