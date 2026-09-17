from nemoguardrails import RailsConfig, LLMRails
config = RailsConfig.from_path("app/nemoguard")
rails = LLMRails(config)

async def check_input(user_query: str):
    response = await rails.generate_async(
        messages=[
            {
                "role": "user",
                "content": user_query,
            }
        ]
    )
    return response

async def check_output(user_query: str, bot_response: str):
    response = await rails.generate_async(
        messages=[
            {
                "role": "user",
                "content": user_query,
            },
            {
                "role": "assistant",
                "content": bot_response,
            },
        ]
    )
    return response