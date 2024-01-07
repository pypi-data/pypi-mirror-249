# Watson Explorer

Explore the data in your Pandas DataFrames using Watson Explorer.

## Installation

Use the package manager [pip](https://pip.Heintjeb.io/en/stable/) to install Watson-Explorer.

```bash
pip install Watson-Explorer
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

```python
from Watson-Explorer import Explorer

"""Place the following statement at the end of your Python file."""
Explorer()

"""
After running the script, it will extract all the dataframes from the file, delete all old HTML files, create new HTML files, and open a local host to display the DataFrames. 
You can access the DataFrames using the dropdown menu. To stop the local host, click on the 'Stop Server' button, and the tab sheet will automatically close.
"""

"""REMARK:
It is not possible to view data from dataframes that are not linked to variables.
For example:
"""

example_dict = {'A' : [1,2,3,4], 'B' : [5,6,7,8]}

class Example():
    def __init__(self, dictionary=None):
        self.dataframe = pd.DataFrame(example_dict)
    
    def return_df_1(self):
        return self.dataframe
    
    def return_df_2(self):
        self.dataframe2 = self.dataframe.assign(D='Test')
        return self.dataframe2

example = Example(example_dict)
example.return_df_1() # The explorer will not include this dataframe.
example_df = example.return_df_2() # The explorer will include this dataframe.

"""REMARK 2:
This library is not designed to load more than 20,000 rows (yet). We suggest using .head() to reduce the size of your dataframe before using this library.
"""
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

### General
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. <br>
Please make sure to update tests as appropriate.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### CSS
Feel free to adjust the CSS file if you don't like the styling.<br>
Also, if you are a very gifted front-end developer, please let me know. I'm open to upgrading the interface.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Contact: heinburgmans.com <br>
Project Link: https://github.com/HeintjeB/watson

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments
The creation of this explorer was inspired by Spyder's Variable Explorer.

<p align="right">(<a href="#readme-top">back to top</a>)</p>