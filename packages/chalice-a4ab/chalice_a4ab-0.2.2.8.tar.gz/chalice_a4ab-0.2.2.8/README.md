# Chalice-A4AB

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Chalice-A4AB)

[![tests](https://github.com/ShotaOki/ChaliceA4AB/actions/workflows/test.yml/badge.svg)](https://github.com/ShotaOki/ChaliceA4AB/actions/workflows/test.yml)
![PyPI - Version](https://img.shields.io/pypi/v/chalice-a4ab)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chalice-a4ab)
![GitHub License](https://img.shields.io/github/license/ShotaOki/ChaliceA4AB)

## What is this?

Chalice plugin: Support `Agents for Amazon Bedrock`

## URL Links

**PYPI :: Chalice-a4ab**  
https://pypi.org/project/chalice-a4ab/

**Github :: Chalice-a4ab**  
https://github.com/ShotaOki/ChaliceA4AB

## Usage

1. Install

   ```
   pip install -U chalice chalice-a4ab pydantic
   ```

1. Replace `from chalice import Chalice` to `from chalice_a4ab import Chalice`.

   Before:

   ```python
   from chalice import Chalice

   app = Chalice("app-name")

   @app.router("path-name")
   ...
   ```

   After:

   ```python
   from chalice_a4ab import Chalice

   app = Chalice("app-name")

   @app.router("path-name")
   ...
   ```

1. **(Optional)** Add Parser Lambda Function

   Add these decorator, function becomes "parser lambda"

   ```python
   from chalice_a4ab import (
       Chalice,
       AgentsForAmazonBedrockConfig,
       ParserLambdaAbortException,
       ParserLambdaResponseModel,
   )

   # Set Config for Agents for Amazon bedrock
   AgentsForAmazonBedrockConfig().apply()

   ...

   # PRE_PROCESSING
   @app.parser_lambda_pre_processing()
   def pre_processing(event, default_result: ParserLambdaResponseModel) -> ParserLambdaResponseModel:
       # [MEMO] is_valid_input :: Allow/Deny API invocation
       # default_result.pre_processing_parsed_response.is_valid_input = True
       return default_result


   # ORCHESTRATION
   @app.parser_lambda_orchestration()
   def orchestration(event: dict, default_result: ParserLambdaResponseModel) -> ParserLambdaResponseModel:
       # [MEMO] Throw this Exception, Overwrite LLM response
       # raise ParserLambdaAbortException(message="Overwrited")
       return default_result
   ```

1. Application works ::

   | What you can do                        | Status |
   | -------------------------------------- | ------ |
   | Execute from Agents for Amazon Bedrock | 〇     |
   | Auto generate OpenAPI schema           | ×      |
   | Management on cli                      | ×      |

## Advanced Usage

Create OpenAPI Schema automatically.

1. Install Chalice-a4ab and Chalice-spec

   ```python
   pip install -U chalice chalice-spec==0.7.0 chalice-a4ab boto3 pydantic
   ```

1. Add Setting

   ```python
   from chalice_a4ab import Chalice, AgentsForAmazonBedrockConfig
   from chalice_spec.docs import Docs, Operation

   # Set Config for Agents for Amazon bedrock
   AgentsForAmazonBedrockConfig(
       instructions="Situation Settings for talking with Human and agent.(more than 40 words)",
       description="Description of application",
   ).apply()

   app = Chalice(app_name="app-name")

   @app.router("path-name",
       methods=["POST"],
       docs=Docs(
           post=Operation(
               request=PyDanticRequestModelClass,
               response=PyDanticOutputModelClass,
           )
       ))
   def post_method():
   ...
   ```

   documentation for `@app.router` sample: https://github.com/TestBoxLab/chalice-spec

1. Management CLI

   **Init command** :: Create AWS Resource and OpenAPI Schema.

   ```bash
   chalice-a4ab init --profile ${PROFILE_NAME} --region ${REGION_NAME}
   ```

   **Sync command** :: Update Already AWS Resource and OpenAPISchema.

   ```bash
   chalice-a4ab sync --profile ${PROFILE_NAME} --region ${REGION_NAME}
   ```

   **Show command** :: Show OpenAPI Schema.

   ```bash
   chalice-a4ab show --profile ${PROFILE_NAME} --region ${REGION_NAME}
   ```

   **Info command** :: Show about Agents for Amazon Bedrock.

   ```bash
   chalice-a4ab info --profile ${PROFILE_NAME} --region ${REGION_NAME}
   ```

   **Invoke command** :: Invoke Agents for Amazon Bedrock.

   ```bash
   chalice-a4ab invoke "Natural Language Query" \
   --agent-id ${AGENT_ID} \
   --agent-alias-id ${AGENT_ALIAS_ID} \
   --end-session \
   --profile ${PROFILE_NAME} --region ${REGION_NAME}
   ```

   **Delete AWS Resource**

   ```bash
   chalice-a4ab delete --profile ${PROFILE_NAME} --region ${REGION_NAME}
   ```

1. Application works ::

   | What you can do                        | Status |
   | -------------------------------------- | ------ |
   | Execute from Agents for Amazon Bedrock | 〇     |
   | Auto generate OpenAPI schema           | 〇     |
   | Management on cli                      | 〇     |

# Develop

1. Setup

   ```bash
   poetry install
   ```

1. Run test

   ```bash
   poetry run pytest
   ```

# Lisence

MIT

# API

## Command Line TOOL

| Command             | Descritpion                                       |
| :------------------ | :------------------------------------------------ |
| chalice-a4ab init   | Create AWS resource for Agents for amazon bedrock |
| chalice-a4ab sync   | Sync OpenAPI schema to AWS                        |
| chalice-a4ab delete | Delete AWS resource for Agents for amazon bedrock |

| Options   | Description                                 |
| :-------- | :------------------------------------------ |
| --bucket  | Set S3 bucket name (for put OpenAPI schema) |
| --profile | Set AWS Profile Name                        |
| --region  | Set AWS Region Name                         |
| --help    | Show Help                                   |

## API

**AgentsForAmazonBedrockConfig**

| Method                         | Type   | Description                              |
| :----------------------------- | :----- | :--------------------------------------- |
| apply                          | -      | Current instace becomes global variable. |
| agents_for_bedrock_schema_json | -      | Get OpenAPI Schema                       |
| save_schema_to_local           | -      | Save OpenAPI Schema to local folder      |
| save_schema_to_s3              | -      | Upload OpenAPI Schema to S3 bucket       |
| save_config_to_local           | -      | Save Config setting to local folder      |
| get_global_config              | static | Get global variable.                     |
