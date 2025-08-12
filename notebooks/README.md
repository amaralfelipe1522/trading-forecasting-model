# 📚 Trading Forecasting - Notebooks

Esta pasta contém os notebooks Jupyter que implementam todo o pipeline de Machine Learning para previsão de descontos em propostas comerciais.

## 🗂️ Estrutura dos Notebooks

### 1. 📊 **01_data_exploration.ipynb**
**Análise Exploratória de Dados (EDA)**
- Carregamento e validação dos dados
- Estatísticas descritivas e visualizações
- Análise de correlações e padrões
- Identificação de insights para modelagem
- Preparação dos dados para treinamento

**🎯 Execute primeiro** para entender seus dados e identificar padrões importantes.

### 2. 🤖 **02_model_training.ipynb**
**Treinamento dos Modelos**
- Criação de pipelines de preprocessamento
- Treinamento de modelos Random Forest por material
- Validação cruzada e avaliação de performance
- Análise de importância das features
- Salvamento dos modelos treinados

**📋 Dependências:** Execute após 01_data_exploration.ipynb

### 3. 🔮 **03_model_inference.ipynb**
**Inferência e Previsões**
- Carregamento dos modelos treinados
- Funções de previsão com intervalos de confiança
- Análise de sensibilidade dos parâmetros
- Simulação de cenários de negociação
- Comparação entre fornecedores
- Geração de relatórios detalhados

**📋 Dependências:** Execute após 02_model_training.ipynb

### 4. ☁️ **04_sagemaker_deployment.ipynb**
**Deploy no Amazon SageMaker**
- Upload de dados e scripts para S3
- Criação de pipeline SageMaker
- Deploy e execução na nuvem
- Monitoramento de execuções
- Download de resultados

**📋 Dependências:** Requer credenciais AWS configuradas

## 🚀 Como Usar

### Instalação das Dependências
```bash
# Instalar dependências
pip install -r ../requirements.txt

# Adicionar dependências para notebooks
pip install jupyter ipywidgets
```

### Execução Sequencial
1. **Análise de Dados:** `01_data_exploration.ipynb`
2. **Treinamento:** `02_model_training.ipynb`  
3. **Inferência:** `03_model_inference.ipynb`
4. **Deploy (opcional):** `04_sagemaker_deployment.ipynb`

### Iniciar Jupyter
```bash
# Navegar para a pasta do projeto
cd /path/to/trading-forecasting-model

# Iniciar Jupyter
jupyter notebook notebooks/
```

## 📁 Estrutura de Arquivos Gerados

```
trading-forecasting-model/
├── data/
│   ├── dados_preparados.csv          # Dados processados (01)
│   └── eda_summary.json              # Resumo da análise (01)
├── models/
│   ├── modelo_material_*.joblib      # Modelos treinados (02)
│   ├── metrics/training_metrics.json # Métricas de treino (02)
│   └── training_session.json        # Info da sessão (02)
├── predicts/
│   ├── previsao_*.json              # Previsões individuais (03)
│   └── sessao_inferencia_*.json     # Resumo da sessão (03)
└── results/ (opcional)
    ├── models/                      # Modelos do SageMaker (04)
    ├── metrics/                     # Métricas do SageMaker (04)
    └── predictions/                 # Previsões do SageMaker (04)
```

## 🔧 Funcionalidades Principais

### 📊 Análise de Dados
- **Visualizações automáticas** de distribuições e correlações
- **Detecção de outliers** e inconsistências
- **Análise por material e fornecedor**
- **Insights automatizados** para modelagem

### 🤖 Modelagem
- **Modelos específicos por material** para maior precisão
- **Pipeline automatizado** de preprocessamento
- **Validação cruzada** para avaliar generalização
- **Análise de importância** das features

### 🔮 Previsões
- **Intervalos de confiança** para quantificar incerteza
- **Análise de sensibilidade** para entender impactos
- **Simulação de cenários** para apoio à decisão
- **Relatórios automáticos** com insights de negócio

### ☁️ Deploy na Nuvem
- **Pipeline SageMaker** totalmente automatizado
- **Escalabilidade** para grandes volumes de dados
- **Monitoramento** e logs detalhados
- **Integração** com serviços AWS

## 💡 Dicas de Uso

### Para Iniciantes
1. Comece com dados de exemplo (incluídos nos notebooks)
2. Execute célula por célula para entender cada etapa
3. Leia os comentários e documentação inline
4. Experimente modificar parâmetros para ver os efeitos

### Para Usuários Avançados
1. Customize os hiperparâmetros dos modelos
2. Adicione novas features ou transformações
3. Implemente novos algoritmos de ML
4. Integre com suas ferramentas de BI existentes

### Para Produção
1. Use o notebook 04 para deploy na AWS
2. Configure monitoramento automático
3. Implemente retreinamento periódico
4. Configure alertas para degradação do modelo

## 🐛 Solução de Problemas

### Erros Comuns
- **Módulos não encontrados:** Instale dependências com `pip install -r requirements.txt`
- **Arquivo não encontrado:** Verifique se executou os notebooks na ordem correta
- **Erro AWS:** Configure credenciais com `aws configure`
- **Memória insuficiente:** Reduza tamanho dos dados ou use instâncias maiores

### Logs e Debug
- Cada notebook gera logs detalhados
- Arquivos de sessão salvam o progresso
- Use `print()` statements para debug adicional

## 📞 Suporte

Para questões específicas:
1. Verifique os logs nos arquivos JSON gerados
2. Consulte a documentação do scikit-learn e SageMaker
3. Revise os comentários inline nos notebooks

## 🔄 Atualizações

Os notebooks são atualizados para:
- Corrigir bugs identificados
- Adicionar novas funcionalidades
- Melhorar performance e usabilidade
- Manter compatibilidade com novas versões das bibliotecas

---

**🎯 Objetivo:** Transformar dados históricos de propostas em insights acionáveis para otimização de negociações comerciais.
