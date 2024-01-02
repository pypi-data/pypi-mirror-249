<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** kajuberdut, incase, twitter_handle, patrick.shechet@gmail.com, incase, String functions in pure Python
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/kajuberdut/incase">
    <img src="https://raw.githubusercontent.com/kajuberdut/incase/main/images/icon.svg" alt="icon" width="160" height="160">
  </a>

  <h3 align="center">incase</h3>

  <p align="center">
    A word case management library with too many features (just in case).
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Incase is a library to help manage word case. It includes a class for abstracting away from case for easy comparison of words or conversion to any case.
Incase also includes a flexible decorator for managing the case of keywords, inputs, and outputs from functions.

Currently, incase supports the following cases: 
caseless, camel, dromedary, medial, snake, pascal, initial_capitals, kebab, dash, upper_snake, uppercase, upper, lowercase, lower, title, alternating, sarcasm, original, word

If you are aware of another case, please open an issue so we can add it!



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installing with pip

  ```sh
  pip install incase
  ```

For information about cloning and dev setup see: [Contributing](#Contributing)


<!-- USAGE EXAMPLES -->
## Usage

### CLI
You can leverage incase in shell scripts or other non-python contexts by calling it from the cli.
Example:


The default output is snake case.
``` shell
$ incase someCamel
some_camel
```

Use the --case option to set output case
``` shell
$ incase someCamel --case lower
some camel
```

### Caseless
Here is an example showing basic usage of the Caseless class.

```python
from incase import Case, Caseless

# Instances of Caseless are strings
example = Caseless("example string")
print(isinstance(example, str))
# True

# By property
print(example.snake)
# example_string

# Or by subscript (string or Case)
print(example["camel"])
# exampleString

print(example[Case.UPPER_SNAKE])
# EXAMPLE_STRING

# Caseless ignore case when comparing to str
print(Caseless("some name") == "SOME_NAME")
# True

# Caseless hashes ignore case also
a_dict = {Caseless("This is a Key"): "this"}
print(a_dict[Caseless("thisIsAKey")])

# Caseless can also generate case coercion functions
make_camel = Caseless.factory("camel")

print(make_camel("snake_case"))
# snakeCase

```

### ASGI Middleware Usage

This ASGI middleware, `JSONCaseTranslatorMiddleware`, translates JSON keys' case between snake_case and camelCase, easing communication between Python backends and JavaScript frontends. It handles JSON key case conversion for incoming and outgoing HTTP requests and responses.

**Example:**
```python
from incase.middleware import JSONCaseTranslatorMiddleware

# Setup your FastAPI or Starlette application and then:
app.add_middleware(JSONCaseTranslatorMiddleware)

```

The middleware is ASGI compliant and should work as middleware with other frameworks but this has not been tested.

#### Updated Usage Example:

To effectively use JSONCaseTranslatorMiddleware in your FastAPI or Starlette application, it's recommended to use a custom response class (camelJsonResponse) for outgoing data. This approach avoids the performance overhead associated with deserializing and re-serializing JSON in middleware. 

Here is how you can set it up to use the custom response with FastAPI. Note the argument to FastAPI to set the default_response_class and also the argument to add_middleware to disable response handling.

``` python
from fastapi import FastAPI
from incase.middleware import JSONCaseTranslatorMiddleware, Request, camelJsonResponse

app = FastAPI(default_response_class=camelJsonResponse)

app.add_middleware(JSONCaseTranslatorMiddleware, handle_response=False)


@app.get("/")
def read_root():
    return {"hello_there": "general kenobi"}


@app.post("/")
async def receive_data(request: Request):
    json_data = await request.json()
    print(json_data)
    return {"Received": json_data}
```

The above app will return `{"helloThere": "general kenobi"}` at the root because the default_response_class will automatically change json keys to camel case. If you post the following json to the root ("/"): `{"thisThing": 1}` you will see `{"Recieved": {"this_thing": 1}}` because the middleware will intercept the incoming json and convert the keys to snake_case.

See also:
- https://www.starlette.io/middleware/#using-middleware
- https://fastapi.tiangolo.com/advanced/middleware/#advanced-middleware

### Helper functions

case_modifier is a function for altering other functions. It can change the incoming case of parameter values, the case of the keywords provided, or the case of the function output.
```python
from incase import Case, case_modifier


# Some functions you don't control
def external_function(expectsCamel, iterationCount):
    # expects camelCase parameter names
    for i in range(iterationCount):
        print(expectsCamel)

# We'll use case_modifier. Now any keyword will be turned to camelCase
f = case_modifier(keywords_case=Case.CAMEL)(external_function)

f(expects_camel="this", iteration_count=1)
# this

# Here, we'll use case modifier as a function decorator
#  to give a sarcastic twist to our output
@case_modifier(args_case="sarcasm")
def say_words(*args) -> None:
    [print(word) for word in args]

say_words("It's all about", "the he said", "SHE SAID")
# It's aLl aBoUt
# ThE He sAi
# ShE SaId

```

Finally, incase is a powerful case coercion function.
```python
from incase import incase


# It covers the basic case
print(incase("snake", "example text"))
# example_text

# But can also handle sequences
print(incase("upper", ["three", "word", "list"]))
# ['THREE', 'WORD', 'LIST']
print(incase("upper", ("three", "word", "tuple")))
# ('THREE', 'WORD', 'TUPLE')

# Even generators
generator = (word for word in ["some", "list"])
incased = incase("upper", generator)
print(incased)
# <generator object _incase_single.<locals>.<genexpr> at ...
print(list(incased))
# ['SOME', 'LIST']

# Or nested objects
nested = {
    "first_key": ["some", "list"],
    "second_key": {"another": "dict"},
    "third_key": 1,
}
print(incase("upper", nested))
# {"first_key": ["SOME", "LIST"], "second_key": {"another": "DICT"}, "third_key": 1}

# Finally, it is possible to map case to objects
print(incase(["upper", "lower", "snake", "camel"], ["some_word"] * 4))
# ['SOME WORD', 'some word', 'some_word', 'someWord']

# By key
print(
    incase(
        {"first_key": "alternating", "second_key": "title"},
        {"first_key": "some example", "second_key": "another example"},
    )
)
# {'first_key': 'SoMe eXaMpLe', 'second_key': 'Another Example'}

print(incase({"bob": "upper"}, "bob"))

```

### Planetary Defense Shield

Note that this is probably not a good idea. However, if you want to be able to easily access objects in globals() by a case other then the one they have, you can use the planetary defense shield.

```python
from incase import planetary_defense_shield

THIS_IS_A_THING = "Some Value"


def badCamelCaseFunction():
    print("hi")


# If you pass a case, instead of a dictionary, this will grab most of globals.
# Also note that the objects that will be cloned are whatever is in globals()
# at the time you pass it as the second argument, so call accordingly.
planetary_defense_shield(
    {"THIS_IS_A_THING": "snake", "badCamelCaseFunction": "snake"}, globals()
)

print(this_is_a_thing)
# Some Value

bad_camel_case_function()
# hi
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Add tests, we aim for 100% test coverage [Using Coverage](https://coverage.readthedocs.io/en/coverage-5.3.1/#using-coverage-py)
4. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the Branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Cloning / Development setup
1. Clone the repo and install
    ```sh
    git clone https://github.com/kajuberdut/incase.git
    cd incase
    pipenv install --dev
    ```
2. Run tests
    ```sh
    pipenv shell
    ward
    ```
  For more about pipenv see: [Pipenv Github](https://github.com/pypa/pipenv)



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Patrick Shechet - patrick.shechet@gmail.com

Project Link: [https://github.com/kajuberdut/incase](https://github.com/kajuberdut/incase)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/kajuberdut/incase.svg?style=for-the-badge
[contributors-url]: https://github.com/kajuberdut/incase/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kajuberdut/incase.svg?style=for-the-badge
[forks-url]: https://github.com/kajuberdut/incase/network/members
[stars-shield]: https://img.shields.io/github/stars/kajuberdut/incase.svg?style=for-the-badge
[stars-url]: https://github.com/kajuberdut/incase/stargazers
[issues-shield]: https://img.shields.io/github/issues/kajuberdut/incase.svg?style=for-the-badge
[issues-url]: https://github.com/kajuberdut/incase/issues
[license-shield]: https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge
[license-url]: https://github.com/kajuberdut/incase/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/patrick-shechet
