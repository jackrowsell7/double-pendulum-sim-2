"""
Main entry point for the Double Pendulum Simulation application
"""

from app.double_pendulum_app import DoublePendulumApp

def main():
    """
    Initialize and run the application
    """
    app = DoublePendulumApp()
    app.initialize()
    app.run()
    app.exit()

if __name__ == "__main__":
    main()