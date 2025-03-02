from langchain_docling import DoclingLoader

FILE_PATH = "https://arxiv.org/pdf/2408.09869"

loader = DoclingLoader(file_path=FILE_PATH)
docs = loader.load()


for d in docs[:3]:
    print(f"- {d.page_content=}")

