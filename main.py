"""
Project Entry Point
"""

import os
import subprocess


def run_dashboard():

    os.system(
        "streamlit run dashboard/streamlit_app.py"
    )


    subprocess.run(
        [
            "streamlit",
            "run",
            "dashboard/streamlit_app.py"
        ]
    )

if __name__ == "__main__":

    run_dashboard()