import type { ScrapedUrls } from "@/types/scrapedurls"

const API_URL = "http://127.0.0.1:8000/api/v1"

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `API error: ${response.status}`)
  }
  return response.json()
}

 
export async function getScrapedUrls(): Promise<ScrapedUrls[]> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/1/webscraper`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return handleResponse<ScrapedUrls[]>(response)
}


export async function startWebCrawler(url: string): Promise<undefined> {
  const accessToken = localStorage.getItem("accessToken")
  const response = await fetch(`${API_URL}/1/webscraper?url=${url}`, {
    method: 'POST',
    body: JSON.stringify({
      url: url
    }),
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return handleResponse<undefined>(response)
}
