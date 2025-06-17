Anotações Gerais

🎯 Por que Random Forest nesse caso?
✅ Vantagens específicas para esse cenário:
Trabalha muito bem com dados tabulares mistos (numéricos + categóricos).
→ Nosso dataset tem variáveis como fornecedor (categórica) e preço unitário, quantidade (numéricas).
Pouco pré-processamento.
→ Não exige normalização ou padronização dos dados. Apenas tratamento básico das categóricas (OneHotEncoder ou LabelEncoder).
Lida bem com não linearidades.
→ A relação entre desconto, fornecedor, condições de pagamento, preço e quantidade provavelmente não é linear.
Robusto a outliers e dados ruidosos.
→ No mundo real, proposta de fornecedores tem variações, preços absurdos e comportamentos estranhos. Random Forest é resistente.
Funciona bem com datasets médios.
→ Para algumas centenas ou poucos milhares de registros por código de material, Random Forest entrega ótima performance.
Fácil interpretação relativa.
→ Permite extrair importância das variáveis, o que é útil para você entender quais fatores mais impactam no desconto.
Boa generalização sem muito risco de overfitting.
→ Ao contrário de Decision Trees isoladas, o ensemble (muitos modelos juntos) corrige esse problema.

💡 Se Random Forest não funcionar bem, próximo passo seria testar:
🔥 XGBoost ou LightGBM → mais rápidos, mais precisos em certos cenários.
🔥 CatBoost → muito bom para dados tabulares, com categóricas embutidas no próprio modelo (nem precisa de OneHotEncoder).
🔥 Regressão Linear/ElasticNet → se os dados mostrarem relação quase linear.
🔥 Árvores de Decisão Simples → se quiser algo extremamente interpretável, mas menos robusto.

source ~/miniconda3/bin/activate