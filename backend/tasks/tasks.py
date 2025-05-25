import subprocess
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from app.models.taskstatus import TaskStatus, TaskStageEnum
from sqlmodel import select

# from app.classes.webscraper.crawler import run_advanced_crawler


rabbitmq_broker = RabbitmqBroker(url="amqp://guest:guest@localhost:5672/#/")
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def start_crawl_task(
    service_id: int,
    taskid: int,
    url: str,
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
    print(f"crawler started.. serviceid: {service_id}")
    # asyncio.run(run_advanced_crawler())
    # subprocess.run(["python", "app\classes\webscraper\crawler.py"])
    subprocess.run(
        [
            "python",
            "-m",
            "app.classes.webscraper.crawler",
            str(service_id),
            str(taskid),
            url,
        ]
    )
