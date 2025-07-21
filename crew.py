import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from web_search_tool import serper_web_search
from firecrawl_tool import firecrawl_scraper

load_dotenv()

# ✅ Use correct model name from Groq
llm = LLM(
    model="llama-3.3-70b-versatile",  # ✅ Valid Groq model
    base_url="https://api.groq.com/openai/v1",  # Required for Groq
    api_key=os.getenv("GROQ_API_KEY"),  # Make sure your .env file has this key
    temperature=0.7,
    max_tokens=4029
)

# Define agents
web_researcher = Agent(
    role="Tech News Investigator",
    goal="Identify recent and relevant tech updates about the target company",
    backstory="Specialist in online news aggregation and current trends.",
    tools=[serper_web_search],
    llm=llm
)

website_scraper = Agent(
    role="Official Site Inspector",
    goal="Extract structured information from the official website of the company",
    backstory="Experienced in parsing corporate content from websites.",
    tools=[firecrawl_scraper],
    llm=llm
)

report_writer = Agent(
    role="Business Report Composer",
    goal="Generate a polished research report from agent findings",
    backstory="Expert in writing high-level executive summaries.",
    llm=llm
)

# Main function to run the report crew
def run_company_report(company: str, website_url: str):
    task_news = Task(
        description=f"Search for recent tech news about {company} in the last 3 months.",
        expected_output="Top 3 news stories in markdown format.",
        agent=web_researcher
    )

    task_scrape_about = Task(
        description=f"Scrape and summarize the 'about' or 'mission' section of {company}'s website: {website_url}",
        expected_output="Company background and mission in markdown format.",
        agent=website_scraper
    )

    task_scrape_products = Task(
        description=f"Scrape and summarize the product/service section from {company}'s website: {website_url}",
        expected_output="Detailed list of products or services in markdown format.",
        agent=website_scraper
    )

    task_compile_report = Task(
        description="Using all previous findings, generate a structured markdown report with sections: Background, Products, and News.",
        expected_output="Final markdown report with headings and clean formatting.",
        agent=report_writer
    )

    crew = Crew(
        agents=[web_researcher, website_scraper, report_writer],
        tasks=[task_news, task_scrape_about, task_scrape_products, task_compile_report],
        process=Process.sequential,
        manager_llm=llm,
        verbose=True
    )

    return str(crew.kickoff())

