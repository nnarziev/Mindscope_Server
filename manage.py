#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import stress_prediction_service


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mindscope_Server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    stress_prediction_service.start()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    stress_prediction_service.stop()
