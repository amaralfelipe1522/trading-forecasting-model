# Carregar o modelo do material específico
import joblib
import pandas as pd

codigo = '10000'
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