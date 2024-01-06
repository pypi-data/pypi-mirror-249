# WrapperXSelector(CroW)

[![PyPI Version](https://img.shields.io/pypi/v/WrapperXSelector.svg)](https://pypi.org/project/WrapperXSelector/)
[![Python Versions](https://img.shields.io/pypi/pyversions/WrapperXSelector.svg)](https://pypi.org/project/WrapperXSelector/)
[![License](https://img.shields.io/pypi/l/WrapperXSelector.svg)](https://opensource.org/licenses/MIT)

The WrapperXSelector(CroW) is a Python-based tool that streamlines web scraping and data extraction tasks through the creation and utilization of wrappers. 
Leveraging Selenium for web automation and BeautifulSoup for HTML parsing, the project empowers users to effortlessly set up wrappers for tables and general 
data on web pages. With functions like setTableWrapper and setGeneralWrapper, users can define the structure of data extraction, while getWrapperData 
facilitates the retrieval of data based on these wrappers. Additionally, the project offers functionality for listing existing wrappers with listWrappers. 
Overall, the Web Wrapper Project serves as a versatile solution for simplifying web scraping workflows and enhancing data extraction efficiency in Python.



**Important Note:**

**1. The Select operation becomes functional exclusively upon the application of a right mouse click.**

**2. Please make sure Chrome is installed on your machine.**




## Table of Contents

- [Installation](#installation)
  - [Requirements](#requirements)
  - [Installation Steps](#installation-steps)
- [Usage](#usage)
  - [Setting up a Table Wrapper](#setting-up-a-table-wrapper)
  - [Setting up a General Wrapper](#setting-up-a-general-wrapper)
  - [Getting Wrapper Data](#getting-wrapper-data)
  - [Listing Wrappers](#listing-wrappers)
- [Dependencies](#dependencies)
- [Disclaimer](#disclaimer)

## Installation

### Requirements

- Python 3.x
- Chrome browser (for Selenium)

### Installation Steps

You can install the Web Wrapper Project using pip:

```bash
pip install WrapperXSelector
```

## Usage

### Setting up a Table Wrapper

To set up a table wrapper, use the `setTableWrapper` function. This function automates the process of creating a web scraping wrapper for a table on a specified web page.

#### Function Input:

- **URL (string):** The URL of the web page containing the table you want to scrape.
- **Wrapper Name (string, optional):** A custom name for the wrapper. If not provided, a unique name will be generated.

```python
from web_wrapper_project import setTableWrapper

# Example: Setting up a table wrapper for "https://example.com" with a custom name
result = setTableWrapper("https://example.com", wrapper_name="my_table_wrapper")
print(result)
```

#### Function Output:

The setTableWrapper function returns a tuple with information about the operation:

- **Success Flag (bool):** True if the operation was successful, False otherwise.
- **Wrapper Name (string):** The name assigned to the wrapper, either custom or auto-generated. None if unsuccessful.
- **Error Code (int or None):** If unsuccessful, an error code indicating the nature of the failure. None if successful.
- **Error Type (string or None):** The type of the raised exception (if any). None if successful.
- **Error Message (string or None):** A descriptive error message (if any). None if successful.

```python
# Example Output
# (True, 'my_table_wrapper_abc123.json', None, None, None)
```



### Setting up a General Wrapper

To set up a general wrapper, use the setGeneralWrapper function. This function facilitates the creation of a web scraping wrapper for a general web page structure.

#### Function Input:

- **URL (string):** The URL of the web page you want to scrape.
- **Wrapper Name (string, optional):** A custom name for the wrapper. If not provided, a unique name will be generated.
- **Repeat (string, optional):** Indicate whether to repeat the pattern. Options are 'yes' or 'no'. Default is 'no'.

```python
from web_wrapper_project import setGeneralWrapper

# Example: Setting up a general wrapper for "https://example.com" with a custom name and repeat pattern
result = setGeneralWrapper("https://example.com", wrapper_name="my_general_wrapper", repeat="yes")
print(result)
```

#### Function Output:

The setGeneralWrapper function returns a tuple with information about the operation:

- **Success Flag (bool):** True if the operation was successful, False otherwise. None if unsuccessful.
- **Wrapper Name (string):** The name assigned to the wrapper, either custom or auto-generated.
- **Error Code (int or None):** If unsuccessful, an error code indicating the nature of the failure. None if successful.
- **Error Type (string or None):** The type of the raised exception (if any). None if successful.
- **Error Message (string or None):** A descriptive error message (if any). None if successful.

```python
# Example Output
# (True, 'my_table_wrapper_abc123.json', None, None, None)
```




### Getting Wrapper Data

To retrieve data from a previously set up wrapper, use the getWrapperData function. This function allows you to extract structured data from a web page based on the defined wrapper.

#### Function Input:

- **Wrapper Name (string):** The name of the wrapper from which to retrieve data.
- **Maximum Data Count:** The number of rows(Default value 100).
- **URL (string, optional):** The URL of the web page. If not provided, the URL from the original wrapper setup will be used.

```python
from web_wrapper_project import getWrapperData

# Example: Getting data from the wrapper named "my_table_wrapper"
result = getWrapperData("my_table_wrapper", 200, url="https://example.com")
print(result)
```

#### Function Output:

The getWrapperData function returns a tuple with information about the operation:

- **Success Flag (bool):** True if the operation was successful, False otherwise.
- **Data (list or string):** If successful, the structured data extracted from the web page based on the wrapper. If unsuccessful, an error message describing the issue.

```python
# Example Output
# (True, [['Column 1', 'Column 2'], ['Data 1', 'Data 2']])

# Example Output for Error
# (False, 'Permission denied: Unable to write to wrappers_5ece4797eaf5e')

```







### Listing Wrappers

To retrieve a list of all available wrappers, use the listWrappers function. This function provides the names of all wrappers that have been set up in the system.

#### Function Input:

None

```python
from web_wrapper_project import listWrappers

# Example: Listing all available wrappers
result = listWrappers()
print(result)
```

#### Function Output:

The listWrappers function returns a tuple with information about the operation:

- **Success Flag (bool):** True if the operation was successful, False otherwise.
- **Wrappers (list or string):** If successful, a list containing the names of all available wrappers. If unsuccessful, an error message describing the issue.

```python
# Example Output
# (True, ['wrapper1.json', 'wrapper2.json'])

# Example Output for Error
# (False, 'Permission denied: Unable to read the wrappers')

```


### Dependencies

- [Selenium](https://pypi.org/project/selenium/)
- [ChromeDriver](https://pypi.org/project/webdriver-manager/)
- [Beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

### Disclaimer

Intended for educational and legal use only. Users must comply with the terms of service of scraped websites and applicable laws and regulations.

