import json
import requests
import datetime
import time
import os

icon_url = "https://github.com/CallMeLaNN/cloudformation-templates/raw/master/codepipeline-slack/codepipeline-service-icon.png"

def build_payload(slack_channel, slack_username, region, pipeline, execution_id, state, deploy_time):
  global icon_url
  text = None
  color = None
  pipeline_url = "https://" + region + ".console.aws.amazon.com/codepipeline/home?region=" + region + "#/view/" + pipeline
  attachment_title = "<" + pipeline_url + "|Visit the CodePipeline here>"
  deploy_date_time = datetime.datetime.strptime(deploy_time, "%Y-%m-%dT%H:%M:%SZ")
  if (state == "STARTED"):
    text = "Start deploying *" + pipeline + "*"
  elif (state == "CANCELED"):
    text = "Deployment *" + pipeline + "* has been cancelled"
  elif (state == "RESUMED"):
    text = "Deployment *" + pipeline + "* has been resumed"
  elif (state == "SUPERSEDED"):
    text = "Deployment *" + pipeline + "* superseded by recent execution"
  elif (state == "SUCCEEDED"):
    text = "Successful deploy of *" + pipeline + "*"
    color = "good"
  elif (state == "FAILED"):
    text = "Something went wrong deploying *" + pipeline + "*"
    color = "danger"
  else:
    print("Unknown state:", state)
    return None

  return {
    "channel": slack_channel,
    "username": slack_username,
    "icon_url": icon_url,
    "mrkdwn": True,
    "text": text,
    "attachments": [
      {
        "title": attachment_title,
        "color": color,
        "footer": "Region: " + region + " | Execution ID: " + execution_id,
        "ts": time.mktime(deploy_date_time.timetuple())
      }
    ]
  }

def lambda_handler(event, context):
  print("Event:", event)

  if (event["source"] == "aws.codepipeline" and event["detail-type"] == "CodePipeline Pipeline Execution State Change"):
    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    slack_channel = os.environ.get("SLACK_CHANNEL")
    slack_username = os.environ.get("SLACK_USERNAME", default="AWS CodePipeline")

    # Get and validate data from the event
    region = event.get("region")
    detail = event.get("detail")
    deploy_time = event.get("time")
    if (detail == None):
      print("Missing detail property in the event.")
      return
    pipeline = detail.get("pipeline")
    execution_id = detail.get("execution-id")
    state = detail.get("state")
    if (state == None):
      print("Missing detail.state property in the event.")
      return

    slack_payload = build_payload(slack_channel, slack_username, region, pipeline, execution_id, state, deploy_time)
    if (slack_payload != None):
      slack_payload = json.dumps(slack_payload)
      print("Request payload:", slack_payload)

      resp = requests.post(slack_webhook_url, data=slack_payload, headers={'Content-Type': 'application/json'})
      print("Slack Response:", resp.status_code, resp.text)
  else:
    print("Unknown event received:", event)
