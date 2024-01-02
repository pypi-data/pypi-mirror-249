import sys
import os
from pathlib import Path
from importlib.metadata import entry_points
from importlib.util import find_spec
from importlib.resources import files
from copy import deepcopy
from collections.abc import Mapping
from click import argument, group, option, pass_context, echo, UNPROCESSED
from yamlstore import Document, Collection
from .util import merge, task_from_module, get_docs, get_ep_docstring, get_module_docstring
from rich.console import Console
from rich import print
from rich.panel import Panel

console = Console()

@group()
@option('--config', default="config.yaml", help="Configuration file to use.", type=Path)
@pass_context
def docop(ctx, config):
    "Document pipeline processor."

    if config.exists():
        cfg = Document(config, title="default")

        # Merge in selected sections from any extra configuration files
        extra_cfgs = tuple(Path(cfg["dirs"]["configs"]).glob("*.yaml"))
        for extra in (Document(cfg) for cfg in extra_cfgs):
            for section in ("sources", "targets", "content", "accounts"):
                if section in extra:
                    if section not in cfg:
                        cfg[section] = deepcopy(extra[section])
                    else:
                        if isinstance(extra[section], Mapping):
                            cfg[section] = merge(cfg[section], extra[section])
    else:
        subcmd = ctx.invoked_subcommand
        if subcmd not in ("init", "tasks"):
            print(f"No configuration file found so don't know where to look for {subcmd}.")
            sys.exit()
        cfg = None

    ctx.obj = cfg



@docop.command()
@argument("directory", required=True, type=Path)
@pass_context
def init(ctx, directory):
    "Initialize a docop project."
    try:
        os.makedirs(directory, exist_ok=False)
    except FileExistsError:
        print(f"Project directory '{directory}' already exists. Not doing anything.")
        return
    else:
        os.mkdir(directory / "content")
        os.mkdir(directory / "configs")
        os.mkdir(directory / "pipes")
        os.mkdir(directory / "tasks")
        config_example = files(__package__).joinpath('config.yaml.in').read_text()
        (directory / "config.yaml").write_text(config_example)
    print(f"Created project directory structure at '{directory}' and added an example configuration file.", end=' ')
    print(f"You can now do 'cd {directory}' and start using docop.")

@docop.command()
@pass_context
def pipes(ctx):
    "List available task pipelines."

    pipes = Collection(directory=Path(ctx.obj["dirs"]["pipes"]), readonly=True)
    for pipe in pipes.values():
        echo(f"{pipe['title']}: {pipe['description']} ({' → '.join(pipe['tasks'])})")


@docop.command()
@pass_context
def tasks(ctx):
    "List available tasks."

    eps = entry_points()
    packaged_tasks = eps.get("docop.tasks", None)
    restricted_tasks = eps.get("docop.tasks.restricted", None)
    if ctx.obj:
        module_tasks = tuple(Path(ctx.obj["dirs"]["tasks"]).glob("*.py"))
    else:
        module_tasks = None

    if packaged_tasks:
        print("\n[bold]Packaged tasks:[/]")
        for task_ref in packaged_tasks:
            doc_str = get_ep_docstring(task_ref)
            print(f"{task_ref.name}: {doc_str}")

    if restricted_tasks:
        print("\n[bold]Packaged restricted-license tasks:[/]")
        for task_ref in restricted_tasks:
            doc_str = get_ep_docstring(task_ref)
            print(f"{task_ref.name}: {doc_str}")

    if module_tasks:
        print("\n[bold]Your local custom tasks:[/]")
        for task_path in module_tasks:
            name = task_path.name[:-3]
            doc_str = get_module_docstring(task_path)
            print(f"{name}: {doc_str}")
    if not packaged_tasks and not restricted_tasks and not module_tasks:
        echo("No tasks found.")


