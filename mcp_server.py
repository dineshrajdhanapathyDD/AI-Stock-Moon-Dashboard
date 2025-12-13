#!/usr/bin/env python3
"""
MCP Server for Stock Moon Dashboard tools.
Provides getStockPrices and getMoonPhase tools via Model Context Protocol.
"""

import json
import sys
import asyncio
from typing import Any, Dict, List, Optional
import logging

# Add src to path
sys.path.insert(0, 'src')

from src.mcp_tools import get_stock_prices, get_moon_phase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServer:
    """MCP server implementation for dashboard tools."""
    
    def __init__(self):
        self.name = "stock-moon-dashboard"
        self.version = "1.0.0"
        
        self.tools = {
            'getStockPrices': {
                'name': 'getStockPrices',
                'description': 'Fetch daily historical stock prices from Yahoo Finance without an API key',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'symbol': {
                            'type': 'string',
                            'description': 'Stock ticker symbol (e.g., AAPL, MSFT, BTC-USD)'
                        },
                        'start_date': {
                            'type': 'string',
                            'description': 'Start date in YYYY-MM-DD format'
                        },
                        'end_date': {
                            'type': 'string',
                            'description': 'End date in YYYY-MM-DD format'
                        },
                        'interval': {
                            'type': 'string',
                            'description': 'Data interval (1d, 1wk, 1mo)',
                            'default': '1d'
                        }
                    },
                    'required': ['symbol', 'start_date', 'end_date']
                }
            },
            'getMoonPhase': {
                'name': 'getMoonPhase',
                'description': 'Fetch moon phase and illumination data using astronomical calculations',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'latitude': {
                            'type': 'number',
                            'description': 'Latitude of location'
                        },
                        'longitude': {
                            'type': 'number',
                            'description': 'Longitude of location'
                        },
                        'start_date': {
                            'type': 'string',
                            'description': 'Start date in YYYY-MM-DD format'
                        },
                        'end_date': {
                            'type': 'string',
                            'description': 'End date in YYYY-MM-DD format'
                        }
                    },
                    'required': ['latitude', 'longitude', 'start_date', 'end_date']
                }
            }
        }
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        return {
            'protocolVersion': '2024-11-05',
            'capabilities': {
                'tools': {}
            },
            'serverInfo': {
                'name': self.name,
                'version': self.version
            }
        }
    
    def handle_list_tools(self) -> Dict[str, Any]:
        """Handle MCP tools/list request."""
        return {
            'tools': list(self.tools.values())
        }
    
    def handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP tools/call request."""
        try:
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            if tool_name == 'getStockPrices':
                result = get_stock_prices(
                    symbol=arguments['symbol'],
                    start_date=arguments['start_date'],
                    end_date=arguments['end_date'],
                    interval=arguments.get('interval', '1d')
                )
                
                return {
                    'content': [
                        {
                            'type': 'text',
                            'text': f"Successfully fetched {len(result)} stock data points for {arguments['symbol']}"
                        },
                        {
                            'type': 'text',
                            'text': json.dumps(result, indent=2)
                        }
                    ]
                }
            
            elif tool_name == 'getMoonPhase':
                result = get_moon_phase(
                    latitude=arguments['latitude'],
                    longitude=arguments['longitude'],
                    start_date=arguments['start_date'],
                    end_date=arguments['end_date']
                )
                
                return {
                    'content': [
                        {
                            'type': 'text',
                            'text': f"Successfully calculated {len(result)} moon phase data points"
                        },
                        {
                            'type': 'text',
                            'text': json.dumps(result, indent=2)
                        }
                    ]
                }
            
            else:
                return {
                    'isError': True,
                    'content': [
                        {
                            'type': 'text',
                            'text': f'Unknown tool: {tool_name}'
                        }
                    ]
                }
                
        except Exception as e:
            logger.error(f"Tool execution failed: {str(e)}")
            return {
                'isError': True,
                'content': [
                    {
                        'type': 'text',
                        'text': f'Tool execution failed: {str(e)}'
                    }
                ]
            }
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP request."""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'initialize':
            return self.handle_initialize(params)
        elif method == 'tools/list':
            return self.handle_list_tools()
        elif method == 'tools/call':
            return self.handle_call_tool(params)
        else:
            return {
                'error': {
                    'code': -32601,
                    'message': f'Method not found: {method}'
                }
            }


def main():
    """Main MCP server function."""
    server = MCPServer()
    
    # Simple command-line interface for testing
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            # Test tools/list
            response = server.handle_list_tools()
            print(json.dumps(response, indent=2))
        
        elif command == 'test-stock':
            # Test stock data fetching
            request = {
                'method': 'tools/call',
                'params': {
                    'name': 'getStockPrices',
                    'arguments': {
                        'symbol': 'AAPL',
                        'start_date': '2024-01-01',
                        'end_date': '2024-01-31'
                    }
                }
            }
            response = server.process_request(request)
            print(json.dumps(response, indent=2))
        
        elif command == 'test-moon':
            # Test moon data fetching
            request = {
                'method': 'tools/call',
                'params': {
                    'name': 'getMoonPhase',
                    'arguments': {
                        'latitude': 40.7128,
                        'longitude': -74.0060,
                        'start_date': '2024-01-01',
                        'end_date': '2024-01-31'
                    }
                }
            }
            response = server.process_request(request)
            print(json.dumps(response, indent=2))
        
        elif command == 'server':
            # Run as MCP server (stdio mode)
            print("Starting MCP server in stdio mode...", file=sys.stderr)
            # In a real implementation, this would handle JSON-RPC over stdio
            # For now, just indicate server mode
            print("MCP Server ready", file=sys.stderr)
    
    else:
        print("MCP Server for Stock Moon Dashboard")
        print("Usage:")
        print("  python mcp_server.py list          - List available tools")
        print("  python mcp_server.py test-stock    - Test stock data fetching")
        print("  python mcp_server.py test-moon     - Test moon data fetching")
        print("  python mcp_server.py server        - Run as MCP server")


if __name__ == "__main__":
    main()