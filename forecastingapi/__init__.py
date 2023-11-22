"""Top-level package for forecastingAPI."""

__author__ = """T. Moudiki"""
__email__ = "thierry.moudiki@gmail.com"
__version__ = "0.2.0"

from .forecastingapi import create_account, get_token, get_forecast

__all__ = [create_account, get_token, get_forecast]
