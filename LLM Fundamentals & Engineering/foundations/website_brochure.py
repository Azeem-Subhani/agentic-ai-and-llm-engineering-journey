"""
Simple website brochure generator.

What this script does:
1. Accepts a website URL
2. Scrapes useful content from the page
3. Sends that content to the OpenAI API
4. Prints a clean brochure in the console

Example:
    python website_brochure.py https://example.com
"""

from __future__ import annotations

import argparse
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from openai import OpenAI


def normalize_url(url: str) -> str:
    """Add https:// if the user forgets to include it."""
    if url.startswith(("http://", "https://")):
        return url
    return f"https://{url}"


def fetch_html(url: str) -> str:
    """Download the webpage HTML."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


def clean_text(text: str) -> str:
    """Remove extra spaces and line breaks."""
    return " ".join(text.split())


def extract_website_content(html: str, url: str) -> Dict[str, List[str] | str]:
    """Pull the most useful brochure-style content from the page."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove tags that usually do not help with page understanding.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = clean_text(soup.title.get_text()) if soup.title else "No title found"

    meta_description_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = ""
    if meta_description_tag and meta_description_tag.get("content"):
        meta_description = clean_text(meta_description_tag["content"])

    headings: List[str] = []
    for tag_name in ["h1", "h2", "h3"]:
        for heading in soup.find_all(tag_name):
            text = clean_text(heading.get_text())
            if text and text not in headings:
                headings.append(text)

    paragraphs: List[str] = []
    for paragraph in soup.find_all("p"):
        text = clean_text(paragraph.get_text())
        if len(text) > 40:
            paragraphs.append(text)

    return {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "headings": headings[:12],
        "paragraphs": paragraphs[:8],
    }


def build_prompt(content: Dict[str, List[str] | str]) -> str:
    """Turn scraped website content into a clear AI prompt."""
    headings_text = "\n".join(f"- {heading}" for heading in content["headings"])
    paragraphs_text = "\n".join(f"- {paragraph}" for paragraph in content["paragraphs"])

    if not headings_text:
        headings_text = "- No clear headings found"

    if not paragraphs_text:
        paragraphs_text = "- No clear paragraphs found"

    return f"""
You are a helpful business analyst and copywriter.

Use the website content below to create a short, clean brochure.
Write in simple, human-friendly language.
Do not invent facts that are not supported by the page content.

Return the result with these exact section headings:
1. Website Title
2. Key Highlights
3. Summary of Services/Content
4. Simple Description

Website URL:
{content["url"]}

Page Title:
{content["title"]}

Meta Description:
{content["meta_description"] or "Not available"}

Headings:
{headings_text}

Paragraphs:
{paragraphs_text}
""".strip()


def generate_brochure(prompt: str) -> str:
    """Send the prompt to OpenAI and return the brochure text."""
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text


def print_brochure(brochure: str) -> None:
    """Print the final brochure in a clean console format."""
    print("\n" + "=" * 80)
    print("WEBSITE BROCHURE")
    print("=" * 80)
    print(brochure)
    print("=" * 80 + "\n")


def main() -> None:
    """Run the brochure generator from the command line."""
    parser = argparse.ArgumentParser(
        description="Scrape a website and turn it into a brochure with OpenAI."
    )
    parser.add_argument("url", help="The website URL to analyze")
    args = parser.parse_args()

    url = normalize_url(args.url)

    try:
        html = fetch_html(url)
        content = extract_website_content(html, url)
        prompt = build_prompt(content)
        brochure = generate_brochure(prompt)
        print_brochure(brochure)
    except requests.RequestException as error:
        print(f"Could not download the webpage: {error}")
    except Exception as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()
