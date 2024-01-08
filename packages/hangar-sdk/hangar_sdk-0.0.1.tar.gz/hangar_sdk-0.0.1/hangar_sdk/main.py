import os
from typing import Annotated, Optional

import httpx
import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

# commands

# actions
# init : creates a new project
# up : runs python and deploys resources
# down : destroys resources


# traits
# logs : shows logs
# ssh : ssh into instances

# CRUD

# resources :
#  - list resources
#  - describe resource
#  - state of resource
#  - last applied and status

# scope : shows scope
# - list scopes
# - describe scope
# - list resources


def print_tree(data, parent=None, tree=None):
    # Initialize the tree if not provided
    if tree is None:
        tree = Tree("Root")
        parent = tree

    if parent is None:
        parent = tree

    # Iterate over items in the dictionary
    for key, value in data.items():
        # For dictionary, recursively build the tree
        if isinstance(value, dict):
            branch = parent.add(f"{key}: ")
            print_tree(value, branch, tree)
        # For list, add each item as a separate branch
        elif isinstance(value, list):
            branch = parent.add(f"{key}: [")
            for item in value:
                if isinstance(item, dict):
                    print_tree(item, branch, tree)
                else:
                    branch.add(str(item))
            branch.add("]")
        # For other types, just add them to the current branch
        else:
            parent.add(f"{key}: {value}")

    return tree


app = typer.Typer()


resources = typer.Typer()

app.add_typer(resources, name="resources")

# # define type URL OPTION

UrlOption = Annotated[
    Optional[str], typer.Option("--url", help="Hangar URL", envvar="HANGAR_URL")
]
DEFAULT_URL = "https://api.tryhangar.com/controlplane"

ApiKeyOption = Annotated[str, typer.Option(help="Api key", envvar="HANGAR_API_KEY")]
JsonOption = Annotated[Optional[bool], typer.Option("--json", help="Output JSON")]

HANGAR_MAIN_URL = "app.tryhangar.com"


@resources.command(name="list")
def list_resources(
    api_key: ApiKeyOption,
    json: JsonOption = False,
    url: UrlOption = DEFAULT_URL,
):
    r = httpx.request(
        "GET",
        url + "/resources",
        headers={"X-API-KEY": api_key},
    )

    if json:
        print(r.json())
        return

    table = Table(title="Resources")

    table.add_column("Resource Id")

    for resource in r.json():
        table.add_row(resource["ResourceId"])

    console = Console()
    console.print(table)


@resources.command()
def describe(
    resource_id: str,
    api_key: ApiKeyOption,
    json: JsonOption = False,
    url: UrlOption = DEFAULT_URL,
):
    r = httpx.request(
        "GET",
        f"{url}/resources/{resource_id}",
        headers={"X-API-KEY": api_key},
    )
    # print(r.json())
    resource = r.json()

    if json:
        print(resource)
        return

    tree = Table(title="Resource: " + resource_id)
    tree.add_column("Scope")
    tree.add_column("Errors")
    tree.add_column("Last Applied")
    tree.add_column("RoleAssumptions")
    tree.add_column("AccountId")
    tree.add_column("Region")
    tree.add_column("Version")

    scope = resource.get("Scope", "")
    error_str = ""
    if "ControlStatus" in resource:
        errors = resource["ControlStatus"]["status"]["errors"]
        for error in errors:
            error_str += error["resource_id"] + ":" + error["message"] + "\n"
    else:
        error_str = "No Errors :)"

    last_applied = resource.get("LastApplied", "")

    role_assumptions = str(resource.get("RoleAssumptions", ""))
    if role_assumptions == "[]":
        role_assumptions = "Default Role"

    account_id = resource.get("AccountId", "")
    region = resource.get("Region", "")
    version = resource.get("Version", "")

    tree.add_row(
        scope, error_str, last_applied, role_assumptions, account_id, region, version
    )

    console = Console()
    console.print(tree)


@resources.command()
def state(
    resource_id: str,
    api_key: ApiKeyOption,
    json: JsonOption = False,
    url: UrlOption = DEFAULT_URL,
):
    r = httpx.request(
        "GET",
        f"{url}/resources/{resource_id}",
        headers={"X-API-KEY": api_key},
        params={"resourceId": resource_id},
    )

    resource = r.json()
    if json:
        print(resource)
        return
    state = resource["ControlState"]

    tree = Tree("State for: " + resource_id)

    for r, v in state.items():
        resource = tree.add(r)
        print_tree(v["values"], tree=resource)

    console = Console()
    console.print(tree)


