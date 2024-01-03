import json
import os
import typer
from rich import print
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from typing_extensions import Annotated
from autogen.retrieve_utils import TEXT_FORMATS
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb
from typing import Optional

client = chromadb.Client()
app = typer.Typer()


@app.callback()
def callback():
    print("[green]K-GPT Command Running[/green]")


@app.command(name='local')
def local_cluster(
        cmd: Annotated[
            str, typer.Argument(help="Enter \"start\" or \"stop\" for turn on/off of minikube local cluster")]):
    """
    Start a minikube cluster locally or stop minikube cluster locally
    """
    if cmd == 'start':
        os.system('minikube start')
    elif cmd == 'stop':
        os.system('minikube stop')


@app.command(name='chat')
def chat(prompt: Annotated[str, typer.Argument(help="Enter a prompt like \"Show all deployments and services\" or "
                                                    "\"Read this yaml file, and found out what's wrong wit the "
                                                    "configuration.\"")],
         doc: Annotated[list[str], typer.Option(help="Enter url or file path, you can enter multiple --doc options,"
                                                     "Accepted file formats:\"['xml', 'htm',"
                                                     "'msg', 'docx',"
                                                     "'org', 'pptx', 'jsonl',"
                                                     "'txt', 'tsv', 'yml', 'json', 'md', 'pdf', 'xlsx', 'csv', "
                                                     "'html', 'log',"
                                                     "'yaml', 'doc', 'odt', 'rtf', 'ppt', 'epub', 'rst']\"")] = []):
    """
    Start chat with the k8s agent, let agent do things for you, you can chat with doc using --doc /path/to/doc/folder
    or --doc doc_url or both using --doc /path/to/docs/folder --doc doc_url
    """
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    termination_notice = (
        '\n\nDo not show appreciation in your responses, say only what is necessary. '
        'if "Thank you" or "You\'re welcome" are said in the conversation, then say TERMINATE '
        'to indicate the conversation is finished and this is your last message.'
    )
    if len(doc) > 0:
        # Running assistant with RAG
        try:
            client.delete_collection('autogen-docs')
        except ValueError:
            print('delete collection')
        assistant = RetrieveAssistantAgent(
            name="K-GPT (RAG enabled)",
            system_message='You are now an Kubernetes (k8s) expert.' 'You should use kubectl '
                           'command to complete task, you should output code blocks in shell '
                           'format',
            llm_config={
                "temperature": 0,
                "timeout": 600,
                "cache_seed": 42,
                "config_list": config_list,
            },
        )

        rag_proxy_agent = RetrieveUserProxyAgent(
            name="User",
            human_input_mode="TERMINATE",
            max_consecutive_auto_reply=15,
            retrieve_config={
                "task": "default",
                "docs_path": doc,
                "model": config_list[0]["model"],
                "embedding_model": "all-mpnet-base-v2",
                "get_or_create": False,
                "must_break_at_empty_line": False
            },
            code_execution_config=False,
            llm_config={"temperature": 0, "seed": 42,
                        "config_list": config_list}
        )
        prompt += termination_notice
        assistant.reset()
        rag_proxy_agent.initiate_chat(assistant, problem=prompt, clear_history=True)
    else:
        # Running assistant without RAG
        assistant = AssistantAgent("K-GPT", llm_config={"temperature": 0, "seed": 41,
                                                        "config_list": config_list},
                                   system_message='You are now an Kubernetes (k8s) expert.' 'You should use kubectl '
                                                  'command to complete task, you should output code blocks in shell '
                                                  'format, do not output yaml')

        user_proxy = UserProxyAgent("User", max_consecutive_auto_reply=15, human_input_mode="TERMINATE",
                                    code_execution_config={"work_dir": "coding", "use_docker": False},
                                    llm_config={"temperature": 0, "seed": 41,
                                                "config_list": config_list})
        prompt += termination_notice
        assistant.reset()
        user_proxy.initiate_chat(assistant, message=prompt, clear_history=True)


@app.command(name='setup')
def setup():
    """
    Run this command first after you install \"agentk8s\", it will prompt you to enter your GPT-4 API KEY
    """
    api_key = typer.prompt("Enter your GPT-4 API KEY")
    config_list = [{
        "model": "gpt-4-1106-preview",
        "api_key": api_key
    }]
    config_path = "./OAI_CONFIG_LIST"
    with open(str(config_path), 'w') as file:
        json.dump(config_list, file)
