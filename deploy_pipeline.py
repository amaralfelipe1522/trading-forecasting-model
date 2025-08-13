#!/usr/bin/env python3
"""
Script para deploy e execução do pipeline SageMaker
"""
import boto3
import sagemaker
from sagemaker_pipeline import create_trading_pipeline

def deploy_and_run_pipeline():
    """Deploy e executa o pipeline de forecasting"""
    
    try:
        # Criar pipeline
        pipeline = create_trading_pipeline()
        
        # Deploy do pipeline
        print("Fazendo deploy do pipeline...")
        pipeline.upsert(role_arn=sagemaker.get_execution_role())
        print("Pipeline deployed com sucesso!")
        
        # Executar pipeline
        print("Iniciando execução do pipeline...")
        execution = pipeline.start()
        
        print(f"Pipeline execution ARN: {execution.arn}")
        print("Pipeline iniciado! Monitore no SageMaker Console.")
        
        return execution
        
    except Exception as e:
        print(f"Erro ao executar pipeline: {str(e)}")
        return None

if __name__ == "__main__":
    execution = deploy_and_run_pipeline()
    
    if execution:
        print(f"\nPara monitorar o pipeline:")
        print(f"aws sagemaker describe-pipeline-execution --pipeline-execution-arn {execution.arn}")
