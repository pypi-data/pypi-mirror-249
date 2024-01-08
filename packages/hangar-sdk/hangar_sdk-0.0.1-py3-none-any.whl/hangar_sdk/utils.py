from rich.tree import Tree


def print_status(resource, status):
    if status is None:
        return Tree(resource + " : " + "Pending"), None, None

    items = list(
        map(
            lambda x: {
                "resource_id": x["resource_id"],
                "resource_type": x["resource_type"],
                "status": x["status"],
            },
            list(status["status"]["resources"].values()),
        )
    )
    items = sorted(items, key=lambda x: x["resource_type"])
    errors = list(
        map(
            lambda x: {
                "resource_id": x["resource_type"],
                "resource_type": x["resource_id"],
                "message": x["message"].split("\n")[0],
            },
            list(status["status"]["errors"].values()),
        )
    )

    tree = Tree(resource)
    for v in items:
        rendered_status = (
            v["resource_type"] + " - " + v["resource_id"] + " " + v["status"]
        )
        matches = [
            x
            for x in errors
            if v["resource_type"] == x["resource_type"]
            and v["resource_id"] == x["resource_id"]
        ]

        if len(matches) != 0:
            rendered_status += " error: " + matches[0]["message"]

        tree.add(rendered_status)

    return tree, items, errors
