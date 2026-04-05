import os
import httpx
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from .mobility_agent import MobilityAgent
from .crawler_agent import CrawlerAgent

load_dotenv()

class AIOrchestrator:
    """
    The brain of the ISEYAA Intelligence Layer.
    Coordinates between specialized agents and abstracts LLM providers.
    """
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "anthropic").lower()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.mobility_agent = MobilityAgent()
        self.crawler_agent = CrawlerAgent()

    async def delegate_task(self, agent_type: str, context: Dict[str, Any], query: str) -> str:
        """
        Delegates a user query to a specialized agent.
        Types: 'lga', 'planner', 'crawler', 'general'
        """
        print(f"[ORCHESTRATOR] Delegating '{agent_type}' task: {query[:50]}...")
        
        # 1. Routing Logic (Phase 3 Alpha)
        system_prompt = await self._get_system_prompt(agent_type, context)
        
        # 2. Provider Execution
        return await self._call_provider(system_prompt, query)

    async def _get_system_prompt(self, agent_type: str, context: Dict[str, Any]) -> str:
        base = "You are an agent in the ISEYAA Geo-Intelligent State Operating System for Ogun State."
        
        if agent_type == "lga":
            lga_name = context.get("lga_name", "Ogun")
            return f"{base} You are the LGA Intelligence Agent for {lga_name}. Provide deep historical, cultural, and economic insights."
        
        
        if agent_type == "planner":
            return f"{base} You are the 'Deep' Travel Planner. Create detailed, inspirational itineraries."
        
        if agent_type == "mobility":
            return await self.mobility_agent.get_system_prompt(context)
            
        if agent_type == "crawler":
            return await self.crawler_agent.get_system_prompt(context)
            
        return f"{base} You are a general intelligence assistant for the Ogun State Tourism & Governance portal."

    async def _call_provider(self, system_prompt: str, user_query: str) -> str:
        if self.provider == "anthropic" and self.anthropic_key:
            return await self._call_claude(system_prompt, user_query)
        return await self._call_openai(system_prompt, user_query)

    async def _call_claude(self, system: str, query: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": "claude-3-5-sonnet-20240620",
                        "max_tokens": 1024,
                        "system": system,
                        "messages": [{"role": "user", "content": query}]
                    },
                    timeout=30.0
                )
                resp.raise_for_status()
                return resp.json()["content"][0]["text"]
        except Exception as e:
            return f"[ORCHESTRATOR-CLAUDE-ERROR] {e}"

    async def _call_openai(self, system: str, query: str) -> str:
        if not self.openai_key:
            return "OpenAI API Key missing. Please configure AI_PROVIDER correctly."
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.openai_key}"},
                    json={
                        "model": "gpt-4o",
                        "messages": [
                            {"role": "system", "content": system},
                            {"role": "user", "content": query}
                        ]
                    },
                    timeout=20.0
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[ORCHESTRATOR-OPENAI-ERROR] {e}"

# Singleton instance
orchestrator = AIOrchestrator()
