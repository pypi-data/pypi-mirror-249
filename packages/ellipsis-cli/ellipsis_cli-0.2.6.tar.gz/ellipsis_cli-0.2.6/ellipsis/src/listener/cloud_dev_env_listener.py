import os
import shlex
import subprocess


from diff_match_patch import diff_match_patch
from fastapi import FastAPI
from loguru import logger

from ellipsis.src.models.workspaces.command import CommandOutput
from ellipsis.src.models.workspaces.constants import (
    HEALTH_CHECK_URL_ROUTE,
    READ_FILE_URL_ROUTE,
    RUN_COMMAND_URL_ROUTE,
    WRITE_FILE_URL_ROUTE,
)
from ellipsis.src.models.workspaces.models import (
    FileChangeRequest,
    FileChangeResponse,
    FileReadRequest,
    FileReadResponse,
    FileWriteRequest,
    FileWriteResponse,
    RunCommandRequest,
    RunCommandResponse,
)


class CloudDevEnvListener:
    
    def __init__(self, repo_root: str):
        # Get the absolute path of the repository root
        repo_root = os.path.abspath(repo_root)
        self.repo_root = repo_root
        os.chdir(self.repo_root)
        logger.info(f"Listener initialized with repo root: {self.repo_root}")


    def create_fastapi_app(self):
        app = FastAPI()

        @app.get(HEALTH_CHECK_URL_ROUTE)
        async def health_check():
            return {
                "ok": True,
                'directory': self.repo_root,
                'pid': os.getpid(),
            }

        @app.post(READ_FILE_URL_ROUTE, response_model=FileReadResponse)
        async def read_file(req: FileReadRequest):
            effective_file_path = os.path.join(self.repo_root, req.path)
            if not os.path.exists(effective_file_path):
                logger.debug(f"File '{effective_file_path}' does not exist.")
                return FileReadResponse(contents=None)
            with open(effective_file_path, "r") as f:
                logger.debug(f"Found file at '{effective_file_path}'")
                contents = f.read()
                return FileReadResponse(contents=contents)

        @app.post(WRITE_FILE_URL_ROUTE, response_model=FileWriteResponse)
        async def write_file(req: FileWriteRequest):
            effective_file_path = os.path.join(self.repo_root, req.path)
            if not os.path.exists(effective_file_path):
                logger.info(f"File '{req.path}' does not exist, creating it.")
                os.makedirs(os.path.dirname(effective_file_path), exist_ok=True)
                with open(effective_file_path, "w") as f:
                    f.write("")
            with open(effective_file_path, "w") as f:
                f.write(req.contents)
            logger.info(f"File '{req.path}' updated successfully.")
            return FileWriteResponse()

        @app.post(RUN_COMMAND_URL_ROUTE, response_model=RunCommandResponse)
        async def run_command(req: RunCommandRequest):
            split_cmd = shlex.split(req.command_str)
            logger.debug(f"Running cmd from {self.repo_root}: $ {req.command_str}")
            result = subprocess.run(
                split_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            output = result.stdout
            return RunCommandResponse(
                ok=True,
                req=req,
                output=CommandOutput(
                    exit_code=result.returncode,
                    all_output=output,
                ),
            )

        # TODO this isn't working yet
        # @app.websocket(EVENTS_URL_ROUTE)
        # async def websocket_endpoint(websocket: WebSocket):
        #     n_events = 0
        #     await websocket.accept()
        #     try:
        #         while True:
        #             msg = await websocket.receive_text()
        #             n_events += 1
        #             if msg.lower() == "close":
        #                 await websocket.close()
        #                 break
        #             else:
        #                 try:
        #                     event_json = json.loads(msg)
        #                 except json.JSONDecodeError:
        #                     logger.error(f"Failed to parse JSON: {msg}")
        #                     await websocket.send_json(
        #                         RejectedResponse(
        #                             ok=False, reason=f"Failed to parse JSON: {msg}"
        #                         )
        #                     )
        #                     continue
        #                 req = BaseWorkspaceRequest.parse_obj(event_json)
        #                 if req.request_type == WorkspaceRequestType.FILE_CHANGE:
        #                     change_file_event: FileChangeRequest = (
        #                         FileChangeRequest.parse_obj(event_json)
        #                     )
        #                     await websocket.send_json(
        #                         self._handle_FileChangeRequest(change_file_event)
        #                     )
        #                 elif req.request_type == WorkspaceRequestType.RUN_COMMAND:
        #                     pass
        #                     # run_command_event: RunCommandRequest = (
        #                     #     RunCommandRequest.parse_obj(event_json)
        #                     # )
        #                     # await websocket.send_json(
        #                     #     self._handle_RunCommandRequest(run_command_event)
        #                     # )
        #                 else:
        #                     logger.info(
        #                         f"Event type {req.request_type} is not supported: {event_json}"
        #                     )
        #                     await websocket.send_json(
        #                         RejectedResponse(
        #                             ok=False,
        #                             reason=f"Event type {req.request_type} is not supported",
        #                         )
        #                     )
        #     except WebSocketDisconnect:
        #         logger.warning(f"Server disconnected after {n_events} events")

        return app

    def _handle_FileChangeRequest(self, e: FileChangeRequest) -> FileChangeResponse:
        effective_file_path = os.path.join(self.repo_root, e.path)
        if not os.path.exists(effective_file_path):
            logger.info(f"File {e.path} does not exist, creating it.")
            os.makedirs(os.path.dirname(effective_file_path), exist_ok=True)
            with open(effective_file_path, "w") as f:
                f.write("")
        with open(effective_file_path, "r") as f:
            text = f.read()
        dmp = diff_match_patch()
        patches = dmp.patch_fromText(e.diff)
        new_text, _ = dmp.patch_apply(patches, text)

        with open(effective_file_path, "w") as f:
            f.write(new_text)
        logger.info(f"File {e.path} updated successfully.")
        return FileChangeResponse(
            ok=True,
            req=e,
        )

    # TODO(nick) how to get stdout and stderr simultaneously?
    # def _handle_RunCommandRequest(
    #     self, event: RunCommandRequest
    # ) -> RunCommandResponse | RejectedResponse:
    #     """
    #     Runs a command and returns the response.
    #     """
    #     pwd = self.repo_root
    #     logger.info(f"Running command '{event.command_str}' in {pwd}")
    #     os.chdir(pwd)
    #     try:
    #         completed_process = run(event.command_str, shell=True, check=True)
    #     except CalledProcessError as err:
    #         logger.warning(f"Command '{event.command_str}' failed.")
    #         return RejectedResponse(
    #             ok=False, reason=f"Command '{event.command_str}' failed: {err}"
    #         )
    #     return RunCommandResponse(
    #         ok=True,
    #         req=event,
    #         output=CommandOutput(
    #             exit_code=completed_process.returncode,
    #             all_output="", # TODO
    #             stdout=str(completed_process.stdout)
    #             if completed_process.stdout
    #             else None,
    #             stderr=str(completed_process.stderr)
    #             if completed_process.stderr
    #             else None,
    #         ),
    #     )
    