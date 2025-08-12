import boto3
import sagemaker
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.parameters import ParameterString, ParameterInteger
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.functions import Join

def create_trading_pipeline():
    # Configuração inicial
    # role = "arn:aws:iam::871276459623:role/SageMakerExecutionRole"  # Substituir pelo seu ARN
    role = sagemaker.get_execution_role()
    session = sagemaker.Session()
    pipeline_session = PipelineSession()
    
    # Parâmetros do pipeline
    input_data_uri = ParameterString(
        name="InputDataUri",
        default_value="s3://sagemaker-my-dataset-study/historico_propostas.xlsx"
    )
    
    model_bucket = ParameterString(
        name="ModelBucket", 
        default_value="sagemaker-processed-models"
    )
    
    # Processador SKLearn para treinamento
    sklearn_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type="ml.t3.medium",
        instance_count=1,
        role=role,
        sagemaker_session=pipeline_session
    )
    
    # Step 1: Treinamento de modelos
    training_step = ProcessingStep(
        name="TrainingModels",
        processor=sklearn_processor,
        inputs=[
            ProcessingInput(
                source=input_data_uri,
                destination="/opt/ml/processing/input"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="models",
                source="/opt/ml/processing/output/models",
                destination=Join(on="", values=["s3://", model_bucket, "/models/"])
            ),
            ProcessingOutput(
                output_name="metrics",
                source="/opt/ml/processing/output/metrics",
                destination=Join(on="", values=["s3://", model_bucket, "/metrics/"])
            )
        ],
        code="scripts/sagemaker_train.py"
    )
    
    # Step 2: Inferência
    inference_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type="ml.t3.medium",
        instance_count=1,
        role=role,
        sagemaker_session=pipeline_session
    )
    
    inference_step = ProcessingStep(
        name="InferenceStep",
        processor=inference_processor,
        inputs=[
            ProcessingInput(
                source=training_step.properties.ProcessingOutputConfig.Outputs["models"].S3Output.S3Uri,
                destination="/opt/ml/processing/input/models"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="predictions",
                source="/opt/ml/processing/output/predictions",
                destination="s3://sagemaker-previsoes-preco-sugerido/previsoes/"
            )
        ],
        code="scripts/sagemaker_inference.py"
    )
    
    # Criar pipeline
    pipeline = Pipeline(
        name="TradingForecastingPipeline",
        parameters=[input_data_uri, model_bucket],
        steps=[training_step, inference_step],
        sagemaker_session=pipeline_session
    )
    
    return pipeline

if __name__ == "__main__":
    pipeline = create_trading_pipeline()
    pipeline.upsert(role_arn=sagemaker.get_execution_role())
    
    # Executar pipeline
    execution = pipeline.start()
    print(f"Pipeline execution started: {execution.arn}")
