"""Callback Handler that writes to a file."""
from typing import Any, Dict, Optional, TextIO, cast, List, Generator
import uuid, os

from langchain_core.agents import AgentAction, AgentFinish
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.openai_info import OpenAICallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.tracers.context import register_configure_hook
from contextvars import ContextVar
from datetime import datetime

from contextlib import contextmanager
from coevalogger.utils.text_print import print_text
from coevalogger.utils.openai_info import standardize_model_name, get_openai_token_cost_for_model, MODEL_COST_PER_1K_TOKENS

class CoevalLogger(BaseCallbackHandler):
    """Callback Handler that writes to a file."""

    def __init__(
        self, filename: str, mode: str = "a", color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Initialize callback handler."""
        if not filename:
            self.file = None
        else:
            if os.path.exists(filename):
                # remove the existing content
                open(filename, 'w').close()
            self.file = cast(TextIO, open(filename, mode, encoding="utf-8"))

        self.color = color
        self.session_id = uuid.uuid1().int
        self.app_key = kwargs.get("app_key", {})
        self.user_info = kwargs.get("user_info", {})
        self.version_tags = kwargs.get("version_tags", [])
        self.turns = kwargs.get("turns", 0)
        self.total_tokens = kwargs.get("total_tokens", 0)
        self.prompt_tokens = kwargs.get("prompt_tokens", 0)
        self.completion_tokens = kwargs.get("completion_tokens", 0)
        self.total_cost = kwargs.get("total_cost", 0)
        self.dialogue_history = kwargs.get("dialogue_history", [])
        self.turn_info = {
            "turn_token_usage": 0,
            "turn_cost": 0,
            "prompts": []
        }
        self.total_duration = kwargs.get("total_duration", 0)

    def __del__(self) -> None:
        """Destructor to cleanup when done."""
        if self.file:
            self.file.close()

    def __repr__(self) -> str:
        return (
            f"Tokens Used: {self.total_tokens}\n"
            f"\tPrompt Tokens: {self.prompt_tokens}\n"
            f"\tCompletion Tokens: {self.completion_tokens}\n"
            f"Total Cost (USD): ${self.total_cost}"
        )

    @staticmethod
    def _get_model_name_from_llm(serialized: Dict[str, Any]) -> str:
        """
        get model name from llm
        """
        model_name = serialized.get("kwargs").get("llm").get("kwargs").get("model", "gpt-3.5-turbo")
        return model_name

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])

        print_text(
            f"\n\n\033[1m> Entering new {class_name} chain...\033[0m",
            end="\n",
        )
        self.model_name = self._get_model_name_from_llm(serialized)

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        print_text("\n\033[1m> Finished chain.\033[0m", end="\n")
        # print_text("\n\033[1m> Finished chain.\033[0m", end="\n", file=self.file)

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        print_text(action.log, color=color or self.color, file=self.file)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""

        if observation_prefix is not None:
            print_text(f"\n{observation_prefix}", file=self.file)
        print_text(output, color=color or self.color, file=self.file)
        if llm_prefix is not None:
            print_text(f"\n{llm_prefix}", file=self.file)

    def on_text(
        self, text: str, color: Optional[str] = None, end: str = "", **kwargs: Any
    ) -> None:
        """Run when agent ends."""
        pass


    def log_answer(self, answer: str, color: Optional[str] = None, end: str = "") -> None:
        """
        log system's answer
        """
        text = "AI:" + answer
        self.turn_info["answer"] = text
        print_text(text, color=color or self.color, end=end, file=self.file)
        # calculate turn duration
        # calculate turn duration
        turn_duration = datetime.now() - self.turn_start_time
        self.total_duration += turn_duration.total_seconds()
        turn_duration = str(turn_duration.total_seconds()) + " s"
        self.turn_info["turn_duration"] = turn_duration

        # add the turn info into dialogue history and reset it
        print_text("turn_duration: " + turn_duration, color=color or self.color, end=end, file=self.file)
        print_text("token usage this turn: " + str(self.turn_info["turn_token_usage"]), color=self.color, end="\n", file=self.file)
        print_text("cost this turn: $" + str(self.turn_info["turn_cost"]), color=self.color, end="\n", file=self.file)

        self.dialogue_history.append(self.turn_info)

        # we reset the turn info here
        self.turn_info = {
            "turn_token_usage": 0,
            "turn_cost": 0,
            "prompts": []
        }

    def log_question(self, question: str, color: Optional[str] = None, end: str = "") -> None:
        """
        log user's input
        """
        header = "----Turn " + str(self.turns + 1) + "----"
        print_text(header, color=color or self.color, end=end, file=self.file)

        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print_text(date_time, color=color or self.color, end=end, file=self.file)

        text = "USER:" + question
        self.turn_info["question"] = text
        print_text(text, color=color or self.color, end=end, file=self.file)
        self.turn_start_time = datetime.now()
        self.turns = self.turns + 1

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        print_text(finish.log, color=color or self.color, end="\n", file=self.file)

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
        ) -> None:
            """Print out the prompts."""

            # This is actually the prompt
            self.turn_info["prompts"].append(prompts[0])
            print_text("prompt:" + prompts[0], color=self.color, end="", file=self.file)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Collect token usage."""

        if response.llm_output is None:
            return None
        if "token_usage" not in response.llm_output:
            return None
        token_usage = response.llm_output["token_usage"]
        completion_tokens = token_usage.get("completion_tokens", 0)
        prompt_tokens = token_usage.get("prompt_tokens", 0)

        self.turn_info["turn_token_usage"] += token_usage.get("total_tokens", 0)

        model_name = standardize_model_name(response.llm_output.get("model_name", ""))
        if model_name in MODEL_COST_PER_1K_TOKENS:
            completion_cost = get_openai_token_cost_for_model(
                model_name, completion_tokens, is_completion=True
            )
            prompt_cost = get_openai_token_cost_for_model(model_name, prompt_tokens)
            turn_cost = prompt_cost + completion_cost

            self.turn_info["turn_cost"] += turn_cost
            self.total_cost += turn_cost

        # each turn might have several turns.
        self.total_tokens += token_usage.get("total_tokens", 0)
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens

    def on_submit(self) -> None:
        """
        submit to server
        TODO:
        send the meta data to the server.
        """
        meta_data = {
            "session_id": self.session_id,
            "turns": self.turns,
            "model_name": self.model_name,
            "conversation": self.dialogue_history,
            "total_token": self.total_tokens,
            "total_cost": self.total_cost,
            "total_duration": str(self.total_duration) + "s",
        }

        if self.user_info:
            meta_data["user_info"] = self.user_info

        if self.version_tags:
            meta_data["version_tags"] = self.version_tags

        return meta_data


coeval_callback_var: ContextVar[Optional[CoevalLogger]] = ContextVar(
    "coeval_callback", default=None
)
register_configure_hook(coeval_callback_var, True)

@contextmanager
def get_coeval_logger(**kwargs: Any) -> Generator[CoevalLogger, None, None]:

    logfile_path = kwargs.get("logfile_path", None)
    # TODO: desearilise the coeval logger object here, Initialize the file object.

    cb = CoevalLogger(logfile_path, **kwargs)
    coeval_callback_var.set(cb)
    yield cb
    coeval_callback_var.set(None)
