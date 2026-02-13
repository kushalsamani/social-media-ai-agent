from typing import List
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from pydantic import BaseModel, Field
from datetime import datetime



from dotenv import load_dotenv

_ = load_dotenv()

llm = LLM(
    model="gemini/gemini-3-flash-preview",
    temperature=0.7
)


class Content(BaseModel):
    content_type: str = Field(..., description="Type of content to be created, e.g., 'social_media', 'blog_post etc.'")
    topic: str = Field(..., description="The topic or subject matter for the content.")
    target_audience: str = Field(..., description="The target audience for the content.")
    tags: List[str] = Field(..., description="A list of tags or keywords to be used for the content.")  
    content: str = Field(..., description="The actual content to be created.")

class ContentList(BaseModel):
    items: List[Content] = Field(..., description="A list of generated content objects.")

@CrewBase
class TheMarketingCrew():
    "The marketing crew is responsible for creating and executing marketing strategies to promote products and services, increase brand awareness, and drive sales. They conduct market research, develop marketing campaigns, manage social media, and analyze the effectiveness of their efforts to ensure the success of the company's marketing initiatives."
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/task.yaml'

    @agent
    def head_of_marketing(self) -> Agent:
        return Agent(
            config = self.agents_config['head_of_marketing'],
            tools = [
                SerperDevTool(), 
                ScrapeWebsiteTool()
            ],
            reasoning = True,
            inject_date = True,
            llm = llm,
            allow_delegation = True,
            max_rpm = 3,
            max_iter = 6
        )

    @agent
    def content_creator_social_media(self) -> Agent:
        return Agent(
            config = self.agents_config['content_creator_social_media'],
            tools = [
                SerperDevTool(), 
                ScrapeWebsiteTool()
            ],
            reasoning = True,
            inject_date = True,
            llm = llm,
            allow_delegation = False,
            max_rpm = 2,
            max_iter = 5
        )
    
    @agent
    def content_creator_blog(self) -> Agent:
        return Agent(
            config = self.agents_config['content_creator_blog'],
            tools = [
                SerperDevTool(), 
                ScrapeWebsiteTool()
            ],
            reasoning = True,
            inject_date = True,
            llm = llm,
            allow_delegation = False,
            max_rpm = 2,
            max_iter = 5
        )
    
    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config = self.agents_config['seo_specialist'],
            tools = [
                SerperDevTool(), 
                ScrapeWebsiteTool() 
            ],
            reasoning = True,
            inject_date = True,
            llm = llm,
            allow_delegation = False,
            max_rpm = 2,
            max_iter = 4
        )
    
    @task
    def market_research(self) -> Task:
        return Task(
            config = self.tasks_config['market_research'],
            agent = self.head_of_marketing(),
            output_file="resources/drafts/market_research_report.md"
        )
    
    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(
            config = self.tasks_config['prepare_marketing_strategy'],
            agent = self.head_of_marketing(),
            output_file="resources/drafts/marketing_strategy.md"
        )
    
    @task
    def create_content_calendar(self) -> Task:
        return Task(
            config = self.tasks_config['create_content_calendar'],
            agent = self.content_creator_social_media(),
            output_file="resources/drafts/content_calendar.md"
        )
    
    @task
    def prepare_post_drafts(self) -> Task:
        return Task(
            config = self.tasks_config['prepare_post_drafts'],
            agent = self.content_creator_social_media(),
            output_json=ContentList,
            output_file="resources/drafts/post_drafts.json"
        )
    
    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(
            config = self.tasks_config['prepare_scripts_for_reels'],
            agent = self.content_creator_social_media(),
            output_json=ContentList,
            output_file="resources/drafts/reel_scripts.json"
        )
    
    @task
    def content_research_for_blogs(self) -> Task:
        return Task(
            config = self.tasks_config['content_research_for_blogs'],
            agent = self.content_creator_blog(),
            output_file="resources/drafts/blogs/blog_content_research.md"
        )
    
    @task
    def draft_blogs(self) -> Task:
        return Task(
            config = self.tasks_config['draft_blogs'],
            agent = self.content_creator_blog(),
            output_json=ContentList,
            output_file="resources/drafts/blogs/blog_drafts.json"
        )
    
    @task
    def seo_optimization(self) -> Task:
        return Task(
            config = self.tasks_config['seo_optimization'],
            agent = self.seo_specialist(),
            output_json=ContentList,
            output_file="resources/drafts/seo_optimized_content.json"
        )
    
    @crew
    def marketing_crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=False,
            max_rpm=3
            )
    
if __name__ == "__main__":

    inputs = {
        "product_name": "AI-Powered Social Media Management Tool",
        "target_audience": "Small to Medium-sized Businesses (SMBs) and Social Media Managers",
        "product_description": "A tool that automates repetitive tasks in Excel using AI, allowing users to save time and increase productivity. It can generate formulas, create macros, and provide insights based on the data in the spreadsheet.",
        "budget": "$10,000",
        "current_date": datetime.now().strftime("%Y-%m-%d")
    }

    crew = TheMarketingCrew()
    result = crew.marketing_crew().kickoff(inputs=inputs)

    import os
    from pathlib import Path


    Path("resources/drafts").mkdir(parents=True, exist_ok=True)
    Path("resources/drafts/blogs").mkdir(parents=True, exist_ok=True)


    # for task_output in result.tasks_output:
    #     if isinstance(task_output.raw, ContentList):
    #         for content_obj in task_output.raw.items:
    #             base_path = "resources/drafts"
                
    #             if content_obj.content_type == "blog_post":
    #                 base_path = "resources/drafts/blogs"
                    
    #             filename = f"{base_path}/{content_obj.content_type}_{content_obj.topic.replace(' ', '_')}.md"
        
    #         with open(filename, "w", encoding="utf-8") as f:
    #             f.write(content_obj.content)

    #         print(f"Saved: {filename}")

    print("Marketing Crew has been successfully created and run.")

