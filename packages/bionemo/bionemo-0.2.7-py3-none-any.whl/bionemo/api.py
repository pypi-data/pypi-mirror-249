# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
"""
This is the BioNemoService Python Client module.

It contains the class BionemoClient, which is a python interface to the BioNemo Service.
The BioNemo Service is an inference-as-a-service developed by NVIDIA for deployment of
AI models in the biology and chemistry domains.
"""

import copy
import http
import io
import json
import os
import sys
import threading
import time
import warnings
from typing import List, Union

import h5py as h5
import numpy as np
import requests
from requests_futures.sessions import FuturesSession

import bionemo.response_handler as response_handler
from bionemo.error import ApiKeyNotSetError, AuthorizationError, BadRequestId, IncorrectParamsError
from bionemo.request_id import RequestId
from bionemo.task_tracker import log_request_status, set_request_log_file
from bionemo.version import __version__

if sys.version_info.minor < 8:
    from typing_extensions import Literal
else:
    from typing import Literal

MAX_CONNECTION_RETRIES = 3
REQUESTS_TIMEOUT_SECS = 1200

# used by generate_future and generate_multiple only
MAX_CONCURRENT_HTTP_REQUESTS = 3
DEFAULT_BINARY_DATA_TYPE = "npz"

# make sure all sessions on single thread to minimize TCP reconnections
_thread_context = threading.local()


def create_session():
    """Create session so that TCP connection does not reset, reducing handshake latency.

    Returns:
        requests.Session: a requests Session instance
    """
    session = requests.Session()
    session.mount(
        "https://", requests.adapters.HTTPAdapter(max_retries=MAX_CONNECTION_RETRIES),
    )
    return session


def create_generate_future_session():
    """Create a futures session.

    Generate needs to be called with multiple concurrent request,
    hence create new session for generate_future.

    Returns:
        requests.session.FuturesSession: a requests FuturesSession instance
    """
    session = requests.Session()
    session.mount(
        "https://", requests.adapters.HTTPAdapter(max_retries=MAX_CONNECTION_RETRIES),
    )
    future_session = FuturesSession(session=session, max_workers=MAX_CONCURRENT_HTTP_REQUESTS)
    return future_session


