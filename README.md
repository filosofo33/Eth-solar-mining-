# Solar-Powered Mining Controller

A Python script that automatically managed cryptocurrency mining operations (with EthOS, linux based OS)based on solar panel output, electricity rates, and solar position data.

## Overview

This script intelligently controls mining operations by considering multiple factors:
- Solar panel power generation
- Time-based electricity rates
- Sun position (azimuth and altitude)
- Cloud cover
- Power consumption

## Features

- Automatically starts mining during night rate periods (22:00-12:00)
- Monitors real-time solar panel generation
- Calculates optimal mining times based on:
  - Solar power generation (>200W threshold)
  - Power consumption (<300W threshold)
  - Sun position relative to panels
  - Cloud cover conditions

## Requirements

- Python 3.x
- Fronius solar inverter accessible at `192.168.0.200`
- API Keys for:
  - OpenWeatherMap
  - Wolfram Alpha

## Dependencies
python
requests
xml.etree.cElementTree


## How It Works

1. **Night Rate Check**: Automatically mines during low-cost electricity periods
2. **Solar Generation Check**: Starts mining if solar generation exceeds 200W
3. **Power Consumption Check**: Stops mining if consumption exceeds 300W
4. **Sun Position Analysis**: 
   - Calculates sun azimuth and altitude
   - Adjusts for cloud cover
   - Makes mining decisions based on optimal panel exposure

