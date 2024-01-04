import csv
import functools
import inspect
import os
from contextlib import contextmanager
from math import ceil
from typing import Tuple, List, Optional, Dict, Union, Callable

import requests
import torch
from transformers import GenerationMixin, PreTrainedTokenizer
from supabase import create_client, Client
from postgrest.exceptions import APIError
from .constants import BACKEND_BASE_URL

# TODO: dotenv is a dev dependency, so this will fail in production
# from dotenv import load_dotenv, find_dotenv

_entity_name: Optional[str] = None
_project_name: Optional[str] = None
_task_name: Optional[str] = None
_run_name: Optional[str] = None
supabase: Client = None


def batch_iterator(sequence, batch_size):
    """
    A generator function to yield batches from a given sequence.

    :param sequence: The sequence (like a list) to be batched.
    :param batch_size: The size of each batch.
    :yield: Batches of the sequence.
    """
    if batch_size <= 0:
        yield sequence
        return

    for i in range(0, len(sequence), batch_size):
        yield sequence[i:i + batch_size]


def get_supabase_client():
    return supabase


def get_client_state() -> Tuple[str, str, str]:
    """Get (project_name, task_name, run_name)"""
    return _project_name, _task_name, _run_name


def init_required(func):
    """Make sure that init() has been called before calling the decorated function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _project_name or not _task_name or not _run_name or not supabase:
            raise Exception("goldenset not initialized. Please call gs.init()")
        return func(*args, **kwargs)

    return wrapper


# TODO: Make run_name optional
# TODO: See if team agrees that _name is redundant. run_name is left because wandb uses name
# TODO: We might want to move auth checks to here? Basically do the id resolves in init
def init(project: str, task: str, run_name: str, entity: Optional[str] = None):
    """Initialize run wth project_name, task_name, and run_name"""
    # TODO: dotenv is a dev dependency, so this will fail in production
    # load_dotenv(find_dotenv())

    global _entity_name
    global _project_name
    global _task_name
    global _run_name
    global supabase

    _entity_name = os.environ.get("GOLDENSET_ENTITY", entity)
    _project_name = os.environ.get("GOLDENSET_PROJECT", project)
    _task_name = os.environ.get("GOLDENSET_TASK", task)
    _run_name = os.environ.get("GOLDENSET_RUN_NAME", run_name)


    # TODO: Promote env var names to constants, and document them
    # TODO: Promote defaults to constants
    url: str = os.environ.get(
        "GOLDENSET_URL", "https://njsizbbehmmlwsvtkxyk.supabase.co"
    )
    key: str = os.environ.get(
        "GOLDENSET_ANON_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5qc2l6YmJlaG1tbHdzdnRreHlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk2NDAzODYsImV4cCI6MjAxNTIxNjM4Nn0.MT3585SXcYd4ivR41skp26Y0os1Rx5_AAt2ubapbNKQ",
    )
    supabase = create_client(url, key)

    api_key = os.environ.get("GOLDENSET_API_KEY", None)
    if api_key:
        # TODO: Not sure if the use of lambda here will cause pickle issues
        supabase._get_token_header = lambda: {"Authorization": api_key}
        supabase._auth_token = supabase._get_token_header()
    else:
        raise Exception(
            "Not authenticated. Please set the GOLDENSET_API_KEY environment variable"
        )

    if not _entity_name:
        # if no entity provided, pick one
        entities = _get_entity_names_of_user()
        if not entities:
            raise Exception("No entities found for user. Is you API key valid?")
        _entity_name = _get_entity_names_of_user()[0]


def finish():
    """Finish the run"""
    global _entity_name
    global _project_name
    global _task_name
    global _run_name
    global supabase

    _entity_name = None
    _project_name = None
    _task_name = None
    _run_name = None
    supabase = None


def _get_entity_names_of_user() -> List[str]:
    entity_name_response = (
        supabase.table("entity").select("name").execute()
    )
    return [d['name'] for d in entity_name_response.data]


def _resolve_ids() -> Tuple[str, str, str]:
    entity_id_response = (
        supabase.table("entity").select("id").eq("name", _entity_name).execute()
    )
    if not entity_id_response.data:
        raise ValueError(
            f"Entity {_entity_name} not found. Check that you have access to {_entity_name}"
        )

    entity_id = entity_id_response.data[0]["id"]

    # Get project_id and assert existence
    project_id_response = (
        supabase.table("project")
        .select("id")
        .eq("name", _project_name)
        .eq("entity_id", entity_id)
        .execute()
    )

    if not project_id_response.data:
        raise ValueError(f"Project {_project_name} for entity {_entity_name} not found")

    project_id = project_id_response.data[0]["id"]

    # Get task ID and assert existence
    task_id_response = (
        supabase.table("task")
        .select("id")
        .eq("project_id", project_id)
        .eq("name", _task_name)
        .execute()
    )
    if not task_id_response.data:
        raise ValueError(f"Task {_task_name} for project {_project_name} and entity {_entity_name} not found")

    task_id = task_id_response.data[0]["id"]
    return entity_id, project_id, task_id


# TODO: We need to decide if its testset or goldenset
# TODO: Are we sure we want to return a list of dicts? This makes it difficult to batch inference
@init_required
def get_golden_set(version: Optional[int] = None) -> List[Dict[str, str]]:
    """
    Returns the golden set for the given project and task


    :param version:
        The version of the goldenset to return, by default None

    :return golden_set:
        List of dictionaries containing the input and output of the golden set, as well as the test_set row id, necessary to log the outputs.
    """
    # Get entity_id and check that user can access
    _, _, task_id = _resolve_ids()

    # Obtain versioned testset id, otherwise take most recent
    if version is not None:
        testset_id_response = (
            supabase.table("testset")
            .select("id")
            .eq("task_id", task_id)
            .eq("version", version)
            .execute()
        )
        if not testset_id_response.data:
            raise ValueError(
                f"Version {version} not found for {_entity_name}/{_project_name}/{_task_name}"
            )
    else:
        testset_id_response = (
            supabase.table("testset")
            .select("id", "version")
            .eq("task_id", task_id)
            .order("version", desc=True)
            .execute()
        )

        if not testset_id_response.data:
            raise ValueError(f"Task {_task_name} has no saved testset. "
                             f"You can create one using the webapp or by calling gs.extend_golden_set()")

        version = testset_id_response.data[0]["version"]

    testset_id = testset_id_response.data[0]["id"]

    # Get questions for a given testset_id  and assert existence
    testset_response = (
        supabase.table("testset_row")
        .select("id, input, output")
        .eq("testset_id", testset_id)
        .execute()
    )
    if not testset_response.data:
        raise ValueError(
            f" The testset for {_entity_name=}/{_project_name=}/{_task_name=}[v{version}] has no rows"
        )

    return [
        {"input": q["input"], "output": q["output"], "id": q["id"]}
        for q in testset_response.data
    ]


# TODO: Set a standard argument order for all functions E -> P -> T -> RS -> Run
# PK -> FK -> Data
def _create_run(run_name: str, task_id: str, entity_id: str) -> Optional[str]:
    """
    Create a run in run table for a given task_id and entity_id

    Parameters
    ----------
    run_name : str
        Name of the run to be created
    task_id : str
        ID of the task the run belongs to, obtained from the task table by querying the task name
    entity_id : str
        ID of the entity creating the run

    Returns
    -------
    str | None : ID of the run created
    """
    # Create new run in run table and return ID
    # TODO don't insert run if name is taken
    # TOOO enforce this on the DB level: (name, task_id, entity_id) should be unique
    run_insertion = (
        supabase.table("run")
        .insert(
            {
                "name": run_name,
                "task_id": task_id,
                "entity_id": entity_id,
            }
        )
        .execute()
    )
    if run_insertion.data:
        return run_insertion.data[0]["id"]

    raise Exception("Failed to create run")


def _run_name_taken(run_name: str, task_id: str, entity_id: str) -> bool:
    # TODO scope this to project
    """
    Check if a run name is taken for a given task_id and entity_id

    Parameters
    ----------
    run_name : str
        Name of the run to be created
    task_id : str
        ID of the task the run belongs to, obtained from the task table by querying the task name
    entity_id : str
        ID of the entity creating the run

    Returns
    -------
    bool : True if run name is taken, False otherwise
    """
    run_name_response = (
        supabase.table("run")
        .select("name")
        .eq("name", run_name)
        .eq("task_id", task_id)
        .eq("entity_id", entity_id)
        .execute()
    )

    return bool(run_name_response.data)


def _populate_rows(
    entity_id: str, project_id: str, task_id: str, run_id: str, testset_row_ids: List[str], completions: List[str], logprobs: Optional[List[List[float]]], model_contexts: Optional[str]
) -> List[Dict[str, str]]:
    """
    Function to populate the run_row table with the completions and testset_row_ids

    Parameters
    ----------
    entity_id : str
        ID of the entity creating the run
    run_id : str
        ID of the run the completions belong to
    completions : List[str]
        List of completions for a given testset_row
    testset_row_ids : List[str]
        List of testset_row_id for a given testset_row, is the row_id of the question a completion belongs to

    Returns
    -------
    List[Dict[str, str]] : List containing the entries into the run_row table, including columns auto-filled by supabase.
    """
    # TODO: I think the FK constraint will catch this, so we don't need to check
    # test_set_response = (
    #    supabase.table("testset_row")
    #    .select("id")
    #    .in_("id", testset_row_ids)
    #    .execute()
    # )

    # if len(test_set_response.data) != len(testset_row_ids):
    #    raise Exception("Invalid testset_row_ids")

    if logprobs is None:
        logprobs = [None] * len(completions)

    if model_contexts is None:
        model_contexts = [None] * len(completions)

    # for long test sets we need to batch requests, see reason here: https://github.com/supabase/postgrest-js/issues/393
    existing_testset_row_ids = []
    existing_run_row_ids = []
    for id_batch in batch_iterator(testset_row_ids, 200):
        existing_entries_response = (
            supabase.table("run_row")
            .select("id, testset_row_id, run_id, run_id!inner(task_id!inner(id, project_id))")
            .eq("run_id", run_id)
            .eq("entity_id", entity_id)
            .eq("run_id.task_id.id", task_id)
            .eq("run_id.task_id.project_id", project_id)
            .in_("testset_row_id", id_batch)
        ).execute()
        existing_testset_row_ids.extend([d["testset_row_id"] for d in existing_entries_response.data])
        existing_run_row_ids.extend([d["id"] for d in existing_entries_response.data])

    insert_list = [
        {
            "run_id": run_id,
            "testset_row_id": testset_row_id,
            "entity_id": entity_id,
            "pred": completion,
            "kwargs": {"logprobs": logprobs_i},
            "model_context": model_context_i,
        }
        for completion, testset_row_id, logprobs_i, model_context_i in zip(completions, testset_row_ids, logprobs, model_contexts) if testset_row_id not in existing_testset_row_ids
    ]

    update_list = [
        {
            "id": id_,
            "run_id": run_id,
            "testset_row_id": testset_row_id,
            "entity_id": entity_id,
            "pred": completion,
            "kwargs": {"logprobs": logprobs_i},
            "model_context": model_context_i,
        }
        for completion, testset_row_id, logprobs_i, id_, model_context_i in zip(completions, testset_row_ids, logprobs, existing_run_row_ids, model_contexts) if
        testset_row_id in existing_testset_row_ids
    ]
    if update_list:
        # TODO use logger
        print(f"Updating {len(update_list)} existing rows")
    try:
        insertion_response = supabase.table("run_row").insert(insert_list).execute()
        for update_dict in update_list:
            supabase.table("run_row").update(update_dict).eq("id", update_dict["id"]).execute()
    except APIError as e:
        if (
            e.message
            == 'insert or update on table "run_row" violates foreign key constraint "run_row_testset_row_id_fkey"'
        ):
            raise ValueError(
                f"At least one of the ids passed does not exist in the golden set"
            )
        else:
            raise Exception("Failed to insert rows")

    if not insertion_response.data:
        raise Exception("Failed to insert rows")

    return insertion_response.data


# TODO: Not sure if ids is a good name.
# I think testset_row_ids is too verbose though and exposes implementation details that the user doesn't need to know
# TODO: kwargs and errors arent implemented
@init_required
def log_run(
    ids: List[str],
    completions: List[str],
    logprobs: Optional[List[List[float]]] = None,
    model_contexts: Optional[List[str]] = None,
    kwargs: Optional[List[dict]] = None,
    errors: Optional[List[Optional[str]]] = None,
) -> Tuple[str, str]:
    """
    Log a run for evaluation.

    :param ids:
        List of ids
    :param completions:
        List of completions
    :param logprobs:
        List of transition logprobs for each completion
    :param model_contexts:
        The context passed to the model as part of a RAG pipeline or similar
    :param kwargs:
        List of kwargs
    :param errors:
        List of errors

    :returns:
        Tuple contained the Run ID and Run Name
    :rtype: Tuple[str, str]
    """
    entity_id, project_id, task_id = _resolve_ids()

    if len(completions) != len(ids):
        raise ValueError(f"Length of completions and ids must be equal. Got {len(completions)} completions and {len(ids)} ids")

    if len(set(ids)) != len(ids):
        from collections import Counter

        raise ValueError(
            f"Found duplicate ids: {[i for i in Counter(ids).items() if i[1] > 1]}"
        )

    run_id = _create_run(run_name=_run_name, task_id=task_id, entity_id=entity_id)

    # Populate run_row table with completions and testset_row_ids
    inserted_data = _populate_rows(
        entity_id=entity_id,
        project_id=project_id,
        task_id=task_id,
        run_id=run_id,
        completions=completions,
        testset_row_ids=ids,
        logprobs=logprobs,
        model_contexts=model_contexts,
    )

    _trigger_metrics_calculation(run_id)

    return run_id, _run_name


def _trigger_metrics_calculation(run_id: str):
    api_key = os.environ.get("GOLDENSET_API_KEY", None)

    api_url = f"{BACKEND_BASE_URL}/launch_background_metrics_computation"
    params = {'run_id': run_id}
    headers = {'Authorization': f'Bearer {api_key}'}

    response = requests.post(api_url, params=params, headers=headers)
    return response


@init_required
def extend_golden_set(path: Optional[str] = None, golden_set: Optional[List[Tuple[str, Optional[str], Optional[List[str]]]]] = None, reader_kwargs: Optional[Dict] = None):
    """
    Extend the golden set with questions and answers from a csv file.

    :param path: The path to the csv file containing the golden set.
        The csv file can contain 1 - 3 columns, containing question (required), ground truth (optional), and keywords (optional), respectively.
        If a `path` is provided, do not pass a `golden_set`.

        Example csv file:
        ```csv
        What is 2+2?,2+2=4,4
        What is a train?,A train is a vehicle that runs on tracks,train tracks vehicle
        What is a car?,A car is a vehicle that runs on roads
        ```

        The csv file should not have any headers.
        If one of the rows has a ground truth, all rows must have a ground truth.
        A row that has keywords must have a ground truth.
        Keywords are space-separated.
    :param golden_set: The golden set to upload.
        If a `golden_set` is provided, do not pass a `path`.

        The `golden_set` is a list of rows in the test set, where every row is represented as a tuple.
        Each such tuple is in the format (question, ground_truth, keywords).

        Example golden set:
        ```python
        [
            ('What is 2+2?', '2+2=4', ['4']),
            ('What is a train?', 'A train is a vehicle that runs on tracks', ['train', 'tracks', 'vehicle']),
            ('What is a car?', 'A car is a vehicle that runs on roads', None)
        ]
        ```

        `question` is a string containing the question.
        `ground_truth` is a string containing the ground truth, or None. If one row has None as ground truth, all rows must have None as ground truth.
        `keywords` is a list of strings containing keywords, or None. If a row has None as ground truth, it must have None as keywords.

    :param reader_kwargs: Optional arguments to pass to `csv.reader`
    """
    if path is None and golden_set is None:
        raise ValueError("Either `path` or `golden_set` must be provided")
    if path is not None and golden_set is not None:
        raise ValueError("Only one of `path` or `golden_set` can be provided")
    if path is not None:
        abs_path = os.path.abspath(path)

        csv_rows: list[Tuple] = []
        with open(abs_path) as f:
            for row in csv.reader(f, **reader_kwargs or {}):
                row_list = list(row)

                # "normalize" row to contain all of question, ground truth, and keywords
                if len(row_list) == 1:
                    # only question is given, add None ground truth
                    row_list.append(None)
                if len(row_list) == 2:
                    # question and ground truth are given, add None keywords
                    row_list.append(None)
                if len (row_list) != 3:
                    raise ValueError(
                        f"Invalid row: {row_list}. Rows must contain 1 - 3 columns, containing question (required), ground truth (optional), and keywords (optional), respectively"
                    )

                # parse keywords to list
                keywords = row_list[-1]
                if keywords is not None:
                    keywords = keywords.split()
                    row_list[-1] = keywords

                csv_rows.append(tuple(row_list))
        golden_set = csv_rows

    # get testset to extend
    entity_id, _, task_id = _resolve_ids()
    testset_id_response = (
        supabase.table("testset")
        .select("id, task_id")
        .eq("task_id", task_id)
    ).execute()
    if len(testset_id_response.data) == 0:
        # no test set exists yet, create one
        # TODO use logger
        print("No goldenset exists yet, creating one")
        insert_response = supabase.table("testset").insert({"task_id": task_id, "entity_id": entity_id}).execute()
        testset_id = insert_response.data[0]["id"]
    else:
        testset_id = testset_id_response.data[0]["id"]

    # extend testset
    insert_data = [{"input": question, "output": answer, "keywords": keywords, "testset_id": testset_id, "entity_id": entity_id} for question, answer, keywords in golden_set]
    supabase.table("testset_row").insert(insert_data).execute()


@contextmanager
def _add_pad_token_if_not_exist(tokenizer: PreTrainedTokenizer):
    pad_token_before = tokenizer.pad_token
    if pad_token_before is None:
        #TODO replace with logging
        print('Adding padding token to tokenizer')
        tokenizer.pad_token = tokenizer.eos_token

    yield

    if pad_token_before is None:
        #TODO replace with logging
        print('Removing padding token from tokenizer')
        tokenizer.pad_token = pad_token_before


@init_required
def log_model(
    model: GenerationMixin,
    tokenizer: PreTrainedTokenizer,
    batch_size: int = -1,
    generation_kwargs: Optional[Dict] = None,
    device: Optional[Union['torch.device', str]] = None,
):
    """
    Run the golden set through the `model` and record the results.

    :param model: The HuggingFace model to log
    :param tokenizer: The tokenizer of the `model`
    :param batch_size: The batch size to use for inference. If -1, the entire golden set will be processed in one batch.
    :param generation_kwargs: Optional arguments to pass to `model.generate`
    :param device: The device to use for inference. If None, the device of the `model` will be used.
        If the `model` does not have a `.device` property, cpu will be used.
    """
    #if _run_name_taken(_run_name, *_resolve_ids()):
    #    # TODO use a logger for this
    #    print(f'WARNING: Run name {_run_name} already taken for entity {_entity_name}, project {_project_name}, task {_task_name}. '
    #          f"Only golden set entries that haven't been previously logged will be logged. "
    #          f"If you want to override the previous run, please delete it first using the webapp.")
    _device = device or getattr(model, "device", None) or torch.device("cpu")

    generation_kwargs = generation_kwargs or dict()
    generation_kwargs.update({"return_dict_in_generate": True, "output_scores": True})

    goldenset = get_golden_set()
    gs_prompts = [d['input'] for d in goldenset]
    gs_prompt_ids = [d['id'] for d in goldenset]
    print(f"Logging {len(gs_prompts)} prompts in {ceil(len(gs_prompts)/batch_size)} batches.")

    completions_accumulator: List[str] = []
    logprobs_accumulator: List[List[float]] = []
    with _add_pad_token_if_not_exist(tokenizer):
        for i_batch, prompt_batch in enumerate(batch_iterator(gs_prompts, batch_size)):
            inputs_tokenized = tokenizer(prompt_batch, return_tensors="pt", padding=True).to(_device)
            outputs = model.generate(**inputs_tokenized, **generation_kwargs)
            out_seq, out_scores = outputs.sequences, outputs.scores

            right_padding_lens: List[int] = []
            for prompt, output in zip(prompt_batch, out_seq):
                right_padding_len = 0
                for i in range(len(output) - 1, -1, -1):
                    if output[i] != tokenizer.pad_token_id:
                        right_padding_len = len(output) - i - 1
                        break
                right_padding_lens.append(right_padding_len)
                # decode and chop off the prompt
                completion = tokenizer.decode(output, skip_special_tokens=True)
                completions_accumulator.append(completion[len(prompt):])

            transition_scores = model.compute_transition_scores(
                out_seq, out_scores, normalize_logits=True
            )

            # chop off transition scores of the right padding
            # left padding and prompt are already chopped off by compute_transition_scores
            for i, scores in enumerate(transition_scores):
                right_pad_len = right_padding_lens[i]
                if right_pad_len > 0:
                    logprobs_accumulator.append(scores[:-right_padding_lens[i]].tolist())
                else:
                    logprobs_accumulator.append(scores.tolist())

            print(f"Batch {i_batch+1}/{ceil(len(gs_prompts)/batch_size)} complete")
    return log_run(
        ids=gs_prompt_ids,
        completions=completions_accumulator,
        logprobs=logprobs_accumulator,
    )


def _check_metric_fn_signature(metric_fn: Callable):
    sig = inspect.signature(metric_fn)
    params = sig.parameters
    if len(params) != 3:
        raise ValueError(f"Metric function must take 3 arguments, but {metric_fn.__name__} takes {len(params)}")

    input_type_hints = [param.annotation for param in params.values()]
    if not all((input_type_hint in [str, inspect.Signature.empty] for input_type_hint in input_type_hints)):
        raise ValueError(f"Metric function must take 3 str arguments, but {metric_fn.__name__} takes {input_type_hints}")

    return_type = sig.return_annotation
    if not (return_type is float or return_type is int or return_type is inspect.Signature.empty):
        raise ValueError(f"Metric function must return a float or int, but {metric_fn.__name__} returns {return_type}")


@init_required
def upload_metric(metric_fn: Callable[[str, str, str], float]):
    """
    Uploads a custom metric function.

    :param metric_fn: A function that takes the prompt (str), reference answer (str), and model answer (str), and returns a score (float).
        It must be a pure function that does not depend on outside scope or perform side effects.
        The name of the function will be set as the metric's name; the docstrings as its description

        If the function uses any imported modules, they must be imported inside the function body.
        Using packages that need to be installed from PyPI is not currently supported.

        EXAMPLE:

        ```python
        import goldenset as gs

        gs.init('<YOUR-PROJECT>', '<YOUR-TASK>', '<YOUR-RUN>')

        def my_metric_fn(prompt: str, reference_answer: str, model_out: str) -> float:
            '''Returns a random score between 0 and 1'''
            import random

            return random.uniform(0, 1)

        gs.upload_metric(my_metric_fn)
        ```


    """
    _check_metric_fn_signature(metric_fn)

    name = metric_fn.__name__
    description = inspect.getdoc(metric_fn)
    definition = inspect.getsource(metric_fn)

    entity_id, _, _ = _resolve_ids()
    supabase.table("custom_metrics").insert({'entity_id': entity_id, 'name': name, 'description': description, 'implementation': definition}).execute()


@init_required
def delete_run():
    raise NotImplementedError("Please delete runs using the webapp")
