# AirAI

A GPT-based assistant able to look up real-time air quality information throughout the world.

### Requirements

- [Python](https://github.com/asdf-community/asdf-python) 3.10
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- [yarn](https://classic.yarnpkg.com/lang/en/docs/install/)
- [OpenWeatherMap](https://openweathermap.org/price) API Key
- [OpenAI](https://platform.openai.com/) API Key
- [Docker](https://docs.docker.com/engine/install) (and [docker-compose](https://docs.docker.com/compose/install/))

### Build and run

1. Copy `.env.example` to `.env` in both backend and ui apps. Make sure to add your OpenWeatherMap and OpenAI API keys to root `.env`.

```bash
cp .env.example .env
cp src/ui/.env.example src/ui/.env
vim .env
```

2. Build and run with `docker-compose` 

```bash
docker-compose build --parallel
docker-compose up -d
```

3. In your browser, navigate to `http://localhost:5173`.

4. To stop the apps, run

```bash
docker-compose down
```

### Run in dev mode

1. Same step one from above. Make sure your envs are in place
2. Activate Pipenv's virtual environment, install dependencies and start the app

```bash
python3 -m pipenv shell
pipenv install
python3 src/main.py
```

3. In another shell session, install frontend dependencies and start the dev server

```bash
cd src/ui
yarn
yarn dev
```

### Stack

- [Vue.js 3.x](https://vuejs.org/) (with [Composition API](https://vuejs.org/guide/extras/composition-api-faq.html) and [SFCs](https://vuejs.org/guide/scaling-up/sfc.html))
  - - [TypeScript](https://www.typescriptlang.org/), [ESLint](https://eslint.org/), [Prettier](https://prettier.io/), [Yarn](https://yarnpkg.com/),
- [FastAPI](https://fastapi.tiangolo.com/) and [LangChain](https://python.langchain.com/en/latest/index.html) for interfacing with LLMs
  - - [Pipenv](https://pipenv.pypa.io/en/latest/), [flake8](https://flake8.pycqa.org/en/latest/), [black](https://github.com/psf/black), [mypy](https://mypy-lang.org/), [aiohttp](https://docs.aiohttp.org/en/stable/)

### Potential improvements

What I'd add to this with time

- **Better contextual justifications:** It'd be interesting if the application could search the web for environmental facts about locations to enrich its pre-trained knowledge. Like "this place has lots of preserved green nature since the political act xyz in 1997 led by activist Jane Doe" - found by searching Google, plus providing source links for the information (which adds confidence considering LLMs sometimes make up facts).

- **Addressing TODOs:** Such as properly implementing the Chain interface for the `PlaceAirQuality` tool, making it compatible with other chain use cases. Plus, I'd look into how to make Mypy make friends with Pydantic without having to initialize dummy properties on super() calls.


### TWIMC: My thought process for doing this

The goal was to create a GPT-powered application capable of providing real time air quality information along with some form of datavis.

First step was researching about the domain. I knew close to nothing about air quality. So i needed a baseline knowledge to evaluate the overall thoroughness of what I was doing. TL;DR is, there is something called Air Quality Index, that is calculated using pollutant concentrations and standard values. These standard values change per country. So each country might have a different scale of AQI. Usually, people use U.S. AQI as reference. There are also places that come up with an AQI that ranges from 1 to 5 only. (U.S. AQI typically ranges from 1 to 500). Some of the main pullutants are PM2.5, O3, CO and NO2. AQI is also relative to pollutant. So each one might have a different AQI. But again, typically people use PM2.5 as a general indicator.

Next I had to figure out how to provide air quality data to the GPT model. If we would optmize for speed, we could download a large dataset of air quality of cities around the world and use a LangChain database access tool to look that up in a more structured way. Though, part of the goal of this project is to provide real-time information, not static, frozen in time.

With that in mind, the application would need to access the web for information. And preferrably, find a go-to site/API for that kind of information.

I found a couple of interesting websites ([#1](https://aqicn.org/), [#2](https://www.iqair.com/)) that aggregated air quality readings from many stations throughout the world in a common format. An option would be to build a web scraper capable of _searching cities based on unreliable user input_ and extracting the desired air quality information from these sites.

A more straightforward option would be finding an API that provided this kind of data. Preferrably with a free plan. I found two options for doing this ([#1](https://www.iqair.com/air-pollution-data-api), [#2](https://openweathermap.org/price)).

An even more straightforward approach would be using the SerpAPI LangChain built-in tool. It's an ultra-generalist tool that can search the web for information. Though, I wanted to provide thorough, structured and exact information about air quality. So I decided to go with the API approach.

I chose to use the OpenWeatherMap API, since they also provided geocoding and reverse geocoding with the same API key.

Next, I had to think of the overarching usability of the application. How the user would interact with it, and how it would display things. For that, I spun up a [Figma draft](https://www.figma.com/file/hqd0hUoHhozdCw3jr8ArzR/AirAI?node-id=0%3A1&t=wqPpiuKKLsA7YPS2-1) for quick iteration on visuals.

Then I had to choose the stack. One of the initial ideas of this project was to use LangChain with Python. To make things simpler, I decided to make one single backend application written in Python and FastAPI. FastAPI because, compared to the most common options (Flask and Django), is a more lightweight solution built on the newer async Python ASGI specification, but still providing support for the whole sync ecosystem by threadpooling for sync handlers. That sounded like a nice fit for my needs.

Off to set up the project. I wanted foolproof and deterministic package management, a straightfoward virtual environment tool, linting, formatting, typehint checking and commit message standards. For that I chose standard modern Python tooling: `pipenv` for package mgmt and virtual envs, `black` for formatting, `flake8` for linting, `mypy` for type checking and `gitlint` for commit message standards. I also added a pre-commit hook to run all quality checks locally before committing.

Next step was designing my LangChain structure. The requirements looked something like this:

- The user would input a city name and the application would look up the air quality information for that city in a real time, non-static data source.

- The information would be represented in a visual way in the frontend, which means it had to be strutuctured in a strict format.

- Along with the visual representation, the AI would write a short sentence answering the user's question. The sentence generation would have enriched context based on the air quality information.

- The app should have capacity to localize the user and access the current date to answer question like `"what is the air quality like in here now?"`.

- The app should have the ability to enrich its answer if applicable, with extra information about demographics. Like `"the city is located in a valley, and that negatively influences air quality."`.

- The app should have reliable ability to know the current date. OpenAI's GPT-3.5 and GPT-4 have decent effectiveness on that, but other LLM models tend to not.

An approach would be having a simple sequential chain of logic to toll between these cases. But that would be very brittle and get difficult to scale logically. LangChain has the concept of "agents", that act as a GPT-powered decision-maker able to use custom tools that you provide, in no particular order. Tools are just Python functions that can be called from the agent's prompt and can be as complex or as simple as you like. Including using other agents and so on. So I decided to use that approach instead.

I also spent a few brain cycles thinking on how I could handle user geolocalization. I could use the user's IP address and look it up on an IP geoloc API (that would require another key just for that, plus potentially paying up if this scales, hypothetically speaking). Or I could use the browser's geolocation API. But that would require the user to allow the browser to access their location. Using the browser's API seemed better, but I wouldn't like to ask for user location upfront, only as needed. So, I thought of somehow short circuiting the chain if the user's location was needed but not provided, to ask the frontend to go get it and try again.

Something to keep in mind is, the more you can restrict and simplify the agent's decision-making, the best. It's well known that sometimes LLMs get lost, especially when provided with complex informations, and even more so when it's all at once. So instead of creating many tools to do small steps, and letting the agent figure out how to wire them together, it's best to make the simplest possible usability, with the least amount of steps possible.

With that in mind, my LangChain design would look something like this:

```plaintext
[AGENT] Provided with context on what they're supposed to do and what tools they have
 |-- [TOOL] locate-user: given user's latitude and longitude (coming from the browser's geoloc API), reverse geocodes it and gets a name for the place the user is ai
 |-- [TOOL] airquality-api: given a location name and date, geocodes the location and gets data on that place's air quality
```

After a few experiments, the agent would get locked in a loop looking for a very specific tool to do trivial things, such as `I need to return this data to the user`, but there was not such tool for that. So I created a dummy tool just to break this loop, that simply gets the agent's input, formats it in a light prompt template and asks the LLM for what to do next.

This makes sense to work because, the agent already has to handle all the complexity overhead of "acting as an agent", so it ends up too confused to do basic reasoning.

The data returned from `airquality-api` is structured JSON data. Returning this directly to the LLM is a terrible idea. Most of the data is not needed and we'd be adding the overhead of interpretation to the LLM, making the whole process more fragile (and expensive). Instead, the tool returns a string like `The air quality in place X is Y.` and the model follows along just fine.

To store the actual strucured data, I used a programmatic approach of just populating a buffer variable instantiated on a per-request basis.

After that, I added one more chain to generate facts about the places involved in the prompt, that ideally would help understand what causes are behind the air quality of places.

Frontend development was pretty straightforward. Vue bootstrap takes care of all the setup. For the most part, it was just iterating on SCSS and componentization.
