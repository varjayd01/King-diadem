
"""
INTEGRATIONS/google_search.py

Search tool suggestions for KING DIADEM.

KING DIADEM remains platform-neutral.
The system does not force users to use a specific provider.
It only suggests available tools.
"""


def suggest_search_tools():

    tools = [

        {
            "name": "Google Search",
            "type": "search engine",
            "strength": "largest global index"
        },

        {
            "name": "DuckDuckGo",
            "type": "privacy search",
            "strength": "privacy focused"
        },

        {
            "name": "Bing",
            "type": "search engine",
            "strength": "AI-assisted search"
        }

    ]

    return {
        "category": "search_tools",
        "platform_neutral": True,
        "tools": tools,
        "note": "KING DIADEM suggests tools but does not enforce a provider."
    }
