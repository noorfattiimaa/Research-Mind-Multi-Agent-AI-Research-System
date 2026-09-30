import time

from agents import (
    build_reader_agent,
    build_Search_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # =========================================================
    # STEP 1 — SEARCH AGENT
    # =========================================================

    print("\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_Search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"""Find recent, reliable and detailed information about:

{topic}

Use the web search tool to find relevant sources.
Return the title, URL and useful information from the sources."""
            )
        ]
    })

    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch Results:\n")
    print(state["search_results"])

    # Give Mistral some time before the next request
    time.sleep(5)


    # =========================================================
    # STEP 2 — READER AGENT
    # =========================================================

    print("\n" + " =" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_prompt = f"""
You are a research reading agent.

Research topic:
{topic}

Below are the search results:

{state["search_results"]}

Your task:

1. Identify the most relevant and reliable URL.
2. Use the scrape_url tool to scrape that URL.
3. Extract detailed information useful for the research.
4. Focus only on information relevant to the topic.

Return the important scraped content and source URL.
"""

    reader_result = reader_agent.invoke({
        "messages": [
            ("user", reader_prompt)
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n")
    print(state["scraped_content"])

    time.sleep(5)


    # =========================================================
    # STEP 3 — WRITER
    # =========================================================

    print("\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report:\n")
    print(state["report"])

    time.sleep(5)


    # =========================================================
    # STEP 4 — CRITIC
    # =========================================================

    print("\n" + " =" * 50)
    print("step 4 - Critic is reviewing the report ...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Report:\n")
    print(state["feedback"])


    # =========================================================
    # RETURN COMPLETE STATE
    # =========================================================

    return state


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    topic = input("\nEnter a research topic: ").strip()

    if not topic:
        print("Please enter a research topic.")
    else:
        run_research_pipeline(topic)