from pipeline.agentic_sales_pipeline.src.agentic_sales_pipeline.crew import AgenticSalesPipeline
from pipeline.email_writer.src.email_writer.crew import EmailWriter
from crewai.flow.flow import listen, start
from crewai import Flow


class SalesPipeline(Flow):
    @start()
    def fetch_leads(self):
        leads = [
            {
                "lead_data": {
                    "name": "João Moura",
                    "job_title": "Director of Engineering",
                    "company": "Clearbit",
                    "email": "joao@clearbit.com",
                    "use_case": "Using AI Agent to do better data enrichment."
                },
            },
        ]
        return leads

    @listen(fetch_leads)
    def score_leads(self, leads):
        # Instantiate the AgenticSalesPipeline class
        pipeline = AgenticSalesPipeline()
        
        # Access the crew instance from the pipeline
        lead_scoring_crew = pipeline.lead_scoring_crew()
        
        # Use kickoff_for_each method
        scores = lead_scoring_crew.kickoff_for_each(leads)
        
        self.state["score_crews_results"] = scores
        return scores

    @listen(score_leads)
    def store_leads_score(self, scores):
        # Here we would store the scores in the database
        return scores

    @listen(score_leads)
    def filter_leads(self, scores):
        return [score for score in scores if score['lead_score'].score > 70]

    @listen(filter_leads)
    def write_email(self, leads):
        # Use the email_writing_crew to generate emails for filtered leads
        pipeline = EmailWriter()
        email_writing_crew = pipeline.email_writing_crew()
        
        scored_leads = [lead.to_dict() for lead in leads]
        emails = email_writing_crew.kickoff_for_each(scored_leads)
        return emails

    @listen(write_email)
    def send_email(self, emails):
        # Here we would send the emails to the leads
        return emails

flow = SalesPipeline()
emails = flow.kickoff()
print(emails)
