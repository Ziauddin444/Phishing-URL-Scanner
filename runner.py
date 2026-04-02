#!/usr/bin/env python3
"""
Interactive Project Runner for Phishing URL Scanner
Helps you run the project in the correct order with user prompts
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a shell command and handle errors"""
    if description:
        print(f"\n▶ {description}")
        print(f"  Command: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        return False

def main():
    os.chdir("/Users/ziauddin/Phishing URL Scanner")
    
    print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║           🚀 PHISHING URL SCANNER - PROJECT RUNNER 🚀                          ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("""
What would you like to do?

1. 🏗️  Setup & Train (Setup venv, install deps, train models)
2. 🤖  Train Only (Train models only - requires setup first)
3. 🌐 Start API (Run Flask API server)
4. 🧪 Test API (Run automated API tests)
5. 🎯 Full Run (Setup → Train → Start API)

Choose an option (1-5): """)
    
    choice = input().strip()
    
    if choice == "1":
        print("\n" + "="*80)
        print("SETUP & TRAIN MODE")
        print("="*80)
        
        # Create venv
        print("\n📦 Creating virtual environment...")
        if not os.path.exists("venv"):
            run_command("python3 -m venv venv", "Creating Python virtual environment")
        else:
            print("✓ Virtual environment already exists")
        
        # Activate venv and install deps
        print("\n📥 Installing dependencies...")
        if platform.system() == "Windows":
            activate_cmd = "venv\\Scripts\\activate.bat && "
        else:
            activate_cmd = "source venv/bin/activate && "
        
        run_command(f"{activate_cmd}pip install --upgrade pip -q", "Upgrading pip")
        run_command(f"{activate_cmd}pip install -r requirements.txt -q", "Installing requirements")
        
        # Train models
        print("\n🤖 Training models...")
        run_command(f"{activate_cmd}python train_models.py", "Training ML models")
        
        print("\n" + "="*80)
        print("✅ SETUP & TRAINING COMPLETE!")
        print("="*80)
        print("\n📚 Next step: Start the API")
        print("   Run: python runner.py")
        print("   Choose option 3")
        
    elif choice == "2":
        print("\n" + "="*80)
        print("TRAINING ONLY MODE")
        print("="*80)
        
        if platform.system() == "Windows":
            activate_cmd = "venv\\Scripts\\activate.bat && "
        else:
            activate_cmd = "source venv/bin/activate && "
        
        print("\n🤖 Training models...")
        run_command(f"{activate_cmd}python train_models.py", "Training ML models")
        
        print("\n✅ Training complete!")
        
    elif choice == "3":
        print("\n" + "="*80)
        print("API SERVER MODE")
        print("="*80)
        
        if platform.system() == "Windows":
            activate_cmd = "venv\\Scripts\\activate.bat && "
        else:
            activate_cmd = "source venv/bin/activate && "
        
        print("\n🌐 Starting Flask API server...")
        print("   API will run on: http://localhost:5000")
        print("   Health check: http://localhost:5000/api/health")
        print("   Press CTRL+C to stop\n")
        
        run_command(f"{activate_cmd}python src/app.py", "Starting Flask API")
        
    elif choice == "4":
        print("\n" + "="*80)
        print("API TESTING MODE")
        print("="*80)
        
        if platform.system() == "Windows":
            activate_cmd = "venv\\Scripts\\activate.bat && "
        else:
            activate_cmd = "source venv/bin/activate && "
        
        print("\n⚠️  Make sure the API server is running!")
        print("   Run in another terminal: python runner.py → Choose option 3\n")
        
        input("Press ENTER to start tests...")
        
        run_command(f"{activate_cmd}python test_api.py", "Running API tests")
        
    elif choice == "5":
        print("\n" + "="*80)
        print("FULL RUN MODE (Setup → Train → API)")
        print("="*80)
        
        # Create venv
        print("\n📦 Creating virtual environment...")
        if not os.path.exists("venv"):
            run_command("python3 -m venv venv", "Creating Python virtual environment")
        else:
            print("✓ Virtual environment already exists")
        
        # Activate venv and install deps
        print("\n📥 Installing dependencies...")
        if platform.system() == "Windows":
            activate_cmd = "venv\\Scripts\\activate.bat && "
        else:
            activate_cmd = "source venv/bin/activate && "
        
        run_command(f"{activate_cmd}pip install --upgrade pip -q", "Upgrading pip")
        run_command(f"{activate_cmd}pip install -r requirements.txt -q", "Installing requirements")
        
        # Train models
        print("\n🤖 Training models...")
        run_command(f"{activate_cmd}python train_models.py", "Training ML models")
        
        # Start API
        print("\n🌐 Starting Flask API server...")
        print("   API running on: http://localhost:5000")
        print("   Press CTRL+C to stop\n")
        run_command(f"{activate_cmd}python src/app.py", "Starting Flask API")
        
    else:
        print("❌ Invalid choice. Please run again and select 1-5.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
