# Django Based AI Powered Code Bot
This is a code assistant bot that leverages the OpenAI API to generate code or debug existing code. The framework is built on Django, a robust web framework capable of handling complex solutions.
The app also utilizes other frameworks to format the output of the generated code effectively.

### How it Works
The application accepts user input, including the type of programming language. This information is formatted using a prompt template and passed through the OpenAI generative model via an API.
The response from the model is parsed, and the main content is retrieved and displayed in the correct program format.

### Its Importance
Developers can leverage this app to increase their productivity by delegating tasks like documentation, debugging, and generating code boilerplate to Large Language Models like ChatGPT.
They can also opt to use good open-source LLMs and set them up locally to avoid exposing company secrets to the public. 
