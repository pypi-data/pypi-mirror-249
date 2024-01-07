# Easy-to-cache
### [git](https://github.com/M1KoDam/EasyToCacheLib) 

## Description ##
Simple python library helping you to cache your data using json.

It is implemented using the functionality of the Fluent API to provide you with a more user-friendly experience.


----------

## Using ##

Using the library is as simple and convenient as possible:

Let's import it first:
First, import everything from the library (use the `from `...` import *` construct).

Examples:

Creating cache object, where first argument is directory path where your cache will be saved and second is flag to load cache after initialization or not:

    cache = Cache("EasyToCacheLib/Data/TestFolder/test_file.json", False)


Adding data using `add` method, where first argument is key and second the value:

    cache.add("a", 10)

You can sort it by adding date using method `sort_by_date`, clear by method `clear` and etc


----------

## Developer ##
Me: [MikoDam](https://github.com/M1KoDam/) 