class BionemoClient:
    """
    A python client to request inference from the BioNemoService.

    Some models (like MegaMolBART) are synchronous and return an immediate result.  Others
    (like MoFlow) are asynchronous i.e. they return a value that can be used to find the
    result once it's ready.

    This class provides a MODEL_sync() call for all supported models, as well
    as a MODEL_async() call for each asynchronous model.  When the caller
    is ready to retrieve the results of an asynchronous call it should call the
    fetch_result() method, passing it the value returned by the MODEL()_async call.
    """

    def __init__(
        self,
        api_key=None,
        org_id=None,
        api_host=None,
        timeout_secs=REQUESTS_TIMEOUT_SECS,
        do_logging=False,
        log_file_path=None,
        log_file_append=True,
    ):
        """Construct an client instance.

        Args:
            api_key (str): The user API key necessary to access the service.
            org_id (str): The organization ID of the user.
            api_host (str): The URL to the backend service API.
            timeout_secs (int): The timeout duration for all requests in seconds. Defaults to 1200 seconds.
            do_logging (bool, Optional): Set to True to enable logging. Defaults to False.
            log_file_path (str, Optional): If logging is enabled this specifies the location of the log file.
                If logging is enabled but log_file_path is not set a tempfile will be used.
            log_file_append (bool): If logging is enabled and log_file_append is True then the log file
                will be appended to.  If logging is enabled and log_file_append is False then the log file
                will be overwritten.  Defaults to True.

        Raises:
            error.ApiKeyNotSetError: if no API key is set.

        If specified, the log file will contain a timestamp and the request information: correlation ID,
        action performed, name of the model and status of the request.

        Note that not all calls result in a log entry - get_smiles(), get_uniprot() and list_models() do
        not log anything.  fetch_tasks() will log the status of all existing tasks, in addition to returning
        task status.
        """
        self.api_key = api_key if api_key is not None else os.getenv("NGC_API_KEY")
        if not self.api_key:
            raise ApiKeyNotSetError(
                "API KEY is not set. Please pass api_key when instantiating BionemoClient"
                " or do'export NGC_API_KEY=<your_ngc_api_key>'"
            )

        self.org_id = org_id if org_id is not None else os.getenv("NGC_ORG_ID")
        # TODO: Understand whether ORG ID use will be necessary in production.
        # if not self.org_id:
        #     warnings.warn(
        #         "ORG ID is not set. If you have one and would like to set it, please pass org_id"
        #         " when instantiating BionemoClient do 'export NGC_ORG_ID=<your_ngc_org_id>'"
        #     )

        self.api_host = api_host if api_host is not None else "https://api.bionemo.ngc.nvidia.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": f"python-client:{__version__}",
        }
        if self.org_id:
            self.headers["Organization-ID"] = self.org_id
        self.timeout_secs = timeout_secs

        # Don't check this until after self.api_key and self.api_host have been set.
        # Here we call list_models as a proxy for key verification. If this fails,
        # list_models will raise an exception with the correct response from the server.
        self.list_models()
        set_request_log_file(do_logging, file_path=log_file_path, append=log_file_append)

    def verify_key(self):
        """ Verify the API key.

        Args:
            None

        Returns:
            bool: True if the API_KEY passed to the constructor is valid, False otherwise.
        """
        try:
            # Why list_models()? It's fast, doesn't require any parameters and doesn't change the state
            # of the users data on the server.
            _ = self.list_models()
            return True
        except Exception:
            return False

    def list_models(self):
        """List available models for inference.

        Returns:
            List: A list of available models and their API methods.
        """
        url = f"{self.api_host}/models"

        if not hasattr(_thread_context, "session"):
            _thread_context.session = create_session()

        response = _thread_context.session.get(url, headers=self.headers, timeout=self.timeout_secs)
        response_handler.ResponseHandler.handle_response(response)
        return response.json()["models"]

    def get_uniprot(self, uniprot_id: str):
        """Get amino acid sequence by UniProt ID.

         Args:
            uniprot_id (str): A UniProt protein ID.

        Returns:
            str: The corresponding amino acid sequence.

        """
        BionemoClient._check_sessions()
        headers = self._setup_headers()
        url = f"{self.api_host}/uniprot/{uniprot_id}"
        response = requests.get(url, headers=headers, timeout=self.timeout_secs, stream=False,)
        response_handler.ResponseHandler.handle_response(response)
        return json.loads(response.content)

    def get_smiles(self, pubchem_cid: str):
        """Get SMILES from PubChem CID.

         Args:
            pubchem_cid (str): A PubChem CID.

        Returns:
            str: The corresponding SMILES string.

        """
        BionemoClient._check_sessions()
        headers = self._setup_headers()
        url = f"{self.api_host}/pubchem/{pubchem_cid}"
        response = requests.get(url, headers=headers, timeout=self.timeout_secs, stream=False,)
        response_handler.ResponseHandler.handle_response(response)
        return json.loads(response.content)

    def _setup_headers(self, return_type=None):
        """Copy self.headers, add logging & return type settings as needed.

        Args:
            return_type (str): The expected return type from the request

        Returns:
            Dict: Header for HTML request.
        """
        headers = copy.copy(self.headers)
        if return_type == "stream":
            headers["x-stream"] = "true"
        return headers

    @staticmethod
    def _check_sessions(return_type: str = None):
        """Make sure we have the right kind of session.

        Args:
            return_type (str): the expected return type from the request
        """
        if return_type not in ["async", "future"] and not hasattr(_thread_context, "session"):
            _thread_context.session = create_session()

        if return_type in ["async", "future"] and not hasattr(_thread_context, "generate_future_session"):
            _thread_context.generate_future_session = create_generate_future_session()

    def _wait_for_response(
        self, py_request_id: RequestId,
    ):
        """Wait for a response from the model, polling periodically.

        The async BioNeMo calls require that you poll a particular URL for the response.
        Construct that URL from the request ID (model:correlation_id) and wait for it
        to return something.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            Dict: The loaded JSON request response

        Raises:
            ValueError: If the model response is anything other than status 200 (OK) or
                        if the task was cancelled or had an inference error.
            requests.Timeout: If the service doesn't respond in time.
        """
        correlation_id = py_request_id.correlation_id
        url = f"{self.api_host}/task/{correlation_id}"

        starting_time = time.time()
        headers = self._setup_headers()
        tmo = py_request_id.timeout if py_request_id.timeout else self.timeout_secs
        while True:
            response = requests.get(url, headers=headers)
            if response.ok:
                status_result = json.loads(response.content)
            else:
                raise ValueError(
                    f"Error in fetching request {url}. Status code: {response.status_code}"
                    f"\nResponse: {response.content}"
                )
            log_request_status(
                py_request_id.correlation_id,
                "check_request_status",
                py_request_id.model_name,
                status_result["control_info"]["status"],
            )
            if status_result["control_info"]["status"] in ["DONE", "CANCEL", "ERROR"]:
                break
            time.sleep(5)  # waiting for the prediction from BioNeMo Server

            if time.time() - starting_time > tmo:
                raise requests.Timeout(f"Timed out waiting for response for {py_request_id.correlation_id}")

        if status_result["control_info"]["status"] in ["CANCEL", "ERROR"]:
            raise ValueError(
                "No output from task with correlation id {} due to task state: {}"
                "\n Detailed response: {}".format(
                    status_result["control_info"]["correlation_id"],
                    status_result["control_info"]["status"],
                    status_result["response"],
                )
            )
        return status_result

    @staticmethod
    def _process_response(
        response, return_type=None,
    ):
        """Process a raw response.

        Args:
            response (requests.models.Response): A requests response.
            return_type (str): The expected payload type in the response.

        Returns:
            Dict (JSON): A post-processed response
        """
        if return_type == "stream":
            response_handler.ResponseHandler.handle_response(response, stream=True)
            return response.iter_lines()
        if return_type in ["async", "future"]:
            return response
        if return_type == "text":
            response_handler.ResponseHandler.handle_response(response)
            return response_handler.ResponseHandler.post_process_generate_response(response, True)
        response_handler.ResponseHandler.handle_response(response)
        return response_handler.ResponseHandler.post_process_generate_response(response, False)

    def _submit_request(
        self, model_name: str, url: str, data, files, timeout=None,
    ):
        """Construct and post() the request.

        Args:
            model_name (str): the name of the requested inference model
            url (str): the API endpoint to which the request will be sent
            data (Dict(JSON)): the data payload
            files (Dict(JSON)): the files payload, if any
            timeout (int): the timeout duration in seconds. A timeout results in a
                requests.exceptions.Timeout exception raised.
        """
        BionemoClient._check_sessions()
        headers = self._setup_headers()

        response = _thread_context.session.post(
            url,
            headers=headers,
            json=data,
            timeout=self.timeout_secs,
            stream=False,
            files=files,
            allow_redirects=False,
        )
        processed_response = BionemoClient._process_response(response)
        # status is unknown at this point.
        log_request_status(processed_response["correlation_id"], "request_inference", model_name, "UNKNOWN")
        return RequestId(model_name, processed_response["correlation_id"], timeout)

    #
    # Syncronous (blocking) calls.
    #
    def megamolbart_embeddings_sync(
        self, smis: List[str],
    ):
        """Request MegaMolBart embeddings inference, wait for the response.

        MegaMolBart is a generative model developed by NVIDIA to produce novel small molecules given
        an input seed molecule.
        https://github.com/NVIDIA/MegaMolBART

        This function will request embeddings for the input SMILES from MegaMolBart.
        Approximate inference duration: < 0.1 second.

        Args:
            smis (List[str]): List of SMILES strings for which embeddings will be generated.
                              Each string may be 1 to 510 characters.

        Returns:
            List[numpy.ndarray]: A list of embeddings, one for each input.
        """
        url = f"{self.api_host}/molecule/megamolbart/embeddings"
        data = {
            "smis": smis,
            "format": DEFAULT_BINARY_DATA_TYPE,
        }
        BionemoClient._check_sessions()
        headers = self._setup_headers()

        response = _thread_context.session.post(
            url, headers=headers, json=data, timeout=self.timeout_secs, stream=False,
        )

        response_handler.ResponseHandler.handle_response(response)
        response_list = BionemoClient._decode_embedding_response(response.content, DEFAULT_BINARY_DATA_TYPE)

        return [x["embeddings"] for x in response_list]

    def esm2_sync(
        self, sequences: List[str], model: Literal["650m", "3b", "15b"] = "650m",
    ):
        """Request ESM2 inference, wait for the response.

        Evolutionary Scale Modeling 2 (ESM2) is a protein-to-embedding generator developed
        by Facebook AI Research.
        https://github.com/facebookresearch/esm

        Approximate inference time: <1 second.

        Args:
            sequences (List[str]): List of strings in the protein alphabet for which embeddings
                                   will be generated. Each string should be 1 to 1024 characters.

        Returns:
            List[Dict[numpy.array]]: A list of outputs corresponding to the input list.
                Each list entry is a dict that contains following keys:
                'representation', 'tokens', 'logits' and 'embeddings', all of which contain
                a numpy array. Each item in the output list corresponds to the input list item.
        """
        url = f"{self.api_host}/protein-embedding/esm2-{model.lower()}/embeddings"
        data = {
            "sequence": sequences,
            "format": DEFAULT_BINARY_DATA_TYPE,
        }
        BionemoClient._check_sessions()
        headers = self._setup_headers()

        response = _thread_context.session.post(
            url, headers=headers, json=data, timeout=self.timeout_secs, stream=False,
        )
        response_handler.ResponseHandler.handle_response(response)
        response_data = BionemoClient._decode_embedding_response(response.content, DEFAULT_BINARY_DATA_TYPE)
        #
        # For esm2, there is padding in the tokens that needs to be removed.
        # For each padded index in "tokens", we must also remove the corresponding
        # indexes in all other arrays.
        # TODO(trvachov): fetch padding values from API rather than hard-coding 0,1,2)
        for response in response_data:
            keep_index_list = [i for i, token in enumerate(response["tokens"]) if token not in [0, 1, 2]]
            response["tokens"] = response["tokens"][keep_index_list]
            response["logits"] = response["logits"][keep_index_list]
            response["representations"] = response["representations"][keep_index_list]
        return response_data

    def esm1nv_sync(
        self, sequences: List[str],
    ):
        """Request ESM1nv inference, wait for response.

        ESM1nv is an embedding generation model developed by NVIDIA, based on prior work
        by Facebook AI Research's ESM-1b model.

        Approximate infernece time: <0.1 second.

        Args:
            sequences (List[str]): List of strings in the protein alphabet for which embeddings
                                   will be generated. Each string should be 1 to 512 characters.

        Returns:
            List[numpy.ndarray]: A list of embeddings, one for each input.
        """
        url = f"{self.api_host}/protein-embedding/esm1nv/embeddings"
        data = {
            "sequence": sequences,
            "format": DEFAULT_BINARY_DATA_TYPE,
        }
        BionemoClient._check_sessions()
        headers = self._setup_headers()

        response = _thread_context.session.post(
            url, headers=headers, json=data, timeout=self.timeout_secs, stream=False,
        )

        response_handler.ResponseHandler.handle_response(response)
        response_list = BionemoClient._decode_embedding_response(response.content, DEFAULT_BINARY_DATA_TYPE)
        return [x["embeddings"] for x in response_list]

    #
    # Asynchronous calls.  Calling
    #
    #     task_id = MODEL_async(...)
    #
    # will return a value that uniquely identifies that request.  Call
    #
    #     fetch_task_status(task_id)
    #
    # to see if the task is ready.  Once it's ready, call
    #
    #     results = fetch_result(task_id)
    #
    # to retrieve the results.
    #
    # Note, the BionemoClient keeps track of asynchronous tasks using a "correlation_id", which
    # is a UUID e.g. 285bc36c-00a9-40eb-acdf-62ecaf2c378b
    #
    # In this python API, we defined a "py_request_id" which is a combination of everything we
    # know about a request: model name, correlation id, call-specific timeout (if used) and
    # status (if known).  The correlation ID is a UUID, the model name is used in identifying
    # how to unwrap the JSON response of certain models.
    def fetch_result(self, py_request_id: RequestId):
        """Get inference results from request id.

        Given a request ID (modelname:correlation_id) get the
        results from the server and dispatch them to the appropriate parser, returning
        the parsed result.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            (multiple types): The result of the model, which is a different type for each model.

        Raises:
            ValueError: If py_request_id is invalid.
        """
        model = py_request_id.model_name

        # Wait for results to become available.
        start_time = time.time()
        while self.fetch_task_status(py_request_id) in ["CREATED", "PROCESSING"]:
            if time.time() - start_time > self.timeout_secs:
                raise requests.Timeout(f"Timed out waiting for results from {py_request_id}")
            time.sleep(1)

        # Get the results, farm out parsing, return results.
        # TODO: Could use a dispatch table here.
        if model == "alphafold2":
            return self._wait_for_alphafold2(py_request_id)
        if model == "diffdock":
            return self._wait_for_diffdock(py_request_id)
        if model == "esmfold":
            return self._wait_for_esmfold(py_request_id)
        if model == "megamolbart":
            return self._wait_for_megamolbart(py_request_id)
        if model == "openfold":
            return self._wait_for_openfold(py_request_id)
        if model == "protgpt2":
            return self._wait_for_simple_response(py_request_id)
        if model == "moflow":
            return self._wait_for_moflow(py_request_id)
        raise ValueError("Unsupported model " + model)

    def moflow_async(
        self, smi: str, num_samples: int = 1, temperature: float = 0.25, timeout=None,
    ):
        """Request MoFlow inference without waiting for inference results.

        MoFlow is a generative model developed at Cornell University to produce novel molecules given an input seed
        molecule.
        https://arxiv.org/abs/2006.10137
        https://github.com/calvin-zcx/moflow

        Approximate inference duration: <1 second.

        Args:
            smi (str): SMILES molecule sequence. 1 - 512 characters.
            num_samples (int): Number of sampled molecules to be returned as SMILES.
                Minimum value of 1.
            temperature (float): Adjust temperature to control the structural output of MoFlow
                generated molecules. Higher temperature settings generate more complex and diverse
                molecules, while lower values generate more chemical valid compounds. Minimum value
                of 0.2.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        data = {
            "smi": f"{smi}",
            "num_samples": num_samples,
            "temperature": temperature,
        }
        url = f"{self.api_host}/molecule/moflow/generate"
        return self._submit_request("moflow", url, data, None, timeout)

    def _wait_for_moflow(self, py_request_id: RequestId):
        """Wait for results from a call to moflow_async, parse results.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            Dict[List]: A dict with keys "generated_molecules" and "similarity_scores".
                        Each key contains a list of length num_samples.
        """
        status_result = self._wait_for_response(py_request_id)
        #
        # Convert
        #  [
        #      {'generated_molecules':'abc', 'similarity':.9},
        #      {'generated_molecules':'xyz', 'similarity':.8},
        #      etc...
        #  ]
        # to
        #  {
        #      'generated_molecules':['abc', 'xyz'],
        #      'similarity':[.9, .8]
        #  }
        result = json.loads(status_result["response"])[0]
        inverted = {}
        inverted["generated_molecules"] = []
        inverted["similarity_scores"] = []
        for item in result:
            inverted["generated_molecules"].append(item["generated_molecules"])
            inverted["similarity_scores"].append(item["similarity_scores"])
        return inverted

    def moflow_sync(
        self, smi: str, num_samples: int = 1, temperature: float = 0.25, timeout=None,
    ):
        """Request MoFlow inference, wait for the response.

        MoFlow is a generative model developed at Cornell University to produce novel molecules
        given an input seed molecule.
        https://arxiv.org/abs/2006.10137
        https://github.com/calvin-zcx/moflow

        Approximate inference duration: <1 second.

        Args:
            smi (str): SMILES molecule sequence. 1 - 512 characters.
            num_samples (int): Number of sampled molecules to be returned as SMILES.
                Minimum value of 1.
            temperature (float): Adjust temperature to control the structural output of MoFlow
                generated molecules. Higher temperature settings generate more complex and diverse
                molecules, while lower values generate more chemical valid compounds. Minimum value
                of 0.2.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            Dict[List]: A dictionary containing moflow output for the input seed.
                The dictionary has keys "generated_molecules" and "similarity_scores". Each key contains
                a list of length num_samples.
        """
        py_request_id = self.moflow_async(smi, num_samples, temperature, timeout)
        return self._wait_for_moflow(py_request_id)

    def megamolbart_async(
        self, smis: List[str], num_samples: int = 10, scaled_radius: float = 1.0, timeout=None,
    ):
        """Request MegaMolBart inference without waiting for inference results.

        MegaMolBart is a generative model developed by NVIDIA to produce novel small molecules given
        an input seed molecule.
        https://github.com/NVIDIA/MegaMolBART

        Approximate inference duration: 10-60 seconds.

        Args:
            smis (List[str]): List of SMILES strings to use as seeds in novel
                molecule generation. 1 - 512 characters.
            num_samples (int): The number of molecules to generate per seed molecule.
                Minimum value of 1.
            scaled_radius (float): The radius in feature-space from which new molecules
                will be sampled. Minimum value of 1.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        url = f"{self.api_host}/molecule/megamolbart/generate"
        data = {
            "smis": smis,
            "num_samples": num_samples,
            "scaled_radius": scaled_radius,
        }
        return self._submit_request("megamolbart", url, data, None, timeout)

    def _wait_for_megamolbart(
        self, py_request_id: RequestId,
    ):
        """Wait for results from a call to megamolbart_async, parse results.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            List[Dict[List]]: A list of same length as the input "smis" containing the generated molecules.
                Each item in the list is a dict with keys "generated_molecules" and "similarity_scores"
                containing lists of generated SMILES strings and a score of similarity to the seed
                molecule, respectively.
        """
        status_result = self._wait_for_response(py_request_id)
        #
        # Convert
        #  [{'generated_molecules':'abc', 'similarity':.9}, {'generated_molecules':'xyz',
        #                                                    'similarity':.8}}]
        # to
        #  {'generated_molecules':['abc', 'xyz']], 'similarity':[.9, .8]}}
        result = json.loads(status_result["response"])
        transformed_output = []
        for result_per_seed in result:
            inverted = {}
            # Rename "sample" to "generated_molecules" to be consistent with MoFlow
            inverted["generated_molecules"] = []
            inverted["similarity_scores"] = []
            for item in result_per_seed:
                inverted["generated_molecules"].append(item["sample"])
                inverted["similarity_scores"].append(item["similarity_scores"])
            transformed_output.append(inverted)
        return transformed_output

    def megamolbart_sync(
        self, smis: List[str], num_samples: int = 10, scaled_radius: float = 1.0, timeout=None,
    ):
        """Request MegaMolBart inference, wait for the response.

        MegaMolBart is a generative model developed by NVIDIA to produce novel small molecules given
        an input seed molecule.
        https://github.com/NVIDIA/MegaMolBART

        Approximate inference duration: 10-60 seconds.

        Args:
            smis (List[str]): List of SMILES strings to use as seeds in novel
                molecule generation. 1 - 512 characters.
            num_samples (int): The number of molecules to generate per seed molecule.
                Minimum value of 1.
            scaled_radius (float): The radius in feature-space from which new molecules
                will be sampled. Minimum value of 1.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            List[Dict[List]]: A list containing generated molecules for each seed in the input list.
                The output list is of same length as the input "smis" containing the
                generated molecules. Each item in the list is a dict with keys
                "generated_molecules" and "similarity_scores" containing lists of generated
                SMILES strings and a score of similarity to the seed molecule, respectively.
        """
        rqst_id = self.megamolbart_async(smis, num_samples, scaled_radius, timeout)
        return self._wait_for_megamolbart(rqst_id)

    def openfold_async(
        self,
        protein_sequence: str,
        msas: str = None,  # File name from which MSAs are read.
        use_msa: bool = True,
        relax_prediction: bool = False,
        timeout=None,
    ):
        """Request OpenFold inference without waiting for inference results.

        OpenFold is an open source protein structure prediction model, similar in
        feature-set and performance to AlphaFold2.
        https://github.com/aqlaboratory/openfold

        Approximate inference duration: 2-10 minutes.

        Args:
            protein_sequence (str): A string represeting a protein using the
                protein alphabet. 1 to 2000 characters.
            msas (str): Path to multi-sequence alignment (MSA) file in .a3m format.
                If use_msa=True, this file will be uploaded and used during
                protein folding.
            use_msa (bool): If True, the specified msas file will be uploaded and
                used as input to the folding model. If False, MSAs will
                be auto-generated, however this typically yields less
                accurate results.
            relax_prediction (bool): If True, a geometry-relaxation step will be
                applied to the folded output. This is performed
                with a short molecular dynamics simulation.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        url = f"{self.api_host}/protein-structure/openfold/predict"
        data = {}
        files = [
            ("sequence", (None, protein_sequence)),
            ("msas", (msas, open(msas, "rb") if msas else None)),
            ("use_msa", (None, str(use_msa).lower())),
            ("relax_prediction", (None, str(relax_prediction).lower())),
        ]
        return self._submit_request("openfold", url, data, files, timeout)

    def _wait_for_openfold(
        self, py_request_id: RequestId,
    ):
        """Wait for results from a call to openfold_async, parse results.

        Args:
            py_request_id (RequestId): a string wih the format 'modelname:correlation_id'

        Returns:
            str: A string representing the folded protein geometry in Protein Data Bank (PDB) format.
        """
        status_result = self._wait_for_response(py_request_id)
        return json.loads(status_result["response"])["pdbs"][0]

    def openfold_sync(
        self,
        protein_sequence: str,
        msas: str = None,  # Path to MSA file.
        use_msa: bool = True,
        relax_prediction: bool = False,
        timeout=None,
    ):
        """Request OpenFold inference, wait for the response.

        OpenFold is an open source protein structure prediction model, similar in
        feature-set and performance to AlphaFold2.
        https://github.com/aqlaboratory/openfold

        Approximate inference duration: 2-10 minutes.

        Args:
            protein_sequence (str): A string represeting a protein using the
                protein alphabet. 1 to 2000 characters.
            msas (str): Path to multi-sequence alignment (MSA) file in .a3m format.
                If use_msa=True, this file will be uploaded and used during
                protein folding.
            use_msa (bool): If True, the specified msas file will be uploaded and
                used as input to the folding model. If False, MSAs will
                be auto-generated, however this typically yields less
                accurate results.
            relax_prediction (bool): If True, a geometry-relaxation step will be
                applied to the folded output. This is performed
                with a short molecular dynamics simulation.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            str: A string representing the folded protein geometry in Protein Data Bank (PDB) format.
        """
        rqst_id = self.openfold_async(protein_sequence, msas, use_msa, relax_prediction, timeout)
        return self._wait_for_openfold(rqst_id)

    def alphafold2_async(
        self,
        protein_sequence: str,
        msas: str = None,
        use_msa: bool = True,
        relax_prediction: bool = False,
        timeout=None,
    ):
        """Request AlphaFold2 inference, without waiting for inference results.

        AlphaFold2 is the second generation protein folding model developed by
        DeepMind.
        https://www.nature.com/articles/s41586-021-03819-2
        https://github.com/deepmind/alphafold

        Approximate inference duration: 5-30 minutes.

        Args:
            protein_sequence (str): A string represeting a protein using the
                protein alphabet. 1 to 3000 characters.
            msas (str): Path to multi-sequence alignment (MSA) file in .a3m format.
                If use_msa=True, this file will be uploaded and used during
                protein folding.
            use_msa (bool): If True, the specified msas file will be uploaded and
                used as input to the folding model. If False, MSAs will
                be auto-generated, however this typically yields less
                accurate results.
            relax_prediction (bool): If True, a geometry-relaxation step will be
                applied to the folded output. This is performed
                with a short molecular dynamics simulation.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        url = f"{self.api_host}/protein-structure/alphafold2/predict"
        data = {}
        files = [
            ("sequence", (None, protein_sequence)),
            ("msas", (msas, open(msas, "rb") if msas else None)),
            ("use_msa", (None, str(use_msa).lower())),
            ("relax_prediction", (None, str(relax_prediction).lower())),
        ]
        return self._submit_request("alphafold2", url, data, files, timeout)

    def _wait_for_alphafold2(
        self, py_request_id: RequestId,
    ):
        """Wait for results from a call to alphafold2_async, parse results.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            str: A string representing the folded protein geometry in Protein Data Bank (PDB) format.
        """
        status_result = self._wait_for_response(py_request_id)
        return json.loads(status_result["response"])["pdbs"][0]

    def alphafold2_sync(
        self,
        protein_sequence: str,
        msas: str = None,  # Path to MSA file.
        use_msa: bool = True,
        relax_prediction: bool = False,
        timeout=None,
    ):
        """Request AlphaFold2 inference, wait for the response.

        AlphaFold2 is the second generation protein folding model developed by
        DeepMind.
        https://www.nature.com/articles/s41586-021-03819-2
        https://github.com/deepmind/alphafold

        Approximate inference duration: 5-30 minutes.

        Args:
            protein_sequence (str): A string represeting a protein using the
                protein alphabet. 1 to 3000 characters.
            msas (str): Path to multi-sequence alignment (MSA) file in .a3m format.
                If use_msa=True, this file will be uploaded and used during
                protein folding.
            use_msa (bool): If True, the specified msas file will be uploaded and
                used as input to the folding model. If False, MSAs will
                be auto-generated, however this typically yields less
                accurate results.
            relax_prediction (bool): If True, a geometry-relaxation step will be
                applied to the folded output. This is performed
                with a short molecular dynamics simulation.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            str: A string representing the folded protein geometry in Protein Data Bank (PDB) format.
        """
        rqst_id = self.alphafold2_async(protein_sequence, msas, use_msa, relax_prediction, timeout)
        return self._wait_for_alphafold2(rqst_id)

    def esmfold_async(
        self, protein_sequence: str, timeout=None,
    ):
        """Request ESMFold inference, without waiting for inference results.

        Evolutionary Scale Modeling (ESM) Fold is a protein structure predictor developed
        by Facebook AI Research.
        https://github.com/facebookresearch/esm#esmfold

        Approximate inference time: 5-10 seconds.

        Args:
            protein_sequence (str): A string represeting a protein using the
                protein alphabet. 1 to 1024 characters.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        url = f"{self.api_host}/protein-structure/esmfold/predict-no-aln"
        data = {
            "sequence": f"{protein_sequence}",
        }
        return self._submit_request("esmfold", url, data, None, timeout)

    def _wait_for_esmfold(
        self, py_request_id: RequestId,
    ):
        """Wait for results from a call to esmfold_async, parse results.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            str: A string representing the folded protein geometry in Protein Data Bank (PDB) format.
        """
        status_result = self._wait_for_response(py_request_id)
        return json.loads(status_result["response"])["pdbs"][0]

    def esmfold_sync(
        self, protein_sequence: str, timeout=None,
    ):
        """Request ESMFold inference, wait for the response.

        Evolutionary Scale Modeling (ESM) Fold is a protein structure predictor developed
        by Facebook AI Research.
        https://github.com/facebookresearch/esm#esmfold

        Approximate inference time: 5-10 seconds.

        Args:
            protein_sequence (str): A string represeting a protein using the
                protein alphabet. 1 to 1024 characters.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            str: A strig representing the folded protein geometry in Protein Data Bank (PDB) format.
        """
        rqst_id = self.esmfold_async(protein_sequence, timeout)
        return self._wait_for_esmfold(rqst_id)

    def protgpt2_async(
        self,
        max_length: int = 150,
        top_k: int = 950,
        repetition_penalty: float = 1.2,
        num_return_sequences: int = 10,
        percent_to_keep: float = 0.1,
        timeout=None,
    ):
        """Request ProtGPT2 inference, without waiting for inference results.

        ProtGPT2 is a protein sequence generator developed by the University of Bayreuth.
        https://www.nature.com/articles/s41467-022-32007-7
        https://huggingface.co/nferruz/ProtGPT2

        Approximate inference time: 5-120 seconds.

        Args:
            max_length (int): Maximum number of tokens to generate. As tokens comprise an average of 3 to 4
                amino acids, the resulting protein sequences will be longer than max_length in terms of number
                of amino acids.
            top_k (int): Sampling of the k most probable tokens from the vocabulary as a decoding mechanism.
                repetition_penalty (float): Penalty to avoid repeats when random sampling at decoding.
                Recommended range is 1.1 to 1.3.
            num_return_sequences (int): Number of protein sequences to be returned in the API’s response.
            percent_to_keep (float, 0-1): The API's response contains only the sequences with the
                top percent_to_keep perplexities. If this value is < 1.0, sequences will be
                generated iteratively until num_return_sequences and percent_to_keep are satisfied.
                This can result in longer runtimes. A value of 1.0 means bypassing this perplexity filter
                and hence a faster response.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        url = f"{self.api_host}/protein-sequence/protgpt2/generate"
        data = {
            "max_length": max_length,
            "top_k": top_k,
            "repetition_penalty": repetition_penalty,
            "num_return_sequences": num_return_sequences,
            "percent_to_keep": percent_to_keep,
        }
        return self._submit_request("protgpt2", url, data, None, timeout)

    def _wait_for_simple_response(self, py_request_id: RequestId):
        """Wait for results from the service, parse results.

        This function just loads the returned json object and returns the response.
        protgpt2 and diffdock use this kind of simple output unwrapping.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            dict: A dictionary containing generated amino acid sequences and their perplexities.
        """
        status_result = self._wait_for_response(py_request_id)
        return json.loads(status_result["response"])

    def protgpt2_sync(
        self,
        max_length: int = 150,
        top_k: int = 950,
        repetition_penalty: float = 1.2,
        num_return_sequences: int = 10,
        percent_to_keep: float = 0.1,
        timeout=None,
    ):
        """Request ProtGPT2 inference, wait for the response.

        ProtGPT2 is a protein sequence generator developed by the University of Bayreuth.
        https://www.nature.com/articles/s41467-022-32007-7
        https://huggingface.co/nferruz/ProtGPT2

        Approximate inference time: 5-120 seconds.

        Args:
            max_length (int): Maximum number of tokens to generate. As tokens comprise an average of 3 to 4
                amino acids, the resulting protein sequences will be longer than max_length in terms of number
                of amino acids.
            top_k (int): Sampling of the k most probable tokens from the vocabulary as a decoding mechanism.
                repetition_penalty (float): Penalty to avoid repeats when random sampling at decoding.
                Recommended range is 1.1 to 1.3.
            num_return_sequences (int): Number of protein sequences to be returned in the API’s response.
            percent_to_keep (float, 0-1): The API's response contains only the sequences with the
                top percent_to_keep perplexities. If this value is < 1.0, sequences will be
                generated iteratively until num_return_sequences and percent_to_keep are satisfied.
                This can result in longer runtimes. A value of 1.0 means bypassing this perplexity filter
                and hence a faster response.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            Dict: A dictionary containing generated amino acid sequences and their perplexities.
        """
        rqst_id = self.protgpt2_async(
            max_length, top_k, repetition_penalty, num_return_sequences, percent_to_keep, timeout,
        )
        # For protgpt2 and diffdock, we just load the reponse.
        return self._wait_for_simple_response(rqst_id)

    def diffdock_async(
        self,
        ligand_file: str,
        protein_file: str,
        poses_to_generate: int = 20,
        diffusion_time_divisions: int = 20,
        diffusion_steps: int = 18,
        save_diffusion_trajectory: bool = False,
        timeout=None,
    ):
        """Request DiffDock inference without waiting for inference results.

        DiffDock performs ligand-protein docking, generating multiple possible
        poses and their confidence values. The model was developed at MIT.
        https://github.com/gcorso/DiffDock

        Approximate inference time: 5-30 seconds.

        Args:
            ligand_file (str): Path to small molecule/ligand file containing geometry in
                Structure-Data file (SD File) format. Maximum filesize is 5 MB.
            protein_file (str): Path to protein geometry in Protein Databank (PDB) format.
                Maximum filesize is 10 MB.
            poses_to_generate (int): number of docking poses to generate. Value range 1-100.
            diffusion_time_divisions (int): The number of discrete time divisions in the
                diffusion process. Value range 1-100.
            diffusion_steps (int): The number of steps to take along the discrete time
                divisions. This must be no greater than diffusion_time_divisions. Value range
                1-100.
            save_diffusion_trajectory (bool): If True, the inference output will contain a
                key entry "visualizations_files" that contains a string with a continuous
                list of PDB atom coordinates, depicting the reverse ligand diffusion during
                inference.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            RequestId: An object used to track the inference request.
                The RequestId contains the model name, correlation ID and other information related
                to this request. It can be used to interact with the task at a later time.
        """
        url = f"{self.api_host}/molecular-docking/diffdock/generate"
        self._setup_headers()
        data = {}
        files = {
            "ligand_file_bytes": open(ligand_file, "rb"),
            "protein_file_bytes": open(protein_file, "rb"),
            "poses_to_generate": (None, poses_to_generate),
            "diffusion_time_divisions": (None, diffusion_time_divisions),
            "diffusion_steps": (None, diffusion_steps),
            "save_diffusion_trajectory": (None, str(save_diffusion_trajectory).lower()),
        }
        return self._submit_request("diffdock", url, data, files, timeout)

    def _wait_for_diffdock(
        self, py_request_id: RequestId,
    ):
        """Wait for results from a call to diffdock_async, parse results.

        Args:
            py_request_id (RequestId): Everything we know about this request.

        Returns:
            dict: A dictionary containing lists of docked positions and confidences.
        """
        status_result = self._wait_for_response(py_request_id)
        return json.loads(status_result["response"])

    def diffdock_sync(
        self,
        ligand_file: str,
        protein_file: str,
        poses_to_generate: int = 20,
        diffusion_time_divisions: int = 20,
        diffusion_steps: int = 18,
        save_diffusion_trajectory: bool = False,
        timeout=None,
    ):
        """Request DiffDock inference, wait for the response.

        DiffDock performs ligand-protein docking, generating multiple possible
        poses and their confidence values. The model was developed at MIT.
        https://github.com/gcorso/DiffDock

        Approximate inference time: 5-30 seconds.

        Args:
            ligand_file (str): Path to small molecule/ligand file containing geometry in
                Structure-Data file (SD File) format. Maximum filesize is 5 MB.
            protein_file (str): Path to protein geometry in Protein Databank (PDB) format.
                Maximum filesize is 10 MB.
            poses_to_generate (int): number of docking poses to generate. Value range 1-100.
            diffusion_time_divisions (int): The number of discrete time divisions in the
                diffusion process. Value range 1-100.
            diffusion_steps (int): The number of steps to take along the discrete time
                divisions. This must be no greater than diffusion_time_divisions. Value range
                1-100.
            save_diffusion_trajectory (bool): If True, the inference output will contain a
                key entry "visualizations_files" that contains a string with a continuous
                list of PDB atom coordinates, depicting the reverse ligand diffusion during
                inference.
            timeout (int): The timeout duration in seconds. If None, the default timeout
                set during construction will be used. A timeout results in a
                requests.exceptions.Timeout exception.

        Returns:
            Dict: A dictionary containing lists of docked positions and confidences.
        """
        rqst_id = self.diffdock_async(
            ligand_file,
            protein_file,
            poses_to_generate,
            diffusion_time_divisions,
            diffusion_steps,
            save_diffusion_trajectory,
            timeout,
        )
        return self._wait_for_simple_response(rqst_id)

    #
    # Utilities
    #
    def fetch_tasks(self, number_of_tasks: int = 10):
        """Get all available information for the 'N' most recent tasks.

        Args:
            number_of_tasks (int): Number of tasks to retrieve.

        Returns:
            List[Dict] : A list of tasks recently submitted by the user, each with a dict of
                         details about the task status.
        """
        if number_of_tasks <= 0:
            raise IncorrectParamsError(
                status_code=http.HTTPStatus.BAD_REQUEST,
                reason=f"Number of tasks was {number_of_tasks}, it must be > 0",
                decoded_content="",
            )

        url = f"{self.api_host}/tasks?source=api&limit={number_of_tasks}"
        headers = self._setup_headers()
        response = requests.get(url, headers=headers)
        response_handler.ResponseHandler.handle_response(response)
        tasks = json.loads(response.content)["tasks"]
        return tasks

    def fetch_task_status(self, py_request_id: Union[str, RequestId]):
        """Get information for a specific task.

        Args:
            py_request_id (str or RequestId): The inference task of interest.

        Returns:
            str: A string representing the task state, one of 'DONE', 'CREATED', 'PROCESSING', 'ERROR'
        """
        url = self._form_url(py_request_id, "task")
        headers = self._setup_headers()
        response = requests.get(url, headers=headers)
        response_handler.ResponseHandler.handle_response(response)
        content = json.loads(response.content)["control_info"]["status"]
        if isinstance(py_request_id, RequestId):
            py_request_id.status = content
        return content

    def delete_task(self, py_request_id: Union[str, RequestId]):
        """Delete the given task.

        Args:
            py_request_id (str or RequestId): The inference task of interest.

        Returns:
            str: a status confirmation the task was deleted.
        """
        url = self._form_url(py_request_id, "task")
        headers = self._setup_headers()
        response = requests.delete(url, headers=headers)
        response_handler.ResponseHandler.handle_response(response)
        return json.loads(response.content)

    def cancel_task(self, py_request_id: Union[str, RequestId]):
        """Cancel a task.

        Args:
            py_request_id (str or RequestId): The correlation_id.

        Returns:
            str: a status confirmation the task was cancelled.
        """
        url = self._form_url(py_request_id, "cancel")
        headers = self._setup_headers()
        response = requests.put(url, headers=headers)
        return json.loads(response.content)

    def _form_url(self, py_request_id: Union[str, RequestId], endpoint: str):
        """ Form a 'task manipulation' URL.
        Args:
            py_request_id (str or RequestId): The correlation ID.
            endpoint: What we need to talk to.
        """
        if not endpoint.isalpha():
            raise Exception(f"Invalid endpoint ->{endpoint}<-")
        if isinstance(py_request_id, RequestId):
            url = f"{self.api_host}/{endpoint}/{py_request_id.correlation_id}"
        elif isinstance(py_request_id, str):
            url = f"{self.api_host}/{endpoint}/{py_request_id}"
        else:
            raise BadRequestId(type(py_request_id))
        return url

    @staticmethod
    def _decode_embedding_response(byte_data, data_format=Literal["npz", "h5"]):
        """Decode a binary model output.

        Given a binary zip file in byte_data whose entries are numpy arrays,
        extract its contents & return a map from each 'filename' to the corresponding
        NumPy array.

        Args:
            byte_data (bytes (build-in python): embedding byte data to decode
            data_format (str): what data type is represented in the byte data

        Returns:
            List[Dict[np.array]] The decoded payload.
                A dict is used for the various properties that may be returned (e.g. "embeddings",
                "tokens"...), and List in which each entry is an embeddings (np.array). A List of dicts is
                used rather than a 2D np.array because
                    a) To clearly indicate that the first index relates to different
                       input/output pairs
                    b) To allow variable length responses per array, which we need to
                       de-pad ESM2.

        Raises:
            ValueError: If `data_format` is not supported.
        """
        file_like_obj = io.BytesIO(byte_data)
        if data_format == "npz":
            payload = np.load(file_like_obj)
        elif data_format == "h5":
            payload = h5.File(file_like_obj)
        else:
            raise ValueError(f"Unsupported response data format: {data_format}")
        # Get any value. There is an assumption all values are arrays of equal length.
        length = len(next(iter(payload.values())))
        # Return a list-of-dicts
        result_list = [{key: payload[key][i] for key in payload.keys()} for i in range(length)]
        return result_list
