# CodePipeline Slack

## Requirements

Follow the requirements in [SAM App Guide](SAM-APP-GUIDE.md)

1. Python 3.6
2. The python version activated if you use Python virtual environment
3. Docker installed

## Local development

### Debugging

1. Change directory to the subfolder. E.g. codepipeline-slack
2. Run `python file.py` or
3. Start Debug on the file. Make sure you provide the environment variable.

> *There is no easy way to use `sam local invoke` to debug Python*

### Running on Lambda Function locally

Run `sam local invoke "CodePipelineSlackFunction" -e events.json --env-vars env.json`

## Deployment

Run `sam validate template.yaml` to validate the template.

Lambda requires a flat folder to add dependencies into the function. Use `build` folder to isolate from source.
You have to package the template first to upload the soruce into S3. Create S3 bucket before running the command.

1. `pip install -r requirements.txt -t build/`
2. `cp *.py build/`
3. `sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket <S3-BUCKET>`
4. `sam deploy --template-file packaged.yaml --capabilities CAPABILITY_IAM --stack-name <STACK-NAME> --tags TAG-NAME=TAG-VALUE --parameter-overrides PARAM_NAME1=PARAM-VALUE1 PARAM_NAME2=PARAM-VALUE2`

## References

* [Serverless Application Model](https://github.com/awslabs/serverless-application-model)
* [Serverless Application Model Specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md)
* [sam cli](https://github.com/awslabs/aws-sam-cli)
* [SAM App Guide](SAM-APP-GUIDE.md)
