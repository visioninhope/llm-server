# import nest_asyncio
from langchain_core.tools import StructuredTool

from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain_community.agent_toolkits.playwright.toolkit import PlayWrightBrowserToolkit

from src.models.tools.search import SearxNgSchema
from src.models.tools import HumanQuery

from .advanced import python_repl
from .search import searx_search
from .llm import multi_modal_llm
from .csv import csv_agent
from .pdf import get_form_field_names, fill_pdf_fields

# nest_asyncio.apply()

repl_tool = StructuredTool.from_function(
	name="python_repl",
    func=python_repl.run,
	description="""A Python shell. Use this to execute python commands. 
                Input should be a valid python command. If you want to 
                see the output of a value, you should print it out with 
                `print(...)`.""",
    handle_tool_error=True,
)

multi_modal_tool = StructuredTool.from_function(
    args_schema=HumanQuery,
    name="multi_modal_tool",
    func=multi_modal_llm,
    description="If you need to understand context in an image use this tool to get a summary.",
    handle_tool_error=True,
)

csv_tool = StructuredTool.from_function(
    name="csv_agent",
    func=csv_agent,
    description="Rewrite the query as a standalone question based on the users query.",
    handle_tool_error=True,
)

searxng_serach_tool = StructuredTool.from_function(
    args_schema=SearxNgSchema,
    name="searxng_serach",
    func=searx_search,
    handle_tool_error=True,
    description="""SearXNG is a metasearch engine, aggregating 
                the results of other search engines while not 
                storing information about its users."""
)

pdf_get_field_names = StructuredTool.from_function(
    name="pdf_get_field_names",
    func=get_form_field_names,
    description="Get the field names of a PDF file. Always call this before pdf_fill_form_fields.",
    handle_tool_error=True,
)

pdf_fill_form_fields = StructuredTool.from_function(
    name="pdf_fill_form_fields",
    func=fill_pdf_fields,
    description="""Do NOT run this tool without first calling 'pdf_get_field_names' to get the fields. 
Fill in a PDF with given field values. In these forms there are multiple places where a value may need used more than once. Only update 3 fields max at a time.

This function takes a dictionary of field names and values, reads a specified
input PDF, and fills in the fields with the provided values. The filled PDF is then
saved to a specified output path. Only text fields are supported. If you want to 
set a field to read-only, you can uncomment the relevant lines in the code.

:param fields_values: A dictionary where each key is the name of the field as 
defined in the PDF form, and each value is the value to set for that field.
""",
    handle_tool_error=True,
)

# def playwright_toolkit():
#     browser = create_async_playwright_browser()
#     toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
#     tools = toolkit.get_tools()
#     return tools




AVAILABLE_TOOLS = {
    'image_summary': multi_modal_tool,
    "searxng_serach": searxng_serach_tool,
	# 'repl_tool': repl_tool,
    # 'csv_tool': csv_tool,
    # 'pdf_get_field_names': pdf_get_field_names,
    # 'pdf_fill_form_fields': pdf_fill_form_fields,
    # 'playwright_toolkit': playwright_toolkit(),
}

TOOL_DESCRIPTIONS = {
    'image_summary': {
        'description': 'Tool for understanding context in an image. Uses GPT-4o (currently).',
        'link': '/tools/image_summary',
        'toolkit': 'Advanced'
    },
    'searxng_serach': {
        'description': searxng_serach_tool.description,
        'link': 'https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.searx_search.SearxSearchWrapper.html',
        'toolkit': 'Advanced'
    },
    'repl_tool': {
        'description': 'Python REPL can execute arbitrary code. Use with caution',
        'link': '/tools/repl_tool',
        'toolkit': 'Advanced'
    },
    'csv_tool': {
        'description': 'Tool for processing CSV files.',
        'link': '/tools/csv_tool',
        'toolkit': 'Basic'
    },
    'pdf_get_field_names': {
        'description': 'Extract field names from PDF forms.',
        'link': '/tools/pdf_get_field_names',
        'toolkit': 'Advanced'
    },
    'pdf_fill_form_fields': {
        'description': 'Fill form fields in PDF documents.',
        'link': '/tools/pdf_fill_form_fields',
        'toolkit': 'Advanced'
    },
}

def tool_details():
    return [
        {
            'name': key.replace('_', ' ').title(),
            'value': key,
            'description': TOOL_DESCRIPTIONS[key]['description'],
            'link': TOOL_DESCRIPTIONS[key]['link'],
            'toolkit': TOOL_DESCRIPTIONS[key]['toolkit']
        }
        for key in AVAILABLE_TOOLS
    ]