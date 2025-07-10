import httpx
import asyncio
import json

async def send_response(response: str, request_id: str = None):
    """Send response to API"""
    async with httpx.AsyncClient() as client:
        try:
            data = {"response": response}
            if request_id:
                data["request_id"] = request_id
            
            result = await client.post(
                "http://127.0.0.1:8000/respond",
                json=data
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
            print(f"📊 Status:")
            print(f"  - Pending requests: {status['pending_requests']}")
            print(f"  - Total pending: {status['total_pending']}")
            if status["current_question"]:
                print(f"  - Current question: {status['current_question']}")
            else:
                print("  - No question waiting for response")
        except Exception as e:
            print(f"❌ Failed to check status: {e}")

async def show_queue():
    """Show the current request queue"""
    async with httpx.AsyncClient() as client:
        try:
            result = await client.get("http://127.0.0.1:8000/queue")
            result.raise_for_status()
            queue_data = result.json()
            
            if queue_data["queue"]:
                print("📋 Request Queue:")
                for i, req in enumerate(queue_data["queue"], 1):
                    print(f"  {i}. [{req['id']}] {req['question']}")
            else:
                print("📋 Queue is empty")
        except Exception as e:
            print(f"❌ Failed to get queue: {e}")

def main():
    print("🤖 Human Interaction API Client")
    print("=" * 40)
    
    while True:
        print("\nSelect operation:")
        print("1. Send response to first request (via response.txt)")
        print("2. Send response to specific request (via response.txt)")
        print("3. Check status")
        print("4. Show queue")
        print("5. Send response to first request (via input)")
        print("6. Send response to specific request (via input)")
        print("7. Exit")
        
        choice = input("\nPlease enter your choice (1-7): ").strip()
        
        if choice == "1":
            with open("response.txt", "r") as f:
                response = f.read()
            if response:
                asyncio.run(send_response(response))
            else:
                print("❌ Response cannot be empty")
        
        elif choice == "2":
            request_id = input("Please enter request ID: ").strip()
            if not request_id:
                print("❌ Request ID cannot be empty")
                continue
                
            with open("response.txt", "r") as f:
                response = f.read()
            if response:
                asyncio.run(send_response(response, request_id))
            else:
                print("❌ Response cannot be empty")
        
        elif choice == "3":
            asyncio.run(check_status())
        
        elif choice == "4":
            asyncio.run(show_queue())
        
        elif choice == "5":
            response = input("Please enter your response: ").strip()
            if response:
                asyncio.run(send_response(response))
            else:
                print("❌ Response cannot be empty")
        
        elif choice == "6":
            request_id = input("Please enter request ID: ").strip()
            if not request_id:
                print("❌ Request ID cannot be empty")
                continue
                
            response = input("Please enter your response: ").strip()
            if response:
                asyncio.run(send_response(response, request_id))
            else:
                print("❌ Response cannot be empty")
        
        elif choice == "7":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice, please try again")

if __name__ == "__main__":
    main() 