@docop.command()
@argument("task_or_pipe", metavar="TASKNAME or PIPENAME", nargs=1, required=True, type=str)
@option('--source', '-s', multiple=True, help='Sources that will be fetched and stored as documents.')
@option('--content', '-c', type=Path, multiple=True, help='Stored documents to process.')
@option('--target', '-t', multiple=True, help='Targets to export document content to')
@option('--account', '-a', multiple=False, help='Account to use (source or target)')
@argument('extras', nargs=-1, type=UNPROCESSED)
@pass_context
def run(ctx, task_or_pipe, source, content, target, account, extras):
    "Run a task or pipeline."

    if extras:
        extras = dict((e.split('=')) for e in extras)

    #
    # MAKE SURE WE HAVE ONE AND ONLY ONE UNAMBIGUOUSLY REFERENCED TASK OR PIPE
    #
    if not task_or_pipe:
        echo("No task or pipe given. Not doing anything.")
        return

    module_tasks = [Path(tf).stem for tf in Path(ctx.obj["dirs"]["tasks"]).glob("*.py")]
    eps = entry_points()
    task_eps = {ep.name:ep for ep in eps.get("docop.tasks", ()) + eps.get("docop.tasks.restricted", ())}
    packaged_tasks = [ep.name for ep in eps.get("docop.tasks", ())]
    restricted_tasks = [ep.name for ep in eps.get("docop.tasks.restricted", ())]
    tasknames = module_tasks + packaged_tasks + restricted_tasks 
    pipenames = [Path(pf).stem for pf in Path(ctx.obj["dirs"]["pipes"]).glob("*.yaml")]

    if task_or_pipe in tasknames and task_or_pipe in pipenames:
        echo(f"There is both a task and and a pipe named '{task_or_pipe}'. Please rename either.")
        return

    if task_or_pipe not in tasknames + pipenames:
        echo(f"No task or pipe named '{task_or_pipe}' found.")
        return

    #
    # CONSTRUCT THE PIPELINE
    #
    if task_or_pipe in tasknames:
        pipe = Document(title=task_or_pipe, description=f"run a [bold]{task_or_pipe}[/] task", readonly=True)
        pipe.data["tasks"] = (task_or_pipe,)
    else:
        pipe_path = Path(ctx.obj["dirs"]["pipes"]) / f"{task_or_pipe}.yaml"
        pipe = Document(pipe_path, readonly=True)

    pipesize = len(pipe["tasks"])
    console.rule(f"Building a pipe to {pipe['description']}")

    #
    # SET UP SOURCE RESOURCES TO RETRIEVE
    #
    if source:
        try:
            source_queue = [(srcname, ctx.obj["sources"][srcname]) for srcname in source]
        except KeyError as exc:
            print(f"⚠️  [bold red] source {exc} not found")
            return
    else:
        source_queue = list(pipe.get("sources", {}).items())

    if source_queue:
        print(" • will fetch resources from %i sources: %s" % (len(source_queue), ", ".join((n[0] for n in source_queue))), end='')

    #
    # SET UP LOCALLY STORED CONTENT TO PROCESS
    #
    content_queue = []
    if content:
        content_root = Path(ctx.obj["dirs"]["content"])
        partial_collections = {}
        for content_path in content:
            if Path(content_path).exists():
                path = Path(content_path)
            else:
                path = content_root / content_path
            if path.is_dir():
                content_queue.append(Collection(path))
            elif path.is_file():
                if path.parent not in partial_collections:
                    partial_collections[path.parent] = Collection(path.parent, autoload=False)
                partial_collections[path.parent] += Document(path)
            else:
                echo(f"Content path '{path}' not found.")
                return
        content_queue.extend(partial_collections.values())

    if content_queue:
        summary = ", ".join((c.name + f" ({len(c)} documents)" for c in content_queue))
        print(" • will process %i collections: %s" % (len(content_queue), summary), end='')

    #
    # SET UP TARGETS TO EXPORT TO
    #
    if target:
        target_queue =[(tgtname, ctx.obj["targets"][tgtname]) for tgtname in target]
    else:
        target_queue = []

    if target_queue:
        print(" • will export content to %i targets: %s" % (len(target_queue), ", ".join((n[0] for n in target_queue))), end='')

    #
    # SET UP ACCOUNT TO USE IF GIVEN
    #
    if account:
        try:
            account = ctx.obj["accounts"][account]
        except KeyError as exc:
            print(f"⚠️  [bold red]account {exc} not found")
            return

    # SET UP GLOBAL CONFIGURATION CONTEXT FOR TASK EXECUTION
    #

    config_ctx = {
        "config": ctx.obj,
        "extras": extras,
        "sources": deepcopy(source_queue),
        "targets": deepcopy(target_queue),
        "content": deepcopy(content_queue)
    }

    #
    # RUN PIPELINE. FIRST TASK FETCHES SOURCES, NEXT ONES PROCESS AND LAST ONE EXPORTS
    #

    tasklist = ' → '.join((task for task in pipe["tasks"]))
    print(f"\n • will run {len(pipe['tasks'])} tasks: [bold]{tasklist}[/]")

    for counter, task in enumerate(pipe["tasks"], start=1):

        #
        # CONSTRUCT TASK EXECUTABLE
        #
        if task in module_tasks:
            task_path = Path(ctx.obj["dirs"]["tasks"]) / f"{task}.py"
            try:
                code = task_from_module(task_path)
            except SyntaxError as exc:
                print(f" ⚠️  [bold red]task has error[/]:", exc.msg)
                return
            docstr = get_module_docstring(task_path)
        else: # task in (packaged_tasks + restricted_tasks)
            spec = find_spec(task_eps[task].module)
            code = spec.loader.get_code(task_eps[task].module)
            docstr = get_ep_docstring(task_eps[task])

        print("\n", Panel(f"\n⚙️  [bold]Task {counter} ({task}) → {docstr}\n"))

        #
        # HANDLE CASE WHEN NO SOURCES OR CONTENT OR TARGETS ARE PROVIDED
        #
        if not (source_queue or content_queue or target_queue):
            ctx = deepcopy(config_ctx)
            ctx["account"] = account
            try:
                exec(code, ctx)
            except Exception as e:
                print("⚠️  [bold red]Task run failed: %s[/]" % e)
            return

        #
        #  PIPELINE SUBLOOP 1: PROCESS EACH SOURCE
        #
        if source_queue:
            while source_queue:
                sourcename, source = source_queue.pop(0)

                print(f"Retrieving content for '{sourcename}'...")
                collection = Collection(name=sourcename, directory=Path(ctx.obj["dirs"]["content"]) / sourcename, autosync=True)

                retrieval_ctx = {
                    "source": source,
                    "collection": collection
                }
                if account:
                    retrieval_ctx["account"] = account
                else:
                    try:
                        retrieval_ctx["account"] = ctx.obj["accounts"][source["account"]]
                    except KeyError as exc:
                        print(f"⚠️  [bold red]account {exc} not found")
                        return

                for ref in source["resources"]:
                    retrieval_ctx["reference"] = ref
                    doc = Document()
                    doc["reference"] = ref
                    collection._modified = False
                    doc._modified = False
                    retrieval_ctx["document"] = doc
                    ctx = merge(retrieval_ctx, config_ctx)
                    try:
                        exec(code, ctx)
                    except Exception as e:
                        print("⚠️  [bold red]Task run failed: %s[/]" % e)
                        return
                    else:
                        # If the task added documents, we're done with this source.
                        if ctx['collection'].modified:
                            break
                        # Otherwise, we'll store the doc that the task modified.
                        if ctx["document"].modified:
                            print(f"↳ fetched \'{doc['title']}\' ✅")
                            collection += ctx["document"]
                            print(f"↳ result at {doc._path} ✅")

                content_queue.append((sourcename, collection))
            continue

        #
        # PIPELINE SUBLOOP 2: PROCESS CONTENT COLLECTIONS OR DOCUMENTS
        #

        # If there is a target queue waiting, let the last task of the pipe do exporting
        if not source_queue and not (target_queue and counter == pipesize):

            for collection in content_queue:
                print(f"Processing '{collection.name}' content collection")
                proc_ctx = {"collection": collection}
                if account:
                    proc_ctx["account"] = account

                for count, (doc_name, doc) in enumerate(collection.items(), start=1):
                    doc._modified = False
                    proc_ctx["document"] = doc
                    ctx = merge(proc_ctx, config_ctx)
                    try:
                        exec(code, ctx)
                    except Exception as e:
                        print(f"⚠️  [bold red]failed to process content[/] '{doc}': %s" % e)
                    else:
                        if ctx["document"].modified:
                            ctx["document"].sync()
            continue

        #
        # PIPELINE SUBLOOP 3: PROCESS EACH TARGET
        #
        if target_queue:

            for targetname, target in target_queue:
                print(f"Targeting '{targetname}' ...")

                for title, collection in content_queue:
                    print(f" ↳ Processing '{title}' content collection")

                    export_ctx = {
                        "collection": collection,
                        "target": target
                    }

                    if account:
                        export_ctx["account"] = account
                    else:
                        try:
                            export_ctx["account"] = ctx.obj["accounts"][target["account"]]
                        except KeyError as exc:
                            print(f"⚠️  [bold red]account {exc} not found")
                            return

                    ctx = merge(export_ctx, config_ctx)

                    try:
                        exec(code, ctx)
                    except Exception as exc:
                        print("⚠️  [bold red]task failed[/] %s" % exc)
                        return


@docop.command()
@pass_context
def content(ctx):
    "List the stored collections of YAML documents."

    docs, batches = get_docs((Path(ctx.obj["dirs"]["content"]),))
    if not (docs or batches):
        echo("No documents found.")
        return

    if batches:
        for batch in batches:
            echo(f"{batch.name} ({len(batch)} docs)")

    if docs:
        for doc in docs:
            echo(f"{doc['title']} ({doc['description']})")


@docop.command()
@pass_context
def configs(ctx):
    "List available configurations."

    configs = Collection(Path(ctx.obj["dirs"]["configs"]), readonly=True)
    for config in configs.values():
        echo(f"{config['title']} ({config['description']})")
