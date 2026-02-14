![GitHsub stars](https://img.shields.io/github/stars/kushalsamani/social-media-ai-agent)
![License](https://img.shields.io/github/license/kushalsamani/social-media-ai-agent)

# Social Media AI Agent

Multi-agent marketing workflow built with CrewAI to generate market research, strategy, content calendars, social posts, reels, blog drafts, and SEO-optimized content.

## What This Project Does

This project runs a sequential AI crew that plans and drafts a full content pipeline for a product:

1. Market research report
2. Marketing strategy
3. 30-day content calendar
4. Social post drafts (JSON)
5. Reel scripts (JSON)
6. Blog research notes
7. Blog drafts (JSON)
8. SEO-optimized blog content (JSON)

Outputs are written to `resources/drafts/`.

## Tech Stack

- Python 3.13+
- [CrewAI](https://docs.crewai.com/) with Google GenAI provider
- CrewAI tools: Serper + website scraping
- Pydantic models for structured JSON outputs
- `python-dotenv` for environment variable loading

## Project Structure

```text
.
|-- marketing_crew.py              # Main crew definition + kickoff
|-- config/
|   |-- agents.yaml                # Agent roles/goals/backstories
|   `-- task.yaml                  # Task prompts + expected output formats
`-- resources/drafts/
    |-- market_research_report.md
    |-- marketing_strategy.md
    |-- content_calendar.md
    |-- post_drafts.json
    |-- reel_scripts.json
    |-- seo_optimized_content.json
    `-- blogs/
        |-- blog_content_research.md
        `-- blog_drafts.json
```

## Agents

Defined in `config/agents.yaml`:

- `head_of_marketing`
- `content_creator_social_media`
- `content_creator_blog`
- `seo_specialist`

All agents currently use `gemini/gemini-3-flash-preview` and run with reasoning enabled.

## Setup

### 1. Install dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

### 2. Configure environment variables

Create/update `.env` in the project root:

```env
GEMINI_API_KEY=your_google_genai_api_key
SERPER_API_KEY=your_serper_api_key
```

## Run

```bash
python marketing_crew.py
```

The script uses default input values in `marketing_crew.py` (`product_name`, `product_description`, `target_audience`, `budget`, and current date), then executes tasks sequentially.

## Output Format

Some tasks return structured JSON validated by this schema:

```json
{
  "items": [
    {
      "content_type": "social_media | blog_post | video_script",
      "topic": "string",
      "target_audience": "string",
      "tags": ["tag1", "tag2"],
      "content": "full content text"
    }
  ]
}
```

Markdown outputs are generated for research and calendar artifacts.

## Customize

### Change business inputs

Edit the `inputs` dict in `marketing_crew.py` to switch product, audience, budget, or description.

### Tune prompts

- Agent behavior: `config/agents.yaml`
- Task behavior and expected outputs: `config/task.yaml`

### Change model/provider

Update the `LLM(...)` configuration in `marketing_crew.py`.

## Notes

- Workflow is `Process.sequential` with `planning=False`.
- Rate limits are configured via `max_rpm` per agent and crew.
- Draft directories are ensured at runtime (`resources/drafts` and `resources/drafts/blogs`).

## Next Improvements

- Add CLI args for dynamic runtime inputs instead of hardcoded values.
- Add task-level unit tests for JSON schema compliance.
- Add logging/telemetry and retry handling for tool/network failures.
- Add CI checks for formatting, linting, and type validation.
