"""
Quick Start CLI - Easy way to run AI agents
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent
from config import validate_config


async def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           AI Agent System for Solopreneurs                   ║
║                                                              ║
║  Powerful AI agents to help you build and grow your business ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not validate_config():
        print("\n❌ Setup Required!")
        print("\nPlease set your GITHUB_TOKEN environment variable:")
        print("\n1. Generate a token at: https://github.com/settings/tokens")
        print("   (You need 'model.inference' scope)")
        print("\n2. Set the environment variable:")
        print("   Windows PowerShell:")
        print("   $env:GITHUB_TOKEN='your_token_here'")
        print("\n   Linux/Mac:")
        print("   export GITHUB_TOKEN='your_token_here'")
        print("\n3. Run this script again")
        return
    
    print("\n✅ Configuration valid! Initializing agents...\n")
    
    orchestrator = OrchestratorAgent()
    
    while True:
        print("\n" + "=" * 60)
        print("🤖 What can I help you with today?")
        print("=" * 60)
        print("\n1. 💼 Evaluate a business idea")
        print("2. 🚀 Complete business setup (solopreneur)")
        print("3. 🔬 Research a topic")
        print("4. 💻 Build/code something")
        print("5. ❌ Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "5":
            print("\n👋 Goodbye! Come back when you need help with your business.")
            break
        
        print("\n")
        
        try:
            if choice == "1":
                print("💼 Business Idea Evaluation")
                print("-" * 60)
                idea = input("\n📝 Describe your business idea:\n> ").strip()
                if not idea:
                    print("⚠️  Please provide a business idea")
                    continue
                
                context = input("\n📝 Additional context (target market, budget, etc.) - optional:\n> ").strip()
                
                print("\n" + "=" * 60)
                print("🤖 Analyzing your business idea...")
                print("=" * 60 + "\n")
                
                async for chunk in orchestrator.run_business_evaluation(idea, context):
                    print(chunk, end="", flush=True)
                print("\n")
            
            elif choice == "2":
                print("🚀 Complete Business Setup")
                print("-" * 60)
                idea = input("\n📝 Describe your business:\n> ").strip()
                if not idea:
                    print("⚠️  Please describe your business")
                    continue
                
                weeks_input = input("\n📝 Timeline in weeks (default 12):\n> ").strip()
                weeks = int(weeks_input) if weeks_input and weeks_input.isdigit() else 12
                
                print("\n" + "=" * 60)
                print("🤖 Creating complete business plan...")
                print("=" * 60 + "\n")
                
                async for chunk in orchestrator.run_complete_business_setup(idea, weeks):
                    print(chunk, end="", flush=True)
                print("\n")
            
            elif choice == "3":
                print("🔬 Research & Analysis")
                print("-" * 60)
                topic = input("\n📝 What would you like to research:\n> ").strip()
                if not topic:
                    print("⚠️  Please provide a research topic")
                    continue
                
                print("\n" + "=" * 60)
                print("🤖 Conducting research...")
                print("=" * 60 + "\n")
                
                async for chunk in orchestrator.run_research_project(topic):
                    print(chunk, end="", flush=True)
                print("\n")
            
            elif choice == "4":
                print("💻 Code Development")
                print("-" * 60)
                project = input("\n📝 What do you want to build:\n> ").strip()
                if not project:
                    print("⚠️  Please describe what you want to build")
                    continue
                
                requirements = input("\n📝 Additional requirements (optional):\n> ").strip()
                
                print("\n" + "=" * 60)
                print("🤖 Generating code and setup instructions...")
                print("=" * 60 + "\n")
                
                async for chunk in orchestrator.run_coding_project(project, requirements):
                    print(chunk, end="", flush=True)
                print("\n")
            
            else:
                print("⚠️  Invalid choice. Please select 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user.")
            continue
        except Exception as e:
            print(f"\n\n❌ Error: {str(e)}")
            print("Please try again or contact support.")
            continue
        
        input("\n\n✅ Task complete! Press Enter to continue...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
