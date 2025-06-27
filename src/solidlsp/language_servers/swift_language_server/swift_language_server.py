"""
Provides Swift specific instantiation of the LanguageServer class. Contains various configurations and settings specific to Swift.
"""

import logging
import os
import pathlib
import re
import threading

from overrides import override

from solidlsp.ls import SolidLanguageServer
from solidlsp.ls_config import LanguageServerConfig
from solidlsp.ls_logger import LanguageServerLogger
from solidlsp.lsp_protocol_handler.lsp_types import InitializeParams
from solidlsp.lsp_protocol_handler.server import ProcessLaunchInfo


class SwiftLanguageServer(SolidLanguageServer):
    """
    Provides Swift specific instantiation of the LanguageServer class using SourceKit-LSP.
    Contains various configurations and settings specific to Swift.
    """

    def __init__(self, config: LanguageServerConfig, logger: LanguageServerLogger, repository_root_path: str):
        """
        Creates a SwiftServer instance. This class is not meant to be instantiated directly.
        Use LanguageServer.create() instead.
        """
        super().__init__(
            config,
            logger,
            repository_root_path,
            # SourceKit-LSP is the official Swift Language Server Protocol implementation
            ProcessLaunchInfo(cmd="sourcekit-lsp", cwd=repository_root_path),
            "swift",
        )

        # Event to signal when initial workspace analysis is complete
        self.analysis_complete = threading.Event()
        self.found_source_files = False

    @override
    def is_ignored_dirname(self, dirname: str) -> bool:
        return super().is_ignored_dirname(dirname) or dirname in [
            ".build",
            ".swiftpm",
            "build",
            "DerivedData",
            ".DS_Store",
            "xcuserdata",
            "*.xcworkspace",
            "*.xcodeproj",
        ]

    def _get_initialize_params(self, repository_absolute_path: str) -> InitializeParams:
        """
        Returns the initialize params for the SourceKit-LSP Language Server.
        """
        # Create basic initialization parameters
        initialize_params: InitializeParams = {  # type: ignore
            "processId": os.getpid(),
            "rootPath": repository_absolute_path,
            "rootUri": pathlib.Path(repository_absolute_path).as_uri(),
            "initializationOptions": {
                # SourceKit-LSP specific configuration
                "fallbackBuildSystem": "swiftpm",
                "backgroundIndexing": True,
                "completion": {"maxResults": 200, "serverSideFiltering": True},
            },
            "capabilities": {
                "workspace": {
                    "applyEdit": True,
                    "workspaceEdit": {"documentChanges": True},
                    "didChangeConfiguration": {"dynamicRegistration": True},
                    "didChangeWatchedFiles": {"dynamicRegistration": True},
                    "symbol": {
                        "dynamicRegistration": True,
                        "symbolKind": {
                            "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
                        },
                    },
                    "executeCommand": {"dynamicRegistration": True},
                    "workspaceFolders": True,
                    "configuration": True,
                },
                "textDocument": {
                    "synchronization": {"dynamicRegistration": True, "willSave": True, "willSaveWaitUntil": True, "didSave": True},
                    "completion": {
                        "dynamicRegistration": True,
                        "contextSupport": True,
                        "completionItem": {
                            "snippetSupport": True,
                            "commitCharactersSupport": True,
                            "documentationFormat": ["markdown", "plaintext"],
                            "deprecatedSupport": True,
                            "preselectSupport": True,
                            "tagSupport": {"valueSet": [1, 2]},
                            "insertReplaceSupport": True,
                            "resolveSupport": {"properties": ["documentation", "detail", "additionalTextEdits"]},
                        },
                        "completionItemKind": {
                            "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
                        },
                        "insertTextMode": 2,
                    },
                    "hover": {"dynamicRegistration": True, "contentFormat": ["markdown", "plaintext"]},
                    "signatureHelp": {
                        "dynamicRegistration": True,
                        "signatureInformation": {
                            "documentationFormat": ["markdown", "plaintext"],
                            "parameterInformation": {"labelOffsetSupport": True},
                            "activeParameterSupport": True,
                        },
                        "contextSupport": True,
                    },
                    "definition": {"dynamicRegistration": True, "linkSupport": True},
                    "references": {"dynamicRegistration": True},
                    "documentHighlight": {"dynamicRegistration": True},
                    "documentSymbol": {
                        "dynamicRegistration": True,
                        "symbolKind": {
                            "valueSet": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
                        },
                        "hierarchicalDocumentSymbolSupport": True,
                        "tagSupport": {"valueSet": [1, 2]},
                    },
                    "codeAction": {
                        "dynamicRegistration": True,
                        "isPreferredSupport": True,
                        "disabledSupport": True,
                        "dataSupport": True,
                        "codeActionLiteralSupport": {
                            "codeActionKind": {
                                "valueSet": [
                                    "",
                                    "quickfix",
                                    "refactor",
                                    "refactor.extract",
                                    "refactor.inline",
                                    "refactor.rewrite",
                                    "source",
                                    "source.organizeImports",
                                    "source.fixAll",
                                ]
                            }
                        },
                        "resolveSupport": {"properties": ["edit"]},
                    },
                    "codeLens": {"dynamicRegistration": True},
                    "formatting": {"dynamicRegistration": True},
                    "rangeFormatting": {"dynamicRegistration": True},
                    "onTypeFormatting": {"dynamicRegistration": True},
                    "rename": {"dynamicRegistration": True, "prepareSupport": True},
                    "foldingRange": {
                        "dynamicRegistration": True,
                        "rangeLimit": 5000,
                        "lineFoldingOnly": True,
                    },
                    "selectionRange": {"dynamicRegistration": True},
                    "publishDiagnostics": {
                        "relatedInformation": True,
                        "versionSupport": False,
                        "tagSupport": {"valueSet": [1, 2]},
                        "codeDescriptionSupport": True,
                        "dataSupport": True,
                    },
                    "callHierarchy": {"dynamicRegistration": True},
                    "semanticTokens": {
                        "dynamicRegistration": True,
                        "tokenTypes": [
                            "namespace",
                            "type",
                            "class",
                            "enum",
                            "interface",
                            "struct",
                            "typeParameter",
                            "parameter",
                            "variable",
                            "property",
                            "enumMember",
                            "event",
                            "function",
                            "method",
                            "macro",
                            "keyword",
                            "modifier",
                            "comment",
                            "string",
                            "number",
                            "regexp",
                            "operator",
                        ],
                        "tokenModifiers": [
                            "declaration",
                            "definition",
                            "readonly",
                            "static",
                            "deprecated",
                            "abstract",
                            "async",
                            "modification",
                            "documentation",
                            "defaultLibrary",
                        ],
                        "formats": ["relative"],
                        "requests": {"range": True, "full": {"delta": True}},
                    },
                },
                "window": {
                    "workDoneProgress": True,
                    "showMessage": {"messageActionItem": {"additionalPropertiesSupport": True}},
                    "showDocument": {"support": True},
                },
                "general": {
                    "regularExpressions": {"engine": "ECMAScript"},
                    "markdown": {"parser": "marked", "version": "1.1.0"},
                },
            },
            "workspaceFolders": [
                {"uri": pathlib.Path(repository_absolute_path).as_uri(), "name": os.path.basename(repository_absolute_path)}
            ],
        }

        return initialize_params

    def _start_server(self):
        """
        Starts the SourceKit-LSP Language Server and waits for initial workspace analysis to complete.

        This prevents zombie processes by ensuring SourceKit-LSP has finished its initial background
        tasks before we consider the server ready.

        Usage:
        ```
        async with lsp.start_server():
            # LanguageServer has been initialized and workspace analysis is complete
            await lsp.request_definition(...)
            await lsp.request_references(...)
            # Shutdown the LanguageServer on exit from scope
        # LanguageServer has been shutdown cleanly
        ```
        """

        def execute_client_command_handler(params):
            return []

        def do_nothing(params):
            return

        def window_log_message(msg):
            """
            Monitor SourceKit-LSP's log messages to detect when initial analysis is complete.
            """
            message_text = msg.get("message", "")
            self.logger.log(f"LSP: window/logMessage: {message_text}", logging.INFO)

            # SourceKit-LSP may log various indexing completion messages
            if any(
                keyword in message_text.lower()
                for keyword in [
                    "indexing complete",
                    "finished indexing",
                    "build complete",
                    "compilation finished",
                    "swift package resolved",
                ]
            ):
                self.logger.log("SourceKit-LSP workspace analysis complete", logging.INFO)
                self.found_source_files = True
                self.analysis_complete.set()
                self.completions_available.set()

        def window_show_message(msg):
            """
            Handle window/showMessage notifications from SourceKit-LSP
            """
            message_text = msg.get("message", "")
            message_type = msg.get("type", 1)  # 1=Error, 2=Warning, 3=Info, 4=Log

            self.logger.log(f"LSP: window/showMessage (type={message_type}): {message_text}", logging.INFO)

            # Look for Swift package resolution or build completion messages
            if any(keyword in message_text.lower() for keyword in ["package resolution complete", "build succeeded", "indexing finished"]):
                self.logger.log("SourceKit-LSP analysis detected via showMessage", logging.INFO)
                if not self.found_source_files:
                    self.found_source_files = True
                    self.analysis_complete.set()
                    self.completions_available.set()

        def progress_notification(params):
            """
            Handle $/progress notifications which may indicate build/indexing progress
            """
            value = params.get("value", {})
            kind = value.get("kind", "")
            message = value.get("message", "")

            if kind == "end" and any(keyword in message.lower() for keyword in ["indexing", "building", "resolving"]):
                self.logger.log(f"SourceKit-LSP progress end: {message}", logging.INFO)
                if not self.found_source_files:
                    self.found_source_files = True
                    self.analysis_complete.set()
                    self.completions_available.set()

        def workspace_configuration_handler(params):
            """
            Handle workspace/configuration requests from SourceKit-LSP
            """
            # Return empty configuration for now
            return [{}] * len(params.get("items", []))

        # Set up notification handlers
        self.server.on_request("client/registerCapability", do_nothing)
        self.server.on_notification("window/logMessage", window_log_message)
        self.server.on_notification("window/showMessage", window_show_message)
        self.server.on_request("workspace/executeClientCommand", execute_client_command_handler)
        self.server.on_request("workspace/configuration", workspace_configuration_handler)
        self.server.on_notification("$/progress", progress_notification)
        self.server.on_notification("textDocument/publishDiagnostics", do_nothing)

        self.logger.log("Starting sourcekit-lsp server process", logging.INFO)
        self.server.start()

        # Send proper initialization parameters
        initialize_params = self._get_initialize_params(self.repository_root_path)

        self.logger.log(
            "Sending initialize request from LSP client to SourceKit-LSP server and awaiting response",
            logging.INFO,
        )
        init_response = self.server.send.initialize(initialize_params)
        self.logger.log(f"Received initialize response from SourceKit-LSP server: {init_response}", logging.INFO)

        # Verify that the server supports our required features
        capabilities = init_response.get("capabilities", {})
        assert "textDocumentSync" in capabilities, "SourceKit-LSP must support textDocumentSync"

        # SourceKit-LSP may not always provide completionProvider in capabilities
        # but it does support completion, so we'll be more lenient here
        if "completionProvider" not in capabilities:
            self.logger.log("Warning: SourceKit-LSP did not advertise completionProvider capability", logging.WARNING)

        # Check for definition support
        if "definitionProvider" not in capabilities:
            self.logger.log("Warning: SourceKit-LSP did not advertise definitionProvider capability", logging.WARNING)

        # Complete the initialization handshake
        self.server.notify.initialized({})

        # Wait for SourceKit-LSP to complete its initial workspace analysis
        # This prevents zombie processes by ensuring background tasks finish
        self.logger.log("Waiting for SourceKit-LSP to complete initial workspace analysis...", logging.INFO)

        # SourceKit-LSP might take longer to analyze Swift packages, so increase timeout
        timeout = 15.0
        if self.analysis_complete.wait(timeout=timeout):
            self.logger.log("SourceKit-LSP initial analysis complete, server ready", logging.INFO)
        else:
            self.logger.log(f"Timeout ({timeout}s) waiting for SourceKit-LSP analysis completion, proceeding anyway", logging.WARNING)
            # Fallback: assume analysis is complete after timeout
            self.analysis_complete.set()
            self.completions_available.set()
