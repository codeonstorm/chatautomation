import re
import sys
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    DomainFilter,
    URLPatternFilter,
    ContentTypeFilter,
)
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer

from sqlmodel import select
from sqlmodel import Session
from app.core.database import get_session
from app.models.scrapedurls import ScrapedUrls
from app.models.taskstatus import TaskStatus, TaskStageEnum
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "..", "..", "webscraped")
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def run_advanced_crawler(
    service_id: int,
    taskid: int,
    urls: list[str],
    # max_depth: int = 2,
    # max_pages: int = 25,
    # keywords: list[str] = ["rag", "openai", "crawler", "async"],
    # allowed_domains: list[str] = [],
    # blocked_domains: list[str] = [],
    # patterns: list[str] = ["*guide*", "*docs*", "*tutorial*"],
    # excluded_tags: list[str] = ['form', 'header', 'footer'],
    # only_text: bool = True,
    # exclude_external_images: bool = True,
    # exclude_all_images: bool = False,
    # exclude_external_links: bool = True,
    # exclude_internal_links: bool = True,
):
    print("Starting advanced crawler...", UPLOAD_DIR)
    db: Session = next(get_session())

    # Create a sophisticated filter chain
    filter_chain = FilterChain(
        [
            # Domain boundaries
            DomainFilter(
                allowed_domains=["5centscdn.net"],
                # blocked_domains=["old.docs.example.com"]
            ),
            # URL patterns to include
            URLPatternFilter(patterns=["*guide*", "*tutorial*", "*blog*"]),
            # Content type filtering
            ContentTypeFilter(allowed_types=["text/html"]),
        ]
    )

    # Create a relevance scorer
    keyword_scorer = KeywordRelevanceScorer(
        keywords=["crawl", "example", "async", "configuration"], weight=0.7
    )

    # Set up the configuration
    config = CrawlerRunConfig(
        deep_crawl_strategy=BestFirstCrawlingStrategy(
            max_depth=0,  # 2
            max_pages=300,
            include_external=False,
            filter_chain=filter_chain,
            # url_scorer=keyword_scorer
        ),
        excluded_tags=["form", "header", "footer"],
        # only_text=True,
        exclude_external_images=True,
        # exclude_all_images=True,
        exclude_external_links=True,
        exclude_internal_links=True,
        scraping_strategy=LXMLWebScrapingStrategy(),
        stream=True,
        verbose=True,
    )

    # Execute the crawl
    results = []
    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun(urls[0], config=config):

            results.append(result)
            score = result.metadata.get("score", 0)
            depth = result.metadata.get("depth", 0)
            print(f"Depth: {depth} | Score: {score:.2f} | {result.url}")

            status = ScrapedUrls(
                service_id=service_id,
                url=result.url,
                status="enabled",
                created_at=result.metadata.get("created_at"),
                updated_at=result.metadata.get("updated_at"),
            )
            db.add(status)
            db.commit()
            db.refresh(status)

            statement = select(TaskStatus).where(TaskStatus.id == taskid)
            task = db.exec(statement)
            task = task.one()

            task.progess = task.progess + 1
            task.status = TaskStageEnum.in_progress
            db.add(task)
            db.commit()
            db.refresh(task)

            path = os.path.join(UPLOAD_DIR, str(status.id) + ".txt")
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\nURL: {result.url}\n")
                f.write(f"Depth: {depth}\n")
                f.write(result.markdown)
                f.write("\n---\n")

    # Analyze the results
    print(f"Crawled {len(results)} high-value pages")
    print(
        f"Average score: {sum(r.metadata.get('score', 0) for r in results) / len(results):.2f}"
    )

    statement = select(TaskStatus).where(TaskStatus.id == taskid)
    task = db.exec(statement)
    task = task.one()

    task.status = TaskStageEnum.completed
    db.add(task)
    db.commit()

    # Group by depth
    depth_counts = {}
    for result in results:
        depth = result.metadata.get("depth", 0)
        depth_counts[depth] = depth_counts.get(depth, 0) + 1
        print(result.markdown)  # Show the first 300 characters of extracted text
        # internal_links = result.links.get("internal", [])
        # print(internal_links)

        url = re.sub(r"^(https?://)", "", result.url)
        print(url, "====")

    print("Pages crawled by depth:")
    for depth, count in sorted(depth_counts.items()):
        print(f"  Depth {depth}: {count} pages")


if __name__ == "__main__":
    print(sys.argv)
    serviceid = sys.argv[1] if len(sys.argv) > 1 else None
    taskid = sys.argv[2] if len(sys.argv) > 2 else None
    url = sys.argv[3] if len(sys.argv) > 3 else None
    print(f"Service ID: {serviceid}, taskid: {taskid} URL: {url}")
    if serviceid and taskid and url:
        asyncio.run(
            run_advanced_crawler(service_id=serviceid, taskid=taskid, urls=[url])
        )
    else:
        print("failed")
