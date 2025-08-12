import pandas as pd
import joblib
import os
import json
from datetime import datetime

def main():
    # Caminhos SageMaker
    models_path = "/opt/ml/processing/input/models"
    output_path = "/opt/ml/processing/output/predictions"
    
    os.makedirs(output_path, exist_ok=True)
    
    # Exemplo de dados para inferência (pode ser parametrizado)
    codigo_material = '10000'  # Pode vir de parâmetro do pipeline
    
    # Buscar modelo específico
    model_filename = f'modelo_material_{codigo_material}.joblib'
    model_path = f"{models_path}/{model_filename}"
    
    if not os.path.exists(model_path):
        available_models = [f for f in os.listdir(models_path) if f.endswith('.joblib')]
        print(f"Modelo {model_filename} não encontrado.")
        print(f"Modelos disponíveis: {available_models}")
        
        if available_models:
            # Usar primeiro modelo disponível
            model_path = f"{models_path}/{available_models[0]}"
            codigo_material = available_models[0].replace('modelo_material_', '').replace('.joblib', '')
            print(f"Usando modelo: {available_models[0]}")
        else:
            raise FileNotFoundError("Nenhum modelo encontrado")
    
    # Carregar modelo
    modelo = joblib.load(model_path)
    
    # Dados de exemplo para inferência
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
    
    # Fazer previsão
    previsao = modelo.predict(df_amostra)
    desconto_sugerido = float(previsao[0])
    
    print(f"Desconto sugerido para material {codigo_material}: {desconto_sugerido:.2f}%")
    
    # Preparar resultado
    resultado = {
        'codigo_material': codigo_material,
        'dados_input': amostra,
        'desconto_sugerido_pct': desconto_sugerido,
        'timestamp': datetime.now().isoformat(),
        'modelo_usado': model_filename
    }
    
    # Salvar resultado
    output_filename = f"previsao_material_{codigo_material}.json"
    output_file_path = f"{output_path}/{output_filename}"
    
    with open(output_file_path, 'w') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"Previsão salva: {output_file_path}")
    
    # Salvar também um resumo de todas as previsões
    summary_path = f"{output_path}/predictions_summary.json"
    summary = {
        'total_predictions': 1,
        'predictions': [resultado]
    }
    
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
