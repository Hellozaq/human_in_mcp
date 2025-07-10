import httpx
import asyncio
import json

async def send_response(response: str):
    """Send response to API"""
    async with httpx.AsyncClient() as client:
        try:
            result = await client.post(
                "http://127.0.0.1:8000/respond",
                json={"response": response}
            )
            result.raise_for_status()
            print("✅ Response sent")
        except Exception as e:
            print(f"❌ Failed to send response: {e}")

async def check_status():
    """Check API status"""
    async with httpx.AsyncClient() as client:
        try:
            result = await client.get("http://127.0.0.1:8000/status")
            result.raise_for_status()
            status = result.json()
            if status["current_question"]:
                print(f"Current question: {status['current_question']}")
            else:
                print("No question waiting for response")
        except Exception as e:
            print(f"❌ Failed to check status: {e}")

def main():
    print("🤖 Human Interaction API Client")
    print("=" * 40)
    
    while True:
        print("\nSelect operation:")
        print("1. Send response")
        print("2. Check status")
        print("3. Exit")
        
        choice = input("\nPlease enter your choice (1-3): ").strip()
        
        if choice == "1":
            response = input("Please enter your response: ").strip()
            if response:
                asyncio.run(send_response(response))
            else:
                print("❌ Response cannot be empty")
        
        elif choice == "2":
            asyncio.run(check_status())
        
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice, please try again")

if __name__ == "__main__":
    main() 
