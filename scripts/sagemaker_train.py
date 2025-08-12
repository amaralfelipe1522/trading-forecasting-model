import subprocess
import sys
import os

# Instalar dependências necessárias
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openpyxl'])

import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib

def main():
    # Caminhos SageMaker
    input_path = "/opt/ml/processing/input"
    output_path = "/opt/ml/processing/output"
    models_path = f"{output_path}/models"
    metrics_path = f"{output_path}/metrics"
    
    os.makedirs(models_path, exist_ok=True)
    os.makedirs(metrics_path, exist_ok=True)
    
    # Carregar dados
    data_file = None
    for file in os.listdir(input_path):
        if file.endswith('.xlsx'):
            data_file = file
            break
    
    if not data_file:
        raise FileNotFoundError("Arquivo Excel não encontrado")
    
    df = pd.read_excel(f"{input_path}/{data_file}", engine='openpyxl')
    codigos_materiais = df['CodigoMaterial'].unique()
    
    metrics_results = {}
    
    # Loop para criar um modelo por material
    for codigo in codigos_materiais:
        print(f"\nTreinando modelo para material {codigo}...")
        
        # Filtrar dados desse material
        df_material = df[df['CodigoMaterial'] == codigo]
        
        # Verificar se há dados suficientes
        if len(df_material) < 10:
            print(f"Poucos dados para {codigo}, pulando...")
            continue
        
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
            remainder='passthrough'
        )
        
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])
        
        # Split treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Treinar
        model.fit(X_train, y_train)
        
        # Avaliação
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"MAE para material {codigo}: {mae:.2f}%")
        
        # Salvar métricas
        metrics_results[str(codigo)] = {
            "mae": float(mae),
            "samples_count": len(df_material),
            "test_samples": len(X_test)
        }
        
        # Salvar o modelo
        model_filename = f'modelo_material_{codigo}.joblib'
        model_path = f"{models_path}/{model_filename}"
        joblib.dump(model, model_path)
        print(f"Modelo salvo: {model_path}")
    
    # Salvar métricas gerais
    with open(f"{metrics_path}/training_metrics.json", 'w') as f:
        json.dump(metrics_results, f, indent=2)
    
    print(f"Treinamento concluído. {len(metrics_results)} modelos criados.")

if __name__ == "__main__":
    main()
