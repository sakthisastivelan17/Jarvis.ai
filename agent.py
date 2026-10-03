from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import google

load_dotenv(dotenv_path=".env.local")


class Jarvis(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are JARVIS, a witty, calm, and highly capable AI assistant. "
                "Speak concisely and naturally, like a helpful companion. "
                "Avoid long-winded answers - keep responses short and conversational. "
                "Reply quickly and directly - don't overthink simple questions."
            )
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.5-flash-native-audio-preview-12-2025",
            voice="Puck",  # try Charon, Kore, Fenrir, Aoede too
            modalities=["AUDIO"],
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Jarvis(),
    )

    await session.generate_reply(
        instructions="Greet the user as JARVIS and ask how you can help."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

