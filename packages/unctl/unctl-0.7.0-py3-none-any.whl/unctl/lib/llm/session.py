from .base import LanguageModel


class LLMSessionKeeper:

    """
    This class is storing LLM session for failure object
    """

    _llm: LanguageModel
    _session_id: str

    def __init__(self, llm: LanguageModel):
        self._llm = llm

    async def init_session(self, data: list[str] | None = None):
        """
        Initialises LLM session
        """
        if data is None:
            data = []

        self._session_id = await self._llm.initiate_session(data=data)

    async def push_info(self, message: str):
        """
        Requests llm to analyse problem and ask for recommendation

        Args:
            message (str):information or ask to be passed to llm.
        """

        await self._llm.push_info(session_id=self._session_id, data=message)

    async def request_llm_recommendation(
        self,
        message: str | None = None,
        instructions: str | None = None,
        polling_timeout=5,
    ):
        """
        Requests llm to analyse problem and ask for recommendation

        Args:
            message (str | None, optional): additional information or
            ask to be passed to llm. Defaults to None.
        """

        if message is not None:
            await self._llm.push_info(session_id=self._session_id, data=message)

        return await self._llm.get_recommendation(
            self._session_id,
            instructions=instructions,
            polling_timeout=polling_timeout,
        )
