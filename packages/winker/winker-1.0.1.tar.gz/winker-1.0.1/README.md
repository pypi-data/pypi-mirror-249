# Winker

Winker is a Python library for creating web apps with a futuristic, minimalistic design.

## Installation

You can install the Winker library using pip:

bash
pip install winker

## Usage

### Creating a Winker App

To create a Winker app, start by importing the WinkerApp class from the winker library:

python
from winker import WinkerApp, Input, Butn, Ttl, STtl, Txb, Lb

Then, initialize a Winker app and add elements to it using the add method:

python
app = WinkerApp()
app.add(Ttl("Welcome to My App"))
app.add(STtl("Please input your details:"))
app.add(Input("text", "Enter your name"))
app.add(Input("file", "Upload your photo"))
app.add(Input("file", "Upload your video"))
app.add(Input("file", "Upload your audio"))
app.add(Txb("Enter your comments", 4))
app.add(Butn("Submit", "submitFunction()"))
app.add(Lb("This is a sample app using Winker"))

app.run("my_app.html")

The run method will generate an HTML file based on the configured app elements.

### Function Descriptions

Here are descriptions of the functions and their usage:

- Ttl(text): Adds a title (h1) element to the app.
- STtl(text): Adds a subtitle (h3) element to the app.
- Input(input_type, label): Adds an input field to the app. The input_type parameter can be text for text input, file for file input, or other valid input types.
- Txb(text, lines): Adds a text area to the app.
- Lb(text): Adds a text (h4) element to the app.
- Butn(text, onclick): Adds a button to the app with the specified text and onclick action.

## Customization

The Winker library includes minimalistic, professionally designed CSS styles. To customize the appearance of your app, you can edit the CSS styles in the WinkerApp class.

## Version

This documentation is for Winker version 1.0.0.

## License

This library is licensed under the MIT License.