scopes = typer.Typer()

app.add_typer(scopes, name="scopes")


@scopes.command(name="list")
def list_scopes(
    api_key: ApiKeyOption,
    url: UrlOption = DEFAULT_URL,
):
    r = httpx.request(
        "GET",
        f"{url}/scopes",
        headers={"X-API-KEY": api_key},
    )
    # print(r.json())
    table = Table(title="Scopes")

    table.add_column("Scope Id")

    for scope in r.json():
        table.add_row(scope)

    console = Console()
    console.print(table)


@scopes.command(name="describe")
def describe_scope(
    scope_id: str,
    api_key: ApiKeyOption,
    url: UrlOption = DEFAULT_URL,
):
    r = httpx.request(
        "GET",
        f"{url}/scopes/" + scope_id,
        headers={"X-API-KEY": api_key},
    )
    res = r.json()[0]

    table = Table(title="Scope: " + scope_id)
    table.add_column("Scope")
    table.add_column("Roles")
    table.add_column("AwsAccount")
    table.add_column("Region")

    scope = res.get("Scope", "")
    role_assumptions = str(res.get("RoleAssumptions", ""))

    if role_assumptions == "[]":
        role_assumptions = "Default Role"

    account_id = res.get("AccountId", "")
    region = res.get("Region", "")

    table.add_row(scope, role_assumptions, account_id, region)

    console = Console()
    console.print(table)


@scopes.command(name="resources")
def list_scope_resources(
    scope: str, api_key: ApiKeyOption, url: UrlOption = DEFAULT_URL
):
    r = httpx.request(
        "GET",
        f"{url}/scopes/{scope}/resources",
        headers={"X-API-KEY": api_key},
    )

    table = Table(title="Scope: " + scope)

    table.add_column("Resource Id")

    for resource in r.json():
        table.add_row(resource["ResourceId"])

    console = Console()
    console.print(table)


logs = typer.Typer()

app.add_typer(logs, name="logs")


@logs.command(name="list")
def list_logs(api_key: ApiKeyOption, url: UrlOption = DEFAULT_URL):
    r = httpx.request(
        "GET",
        f"{url}/resources",
        headers={"X-API-KEY": api_key},
    )

    resource_list = r.json()

    table = Table()
    table.add_column("Scope")
    table.add_column("ResourceId")
    table.add_column("Log identifier")

    for resource in resource_list:
        # print(resource["Config"])
        if (
            resource["Config"]
            and resource["Config"] != {}
            and resource["Config"]["construct"] == "cluster"
            # and resource["Config"]["services"] != []
        ):
            # print("hello")
            for service in resource["Config"]["services"]:
                # print(resource["Region"], resource["Config"]["name"], service["name"])
                table.add_row(
                    resource["Scope"],
                    resource["ResourceId"],
                    resource["Region"]
                    + ":"
                    + resource["Config"]["name"]
                    + ":"
                    + service["name"]
                    + "/task",
                )

    console = Console()

    console.print(table)


# @logs.command("tail")
# def tail(
#     log_group: str,
#     api_key: Annotated[str, typer.Option(help="Api key", envvar="HANGAR_API_KEY")],
# ):
#     with httpx.stream(
#         "GET",
#         "http://localhost:8000/controlplane/logs",
#         headers={"X-API-KEY": api_key},
#         params={"log_group_name": log_group},
#     ) as r:
#         for line in r.iter_lines():
#             print(line)


@app.command()
def up(file: str, api_key: ApiKeyOption, url: UrlOption = DEFAULT_URL):
    typer.echo("Deploying resources...")
    import importlib.util

    os.environ["HANGAR_API_KEY"] = api_key
    os.environ["HANGAR_URL"] = url

    spec = importlib.util.spec_from_file_location("hangar_module", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, "hangar_run"):
        mod.hangar_run()


@app.command()
def down(file: str):
    typer.echo("Destroying resources...")
    import importlib.util

    from hangar_sdk.library import Config

    Config.mode = "delete"

    spec = importlib.util.spec_from_file_location("hangar_module", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, "hangar_run"):
        mod.hangar_run()
